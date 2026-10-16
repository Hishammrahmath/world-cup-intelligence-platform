import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "MatchIQ · World Cup 2026 Momentum Analytics",
  description: "Event-weighted momentum, turning points, and fact-only explanations for every FIFA World Cup 2026 match.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

