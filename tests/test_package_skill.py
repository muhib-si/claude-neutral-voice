"""Portable-format and release-artifact regressions; no Claude model calls."""

import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest import mock
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("package_skill", ROOT / "scripts/package_skill.py")
package_skill = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(package_skill)


class PackageSkillTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.skill_dir = self.root / "neutral-voice"
        self.skill_dir.mkdir()
        self.license = self.root / "LICENSE"
        self.license.write_bytes(b"Apache License\r\nVersion 2.0\r\n")
        self.output_dir = self.root / "dist"
        self.write_skill()

    def write_skill(self, name="neutral-voice", description="Revises assistant narration. Use for a neutral voice.", extra="", body="# Neutral Voice\nWrite directly.\n"):
        text = f"---\nname: {name}\ndescription: {description}\n{extra}---\n{body}"
        (self.skill_dir / "SKILL.md").write_bytes(text.encode("utf-8"))
        return text

    def build(self):
        return package_skill.build_skill(self.skill_dir, self.license, self.output_dir)

    def assert_invalid(self):
        with self.assertRaises(package_skill.SkillValidationError):
            self.build()

    def test_original_reserved_names_and_substrings_are_rejected(self):
        for name in ("claude-neutral-voice", "anthropic-helper", "myclaudetool"):
            with self.subTest(name=name):
                self.write_skill(name=name)
                with self.assertRaisesRegex(package_skill.SkillValidationError, "reserved"):
                    self.build()

    def test_name_constraints(self):
        for name in ("x" * 65, "Neutral-voice", "-neutral", "neutral-", "neutral--voice", "<name>", "null", "123"):
            with self.subTest(name=name):
                self.write_skill(name=name)
                self.assert_invalid()

    def test_missing_required_fields(self):
        for frontmatter in ("description: Direct prose", "name: neutral-voice", "{}"):
            with self.subTest(frontmatter=frontmatter):
                (self.skill_dir / "SKILL.md").write_text(f"---\n{frontmatter}\n---\nBody\n", encoding="utf-8")
                self.assert_invalid()

    def test_name_and_folder_must_match(self):
        self.write_skill(name="writing-neutrally")
        with self.assertRaisesRegex(package_skill.SkillValidationError, "folder"):
            self.build()

    def test_valid_name_and_description_at_maximum_lengths(self):
        name = "n" * 64
        self.skill_dir = self.skill_dir.rename(self.root / name)
        self.write_skill(name=name, description="x" * 1024)
        self.assertEqual(self.build().name, f"{name}.zip")

    def test_archive_name_is_derived_without_a_hard_coded_valid_name(self):
        self.skill_dir = self.skill_dir.rename(self.root / "writing-neutrally")
        self.write_skill(name="writing-neutrally")
        output = self.build()
        self.assertEqual(output.name, "writing-neutrally.zip")
        with ZipFile(output) as archive:
            self.assertEqual(archive.namelist(), ["writing-neutrally/SKILL.md", "writing-neutrally/LICENSE"])

    def test_description_constraints(self):
        for description in ('""', '"   "', "null", "123", "x" * 1025, '"Use <voice>neutral</voice>."'):
            with self.subTest(description=description):
                self.write_skill(description=description)
                self.assert_invalid()

    def test_full_yaml_folded_description_and_portable_optional_fields(self):
        self.write_skill(description=">-\n  Revises assistant prose.\n  Use for neutral narration.", extra=(
            "license: Apache-2.0\ncompatibility: Any assistant with Skills support\n"
            "metadata:\n  author: Example\n  version: '1.0'\nallowed-tools: Read\n"
        ))
        self.assertTrue(self.build().is_file())

    def test_invalid_yaml_duplicate_keys_and_unsupported_fields(self):
        for extra in ("name: another-name\n", "unknown: value\n", "metadata: [broken\n", "metadata:\n  version: 1\n", "compatibility: ''\n"):
            with self.subTest(extra=extra):
                self.write_skill(extra=extra)
                self.assert_invalid()

    def test_exact_skill_filename(self):
        (self.skill_dir / "SKILL.md").unlink()
        (self.skill_dir / "skill.md").write_text("wrong case", encoding="utf-8")
        self.assert_invalid()

    def test_body_line_limit_is_a_project_release_check(self):
        self.write_skill(body="Line\n" * 500)
        with self.assertRaisesRegex(package_skill.SkillValidationError, "release check"):
            self.build()

    def test_archive_exact_paths_source_bytes_license_and_no_stale_name(self):
        original = self.write_skill()
        output = self.build()
        self.assertEqual(output.name, "neutral-voice.zip")
        self.assertFalse((self.output_dir / "claude-neutral-voice.zip").exists())
        with ZipFile(output) as archive:
            self.assertEqual(archive.namelist(), ["neutral-voice/SKILL.md", "neutral-voice/LICENSE"])
            self.assertEqual(archive.read("neutral-voice/SKILL.md"), original.encode("utf-8"))
            self.assertEqual(archive.read("neutral-voice/LICENSE"), b"Apache License\nVersion 2.0\n")
            self.assertEqual(archive.testzip(), None)

    def test_deterministic_rebuild_and_newline_normalization(self):
        original = self.write_skill()
        first = self.build().read_bytes()
        (self.skill_dir / "SKILL.md").write_bytes(original.replace("\n", "\r\n").encode("utf-8"))
        self.assertEqual(self.build().read_bytes(), first)

    def test_validation_failure_preserves_existing_archive(self):
        output = self.build()
        previous = output.read_bytes()
        self.write_skill(name="claude-neutral-voice")
        self.assert_invalid()
        self.assertEqual(output.read_bytes(), previous)
        self.assertEqual(list(self.output_dir.iterdir()), [output])

    def test_missing_license_does_not_create_output(self):
        self.license.unlink()
        self.assert_invalid()
        self.assertFalse(self.output_dir.exists())

    def test_atomic_replace_failure_preserves_archive_and_cleans_temporary_file(self):
        output = self.build()
        previous = output.read_bytes()
        with mock.patch.object(package_skill.os, "replace", side_effect=OSError("Simulated failure")):
            with self.assertRaises(OSError):
                self.build()
        self.assertEqual(output.read_bytes(), previous)
        self.assertEqual(list(self.output_dir.iterdir()), [output])


if __name__ == "__main__":
    unittest.main()
