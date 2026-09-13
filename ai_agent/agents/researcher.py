from agents import get_llm
from app.tools.logs import fetch_logs
from app.tools.database import check_database_health
from app.tools.github import get_recent_deployments


def researcher_agent(incident: str, supervisor_plan: str) -> list[str]:
    """
    Researcher gathers evidence based on the supervisor's investigation plan.
    Calls real tools (logs, database, deployments) and returns collected evidence.
    """

    llm = get_llm()
    evidence: list[str] = []

    # --- Step 1: Fetch recent logs ---
    print("[Researcher] Fetching logs...")
    logs = fetch_logs()
    evidence.append(f"=== Application Logs ===\n{logs}")

    # --- Step 2: Check database health ---
    print("[Researcher] Checking database health...")
    db_status = check_database_health()
    evidence.append(f"=== Database Health ===\n{db_status}")

    # --- Step 3: Fetch recent deployments ---
    print("[Researcher] Fetching recent deployments...")
    deployments = get_recent_deployments()
    evidence.append(f"=== Recent Deployments ===\n{deployments}")

    # --- Step 4: Ask LLM to summarize findings ---
    evidence_text = "\n\n".join(evidence)

    prompt = f"""
You are a production incident researcher.

Incident:
{incident}

Investigation Plan:
{supervisor_plan}

Raw Evidence Collected:
{evidence_text}

Summarize the key findings relevant to the incident.
Highlight anomalies, error patterns, and anything suspicious.
"""

    response = llm.invoke(prompt)
    evidence.append(f"=== Researcher Summary ===\n{response.content}")

    return evidence
