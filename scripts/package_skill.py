"""Validate and package the portable skill; Python 3.9+ and requirements-dev.txt."""

import argparse
import os
from pathlib import Path
import re
import tempfile
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

# ZIP dates start in 1980. A fixed date makes identical sources reproducible.
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)

try:
    import yaml
except ImportError as error:
    raise SystemExit(
        "Missing maintainer dependency PyYAML. Run: "
        "python -m pip install -r requirements-dev.txt"
    ) from error


class SkillValidationError(ValueError):
    """An input fails the portable format or this project's release checks."""


class UniqueKeyLoader(yaml.SafeLoader):
    """Use YAML parsing while rejecting ambiguous duplicate mapping keys."""


def unique_mapping(loader, node, deep=False):
    loader.flatten_mapping(node)
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError as error:
            raise yaml.constructor.ConstructorError(
                None, None, "YAML mapping keys must be scalar", key_node.start_mark
            ) from error
        if duplicate:
            raise yaml.constructor.ConstructorError(
                None, None, f"Duplicate YAML key: {key}", key_node.start_mark
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping
)


def read_text(path):
    try:
        # Universal newline handling gives stable LF bytes on every platform.
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise SkillValidationError(f"Cannot read UTF-8 file {path}: {error}") from error


def validate_skill(skill_dir):
    path = skill_dir / "SKILL.md"
    # Windows resolves filenames without case sensitivity; the format does not.
    if not path.is_file() or "SKILL.md" not in {entry.name for entry in skill_dir.iterdir()}:
        raise SkillValidationError(f"Missing exact filename: {path}")
    text = read_text(path)
    lines = text.splitlines(keepends=True)
    if not lines or lines[0] != "---\n":
        raise SkillValidationError("SKILL.md must start with YAML frontmatter (---).")
    end = next(
        (index for index in range(1, len(lines)) if lines[index].rstrip("\n") == "---"),
        None,
    )
    if end is None:
        raise SkillValidationError("SKILL.md YAML frontmatter needs a closing ---.")
    try:
        metadata = yaml.load("".join(lines[1:end]), Loader=UniqueKeyLoader)
    except yaml.YAMLError as error:
        raise SkillValidationError(f"Invalid YAML frontmatter: {error}") from error
    if not isinstance(metadata, dict):
        raise SkillValidationError("YAML frontmatter must be a mapping.")
    allowed = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
    if any(key not in allowed for key in metadata):
        raise SkillValidationError("Unsupported frontmatter field; use portable Agent Skills fields.")
    name = metadata.get("name")
    if not isinstance(name, str) or not 1 <= len(name) <= 64:
        raise SkillValidationError("name must be a string of 1-64 characters.")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        raise SkillValidationError(
            "name must use lowercase letters, digits, and single interior hyphens."
        )
    if any(word in name for word in ("claude", "anthropic")):
        raise SkillValidationError("name contains a reserved word: claude or anthropic.")
    if skill_dir.name != name:
        raise SkillValidationError(f"Skill folder {skill_dir.name!r} must match name {name!r}.")
    description = metadata.get("description")
    if not isinstance(description, str) or not description.strip() or len(description) > 1024:
        raise SkillValidationError("description must be a nonempty string of at most 1024 characters.")
    if re.search(r"<[^>]*>", description):
        raise SkillValidationError("description cannot contain XML tags.")
    for field in ("license", "compatibility", "allowed-tools"):
        if field in metadata and not isinstance(metadata[field], str):
            raise SkillValidationError(f"{field} must be a string when present.")
    if "compatibility" in metadata and not 1 <= len(metadata["compatibility"]) <= 500:
        raise SkillValidationError("compatibility must contain 1-500 characters.")
    if "metadata" in metadata and (
        not isinstance(metadata["metadata"], dict)
        or any(not isinstance(key, str) or not isinstance(value, str)
               for key, value in metadata["metadata"].items())
    ):
        raise SkillValidationError("metadata must map string keys to string values.")
    # Anthropic's authoring recommendation is a release gate for this small skill.
    if len("".join(lines[end + 1:]).splitlines()) >= 500:
        raise SkillValidationError("Project release check: keep the SKILL.md body under 500 lines.")
    return name, text.encode("utf-8")


def build_skill(skill_dir, license_path, output_dir):
    skill_dir = Path(skill_dir).resolve()
    name, skill_bytes = validate_skill(skill_dir)
    license_bytes = read_text(Path(license_path)).encode("utf-8")
    sources = {f"{name}/SKILL.md": skill_bytes, f"{name}/LICENSE": license_bytes}
    output_dir = Path(output_dir)
    # All source validation happens before creating or replacing an output.
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / f"{name}.zip"
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            prefix=f".{name}-", suffix=".zip.tmp", dir=output_dir, delete=False
        ) as stream:
            temporary = Path(stream.name)
        with ZipFile(temporary, "w", compression=ZIP_DEFLATED) as archive:
            for filename, contents in sources.items():
                entry = ZipInfo(filename, ZIP_TIMESTAMP)
                entry.create_system = 3
                entry.compress_type = ZIP_DEFLATED
                entry.external_attr = 0o100644 << 16
                archive.writestr(entry, contents)
        with ZipFile(temporary) as archive:
            if archive.testzip() is not None or archive.namelist() != list(sources):
                raise SkillValidationError("Archive integrity or path verification failed.")
            for filename, contents in sources.items():
                if archive.read(filename) != contents:
                    raise SkillValidationError(f"Archive content mismatch: {filename}")
        os.replace(temporary, output)
        return output
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def main():
    root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-dir", type=Path, help="Skill folder (defaults to the sole folder in skills/).")
    parser.add_argument("--output-dir", type=Path, default=root / "dist")
    args = parser.parse_args()
    try:
        skill_dir = args.skill_dir
        if skill_dir is None:
            skills_root = root / "skills"
            candidates = sorted(
                path for path in skills_root.iterdir()
                if path.is_dir() and (path / "SKILL.md").is_file()
            ) if skills_root.is_dir() else []
            if len(candidates) != 1:
                raise SkillValidationError("Expected one skill under skills/; select one with --skill-dir.")
            skill_dir = candidates[0]
        output = build_skill(skill_dir, root / "LICENSE", args.output_dir)
    except (SkillValidationError, OSError) as error:
        parser.exit(1, f"Packaging failed: {error}\n")
    print(f"Built and verified {output}")


if __name__ == "__main__":
    main()
