from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
import os
from tools import search_flights, search_hotels, calculate_budget, check_flight_details, book_flight, manage_booking
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

load_dotenv()

console = Console()


# 1. Đọc System Prompt
with open("system_prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

# 2. Khai báo State
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# 3. Khởi tạo LLM và Tools
tools_list = [search_flights, search_hotels, calculate_budget, check_flight_details, book_flight, manage_booking]

# Sử dụng OpenRouter API theo yêu cầu của user
llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    model="google/gemini-2.5-flash",
)
llm_with_tools = llm.bind_tools(tools_list)

# 4. Agent Node
def agent_node(state: AgentState):
    messages = state["messages"]
    
    if not messages or not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
        
    response = llm_with_tools.invoke(messages)
    
    # === LOGGING
    if response.tool_calls:
        for tc in response.tool_calls:
            console.print(f"[bold yellow]⚙️ Gọi tool:[/bold yellow] [cyan]{tc['name']}[/cyan]\n[dim]Tham số: {tc['args']}[/dim]")
        
    return {"messages": [response]}

# 5. Xây dựng Graph
builder = StateGraph(AgentState)
builder.add_node("agent", agent_node)

tool_node = ToolNode(tools_list)
builder.add_node("tools", tool_node)

# TODO: Sinh viên khai báo edges
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")

memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

# 6. Chat loop
if __name__ == "__main__":
    console.print(Panel.fit("[bold blue]✈️ TravelBuddy - Trợ lý Du lịch Thông minh[/bold blue]\n[dim]Gõ 'quit' để thoát[/dim]", border_style="blue"))
    
    while True:
        user_input = input("\nBạn: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            break
            
        console.print("[dim italic]TravelBuddy đang suy nghĩ...[/dim italic]")
        config = {"configurable": {"thread_id": "session_1"}}
        result = graph.invoke({ "messages": [("human", user_input)] }, config)
        final = result["messages"][-1]
        
        # Xử lý nội dung hiển thị cho đẹp
        output_text = final.content
        if isinstance(output_text, list):
            output_text = "\n".join(item.get("text", "") if isinstance(item, dict) else str(item) for item in output_text)
            
        console.print("\n[bold magenta]TravelBuddy:[/bold magenta]")
        console.print(Panel(Markdown(output_text), border_style="magenta"))
        
        # Lưu tự động lịch sử vào test_result.md
        with open("test_result.md", "a", encoding="utf-8") as f:
            f.write(f"**Bạn:** {user_input}\n\n")
            f.write(f"**TravelBuddy:**\n{output_text}\n\n---\n\n")
