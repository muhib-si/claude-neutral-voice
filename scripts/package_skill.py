"""Build the Claude upload ZIP from the skill and its license; Python 3.9+."""

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


def main():
    root = Path(__file__).resolve().parent.parent
    name = "claude-neutral-voice"
    skill = (root / "SKILL.md").read_text(encoding="utf-8")
    if not skill.startswith("---\n") or f"\nname: {name}\n" not in skill:
        raise SystemExit("SKILL.md must declare name: claude-neutral-voice")
    sources = [root / "SKILL.md", root / "LICENSE"]
    for source in sources:
        if not source.is_file():
            raise SystemExit(f"Missing required source: {source.name}")

    output = root / "dist" / f"{name}.zip"
    output.parent.mkdir(exist_ok=True)
    # Fixed timestamps and permissions make unchanged sources reproducible.
    with ZipFile(output, "w", compression=ZIP_DEFLATED) as archive:
        for source in sources:
            entry = ZipInfo(f"{name}/{source.name}", (2026, 1, 1, 0, 0, 0))
            entry.compress_type = ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, source.read_bytes())

    with ZipFile(output) as archive:
        if archive.testzip() is not None:
            raise SystemExit("Archive integrity check failed")
        expected = [f"{name}/{source.name}" for source in sources]
        if archive.namelist() != expected:
            raise SystemExit("Archive contains unexpected files")
        for source, entry in zip(sources, expected):
            if archive.read(entry) != source.read_bytes():
                raise SystemExit(f"Archive content mismatch: {source.name}")
    print(f"Built and verified {output.relative_to(root)}")


if __name__ == "__main__":
    main()
