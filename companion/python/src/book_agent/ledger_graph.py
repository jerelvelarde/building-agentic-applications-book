from typing import Literal, TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import interrupt


class Proposal(TypedDict):
    amount_cents: int
    merchant: str
    version: int
    idempotency_key: str


class LedgerState(TypedDict):
    objective: str  # UI-owned input
    proposal: Proposal  # agent-owned semantic state
    decision: Literal["pending", "approved", "rejected"]  # human-owned after interrupt
    receipt_id: str | None  # runtime-owned result


class ApprovalDecision(TypedDict):
    approved: bool
    proposal_version: int


def request_approval(state: LedgerState) -> dict[str, str]:
    proposal = state["proposal"]
    # LangGraph restarts this node on resume. Keep side effects after interrupt.
    decision: ApprovalDecision = interrupt(
        {
            "type": "ledger_write_approval",
            "proposal": proposal,
            "expected_version": proposal["version"],
        }
    )
    if decision["proposal_version"] != proposal["version"]:
        raise ValueError("approval does not match current proposal version")
    return {"decision": "approved" if decision["approved"] else "rejected"}


def commit(state: LedgerState) -> dict[str, str | None]:
    if state["decision"] != "approved":
        return {"receipt_id": None}
    # A real adapter would pass this idempotency key to the external write API.
    return {"receipt_id": f"receipt:{state['proposal']['idempotency_key']}"}


def build_ledger_graph():
    builder = StateGraph(LedgerState)
    builder.add_node("request_approval", request_approval)
    builder.add_node("commit", commit)
    builder.add_edge(START, "request_approval")
    builder.add_edge("request_approval", "commit")
    builder.add_edge("commit", END)
    return builder.compile(checkpointer=InMemorySaver())
