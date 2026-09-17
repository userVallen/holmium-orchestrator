import type { Metadata } from "next";
import { Oxygen, Inter } from "next/font/google";
import "./globals.css";
import { cn } from "@/lib/utils";

const inter = Inter({ subsets: ["latin"], variable: "--font-sans" });

const oxygen = Oxygen({
  variable: "--font-oxygen",
  subsets: ["latin"],
  weight: "400",
});

export const metadata: Metadata = {
  title: "Holmium",
  description: "Holmium orchestrator",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="en"
      className={cn(
        "h-full",
        "antialiased",
        oxygen.variable,
        "font-sans",
        inter.variable,
      )}
    >
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
