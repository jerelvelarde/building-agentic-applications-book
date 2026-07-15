import type { ToolRiskMetadata } from "./risk.js";

export interface AuthenticatedRequestContext {
  readonly principalId: string;
  readonly tenantId: string;
  readonly approvedProposalVersion: number;
  readonly idempotencyKey: string;
}

export interface CreateTransactionInput {
  readonly tenantId: string;
  readonly amountCents: number;
  readonly merchant: string;
  readonly proposalVersion: number;
  readonly idempotencyKey: string;
}

export interface TransactionReceipt {
  readonly receiptId: string;
  readonly transactionId: string;
  readonly tenantId: string;
  readonly createdBy: string;
  readonly idempotencyKey: string;
  readonly ledgerRevision: number;
  readonly committedAt: string;
  readonly authoritative: true;
}

export interface LedgerWritePort {
  createTransaction(
    input: CreateTransactionInput,
    principalId: string,
  ): Promise<TransactionReceipt>;
}

export async function executeLedgerWrite(
  context: AuthenticatedRequestContext,
  input: Omit<CreateTransactionInput, "tenantId" | "idempotencyKey">,
  risk: ToolRiskMetadata,
  port: LedgerWritePort,
): Promise<TransactionReceipt> {
  if (!context.principalId || !context.tenantId) {
    throw new Error("authenticated principal and tenant are required");
  }
  if (risk.effect !== "write" || risk.approval !== "always") {
    throw new Error("ledger mutation must use an approval-gated write policy");
  }
  if (input.proposalVersion !== context.approvedProposalVersion) {
    throw new Error("approval does not match the current proposal version");
  }
  if (!context.idempotencyKey) {
    throw new Error("idempotency key is required");
  }
  if (input.amountCents <= 0 || !Number.isInteger(input.amountCents)) {
    throw new Error("amount must be a positive integer number of cents");
  }
  if (!input.merchant.trim()) {
    throw new Error("merchant is required");
  }

  // Only the authenticated server runtime receives this port. A frontend tool
  // can propose the mutation, but it cannot bypass tenant authorization here.
  return port.createTransaction(
    {
      ...input,
      tenantId: context.tenantId,
      idempotencyKey: context.idempotencyKey,
    },
    context.principalId,
  );
}
