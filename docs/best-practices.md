# Best-practices review

Reviewed against Anthropic's
[authoring guide](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices),
[metadata requirements](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview#skill-structure),
and the [Agent Skills specification](https://agentskills.io/specification).

## Format requirements

- The identifier is `neutral-voice`, with a matching source and upload folder.
- The package builder rejects reserved names, invalid syntax, missing or invalid
  fields, and name/folder mismatches before writing an archive.
- Source instructions live at `skills/neutral-voice/SKILL.md`; the upload archive
  contains `neutral-voice/SKILL.md` and its license. Repository branding and URLs
  do not determine the installed identifier.

The previous identifier used a reserved word. Claude Code loading that version
did not establish portability or upload acceptance. The old upload archive has
been removed rather than retained as an alternative install path.

## Authoring changes

The revision shortens repeated guidance, narrows discovery, demonstrates finished
rewrites, and adds a silent review-and-repair loop. Human speakers, quotations,
code, uncertainty, and action status remain protected. The entrypoint is small
enough to stay self-contained; extra runtime reference files would add navigation
without solving a demonstrated need.

The skill has no runtime tools. Advice about MCP names, executable helpers,
package installation, and visual inspection does not apply to its writing task.
Maintainer build dependencies are documented separately and are not shipped in
the skill archive.

## Evidence and outstanding checks

Regression tests check the original naming failure and packaging invariants.
Six qualitative Codex samples support basic instruction consistency, with the
method and limitations [recorded explicitly](../tests/reviews/codex-smoke-2026-10-20.md).
Eight task cases and twenty trigger cases are ready for Claude evaluation. The
matched speaker-boundary pair checks identical wording as assistant narration
and as a quotation from a human letter.

Multi-model comparisons, measured discovery, live conversation persistence, and
claude.ai/API uploads remain untested. No claim of full platform compatibility
or measured behavioral improvement follows from the local checks. See the
[evaluation procedure](../tests/README.md) for the remaining work.
