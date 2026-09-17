import { AgentResponse } from "@/types/agent";

export async function runAgent(prompt: string): Promise<string> {
  const res = await fetch("http://127.0.0.1:8000/api/agent/run", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt }),
  });

  if (!res.ok) {
    throw new Error("Failed to connect to the FastAPI backend.");
  }

  const data: AgentResponse = await res.json();
  return data.agent_response || "No response generated.";
}
