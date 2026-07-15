import type {
  LedgerWritePort,
  TransactionReceipt,
} from "../../../src/level-1/runtime-boundary.ts";
import { executeLedgerWrite } from "../../../src/level-1/runtime-boundary.ts";
import { getLevel1ToolRisk } from "../../../src/level-1/risk.ts";
import type {
  AuthenticatedPrincipal,
  CommitProposalInput,
  CreateProposalInput,
  LedgerPeriod,
  LedgerSummary,
  TransactionProposal,
} from "../shared/contracts.ts";

interface StoredProposal extends TransactionProposal {
  readonly principalId: string;
  readonly tenantId: string;
}

interface StoredTransaction {
  readonly amountCents: number;
  readonly merchant: string;
  readonly receipt: TransactionReceipt;
}

export type LedgerServiceErrorCode =
  | "UNAUTHENTICATED"
  | "FORBIDDEN"
  | "NOT_FOUND"
  | "STALE_PROPOSAL"
  | "INVALID_IDEMPOTENCY_KEY";

export class LedgerServiceError extends Error {
  override readonly name = "LedgerServiceError";
  readonly code: LedgerServiceErrorCode;
  readonly status: number;
  readonly retryable: boolean;

  constructor(
    code: LedgerServiceErrorCode,
    message: string,
    status: number,
    retryable = false,
  ) {
    super(message);
    this.code = code;
    this.status = status;
    this.retryable = retryable;
  }
}

function requirePrincipal(principal: AuthenticatedPrincipal): void {
  if (!principal.principalId || !principal.tenantId) {
    throw new LedgerServiceError(
      "UNAUTHENTICATED",
      "an authenticated principal and tenant are required",
      401,
    );
  }
}

export class LedgerService implements LedgerWritePort {
  private readonly proposals = new Map<string, StoredProposal>();
  private readonly transactionsByIdempotencyKey = new Map<
    string,
    StoredTransaction
  >();
  private readonly transactionsById = new Map<string, StoredTransaction>();
  private proposalCounter = 0;
  private transactionCounter = 0;
  private ledgerRevision = 7;
  private readonly now: () => Date;

  constructor(now: () => Date = () => new Date()) {
    this.now = now;
  }

  readLedger(
    principal: AuthenticatedPrincipal,
    period: LedgerPeriod,
  ): LedgerSummary {
    requirePrincipal(principal);
    const committedSpending = [...this.transactionsById.values()]
      .filter(
        (transaction) => transaction.receipt.tenantId === principal.tenantId,
      )
      .reduce((total, transaction) => total + transaction.amountCents, 0);
    const scale = period === "quarter" ? 3 : 1;
    return {
      schemaVersion: 1,
      ledgerRevision: this.ledgerRevision,
      period,
      incomeCents: 720_000 * scale,
      spendingCents: 184_550 * scale + committedSpending,
      asOf: this.now().toISOString(),
      source: "synthetic-ledger-v1",
    };
  }

  createProposal(
    principal: AuthenticatedPrincipal,
    input: CreateProposalInput,
  ): TransactionProposal {
    requirePrincipal(principal);
    this.proposalCounter += 1;
    const proposalId = `proposal-${this.proposalCounter.toString().padStart(4, "0")}`;
    const proposal: StoredProposal = {
      ...input,
      proposalId,
      proposalVersion: 1,
      idempotencyKey: `${principal.tenantId}:${proposalId}:v1`,
      principalId: principal.principalId,
      tenantId: principal.tenantId,
    };
    this.proposals.set(proposalId, proposal);
    return this.publicProposal(proposal);
  }

  reviseProposal(
    principal: AuthenticatedPrincipal,
    proposalId: string,
    input: CreateProposalInput,
  ): TransactionProposal {
    const current = this.requireOwnedProposal(principal, proposalId);
    const proposalVersion = current.proposalVersion + 1;
    const revised: StoredProposal = {
      ...current,
      ...input,
      proposalVersion,
      idempotencyKey: `${principal.tenantId}:${proposalId}:v${proposalVersion}`,
    };
    this.proposals.set(proposalId, revised);
    return this.publicProposal(revised);
  }

