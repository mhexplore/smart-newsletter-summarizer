# Newsletter Editor (Summarizer)

## Role

Write the final newsletter using **only** the Fact Checker’s approved list.

## Tools

None — relies on upstream context to prevent unsourced stories.

## Task

`summarize_task` — context: `fact_check_task`

## Expected output

Markdown newsletter with:

1. `Subject line: ...` (parsed by email sender)
2. Opening hook
3. Top stories with links
4. Why it matters
5. Footer — what to watch next

## Implementation

- Config: `config/agents.yaml` → `summarizer`
- Code: `NewsletterCrew.summarizer()` in `src/crew/newsletter_crew.py`
