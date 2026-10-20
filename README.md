# Claude Neutral Voice

A Claude skill for plain, direct answers without first-person self-reference,
flattery, or simulated friendship.

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
| "Great question! I'd be happy to help." | Start with the answer. |
| "I think option B may cost less, but I haven't checked the prices." | "Option B may cost less; prices have not been checked." |
| "You're absolutely right. Brilliant catch!" | "That correction is valid because..." Only when the correction is valid. |
| "I'm sorry, I gave you the wrong total." | "The previous answer gave the wrong total. The correct total is 43." Only when that is the verified correction. |
| "I'm always here for you." | Remove the relationship claim and address the actual request. |
| "Would you like me to expand this?" | End the answer unless a scope choice is needed. |

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

1. [Download the skill ZIP](dist/claude-neutral-voice.zip?raw=true).
2. In Claude, open **Customize > Skills**.
3. Select **+ > Create skill > Upload a skill**, upload the ZIP, and enable it.
4. Start the conversation with:

   > Use claude-neutral-voice for all assistant narration in this conversation.

The ZIP contains a `claude-neutral-voice` folder with `SKILL.md` and `LICENSE`.
It needs no scripts, dependencies, network access, or additional tool permissions
to apply the voice.

See Anthropic's [installation guidance](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

## Install in Claude Code

Clone this repository into the personal skills directory:

```sh
git clone https://github.com/muhib-si/claude-neutral-voice.git ~/.claude/skills/claude-neutral-voice
```

Then invoke:

```text
/claude-neutral-voice
```

For one project, use `.claude/skills/claude-neutral-voice` in that project's
directory instead. See the [Claude Code skills documentation](https://code.claude.com/docs/en/skills).

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

[Behavioral acceptance checks](tests/acceptance.md) cover neutral narration,
pronoun-free intimacy, factual uncertainty, correction of errors, protected
quotations, and human-authored deliverables. These checks have not yet been run
in Claude. Structural validation and archive checks do not establish behavioral
reliability.

To rebuild the upload ZIP after editing the skill:

```sh
python scripts/package_skill.py
```

## License

[Apache License 2.0](LICENSE). This is an independent project and is not affiliated
with or endorsed by Anthropic.
