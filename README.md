# Mirror Symmetry Atlas

镜像对称及相关领域的交互式知识平台。项目核心是 YAML 数据真值、学术身份消歧和静态导出的 Next.js 前端。

## 技术栈

- Next.js 16 App Router + TypeScript + React 19
- Tailwind CSS v4
- `react-force-graph-2d`
- `js-yaml`
- GitHub Pages static export (`next.config.ts` 使用 `output: "export"`)

## 开发

```bash
pnpm install
pnpm dev
```

本地预览默认在 `http://localhost:3000`。

## 验证

```bash
pnpm lint
pnpm typecheck
pnpm lint:data
pnpm build
```

`pnpm build` 会先生成 `src/lib/people-names.json`、`src/lib/institution-names.json`，再跑 `scripts/lint-data.py`，最后静态导出到 `out/`。

## 数据维护

- 人物、机构、概念、会议等真值放在 `data/`。
- 论文身份、作者匹配、非数学污染等规则以 `scripts/` 内 SSOT 模块为准，尤其是 `name_match.py`、`paper_identity.py`、`lib_truth.py`、`non_math_keywords.py`。
- 可再生成的 API cache、网页抓取缓存和 arXiv source 默认放在 `.cache/msa/papers/`，不进入 git。可用 `MSA_CACHE_DIR=/path/to/cache` 覆盖。
- 改 `data/**` 前先读 `CONTRIBUTING.md`、`HANDOFF.md` 和项目入口规则。

## 部署

push 到 `main` 后 `.github/workflows/deploy.yml` 会执行：

```bash
pnpm install --frozen-lockfile
pnpm lint
pnpm typecheck
pnpm build
```

通过后上传 `out/` 到 GitHub Pages。
