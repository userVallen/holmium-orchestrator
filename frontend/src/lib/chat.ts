import { Message, Role } from "@/types/agent";

const STORAGE_KEY = "chat_history";

interface createMessageInput {
  role: Role;
  content: string;
}

export function createMessage({ role, content }: createMessageInput): Message {
  return {
    id: crypto.randomUUID(),
    role: role,
    content: content,
  };
}

export function loadMessages(): Message[] {
  if (typeof window === "undefined") return [];

  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    return saved ? JSON.parse(saved) : [];
  } catch (err) {
    console.error("Failed to load messages from local storage", err);
    return [];
  }
}

export function saveMessages(messages: Message[]): void {
  if (typeof window === "undefined") return;

  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(messages));
  } catch (err) {
    console.error("Failed to save messages to local storage", err);
  }
}
