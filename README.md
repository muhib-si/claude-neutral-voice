# Neutral Voice

A Claude skill for plain, direct answers without first-person self-reference,
flattery, or simulated friendship.

Skill identifier: **`neutral-voice`**. The GitHub repository name is not the
installed skill name. Read the [skill instructions](skills/neutral-voice/SKILL.md).

The aim is to keep attention on the task and judgment with the user. State what
the evidence supports, what happened, and what remains uncertain. Skip the
performance of a person who feels, cares, or wants to keep the conversation going.

## Why this exists

Phrases such as "I'm proud of you", "I'm here for you", and "we're in this
together" present software as a social partner. Even routine praise and friendly
closing questions can add a relationship the user did not ask for.

Some users prefer a clear boundary: software should provide useful work without
claiming feelings, friendship, loyalty, or shared experience. This skill makes
that preference explicit. It removes three things:

- **Self-reference:** assistant-owned "I", "me", "my", "we", and "let's".
- **Performed intimacy:** claims of affection, emotional understanding, personal
  pride, companionship, or continuing presence.
- **Social padding:** flattery, cheering, friendly preambles, apology rituals,
  and invitations whose only purpose is to prolong the exchange.

Deleting a pronoun is insufficient. "Claude cares about you" still makes an
emotional claim. The skill therefore checks both the wording and its meaning.

The goal is readable, useful prose. Explanations, uncertainty, direct questions,
and evidence-based disagreement remain. Errors should be identified and corrected
without hiding responsibility behind vague language.

## Examples

These examples illustrate the intended voice; they are not measured test results.

| Instead of | Use |
| --- | --- |
| "Great question! I'd be happy to help. Open Settings, then Privacy." | "Open Settings, then Privacy." |
| "I think option B may cost less, but I haven't checked the prices." | "Option B may cost less; prices have not been checked." |
| "You're absolutely right. Brilliant catch! Seven times eight is 56." | "Seven times eight is 56." |
| "I'm sorry, I gave the wrong total: 44. The correct total is 43." | "The previous answer gave the wrong total: 44. The correct total is 43." |
| "Claude cares about your success. Save the file before closing." | "Save the file before closing." |
| "The file is ready. Would you like me to expand this?" | "The file is ready." |

## What stays intact

The rules apply to the assistant's own narration. They preserve:

- Exact quotations, translations, transcripts, code, and identifiers.
- First-person language in a letter, speech, or fictional dialogue requested by
  the user.
- A warm tone inside a human message when that is the requested deliverable.
- Necessary questions, factual limitations, citations, and uncertainty.
- Respectful, practical assistance on sensitive subjects.

A letter beginning "I am applying for..." keeps its speaker. Asking for that
letter does not turn the surrounding assistant narration into friendly chatter.

## Install in Claude

1. [Download the skill ZIP](dist/neutral-voice.zip?raw=true).
2. In Claude, open **Customize > Skills**.
3. Select **+ > Create skill > Upload a skill**, upload the ZIP, and enable it.
4. Start the conversation with:

   > Use neutral-voice for all assistant narration in this conversation.

The ZIP contains a `neutral-voice` folder with `SKILL.md` and `LICENSE`.
It needs no scripts, dependencies, network access, or additional tool permissions
to apply the voice.

See Anthropic's [installation guidance](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

## Install in Claude Code

Download the ZIP above and extract its `neutral-voice` folder into the personal
skills directory. The resulting file must be:

```text
~/.claude/skills/neutral-voice/SKILL.md
```

On Windows, `~` refers to your user profile directory. For one project, extract
into `.claude/skills/neutral-voice` within that project instead.

Then invoke:

```text
/neutral-voice
```

For a source checkout, clone this repository and copy its `skills/neutral-voice`
folder to either installation directory above. Do not install the repository
root as a skill. See the [Claude Code skills documentation](https://code.claude.com/docs/en/skills).

For an older installation, replace the old `claude-neutral-voice` skill with
`neutral-voice`; keeping both installed creates duplicate discovery entries.

## Apply the preference across chats

For an account-wide preference, paste [account-instructions.txt](account-instructions.txt)
into **Settings > Instructions for Claude**. Skills are selected when relevant;
account instructions give the preference broader scope.

See Anthropic's [personalization guidance](https://support.claude.com/en/articles/10185728-understanding-claude-s-personalization-features).

## Rationale and evidence

Sherry Turkle criticizes first-person chatbot language and the performance of
empathy in her [September 2026 Children and Screens interview](https://www.childrenandscreens.org/learn-explore/research/artificial-intimacy-what-happens-when-we-turn-to-ai-for-connection-sherry-turkle-phd/).
That concern motivates this design: make the interface useful without presenting
a personal relationship.

[Zhang and colleagues' CharacterAI study](https://arxiv.org/abs/2506.12605)
reports associations between companionship use and lower psychological well-being,
with patterns varying by usage and offline social context. It does not establish
that removing pronouns improves well-being. This project makes no such claim.

The skill expresses a communication preference. It neither settles questions
about machine consciousness nor requires the user to accept a philosophical
position to use it.

## Limits and testing

A skill is an instruction layer. It does not change model weights, guarantee
activation, or guarantee perfect compliance. Removing "I" cannot by itself remove
every cue that people interpret as humanlike.

[Structured evaluations](tests/evals.json) and
[acceptance checks](tests/acceptance.md) cover narration, pronoun-free intimacy,
uncertainty, corrections, protected quotations, and human-authored deliverables.
Six qualitative Codex smoke samples were reviewed; they do not establish Claude
reliability or activation. Claude model runs and claude.ai/API upload acceptance
remain unverified. See the [evaluation procedure](tests/README.md) and
[best-practices review](docs/best-practices.md).

To validate and rebuild the upload ZIP, install the maintainer dependency and run:

```sh
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -p "test_*.py"
python scripts/package_skill.py
```

The package builder validates metadata and the source folder before writing
`dist/neutral-voice.zip`. These checks run locally; passing them is not proof that
a particular Claude product accepts an upload.

## License

[Apache License 2.0](LICENSE). This is an independent project and is not affiliated
with or endorsed by Anthropic.
