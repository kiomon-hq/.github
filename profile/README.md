# Kiomon

**Persistent memory for AI agents and apps.** Capture what your users read and decide,
retrieve it with provenance, and govern its lifecycle — from your own product.

[kiomon.com](https://kiomon.com) · [Documentation](https://kiomon.com/docs)

## Open-source SDKs

| Repository | Registry | Install |
|---|---|---|
| [`python-sdk`](https://github.com/kiomon-hq/python-sdk) | PyPI `kiomon` | `pip install kiomon` |
| [`typescript-sdk`](https://github.com/kiomon-hq/typescript-sdk) | npm `@kiomon/kiomon` and `kiomon` | `npm install @kiomon/kiomon` |

Both SDKs are MIT-licensed, have zero runtime dependencies, and expose the same twelve
memory-native verbs — named exactly like the hosted MCP tools, so a capability you have in an
agent you also have in code. Field names are the wire names in both, so an SDK call can be
diffed against the equivalent MCP tool call.

```
retrieve_memory    search_memory      get_memory        get_workspace_context
get_latest_briefing reflect_session  draft_memory      manage_memory
explore_memory_graph record_outcome   list_workspaces   select_workspace
```

```python
from kiomon import Kiomon

kiomon = Kiomon(api_key=os.environ["KIOMON_API_KEY"])
packet = kiomon.retrieve_memory(intent="execute", query="how does our deploy pipeline work?")
```

```ts
import { Kiomon } from "@kiomon/kiomon";

const kiomon = new Kiomon({ apiKey: process.env.KIOMON_API_KEY! });
const packet = await kiomon.retrieveMemory({ intent: "execute", query: "how does our deploy pipeline work?" });
```

## Contributing

Issues and pull requests are welcome in the repository for the language you are working in. Every
repository shares this organisation's [contributing guide][contributing], [code of conduct][coc]
and [security policy][security].

[contributing]: https://github.com/kiomon-hq/.github/blob/main/CONTRIBUTING.md
[coc]: https://github.com/kiomon-hq/.github/blob/main/CODE_OF_CONDUCT.md
[security]: https://github.com/kiomon-hq/.github/blob/main/SECURITY.md

## License

MIT © Kiomon
