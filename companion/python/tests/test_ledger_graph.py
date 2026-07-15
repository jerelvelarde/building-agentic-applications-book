from langgraph.types import Command

from book_agent import build_ledger_graph


def initial_state() -> dict:
    return {
        "objective": "Add the reviewed transaction",
        "proposal": {
            "amount_cents": 1299,
            "merchant": "Example Cafe",
            "version": 3,
            "idempotency_key": "txn-proposal-3",
        },
        "decision": "pending",
        "receipt_id": None,
    }


def test_graph_interrupts_and_resumes_same_thread() -> None:
    graph = build_ledger_graph()
    config = {"configurable": {"thread_id": "ledger-thread-1"}}

    paused = graph.invoke(initial_state(), config)
    assert paused["decision"] == "pending"
    assert paused["__interrupt__"]

    resumed = graph.invoke(Command(resume={"approved": True, "proposal_version": 3}), config)
    assert resumed["decision"] == "approved"
    assert resumed["receipt_id"] == "receipt:txn-proposal-3"


def test_graph_rejects_stale_approval_version() -> None:
    graph = build_ledger_graph()
    config = {"configurable": {"thread_id": "ledger-thread-2"}}
    graph.invoke(initial_state(), config)

    try:
        graph.invoke(Command(resume={"approved": True, "proposal_version": 2}), config)
    except ValueError as error:
        assert "current proposal version" in str(error)
    else:
        raise AssertionError("stale approval should fail")
