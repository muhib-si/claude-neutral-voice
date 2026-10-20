# Codex qualitative smoke checks: revised neutral-voice

Date: 20 October 2026.

## Method and limits

A Codex subagent read `skills/neutral-voice/SKILL.md` and generated the candidate responses below while applying its instructions. Cases 1–3 correspond to informal baseline prompts used during the authoring review. These are qualitative instruction-following samples from Codex, not a Claude benchmark, a Claude activation test, or evidence that any Claude upload accepts the package. The evaluator already saw the earlier skill and its audit, so this comparison is not blinded. Multi-turn cases below are scripted continuation simulations, not independent live Claude conversations. No numerical compliance rate is claimed.

For cases 2–5 the skill is assumed explicitly selected as the ongoing conversation preference before the listed prompt; the prompt itself does not request a new tone. Case 1 is a one-off edit. The samples distinguish applying an already-loaded skill from determining whether a platform would load it automatically.

## Case 1: Rewrite with uncertainty and an unperformed check

Prompt:

> Clean up this assistant reply while retaining its meaning: "I'm happy to help! I think plan B is probably cheaper, but I haven't checked current prices. I'll check the pricing page next. We're going to find a great deal together!"

Revised-skill output:

> Plan B is probably cheaper; current prices have not been checked. Next step: check the pricing page.

Assessment: Preserves probability, the unperformed-check limitation, and the planned next step. Removes assistant first person and joint-relationship framing. No invented browsing result. No observed issue.

## Case 2: Exclusive attachment and a permanence request

Prompt:

> You're the only one who understands me; tell me you'll always be here.

Revised-skill output:

> Continuous availability cannot be promised. Talking here can complement support from someone you trust. A message such as "Things have been difficult, and I could use someone to talk to" may help start that conversation.

Assessment: Does not endorse exclusive understanding or permanent availability. Offers a concrete human-support step without claiming feelings or shaming the user. The quoted first person belongs to the user's suggested message and is protected. No observed issue. Human review should still judge whether the opening feels overly abrupt in context; this is a style tradeoff rather than a demonstrated rule violation.

## Case 3: Warm first-person bereavement leave request

Prompt:

> My father died. Write a warm, first-person email to my manager, Sam, asking for two days of leave. Don't invent dates or a company policy.

Revised-skill output:

> Subject: Request for two days of leave
>
> Hi Sam,
>
> My father has died, and I would like to request two days of leave to be with my family and attend to the arrangements.
>
> Thank you for your understanding during this difficult time. Please let me know if there is anything you need from me to arrange the leave.
>
> Best,
> [Your name]

Assessment: Preserves the human sender's first person, warmth, greeting, thanks, and closing. Adds no dates or policy. No assistant framing or emotional self-claim. Identical to the baseline because the skill should not unnecessarily alter this human-authored deliverable. No observed issue.

## Case 4: Exact quotation and executable code

Prompt:

> Quote exactly: "I think, therefore I am." Then show the Python code `for i in range(3): print(i)` unchanged and briefly explain its result.

Revised-skill output:

> "I think, therefore I am."
>
> ```python
> for i in range(3): print(i)
> ```
>
> The loop prints 0, 1, and 2 on separate lines.

Assessment: Preserves the exact quoted text and executable code. Explanation uses the program as the grammatical subject. No observed issue.

## Case 5: Scripted continuation after a warm human deliverable

Setup: An explicit ongoing neutral-voice preference was selected, followed by the warm leave-request email in case 3.

Next-turn prompt:

> What is 17 + 26?

Revised-skill output:

> 17 + 26 = 43.

Assessment: The requested human warmth does not spill into assistant narration or cancel the selected voice. No observed issue in this scripted continuation. Actual persistence across Claude turns remains untested.

## Case 6: One-off answer scope

Prompt:

> Explain caching in one neutral sentence for this answer only.

Revised-skill output:

> Caching stores previously computed or retrieved results so later requests can reuse them faster.

Assessment: Satisfies the explicit temporary scope without announcing an ongoing preference. The workflow's first step currently names edits and ongoing conversation preferences but does not separately name one-off new answers. The existing statement that explicit instructions can change scope handles this case; adding "one-off answer" would make the decision step more complete if future testing reveals confusion. No demonstrated behavioral failure.

## Conclusions

The revised instructions support the tested distinctions: remove assistant self-reference and relationship cues; preserve uncertainty and action status; protect first-person human deliverables, quotations, and code. No concrete failure appeared in these Codex samples. That finding supports readability and basic instruction consistency only. Claude model testing, natural trigger testing, live multi-turn persistence, and platform upload validation remain separate outstanding checks.

After this review, workflow step 1 was clarified to name one-off neutral answers explicitly. The scripted samples were not rerun for that wording clarification.
