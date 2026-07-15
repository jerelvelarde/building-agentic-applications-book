import { z } from "zod";

export const ledgerPeriodSchema = z.enum(["month", "quarter"]);

export const ledgerSummarySchema = z
  .object({
    schemaVersion: z.literal(1),
    ledgerRevision: z.number().int().nonnegative(),
    period: ledgerPeriodSchema,
    incomeCents: z.number().int().nonnegative(),
    spendingCents: z.number().int().nonnegative(),
    asOf: z.string().datetime(),
    source: z.literal("synthetic-ledger-v1"),
  })
  .strict();

export const createProposalInputSchema = z
  .object({
    amountCents: z.number().int().positive(),
    merchant: z.string().trim().min(1).max(100),
  })
  .strict();

export const transactionProposalSchema = createProposalInputSchema
  .extend({
    proposalId: z.string().min(1),
    proposalVersion: z.number().int().positive(),
    idempotencyKey: z.string().min(1),
  })
  .strict();

export const commitProposalInputSchema = z
  .object({
    proposalId: z.string().min(1),
    proposalVersion: z.number().int().positive(),
    idempotencyKey: z.string().min(1),
  })
  .strict();

export const transactionReceiptSchema = z
  .object({
    receiptId: z.string().min(1),
    transactionId: z.string().min(1),
    tenantId: z.string().min(1),
    createdBy: z.string().min(1),
    idempotencyKey: z.string().min(1),
    ledgerRevision: z.number().int().positive(),
    committedAt: z.string().datetime(),
    authoritative: z.literal(true),
  })
  .strict();

export const apiErrorSchema = z
  .object({
    error: z.object({
      code: z.string().min(1),
      message: z.string().min(1),
      retryable: z.boolean(),
    }),
  })
  .strict();

export type LedgerPeriod = z.output<typeof ledgerPeriodSchema>;
export type LedgerSummary = z.output<typeof ledgerSummarySchema>;
export type CreateProposalInput = z.output<typeof createProposalInputSchema>;
export type TransactionProposal = z.output<typeof transactionProposalSchema>;
export type CommitProposalInput = z.output<typeof commitProposalInputSchema>;
export type AuthoritativeReceipt = z.output<typeof transactionReceiptSchema>;
export type ApiErrorBody = z.output<typeof apiErrorSchema>;

export interface AuthenticatedPrincipal {
  readonly principalId: string;
  readonly tenantId: string;
}
