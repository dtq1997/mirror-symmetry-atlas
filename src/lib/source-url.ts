/** [Codex] Local evidence paths/placeholders are not public web destinations. */
export function publicSourceUrl(value: string | undefined): string | undefined {
  if (!value) return undefined;
  try {
    const url = new URL(value);
    return ["https:", "http:", "mailto:"].includes(url.protocol) ? value : undefined;
  } catch { return undefined; }
}
