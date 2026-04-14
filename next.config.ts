import type { NextConfig } from "next";

const isProd = process.env.NODE_ENV === "production";

const nextConfig: NextConfig = {
  output: "export",
  basePath: isProd ? "/mirror-symmetry-atlas" : "",
  images: { unoptimized: true },
  turbopack: {},
};

export default nextConfig;
