"use client";

import { useState, useRef, useEffect } from "react";

import { runAgent } from "@/lib/api";
import { createMessage } from "@/lib/chat";

import { Message, AgentError } from "@/types/agent";

import { InputArea } from "@/components/input-area";
import { ChatArea } from "@/components/chat-area";

export default function Home() {
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, loading]);

  const handleRunAgent = async (prompt: string) => {
    if (!prompt.trim() || loading) return;

    const userMessage: Message = createMessage({
      role: "user",
      content: prompt,
    });

    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);

    try {
      const result = await runAgent(prompt);

      const agentMessage: Message = createMessage({
        role: "agent",
        content: result,
      });

      setMessages((prev) => [...prev, agentMessage]);
    } catch (err: unknown) {
      const errorObject = err as AgentError;

      const errorMessage: Message = createMessage({
        role: "agent",
        content: errorObject.message || "An error occurred.",
      });

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex flex-1 w-full max-h-screen flex-col items-center justify-between font-primary bg-white dark:bg-black">
      <div
        className={`flex flex-col w-full items-center text-center pb-8 ${messages.length === 0 ? `absolute top-60 gap-8 h-auto` : `h-screen justify-between`}`}
      >
        {messages.length === 0 && (
          <h1 className="max-w-xs text-6xl font-heading font-bold leading-10 text-black dark:text-zinc-50">
            Holmium
          </h1>
        )}

        {messages.length > 0 && (
          <ChatArea messages={messages} loading={loading} />
        )}

        <InputArea onSubmit={handleRunAgent} loading={loading} />
      </div>
    </main>
  );
}
