import os
from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from Tools import add, get_weather

load_dotenv(Path(__file__).parent / ".env", override=True)

model = ChatOpenAI(
    model=os.environ["MODEL"],
    timeout=20,
    max_retries=0,
)

agent = create_agent(model, tools=[add, get_weather])

if __name__ == "__main__":
    question = input("Your prompt: ")
    result = agent.invoke(
        {"messages": [("user", question)]},
        config={"recursion_limit": 10},
    )
    for m in result["messages"]:
        m.pretty_print()