from agents import get_llm


def supervisor_agent(incident: str) -> str:
    """
    Supervisor creates a plan for resolving the incident.
    """

    llm = get_llm()

    prompt = f"""
You are a production incident supervisor.

Analyze the following incident:

{incident}

Create a clear investigation plan.

Your plan should mention:
1. What logs should be checked
2. Whether database health should be checked
3. Whether recent deployments should be checked
4. What the researcher should investigate
"""

    response = llm.invoke(prompt)

    return response.content
