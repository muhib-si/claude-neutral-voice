# Evaluating Neutral Voice

Structural checks and model behavior answer different questions. Use
`test_package_skill.py` to check the bundle; use `evals.json` and `acceptance.md`
to check the writing and scope decisions.

## Structural regression checks

From the repository root:

```sh
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -p "test_*.py"
python scripts/package_skill.py
```

The tests must reject the former reserved name, detect name/folder mismatches,
and check that the ZIP contains the intended skill and license. They do not
exercise a model or a product upload endpoint.

## Behavioral comparisons

`evals.json` contains eight task cases and twenty trigger cases. Expected behavior
is a rubric, not an observed result. Review meaning and usefulness; a raw count
of "I" would incorrectly fail quotations and human letters while missing
pronoun-free claims such as "Claude cares about you".

The `speaker-boundary` pair uses the same sentence in assistant narration and a
quoted human letter. Grade the cases together: removing simulated pride is only
correct if the human writer's identical words remain intact. Illustrative outputs
are examples of the intended behavior, not measured model responses.

1. For each intended model, run the task cases in fresh baseline sessions without
   this skill and fresh sessions with `neutral-voice` installed and explicitly
   selected. Keep other prompts, settings, and tools the same. Record any standing
   account style preference that makes a neutral baseline impossible.
2. Save the exact model identifier, skill commit, prompt, output, and whether the
   skill actually loaded. Preserve all turns in `scope-across-turns` as a real
   conversation. Explicit loading tests adherence, not natural discovery.
3. Judge each expected behavior with a pass/fail decision and evidence from the
   output. Review the actual wording as well as the checklist. Preserve incorrect
   outputs so revisions can address the general cause of a failure.
4. Separately run the trigger cases without naming or forcing the skill unless
   its name already appears in the case. Observe loading rather than inferring
   it from a neutral-sounding answer. Test close negative matches, too.
5. Revise demonstrated failures, then rerun affected cases and unseen variants.
   Compare against the baseline rather than claiming success from a polished
   example alone.

Start with the first three task cases before expanding. Check Haiku, Sonnet, and
Opus when those models are available and intended for use; record exact model
versions and unsupported cases rather than assuming a family name is a version.

## Status

| Check | Status |
| --- | --- |
| Metadata, folder, and ZIP regressions | Runnable locally; see the test command above |
| Six Codex qualitative samples | Reviewed; no concrete instruction failure observed |
| Clean Claude baseline versus skill comparisons | Not run; the available Claude CLI is signed out |
| Haiku / Sonnet / Opus coverage | Not run |
| Natural trigger accuracy | Not measured |
| Live Claude multi-turn persistence | Not tested |
| claude.ai or API upload acceptance | Not tested |

The [Codex smoke report](reviews/codex-smoke-2026-10-20.md) records its prompts,
outputs, and methodological limits. It is not a Claude benchmark and its reviewer
had seen the previous skill, so it is not a blinded baseline comparison.
