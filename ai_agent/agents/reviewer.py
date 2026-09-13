from agents import get_llm


def reviewer_agent(
    incident: str,
    evidence: list[str],
    root_cause: str,
    proposed_fix: str,
) -> str:
    """
    Reviewer validates the debugger's diagnosis and proposed fix.
    Returns a review decision: APPROVED or NEEDS_MORE_INVESTIGATION.
    """

    llm = get_llm()
    evidence_text = "\n\n".join(evidence)

    prompt = f"""
You are a production incident reviewer.

Incident:
{incident}

Evidence:
{evidence_text}

Debugger Root Cause Analysis:
{root_cause}

Proposed Fix:
{proposed_fix}

Review the analysis carefully.

Check:
1. Is the root cause well-supported by the evidence?
2. Is the proposed fix safe and appropriate?
3. Could the fix cause downtime or make things worse?
4. Is a rollback plan required?
5. What additional validation or monitoring is needed post-fix?

Format your response EXACTLY as:

DECISION: <APPROVED | NEEDS_MORE_INVESTIGATION>

REVIEW:
<your full review here>

SAFE_NEXT_STEPS:
<numbered list of next steps>
"""

    response = llm.invoke(prompt)
    return response.content
