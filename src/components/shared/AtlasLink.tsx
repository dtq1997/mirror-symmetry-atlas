import NextLink from "next/link";
import type { ComponentProps } from "react";
import { entityRoute } from "@/lib/entity-route";

/** [Codex] Uncatalogued references remain visible without sending readers to 404. */
export default function AtlasLink({ href, children, ...props }: ComponentProps<typeof NextLink>) {
  const route = typeof href === "string" ? entityRoute(href) : null;
  const label = route && children === route.slug ? route.label : children;
  if (route && !route.exists) {
    return <span className={props.className} title="尚未建档，暂无详情页" data-unresolved-reference={route.slug}>
      {label}<span className="ml-1 text-[10px] text-[#8888a0]">（未建档）</span>
    </span>;
  }
  return <NextLink href={href} {...props}>{label}</NextLink>;
}
