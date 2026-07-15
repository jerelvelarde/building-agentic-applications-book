import { createHash, randomUUID } from "node:crypto";

export type JsonValue =
  | null
  | boolean
  | number
  | string
  | JsonValue[]
  | JsonObject;
export interface JsonObject {
  readonly [key: string]: JsonValue;
}

export interface Principal {
  readonly id: string;
  readonly roles: readonly string[];
}

export interface WriteRequest {
  readonly requestId: string;
  readonly actionId: string;
  readonly toolName: string;
  readonly arguments: JsonObject;
  readonly requestedBy: string;
  readonly eligibleApproverIds: readonly string[];
  readonly eligibleApproverRoles: readonly string[];
  readonly expiresAt: number;
  readonly idempotencyKey: string;
}

export interface ApprovalGrant {
  readonly grantId: string;
  readonly requestId: string;
  readonly actionId: string;
  readonly actionDigest: string;
  readonly approvedBy: string;
  readonly expiresAt: number;
  readonly idempotencyKey: string;
}

export interface AuditRecord {
  readonly event: "requested" | "approved" | "executed" | "replay_suppressed";
  readonly requestId: string;
  readonly actionId: string;
  readonly actorId: string;
  readonly at: number;
  readonly actionDigest: string;
}

function canonicalJson(value: JsonValue): string {
  if (value === null || typeof value !== "object") return JSON.stringify(value);
  if (Array.isArray(value)) return `[${value.map(canonicalJson).join(",")}]`;
  return `{${Object.keys(value)
    .sort()
    .map((key) => `${JSON.stringify(key)}:${canonicalJson(value[key] ?? null)}`)
    .join(",")}}`;
}

export function actionDigest(request: WriteRequest): string {
  return createHash("sha256")
    .update(
      canonicalJson({
        requestId: request.requestId,
        actionId: request.actionId,
        toolName: request.toolName,
        arguments: request.arguments,
      }),
    )
    .digest("hex");
}

export class GovernedWriteGate<TResult> {
  private readonly requests = new Map<string, WriteRequest>();
  private readonly results = new Map<string, TResult>();
  private readonly auditLog: AuditRecord[] = [];

  constructor(private readonly now: () => number = Date.now) {}

  register(request: WriteRequest): void {
    if (request.expiresAt <= this.now())
      throw new Error("write request is already expired");
    if (this.requests.has(request.requestId))
      throw new Error("duplicate request id");
    this.requests.set(request.requestId, request);
    this.record("requested", request, request.requestedBy);
  }

  approve(
    requestId: string,
    approver: Principal,
    expectedActionId: string,
  ): ApprovalGrant {
    const request = this.requireLiveRequest(requestId);
    if (request.actionId !== expectedActionId)
      throw new Error("approval action binding mismatch");
    const eligible =
      request.eligibleApproverIds.includes(approver.id) ||
      approver.roles.some((role) =>
        request.eligibleApproverRoles.includes(role),
      );
    if (!eligible) throw new Error("principal is not an eligible approver");

    this.record("approved", request, approver.id);
    return {
      grantId: randomUUID(),
      requestId,
      actionId: request.actionId,
      actionDigest: actionDigest(request),
      approvedBy: approver.id,
      expiresAt: request.expiresAt,
      idempotencyKey: request.idempotencyKey,
    };
  }

  async execute(
    grant: ApprovalGrant,
    effect: (request: WriteRequest) => Promise<TResult>,
  ): Promise<TResult> {
    const request = this.requireLiveRequest(grant.requestId);
    if (
      grant.actionId !== request.actionId ||
      grant.actionDigest !== actionDigest(request)
    ) {
      throw new Error("approval grant does not match the stored action");
    }

    const prior = this.results.get(grant.idempotencyKey);
    if (prior !== undefined) {
      this.record("replay_suppressed", request, grant.approvedBy);
      return prior;
    }

    const result = await effect(request);
    this.results.set(grant.idempotencyKey, result);
    this.record("executed", request, grant.approvedBy);
    return result;
  }

  audit(): readonly AuditRecord[] {
    return this.auditLog.map((record) => ({ ...record }));
  }

  private requireLiveRequest(requestId: string): WriteRequest {
    const request = this.requests.get(requestId);
    if (!request) throw new Error("unknown write request");
    if (request.expiresAt <= this.now())
      throw new Error("write request expired");
    return request;
  }

  private record(
    event: AuditRecord["event"],
    request: WriteRequest,
    actorId: string,
  ): void {
    this.auditLog.push({
      event,
      requestId: request.requestId,
      actionId: request.actionId,
      actorId,
      at: this.now(),
      actionDigest: actionDigest(request),
    });
  }
}
