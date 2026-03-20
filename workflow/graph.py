from langgraph.graph import StateGraph
from workflow.nodes import evaluate_node

def create_graph():

    workflow = StateGraph(dict)

    workflow.add_node("evaluate", evaluate_node)

    workflow.set_entry_point("evaluate")

    workflow.set_finish_point("evaluate")

    return workflow.compile()