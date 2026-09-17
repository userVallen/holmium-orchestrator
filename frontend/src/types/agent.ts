export type Role = "user" | "agent";

export interface Message {
  id: string;
  role: Role;
  content: string;
}

export interface AgentRequest {
  prompt: string;
}

export interface AgentResponse {
  agent_response: string;
}

export interface AgentError {
  code: number;
  message: string;
}
