import ReactMarkdown from "react-markdown";

import { Message } from "@/types/agent";

import { ScrollArea } from "@/components/ui/scroll-area";
import { Spinner } from "@/components/ui/spinner";

interface ChatAreaProps {
  messages: Message[];
  loading: boolean;
}

export function ChatArea({ messages, loading }: ChatAreaProps) {
  return (
    <ScrollArea className="w-full overflow-auto pb-6">
      <div className="flex flex-col pt-8 gap-6 text-start max-w-2xl mx-auto px-4">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex w-full ${msg.role === "agent" ? "justify-start" : "justify-end"}`}
          >
            <div
              className={`max-w-[80%] rounded-2xl px-5 py-3 text-base shadow-sm 
                ${
                  msg.role === "agent"
                    ? "bg-primary text-primary-foreground"
                    : "bg-card border border-border text-card-foreground prose prose-sm dark:prose-invert"
                }`}
            >
              <ReactMarkdown>{msg.content}</ReactMarkdown>
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex justify-start">
            <div className="flex items-center gap-3 bg-card border border-border text-card-foreground rounded-2xl rounded-bl-none px-5 py-3 text-sm shadow-sm">
              <Spinner className="size-4" />
              <span className="text-muted-foreground font-medium">
                Thinking...
              </span>
            </div>
          </div>
        )}
      </div>
    </ScrollArea>
  );
}
