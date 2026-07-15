import { HttpAgent } from "@ag-ui/client";
import { createBot } from "@copilotkit/channels";
import { slack } from "@copilotkit/channels-slack";

export interface SlackBotConfig {
  readonly botToken: string;
  readonly appToken: string;
  readonly agentUrl: string;
  readonly agentAuthorization?: string;
}

export function createSlackAgentBot(config: SlackBotConfig) {
  if (!config.botToken || !config.appToken || !config.agentUrl) {
    throw new Error("Slack tokens and AG-UI agent URL are required");
  }

  const bot = createBot({
    adapters: [
      slack({
        botToken: config.botToken,
        appToken: config.appToken,
        respondTo: {
          directMessages: true,
          appMentions: { reply: "thread" },
          threadReplies: "mentionsOnly",
        },
      }),
    ],
    agent: (threadId) => {
      const agent = new HttpAgent(
        config.agentAuthorization
          ? {
              url: config.agentUrl,
              headers: { Authorization: config.agentAuthorization },
            }
          : { url: config.agentUrl },
      );
      agent.threadId = threadId;
      return agent;
    },
    store: { lockTtl: 60_000, dedupTtl: 300_000 },
  });

  bot.onMention(async ({ thread }) => {
    await thread.runAgent();
  });
  return bot;
}