  async approveAndCommit(
    principal: AuthenticatedPrincipal,
    input: CommitProposalInput,
  ): Promise<TransactionReceipt> {
    const proposal = this.requireOwnedProposal(principal, input.proposalId);
    if (proposal.proposalVersion !== input.proposalVersion) {
      throw new LedgerServiceError(
        "STALE_PROPOSAL",
        "approval does not match the current proposal revision",
        409,
      );
    }
    if (proposal.idempotencyKey !== input.idempotencyKey) {
      throw new LedgerServiceError(
        "INVALID_IDEMPOTENCY_KEY",
        "idempotency key does not match the approved proposal",
        409,
      );
    }

    return executeLedgerWrite(
      {
        principalId: principal.principalId,
        tenantId: principal.tenantId,
        approvedProposalVersion: proposal.proposalVersion,
        idempotencyKey: proposal.idempotencyKey,
      },
      {
        amountCents: proposal.amountCents,
        merchant: proposal.merchant,
        proposalVersion: proposal.proposalVersion,
      },
      getLevel1ToolRisk("propose_transaction"),
      this,
    );
  }

  createTransaction(
    input: {
      readonly tenantId: string;
      readonly amountCents: number;
      readonly merchant: string;
      readonly proposalVersion: number;
      readonly idempotencyKey: string;
    },
    principalId: string,
  ): Promise<TransactionReceipt> {
    const prior = this.transactionsByIdempotencyKey.get(input.idempotencyKey);
    if (prior) return Promise.resolve(prior.receipt);

    this.transactionCounter += 1;
    this.ledgerRevision += 1;
    const transactionId = `txn-${this.transactionCounter.toString().padStart(4, "0")}`;
    const receipt: TransactionReceipt = {
      receiptId: `receipt:${transactionId}`,
      transactionId,
      tenantId: input.tenantId,
      createdBy: principalId,
      idempotencyKey: input.idempotencyKey,
      ledgerRevision: this.ledgerRevision,
      committedAt: this.now().toISOString(),
      authoritative: true,
    };
    const stored = {
      amountCents: input.amountCents,
      merchant: input.merchant,
      receipt,
    } satisfies StoredTransaction;
    this.transactionsByIdempotencyKey.set(input.idempotencyKey, stored);
    this.transactionsById.set(transactionId, stored);
    return Promise.resolve(receipt);
  }

  findTransaction(
    principal: AuthenticatedPrincipal,
    transactionId: string,
  ): StoredTransaction {
    requirePrincipal(principal);
    const transaction = this.transactionsById.get(transactionId);
    if (!transaction) {
      throw new LedgerServiceError("NOT_FOUND", "transaction not found", 404);
    }
    if (transaction.receipt.tenantId !== principal.tenantId) {
      throw new LedgerServiceError(
        "FORBIDDEN",
        "transaction belongs to another tenant",
        403,
      );
    }
    return transaction;
  }

  transactionCount(tenantId: string): number {
    return [...this.transactionsById.values()].filter(
      (transaction) => transaction.receipt.tenantId === tenantId,
    ).length;
  }

  private requireOwnedProposal(
    principal: AuthenticatedPrincipal,
    proposalId: string,
  ): StoredProposal {
    requirePrincipal(principal);
    const proposal = this.proposals.get(proposalId);
    if (!proposal) {
      throw new LedgerServiceError("NOT_FOUND", "proposal not found", 404);
    }
    if (
      proposal.tenantId !== principal.tenantId ||
      proposal.principalId !== principal.principalId
    ) {
      throw new LedgerServiceError(
        "FORBIDDEN",
        "proposal is not owned by the authenticated principal",
        403,
      );
    }
    return proposal;
  }

  private publicProposal(proposal: StoredProposal): TransactionProposal {
    return {
      proposalId: proposal.proposalId,
      proposalVersion: proposal.proposalVersion,
      idempotencyKey: proposal.idempotencyKey,
      amountCents: proposal.amountCents,
      merchant: proposal.merchant,
    };
  }
}
