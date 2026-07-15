import {
  ToolCallStatus,
  useFrontendTool,
  useHumanInTheLoop,
  useRenderTool,
} from "@copilotkit/react-core/v2";
import { z } from "zod";

const visibleLedgerSchema = z.object({
  period: z.enum(["month", "quarter"]),
});

const searchSchema = z.object({
  query: z.string().min(1).max(120),
});

const proposalSchema = z.object({
  amountCents: z.number().int().positive(),
  merchant: z.string().min(1).max(100),
  proposalVersion: z.number().int().positive(),
});

export interface VisibleLedger {
  readonly period: "month" | "quarter";
  readonly incomeCents: number;
  readonly spendingCents: number;
}

export interface LedgerToolOptions {
  readonly authenticated: boolean;
  readonly readVisibleLedger: (
    period: VisibleLedger["period"],
  ) => Promise<VisibleLedger>;
}

export function useLedgerTools(options: LedgerToolOptions): void {
  useFrontendTool<z.output<typeof visibleLedgerSchema>>({
    name: "get_visible_ledger",
    description: "Read the aggregate ledger currently visible in the UI.",
    parameters: visibleLedgerSchema,
    available: options.authenticated,
    handler: async ({ period }, { signal }) => {
      if (signal?.aborted) throw new Error("ledger read aborted");
      return options.readVisibleLedger(period);
    },
  });

  useRenderTool({
    name: "search_transactions",
    parameters: searchSchema,
    render: ({ status, parameters, result }) => {
      if (status === "inProgress") return <p>Preparing transaction search…</p>;
      if (status === "executing") {
        return <p>Searching for “{parameters.query}”…</p>;
      }
      return <pre aria-label="Transaction search result">{result}</pre>;
    },
  });

  useHumanInTheLoop<z.output<typeof proposalSchema>>({
    name: "propose_transaction",
    description: "Ask the user to approve a transaction proposal.",
    parameters: proposalSchema,
    render: (props) => {
      if (props.status === ToolCallStatus.InProgress) {
        return <p>Preparing transaction proposal…</p>;
      }
      if (props.status === ToolCallStatus.Complete) {
        return <p>Decision recorded.</p>;
      }

      const { amountCents, merchant, proposalVersion } = props.args;
      return (
        <section aria-label="Transaction approval">
          <p>
            Add ${(amountCents / 100).toFixed(2)} at {merchant}?
          </p>
          <button
            type="button"
            onClick={() =>
              void props.respond({ approved: false, proposalVersion })
            }
          >
            Reject
          </button>
          <button
            type="button"
            onClick={() =>
              void props.respond({ approved: true, proposalVersion })
            }
          >
            Approve
          </button>
        </section>
      );
    },
  });
}
