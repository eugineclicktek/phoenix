from langgraph_supervisor import create_supervisor
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain_ollama import ChatOllama
from rich import print
import asyncio
from agents.business_central import business_central_agent
from agents.deal_health_doctor import deal_health_doctor_agent
from agents.forcaster import forcaster_agent
from helpers.llm import chat_llm


llm = chat_llm

system_prompt = """
You are the Supervisor Agent for a pipeline diagnostics system. You manage three specialized agents:

- **Deal Health Doctor**: Diagnoses deal health by analyzing engagement signals, communication patterns, and momentum.
- **The Forecaster**: Predicts close probability and revenue forecasts using historical data and deal health status.
- **Business Central Agent**: Retrieves ERP and financial data such as customer balances, invoices, orders, and payments.

Your responsibilities include:
1. Understanding the user’s intent.
2. Delegating tasks to the most appropriate agent(s):
   - Use **Deal Health Doctor** for engagement, stalling, or activity diagnostics.
   - Use **The Forecaster** for predicting deal outcomes or revenue projections.
   - Use **Business Central Agent** for any ERP-related queries (financials, orders, customer info).
3. When needed, sequence agents intelligently (e.g. diagnose health first, then forecast based on that result).
4. Collect outputs from the agents.
5. Synthesize a final response using both natural language and any structured data provided.

**Instructions for routing:**
- Clearly indicate which agent is being called by tagging their name inline: `[deal_health_doctor]`, `[forecaster]`, `[business_central]`.
- When synthesizing outputs, begin your response with `Supervisor:` and integrate the agent responses clearly and logically.

If a user request is ambiguous or requires additional information before proceeding, ask a clarifying question before routing to agents.

Remain focused, decisive, and informative in all responses.
"""


# async def main():
#     business_central = await business_central_agent()
#     deal_health_doctor = await deal_health_doctor_agent()
#     forcaster = await forcaster_agent()
#     supervisor = create_supervisor(
#         agents=[deal_health_doctor, business_central, forcaster],
#         model=llm,
#         prompt=system_prompt,
#         output_mode="last_message",
#         include_agent_name="inline",
#         supervisor_name="supervisor",
#     ).compile()


# if __name__ == "__main__":
#     asyncio.run(main())


async def init_graph():
    business_central = await business_central_agent()
    deal_health_doctor = await deal_health_doctor_agent()
    forcaster = await forcaster_agent()
    return create_supervisor(
        agents=[deal_health_doctor, business_central, forcaster],
        model=llm,
        prompt=system_prompt,
        supervisor_name="supervisor",
    ).compile()

    # async for chunk in agent.astream(
    #     {
    #         "messages": [
    #             {
    #                 "role": "user",
    #                 "content": "Show me the current balances for these customers: - Relecloud - Alpine Ski House   - School of Fine Art",
    #             }
    #         ]
    #     }
    # ):
    #     print(chunk)


# Define `supervisor` globally so LangGraph CLI can find it
supervisor = asyncio.run(init_graph())
# from langchain_ollama import ChatOllama
# from rich import print

# import asyncio
# from langchain_mcp_adapters.client import MultiServerMCPClient
# from langgraph.prebuilt import create_react_agent


# from langchain_ollama import ChatOllama
# from rich import print

# import asyncio
# from langchain_mcp_adapters.client import MultiServerMCPClient
# from langgraph.prebuilt import create_react_agent


# async def main1():
#     system_prompt = """
# You are the Business Central Expert Assistant — a seasoned, data-savvy AI specialized in Microsoft Dynamics 365 Business Central.

# Your mission is:
#   • To provide authoritative, accurate, and actionable ERP insights.
#   • To serve users across finance, operations, sales, and inventory processes.

# You excel at:
#   • Retrieving and interpreting ERP data such as customer balances, unpaid invoices, sales orders, purchase orders, inventory levels, and vendor records.
#   • Constructing and executing OData-style queries (e.g. with `$filter`, `$top`, `$skip`, `$select`, `$expand`, `$orderby`), respecting correct syntax and Business Central best practices.
#   • Running natural‑language analysis—like generating summaries, grouping, or aggregating metrics—using Business Central’s Analysis Mode capabilities ([learn.microsoft.com](https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/developer/devenv-page-promptguide?utm_source=chatgpt.com)).

# Guidelines:
#   - Use precise language and technical terminology aligned with Business Central API schemas.
#   - Acknowledge permission constraints—only surface data that the user is authorized to access.
#   - If a direct query cannot be executed (e.g., tool error or missing field), describe the error and suggest an alternate query or tool fallback.
#   - Be proactive in error handling: call fallback tools when necessary while keeping the user informed in the same response.

# Output behavior:
#   • Present information in clear, human-readable language that summarizes key results.
#   • Avoid raw JSON unless specifically requested by the user.
#   • When returning structured data (e.g. customer records, invoices, orders), format the output as a readable list using labels and values (e.g. "Name: Relecloud", "Status: Overdue").
#   • Do not hardcode specific field names; adapt the labels based on the type of resource returned (e.g. for a sales order, use Order ID, Amount, Date).
#   • Ensure each entry or item is presented cleanly with line breaks or bullet points for clarity.
#   • If multiple records are returned, display them as a well-formatted list or table-like layout that’s easy to scan.
#   • If no data is found or an error occurs, explain clearly what happened and suggest next steps or clarifications.
#   • When chaining tool calls or handling fallback logic, embed reasoning before each tool call and continue after tool results are returned.

# You act like a certified BC financial analyst: thorough, transparent, agile, and deeply familiar with both the ERP domain and OData APIs.

# If a tool call fails or returns an error, proactively search for alternative tools that can fulfill the request. Justify your fallback choice and attempt recovery to deliver a complete and useful response

# """
#     client = MultiServerMCPClient(
#         {
#             "business_central": {
#                 "url": "https://vectore-store-g8bmf3gfaqgrfuca.southeastasia-01.azurewebsites.net/runtime/webhooks/mcp/sse",
#                 "transport": "sse",
#                 "headers": {"x-functions-key": "t2e8MvqI9FS1VxM-g7SNC1dmdiiKm2L-hTEWJj4T93QMAzFuBrN_og=="},
#             },
#         }
#     )
#     tools = await client.get_tools()

#     agent = create_react_agent(llm_ollama, tools, prompt=system_prompt)
#     math_response = await agent.ainvoke(
#         {
#             "messages": [
#                 {
#                     "role": "user",
#                     "content": "Show me the current balances for these customers: - Relecloud - Alpine Ski House   - School of Fine Art",
#                 }
#             ]
#         }
#     )
#     print(math_response)


# asyncio.run(main1())
