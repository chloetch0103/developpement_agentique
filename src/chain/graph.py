from langgraph.graph import END, START, StateGraph

from chain.state import State


def spec_node(state: State) -> dict:
    return {"spec": f"Spécification pour {state['task']}"}


def coder_node(state: State) -> dict:
    return {"code": f"# code basé sur {state['spec']}"}


def fake_runner_node(state: State) -> dict:
    attempts = state.get("attempts", 0)
    return {"attempts": attempts + 1}


def attempts_conditions(state: State) -> str:
    attempts = state.get("attempts", 0)
    if attempts < 2:
        return "coder"
    return END


def build_graph():
    builder = StateGraph(State)
    builder.add_node("spec", spec_node)
    builder.add_node("coder", coder_node)
    builder.add_node("fake_runner", fake_runner_node)
    builder.add_edge(START, "spec")
    builder.add_edge("spec", "coder")
    builder.add_edge("coder", "fake_runner")
    builder.add_conditional_edges("fake_runner", attempts_conditions, ["coder", END])

    return builder.compile()


if __name__ == "__main__":
    print(build_graph().get_graph().draw_mermaid())
    for etape in build_graph().stream({"task": "fizzbuzz", "attempts": 0}):
        print(etape)
