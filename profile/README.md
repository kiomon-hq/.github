<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)"
            srcset="https://raw.githubusercontent.com/kiomon-hq/.github/main/profile/assets/banner-dark.svg">
    <img alt="Kiomon — persistent memory for AI agents and apps"
         src="https://raw.githubusercontent.com/kiomon-hq/.github/main/profile/assets/banner-light.svg"
         width="100%">
  </picture>
</div>

<p align="center">
  <br>
  Kiomon captures what your tools read, write and decide, links it into a graph, and hands an agent
  back a <em>cited context packet</em> rather than a list of search hits — behind a write gate, so
  nothing reaches memory unreviewed.
</p>

<p align="center">
  <a href="https://kiomon.com">Website</a> &nbsp;·&nbsp;
  <a href="https://docs.kiomon.com">Docs</a> &nbsp;·&nbsp;
  <a href="https://kiomon.com/blog">Blog</a> &nbsp;·&nbsp;
  <a href="https://app.kiomon.com/signup">Start free</a>
</p>

## Get started

Sign up at [app.kiomon.com](https://app.kiomon.com/signup), then point any MCP client at
`https://mcp.kiomon.com/mcp` with your API key — Claude, Cursor, Codex, or your own agent:

```sh
claude mcp add kiomon --transport http https://mcp.kiomon.com/mcp \
  --header "Authorization: Bearer $KIOMON_API_KEY"
```

Or call it from code. Both SDKs are dependency-free:

```sh
pip install kiomon            # Python 3.10+
npm install @kiomon/kiomon    # Node 18+, Bun, Deno, Workers
```

Or keep it on your machine — one binary, one SQLite file, no account, no network:

```sh
curl -fsSL https://raw.githubusercontent.com/kiomon-hq/kiomon/main/install.sh | sh
```

## Repositories

| Repository | What it is |
|---|---|
| [`python-sdk`](https://github.com/kiomon-hq/python-sdk) | Python client for the hosted service — typed end to end, standard library only |
| [`typescript-sdk`](https://github.com/kiomon-hq/typescript-sdk) | TypeScript client — `@kiomon/kiomon`, plus the unscoped `kiomon` alias |
| [`kiomon`](https://github.com/kiomon-hq/kiomon) | Kiomon local — the memory engine as one Rust binary and one SQLite file (Apache-2.0) |
| [`docs`](https://github.com/kiomon-hq/docs) | Source of [docs.kiomon.com](https://docs.kiomon.com) |

## Contributing

Issues and pull requests are welcome in the repository you are working in. Every repository shares
this organisation's [contributing guide][contributing], [code of conduct][coc] and
[security policy][security].

## License

SDKs MIT · Kiomon local Apache-2.0 · © Kiomon

[contributing]: https://github.com/kiomon-hq/.github/blob/main/CONTRIBUTING.md
[coc]: https://github.com/kiomon-hq/.github/blob/main/CODE_OF_CONDUCT.md
[security]: https://github.com/kiomon-hq/.github/blob/main/SECURITY.md
