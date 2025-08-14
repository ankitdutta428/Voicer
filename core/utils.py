import operator
from typing import Annotated, Sequence, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode # This is the correct import needed

# Define the state for our graph
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]

def create_react_agent(llm, tools, checkpointer):
    """
    Creates a LangGraph ReAct agent with the correct structure.
    """
    # ToolNode is the correct way to create a node that executes tools
    tool_node = ToolNode(tools)

    # Define the function that determines whether to continue or end the workflow
    def should_continue(state):
        messages = state['messages']
        last_message = messages[-1]
        # If the model did not invoke a tool, then we finish
        if not last_message.tool_calls:
            return "end"
        # Otherwise, we continue and call the tool
        else:
            return "continue"

    # Define the function that calls the model
    def call_model(state):
        messages = state['messages']
        response = llm.invoke(messages)
        # We return a list, because this will get added to the existing list
        return {"messages": [response]}

    # Define the graph workflow
    workflow = StateGraph(AgentState)

    # Define the two nodes we will cycle between
    workflow.add_node("agent", call_model)
    workflow.add_node("action", tool_node)

    # Set the entrypoint as `agent`
    workflow.set_entry_point("agent")

    # Add the conditional edge
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "continue": "action",
            "end": END,
        },
    )

    # Add a normal edge from the action (tool) node back to the agent
    workflow.add_edge("action", "agent")

    # Compile the graph and add the checkpointer
    graph = workflow.compile(checkpointer=checkpointer)
    
    return graph
