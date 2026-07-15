import { EventType, type CustomEvent } from "@ag-ui/core";
import type { MachineIntent, PolicyDecision } from "./machine-policy.js";

export interface MachineEnforcer {
  authorize(intent: MachineIntent): Promise<PolicyDecision>;
}

export interface AgUiEventSink {
  emit(event: CustomEvent): void;
}

export class VisibleMachineBridge {
  constructor(
    private readonly enforcer: MachineEnforcer,
    private readonly events: AgUiEventSink,
  ) {}

  async request(intent: MachineIntent): Promise<PolicyDecision> {
    this.events.emit({
      type: EventType.CUSTOM,
      name: "machine.intent.proposed",
      value: intent,
    });

    // AG-UI provides visibility. Only this separately deployed enforcer can
    // authorize the action; emitting an "approved" event grants no capability.
    const decision = await this.enforcer.authorize(intent);
    this.events.emit({
      type: EventType.CUSTOM,
      name: "machine.intent.decided",
      value: decision,
    });
    return decision;
  }
}
