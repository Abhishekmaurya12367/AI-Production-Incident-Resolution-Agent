from agents import get_llm


def debugger_agent(
    incident: str,
    supervisor_plan: str,
    evidence: list[str],
) -> tuple[str, str]:
    """
    Debugger analyzes the collected evidence to identify the root cause
    and propose a concrete fix.

    Returns:
        (root_cause, proposed_fix) as a tuple of strings.
    """

    llm = get_llm()
    evidence_text = "\n\n".join(evidence)

    prompt = f"""
You are a senior production incident debugger.

Incident:
{incident}

Investigation Plan:
{supervisor_plan}

Evidence Collected:
{evidence_text}

Your job:
1. Identify the ROOT CAUSE of the incident.
2. Propose a clear, actionable FIX.
3. Estimate the SEVERITY (P1 / P2 / P3).
4. State whether the fix requires downtime.

Format your response EXACTLY as:

ROOT_CAUSE:
<your analysis here>

PROPOSED_FIX:
<step-by-step fix here>

SEVERITY: <P1 | P2 | P3>

REQUIRES_DOWNTIME: <yes | no>
"""

    response = llm.invoke(prompt)
    content = response.content

    # --- Parse structured output ---
    root_cause = _extract_section(content, "ROOT_CAUSE")
    proposed_fix = _extract_section(content, "PROPOSED_FIX")

    # Fallback: return full content if parsing fails
    if not root_cause:
        root_cause = content
    if not proposed_fix:
        proposed_fix = "See root cause analysis above."

    return root_cause, proposed_fix


def _extract_section(text: str, section: str) -> str:
    """Extract a labelled section from the LLM response."""
    marker = f"{section}:"
    if marker not in text:
        return ""
    parts = text.split(marker, 1)
    remainder = parts[1]
    # Stop at the next all-caps section header
    import re
    next_section = re.search(r"\n[A-Z_]+:", remainder)
    if next_section:
        return remainder[: next_section.start()].strip()
    return remainder.strip()
