import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import Link from "next/link";
import "katex/dist/katex.min.css";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Mirror Symmetry Atlas",
  description:
    "Interactive knowledge platform for the mirror symmetry community",
};

const NAV_ITEMS = [
  { href: "/", label: "首页" },
  { href: "/people", label: "人物" },
  { href: "/concepts", label: "概念" },
  { href: "/timeline", label: "时间线" },
  { href: "/papers", label: "论文" },
  { href: "/conferences", label: "会议" },
  { href: "/literature", label: "文献" },
];

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="zh-CN"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased dark`}
    >
      <body className="min-h-full flex flex-col bg-[#0a0a0f] text-[#e8e8f0]">
        {/* Navigation */}
        <nav className="h-[56px] border-b border-[#2a2a3a] bg-[#14141f]/80 backdrop-blur-md sticky top-0 z-50 flex items-center px-6 shrink-0">
          <Link
            href="/"
            className="font-semibold text-lg tracking-tight mr-8 text-[#e8e8f0] hover:text-[#6366f1] transition-colors"
          >
            Mirror Symmetry Atlas
          </Link>
          <div className="flex items-center gap-1">
            {NAV_ITEMS.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className="px-3 py-1.5 text-sm text-[#8888a0] hover:text-[#e8e8f0] hover:bg-[#2a2a3a] rounded-md transition-colors"
              >
                {item.label}
              </Link>
            ))}
          </div>
        </nav>

        {/* Main content */}
        <main className="flex-1 flex flex-col">{children}</main>
      </body>
    </html>
  );
}
