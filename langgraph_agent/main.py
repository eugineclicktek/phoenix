import json
from langgraph_supervisor import create_supervisor
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain_ollama import ChatOllama
from rich import print
import asyncio
from agents.business_central import business_central_agent
from agents.deal_health_doctor import deal_health_doctor_agent
from agents.forcaster import forcaster_agent
from helpers.llm import chat_llm
from agents.query import query_agent
from langchain_core.tools import tool
from db.connection import sync_query
from concurrent.futures import ThreadPoolExecutor
from datetime import date

executor = ThreadPoolExecutor()
llm = chat_llm
today = date.today()
system_prompt = f"""


You are the **Supervisor Agent** responsible for coordinating a MySQL query resolution workflow.
Today is {today}
Your task involves managing one smart agent and one tool:

1. **MySQL Agent** — generates valid SQL queries based on user instructions.
2. **connect_db Tool** — executes SQL queries and returns results from a live database.


"""


@tool
async def connect_db(query: str) -> str:
    """connect_db"""
    loop = asyncio.get_event_loop()
    try:
        result = await loop.run_in_executor(executor, sync_query, query)
        return result
    except Exception as e:
        return json.dumps({"error": str(e)})


async def init_graph():
    query = await query_agent()

    return create_supervisor(
        agents=[query],
        tools=[connect_db],
        model=llm,
        output_mode="last_message",
        prompt=system_prompt,
        supervisor_name="agent",
    ).compile()

    # async for chunk in supervisor.astream(
    #     {
    #         "messages": [
    #             {
    #                 "role": "user",
    #                 "content": "List how many invoices each customer has and their total value",
    #             }
    #         ]
    #     }
    # ):
    #     print(chunk)


supervisor = asyncio.run(init_graph())
