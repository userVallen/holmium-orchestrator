"use client";

import { useState } from "react";

import { Textarea } from "./ui/textarea";
import { ArrowUp } from "lucide-react";

interface InputAreaProps {
  onSubmit: (prompt: string) => void;
  loading: boolean;
}

export function InputArea({ onSubmit, loading }: InputAreaProps) {
  const [prompt, setPrompt] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!prompt.trim() || loading) return;
    onSubmit(prompt);
    setPrompt("");
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="flex items-center justify-center min-h-16 max-w-[90%] w-160 rounded-[10rem] px-7 py-4 bg-input/50"
    >
      <Textarea
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        onKeyDown={handleKeyDown}
        className="resize-none py-0 min-h-[20px] max-h-[100px] bg-transparent focus-visible:border-none focus-visible:outline-none focus-visible:ring-0 [field-sizing:content]"
        placeholder={loading ? "Agent is thinking..." : "Ask me anything"}
      />

      <button
        type="submit"
        disabled={loading || !prompt.trim()}
        className="flex rounded-full bg-blue-200 p-2 items-center justify-center hover:bg-blue-300 active:scale-90"
      >
        <ArrowUp />
      </button>
    </form>
  );
}
