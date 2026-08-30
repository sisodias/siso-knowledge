# GitHub Repo Research Log

Research for indices 0-89. Researched via `gh repo view` and README fetch.
---

### slopus/happy (15552 stars)

**URL:** https://github.com/slopus/happy
**Description:** Mobile and Web client for Codex and Claude Code, with realtime voice, encryption and fully featured

**Research:** A mobile and web client for Claude Code and Codex CLI. Provides end-to-end encrypted remote access to AI coding agents from any device. Has iOS, Android, and web apps. The CLI component (`happy-coder`) pairs with the apps to enable mobile-first AI coding sessions. Directly relevant to Claude Code ecosystem -- adds a remote/mobile control plane to the agent.
---

### ansible/awx (15320 stars)

**URL:** https://github.com/ansible/awx
**Description:** AWX provides a web-based user interface, REST API, and task engine built on top of Ansible. It is one of the upstream projects for Red Hat Ansible Automation Platform.

**Research:** Enterprise-grade Ansible orchestration platform with web UI, REST API, and task engine. While not AI-native, AWX is highly relevant to autonomous agent infrastructure -- it provides the operational backbone for managing infrastructure-as-code at scale. Could serve as a model for AI agent task execution systems. The API-driven architecture is directly applicable to agent task queuing and job scheduling.
---

### volcengine/OpenViking (15312 stars)

**URL:** https://github.com/volcengine/OpenViking
**Description:** OpenViking is an open-source context database designed specifically for AI Agents (such as openclaw). OpenViking unifies the management of context (memory, resources, and skills) that Agents need through a file system paradigm, enabling hierarchical context delivery and self-evolving.

**Research:** A context database specifically built for AI agents. Uses a filesystem paradigm to unify memory, resources, and skills management. Addresses key agent pain points: fragmented context, surging context demand, poor retrieval effectiveness, unobservable context chains, and limited memory iteration. Explicitly mentions OpenClaw as a target integration. This is directly adjacent to the OpenClaw/Claude Code ecosystem -- could be a memory layer for autonomous agents. Filed under AI agents, memory systems.
---

### plandex-ai/plandex (15092 stars)

**URL:** https://github.com/plandex-ai/plandex
**Description:** Open source AI coding agent. Designed for large projects and real world tasks.

**Research:** An AI coding agent designed for large, real-world software projects. Takes a long-running, context-preserving approach to multi-file code changes. Has a server component and a CLI. Similar in spirit to Claude Code but with its own agent runtime. Directly competitive/complementary to Claude Code -- useful to understand the landscape of AI coding agents. Key differentiator: designed specifically for long-running, complex tasks.
---

### RightNow-AI/openfang (14812 stars)

**URL:** https://github.com/RightNow-AI/openfang
**Description:** Open-source Agent Operating System

**Research:** An open-source Agent OS built in Rust (137K LOC, 14 crates, 1767+ tests). Designed for autonomous 24/7 agents that work on schedules, build knowledge graphs, monitor targets, generate leads, manage social media. Single ~32MB binary. Dashboard at localhost:4200. Notably different from Python-based agent frameworks -- Rust-first gives it performance and reliability advantages. The "Agent OS" framing is directly relevant to autonomous agent infrastructure. Filed under AI agents, developer tooling.
---

### kepano/obsidian-skills (14583 stars)

**URL:** https://github.com/kepano/obsidian-skills
**Description:** Agent skills for Obsidian. Teach your agent to use Markdown, Bases, JSON Canvas, and use the CLI.

**Research:** A set of Agent Skills for Obsidian-compatible content formats. Follows the Agent Skills specification so they're compatible with Claude Code, Codex CLI, and OpenCode. Includes skills for Obsidian Flavored Markdown, Bases (database tables), JSON Canvas, Obsidian CLI, and Defuddle (web content extraction). Directly relevant to Claude Code skills ecosystem -- an official-looking set of production-quality skills for a popular note-taking platform. Low barrier to integrate.
---

### AndyMik90/Aperant (13352 stars)

**URL:** https://github.com/AndyMik90/Aperant
**Description:** Autonomous multi-session AI coding

**Research:** Multi-agent autonomous coding framework with a Kanban board UI. The repo is branded as "Auto Claude" and mentions being listed in Awesome Claude Code. Supports Windows, macOS (Apple Silicon + Intel), and Linux (AppImage, Debian, Flatpak). Cross-platform AI coding agent with a GUI workflow. Multi-agent nature is relevant to Claude Code infrastructure discussions.
---

### eigent-ai/eigent (13042 stars)

**URL:** https://github.com/eigent-ai/eigent
**Description:** Eigent: The Open Source Cowork Desktop to Unlock Your Exceptional Productivity. Local and Free Alternative to Claude Cowork.

**Research:** Open-source Cowork desktop application built on CAMEL-AI. Brings multi-agent workforce coordination with parallel execution, customization, and privacy protection. 100% open source, local deployment, MCP integration, enterprise SSO/access control. Explicitly positioned as an alternative to Claude Cowork. Relevant to multi-agent coordination and Claude Code-adjacent tooling.
---

### NevaMind-AI/memU (13004 stars)

**URL:** https://github.com/NevaMind-AI/memU
**Description:** Memory for 24/7 proactive agents like openclaw (moltbot, clawdbot).

**Research:** A memory framework for 24/7 proactive agents. Reduces LLM token cost for always-online agents by ~1/10. Treats memory like a filesystem (folders=categories, files=memory items). Includes memU Bot -- an enterprise-ready OpenClaw alternative. Explicitly designed as an alternative to OpenClaw with long-term memory and proactive intent understanding. Filed under AI agents, memory systems.
---

### ag-ui-protocol/ag-ui (12522 stars)

**URL:** https://github.com/ag-ui-protocol/ag-ui
**Description:** AG-UI: the Agent-User Interaction Protocol. Bring Agents into Frontend Applications.

**Research:** An open, lightweight, event-based protocol for agent-human interaction. Agent backends emit events compatible with ~16 standard event types; frontend apps consume them. Works with any transport (SSE, WebSockets, webhooks). Ships with reference HTTP implementation and default connector. Created by the CopilotKit team. Directly relevant to AI agent UX/interaction patterns -- a standardization effort for how agents communicate with user-facing apps.
---

### steveyegge/gastown (12430 stars)

**URL:** https://github.com/steveyegge/gastown
**Description:** Gas Town - multi-agent workspace manager

**Research:** Multi-agent orchestration system explicitly built for Claude Code. Persists work state in git-backed hooks so agents survive restarts. Has a "Mayor" AI coordinator, "Rig" per-project workers, "Polecats" worker agents, and "Beads" ledger for state. Enables scaling to 20-30 agents without chaos. Directly relevant to Claude Code infrastructure -- it's a Claude Code-native multi-agent coordination layer using git worktrees for isolation.
---

### PipedreamHQ/pipedream (11178 stars)

**URL:** https://github.com/PipedreamHQ/pipedream
**Description:** Connect APIs, remarkably fast. Free for developers.

**Research:** API integration and workflow automation platform. Connects APIs with code (Node.js, Python, Go, Bash). Free for developers. While not AI-specific, it's a powerful tool for building API integrations that AI agents could use for tool calling, webhooks, and workflow automation. Useful for agent tool-building patterns.
---

### getumbrel/umbrel (10792 stars)

**URL:** https://github.com/getumbrel/umbrel
**Description:** An elegant home server OS. Run OpenClaw, store your files and photos, run a Bitcoin node, and do more with over 300 apps in the Umbrel App Store.

**Research:** A home server OS for self-hosting. Explicitly mentions running OpenClaw as an app. Enables self-hosting data and services at home. 300+ apps in the app store. Relevant to the OpenClaw deployment ecosystem -- provides an OS-level container for running OpenClaw and other self-hosted services.
---

### OffcierCia/DeFi-Developer-Road-Map (10711 stars)

**URL:** https://github.com/OffcierCia/DeFi-Developer-Road-Map
**Description:** DeFi Developer roadmap is a curated Developer handbook which includes a list of the best tools for DApps development, resources and references!

**Research:** A curated DeFi/blockchain developer handbook. Not directly relevant to AI agents or Claude Code, but notable for its popularity (10K+ stars) as a developer resource hub. Useful if researching developer tooling ecosystems but low relevance to autonomous agent infrastructure.
---

### cft0808/edict (10663 stars)

**URL:** https://github.com/cft0808/edict
**Description:** 三省六部制 . OpenClaw Multi-Agent Orchestration System -- 9 specialized AI agents with real-time dashboard, model config, and full audit trails

**Research:** A multi-agent orchestration system for OpenClaw inspired by Chinese imperial bureaucracy ("三省六部制" -- Three Departments and Six Ministries). 12 agents total (11 business roles + 1 compatibility role): Crown Prince (sorting), Middle Secretariat (planning), Chancellery (review/rejection), Department of State Affairs (dispatch), and Six Ministries executing in parallel. React dashboard with real-time monitoring. Backend uses stdlib only (no external dependencies). Explicitly requires OpenClaw. Directly relevant to multi-agent orchestration patterns for OpenClaw.
---

### timlrx/tailwind-nextjs-starter-blog (10424 stars)

**URL:** https://github.com/timlrx/tailwind-nextjs-starter-blog
**Description:** Next.js, Tailwind CSS blogging starter template. Configured with the latest technologies for technical writing.

**Research:** A popular Next.js + Tailwind CSS blogging starter template with MDX support. High star count driven by being a go-to starter for developer blogs. Not AI-agent specific, but useful as a reference for building content-heavy sites. The Next.js App Router + Contentlayer pattern is relevant for building AI agent documentation or blog UIs.
---

### cloudflare/moltworker (9661 stars)

**URL:** https://github.com/cloudflare/moltworker
**Description:** Run OpenClaw (formerly Moltbot, formerly Clawdbot) on Cloudflare Workers

**Research:** A proof-of-concept running OpenClaw in Cloudflare Workers (Cloudflare Sandbox). Enables OpenClaw with Cloudflare Access auth, Browser Rendering, AI Gateway, and R2 Storage. ~$34.50/month for 24/7 operation. Relevant to OpenClaw deployment patterns -- shows a serverless/cloud-native approach to running autonomous agents.
---

### mcp-use/mcp-use (9450 stars)

**URL:** https://github.com/mcp-use/mcp-use
**Description:** Fullstack MCP framework to build MCP Apps for ChatGPT/Claude and MCP Servers for AI Agents.

**Research:** A full-stack MCP framework from Manufact for building MCP servers and MCP apps. Provides TypeScript and Python SDKs, an MCP Inspector for debugging, and cloud deployment via Manufact MCP Cloud. Directly relevant to Claude Code's MCP integration -- it's a framework for building the tools and servers that Claude Code agents consume. High relevance to Claude Code, AI agents, and developer tooling.
---

### diet103/claude-code-infrastructure-showcase (9270 stars)

**URL:** https://github.com/diet103/claude-code-infrastructure-showcase
**Description:** Examples of my Claude Code infrastructure with skill auto-activation, hooks, and agents

**Research:** A production-tested reference library for Claude Code infrastructure patterns. Solves the "skills don't activate automatically" problem. Includes auto-activating skills via hooks, modular skill patterns (500-line rule), specialized agents, and a dev docs system that survives context resets. 6 months of real-world iteration distilled into copy-paste patterns. Extremely high relevance to Claude Code -- directly addresses practical scaling challenges.
---

### davidkimai/Context-Engineering (8571 stars)

**URL:** https://github.com/davidkimai/Context-Engineering
**Description:** A frontier, first-principles handbook for moving beyond prompt engineering to the discipline of context design, orchestration, and optimization.

**Research:** A comprehensive handbook on context engineering (filling the context window optimally) inspired by Andrej Karpathy. References 1400+ research papers. Includes agent commands for Claude Code, OpenCode, Amp, Kiro, Codex, and Gemini CLI. Covers context rot, IBM Zurich's cognitive tools research, MemOS, latent reasoning, and dynamic recursive depths. Extremely high relevance to AI agent optimization -- this is the theoretical foundation for making autonomous agents more effective by managing their context.
---

### manaflow-ai/cmux (7844 stars)

**URL:** https://github.com/manaflow-ai/cmux
**Description:** Ghostty-based macOS terminal with vertical tabs and notifications for AI coding agents

**Research:** A macOS terminal built on Ghostty with features designed for AI coding agents: notification rings when agents need attention, notification panel, in-app browser. 17-language internationalization. Downloadable as DMG. Relevant to Claude Code user experience -- a terminal purpose-built for watching over AI coding agents, similar to the superset-sh/superset project.
---

### automazeio/ccpm (7681 stars)

**URL:** https://github.com/automazeio/ccpm
**Description:** Project management skill system for Agents that uses GitHub Issues and Git worktrees for parallel agent execution.

**Research:** Agent Skills-compatible project management system. Uses GitHub Issues as the task database and git worktrees for parallel agent execution. Traceable workflow from PRD -> Epic -> GitHub Issues -> production code. Works with Claude Code, Codex, OpenCode, Factory, Amp, Cursor, and any Agent Skills-compatible harness. High relevance to AI agent task management and Claude Code integration patterns.
---

### HumanAIGC/EMO (7633 stars)

**URL:** https://github.com/HumanAIGC/EMO
**Description:** Emote Portrait Alive: Generating Expressive Portrait Videos with Audio2Video Diffusion Model under Weak Conditions

**Research:** Alibaba's ECCV 2024 paper on generating expressive portrait videos from audio using diffusion models. Not relevant to AI agents, Claude Code, or autonomous agents. Filed under AI multimedia/generative AI.
---

### snarktank/ai-dev-tasks (7633 stars)

**URL:** https://github.com/snarktank/ai-dev-tasks
**Description:** A simple task management system for managing AI dev agents

**Research:** Structured markdown-based workflow for AI-assisted feature development. Provides PRD templates, task generation from PRDs, and iterative implementation with checkpoints. Works with Amp, Claude Code, Windsurf, and other AI coding assistants. PRD -> task list -> one-task-at-a-time implementation with human review. Relevant to AI agent task management patterns.
---

### leerob/next-mdx-blog (7563 stars)

**URL:** https://github.com/leerob/next-mdx-blog
**Description:** Next.js + MDX blog template with Tailwind CSS and TypeScript.

**Research:** Lee Robinson's blog template. High star count from Lee's influence in the Next.js community. Not AI-agent specific but useful as a reference for content sites. Similar to the timlrx/tailwind-nextjs-starter-blog.
---

### MemTensor/MemOS (7375 stars)

**URL:** https://github.com/MemTensor/MemOS
**Description:** AI memory OS for LLM and Agent systems (moltbot, clawdbot, openclaw), enabling persistent Skill memory for cross-task skill reuse and evolution.

**Research:** An AI memory OS for LLM/agent systems. Targets moltbot, clawdbot, and openclaw. Enables persistent skill memory for cross-task reuse and evolution. Claims +43.70% accuracy vs OpenAI Memory. Apache 2.0 licensed. Filed under AI agents, memory systems -- directly competes with NevaMind-AI/memU in the agent memory space.
---

### superset-sh/superset (7305 stars)

**URL:** https://github.com/superset-sh/superset
**Description:** IDE for the AI Agents Era - Run an army of Claude Code, Codex, etc. on your machine

**Research:** A macOS app that lets you run multiple Claude Code, Codex, and other CLI agents simultaneously with worktree isolation, agent monitoring, diff viewing, and workspace presets. Self-described as "The Terminal for Coding Agents." Run 10+ agents in parallel. Very high relevance to Claude Code -- it's a GUI wrapper for managing Claude Code at scale.
---

### HKUDS/ClawWork (7281 stars)

**URL:** https://github.com/HKUDS/ClawWork
**Description:** ClawWork: OpenClaw as Your AI Coworker - $15K earned in 11 Hours

**Research:** An OpenClaw-based AI coworker system. Economic benchmark where AI agents must earn income by completing real professional tasks (from GDPVal dataset) and pay for their own token usage. Top agent (ATIC + Qwen3.5-Plus) earned ~$19.9K in 8 hours. Relevant to OpenClaw ecosystem -- demonstrates economic viability of autonomous agents and provides a benchmark framework for evaluating agent productivity.
---

### MiroMindAI/MiroThinker (7024 stars)

**URL:** https://github.com/MiroMindAI/MiroThinker
**Description:** MiroThinker is a deep research agent optimized for complex research and prediction tasks. Achieves 88.2 on BrowseComp.

**Research:** Deep research agent optimized for complex research and prediction. MiroThinker-H1 achieves 88.2 on BrowseComp, MiroThinker-1.7-mini achieves 72.3 on BrowseComp-ZH with only 30B parameters. Supports interactive scaling as a third dimension of performance. Available via online demo (dr.miromind.ai) and open-source on HuggingFace. Not directly Claude Code-related but highly relevant to AI agent capability benchmarks and the deep research agent category.
---

*Skipped: Yechan-Heo/oh-my-claudecode -- repository no longer exists (404 from GitHub)*
---

### camel-ai/owl (19208 stars)

**URL:** https://github.com/camel-ai/owl
**Description:** OWL: Optimized Workforce Learning for General Multi-Agent Assistance in Real-World Task Automation

**Research:** CAMEL-AI's OWL is a multi-agent framework for real-world task automation, using "Optimized Workforce Learning" to coordinate multiple agents. Backed by a 2025 arXiv paper. One of the largest multi-agent frameworks by stars. Strong relevance to autonomous agent ecosystems -- models agent collaboration patterns that could inform Claude Code sub-agent orchestration strategies.
---

### iOfficeAI/AionUi (19036 stars)

**URL:** https://github.com/iOfficeAI/AionUi
**Description:** Free, local, open-source 24/7 Cowork app and OpenClaw for Gemini CLI, Claude Code, Codex, OpenCode, Qwen Code, Goose CLI, Auggie, and more

**Research:** An open-source cowork desktop app that integrates with Claude Code, Codex, Gemini CLI, and other AI coding agents. Positions itself as a "free Claude Cowork" alternative. The project explicitly references OpenClaw and mentions 24/7 always-on operation. High relevance to Claude Code and OpenClaw ecosystems -- it's a desktop wrapper for AI coding agents with a coworker paradigm.
---

### google/adk-python (18417 stars)

**URL:** https://github.com/google/adk-python
**Description:** An open-source, code-first Python toolkit for building, evaluating, and deploying sophisticated AI agents with flexibility and control.

**Research:** Google's Agent Development Kit (ADK) is a code-first Python framework for building, evaluating, and deploying AI agents. Model-agnostic and deployment-agnostic, though optimized for Gemini. Part of a broader Google ecosystem including ADK for Java, Go, and Web. Directly relevant to agent framework development -- demonstrates Google's take on agent orchestration patterns, tool use, and evaluation pipelines.
---

### livekit/livekit (17654 stars)

**URL:** https://github.com/livekit/livekit
**Description:** End-to-end realtime stack for connecting humans and AI

**Research:** LiveKit provides real-time audio/video infrastructure for connecting humans and AI. Supports AI voice agents with WebRTC. The realtime audio channel could be a key integration point for voice-enabled AI coding agents or autonomous agents that need real-time communication. Relevant to AI agent infrastructure -- provides the communication substrate for real-time agent-human interaction.
---

### yetone/avante.nvim (17586 stars)

**URL:** https://github.com/yetone/avante.nvim
**Description:** Use your Neovim like using Cursor AI IDE!

**Research:** A Neovim plugin that replicates Cursor AI IDE behavior, providing AI-driven code suggestions and the ability to apply AI recommendations directly in Neovim. Written in Lua with a Rust backend. Represents an alternative to Claude Code for terminal-native users -- brings AI coding assistance to the Neovim ecosystem with a Cursor-like UX. High relevance to Claude Code's competitive landscape.
---

### TransformerOptimus/SuperAGI (17277 stars)

**URL:** https://github.com/TransformerOptimus/SuperAGI
**Description:** SuperAGI - A dev-first open source autonomous AI agent framework. Enabling developers to build, manage & run useful autonomous agents quickly and reliably.

**Research:** SuperAGI is a dev-first autonomous AI agent framework focused on building, managing, and running agents reliably. One of the older names in the open-source agent space. Provides agent spawning, tool use, and execution management. Relevant to agent framework comparison -- represents a mature approach to autonomous agent orchestration that pre-dates many Claude Code integrations.
---

### camel-ai/camel (16391 stars)

**URL:** https://github.com/camel-ai/camel
**Description:** CAMEL: The first and the best multi-agent framework. Finding the Scaling Law of Agents.

**Research:** The original CAMEL multi-agent framework -- one of the earliest academic/industry attempts to systematize multi-agent collaboration. Published foundational papers on role-playing agent cooperation. Now a full ecosystem including OWL. Key research influence on how multiple agents should communicate and divide labor. Highly relevant to understanding multi-agent orchestration theory.
---

### OthmanAdi/planning-with-files (16344 stars)

**URL:** https://github.com/OthmanAdi/planning-with-files
**Description:** Claude Code skill implementing Manus-style persistent markdown planning -- the workflow pattern behind the $2B acquisition.

**Research:** A Claude Code skill that implements persistent markdown-based planning, inspired by the Manus AI workflow. Explicitly references the Manus $2B acquisition as the business model inspiration. Provides structured task planning that survives agent restarts -- directly relevant to Claude Code's skill system and the challenge of maintaining agent state across sessions.
---

### agent0ai/agent-zero (16182 stars)

**URL:** https://github.com/agent0ai/agent-zero
**Description:** Agent Zero AI framework

**Research:** Agent Zero is an organic agentic framework that "grows and learns with you" -- uses a skills system based on portable SKILL.md format compatible with Claude Code and Codex. Emphasizes lightweight, dependency-free execution. High relevance to Claude Code -- the skills format is directly compatible, making it a sibling ecosystem in the agent skills landscape.
---

### karpathy/llm-council (15873 stars)

**URL:** https://github.com/karpathy/llm-council
**Description:** LLM Council works together to answer your hardest questions

**Research:** Andrej Karpathy's implementation of a multi-LLM "council" where multiple models vote or collaborate to answer complex questions. Simple but influential -- demonstrates ensemble/ deliberation patterns for AI agents. Authoritative source (Karpathy) gives it outsized influence on how the field thinks about multi-model agent collaboration.
---

### refly-ai/refly (7013 stars)

**URL:** https://github.com/refly-ai/refly
**Description:** The first open-source agent skills builder. Define skills by vibe workflow, run on Claude Code, Cursor, Codex & more.

**Research:** An open-source skills builder for AI agents. Lets you define skills through a visual "vibe workflow" builder, deployable to Claude Code, Cursor, Codex, and more. Explicitly supports OpenClaw/Clawdbot. Positions skills as "infrastructure, not prompts." Highly relevant to Claude Code's skill system -- represents a no-code/low-code approach to creating Claude Code-compatible skills. Also integrates with Lovable, Slack, and Lark/Feishu.
---

### InternLM/MindSearch (6806 stars)

**URL:** https://github.com/InternLM/MindSearch
**Description:** An LLM-based Multi-agent Framework of Web Search Engine (like Perplexity.ai Pro and SearchGPT)

**Research:** MindSearch is InternLM's multi-agent web search framework -- multiple LLM agents cooperate to perform deep web research, mimicking human search behavior with concurrent querying. Based on Lagent v0.5. Comparable to Perplexity Pro. Relevant to AI agent research capabilities -- demonstrates how to coordinate multiple agents for complex information retrieval tasks.
---

### VoltAgent/voltagent (6791 stars)

**URL:** https://github.com/VoltAgent/voltagent
**Description:** AI Agent Engineering Platform built on an Open Source TypeScript AI Agent Framework

**Research:** VoltAgent is a TypeScript-native AI agent framework and engineering platform. Built around the idea of composable agent components. Cross-platform with i18n support (Chinese, Japanese, Korean). Relevant to Claude Code's ecosystem -- TypeScript/JavaScript is the language of many Claude Code extensions and hooks, making this a natural integration target for Claude Code-based workflows.
---

### teng-lin/notebooklm-py (6184 stars)

**URL:** https://github.com/teng-lin/notebooklm-py
**Description:** Unofficial Python API and agentic skill for Google NotebookLM. Full programmatic access to NotebookLM's features via Python, CLI, and AI agents like Claude Code, Codex, and OpenClaw.

**Research:** An unofficial but comprehensive Python client for Google NotebookLM, including a ready-made agentic skill for Claude Code, Codex, and OpenClaw. Exposes NotebookLM features (sources, summaries, audio overviews) programmatically. Relevant to Claude Code -- provides a skill that gives Claude Code access to NotebookLM's research/organization capabilities, bridging personal knowledge management with AI coding.
---

### Shopify/polaris-react (6106 stars)

**URL:** https://github.com/Shopify/polaris-react
**Description:** Shopify's Polaris Design System - React implementation (Deprecated)

**Research:** Polaris React is now deprecated in favor of Polaris Web Components (October 2025). The shift from React to Web Components reflects a broader industry move toward framework-agnostic UI components. Interesting as a design system reference for agent UI work, but not directly relevant to AI agent development. Included for completeness on Shopify's design system evolution.
---

### BrowserMCP/mcp (6083 stars)

**URL:** https://github.com/BrowserMCP/mcp
**Description:** Browser MCP is a Model Context Provider (MCP) server that allows AI applications to control your browser

**Research:** BrowserMCP is an MCP server that gives AI agents full browser control using your existing browser profile. Runs locally for privacy, avoids bot detection by using real browser fingerprints. Directly relevant to Claude Code and AI agent ecosystems -- browser automation is a major gap in CLI-based agents, and MCP integration means it could work seamlessly with Claude Code's tool system.
---

### kyegomez/swarms (5906 stars)

**URL:** https://github.com/kyegomez/swarms
**Description:** The Enterprise-Grade Production-Ready Multi-Agent Orchestration Framework.

**Research:** Swarms (from Agora) is an enterprise-grade multi-agent orchestration framework. Positions itself as production-ready with a focus on swarming patterns -- many small agents cooperating like a hive. Agora is an open-source AI research org. Relevant to multi-agent orchestration comparison -- represents a more aggressive "many agents" approach vs. the "few specialized agents" approach in frameworks like CAMEL.
---

### Uniswap/web3-react (5690 stars)

**URL:** https://github.com/Uniswap/web3-react
**Description:** A simple, maximally extensible, dependency minimized framework for building modern Ethereum dApps

**Research:** Web3-react is Uniswap's React hook-based framework for Ethereum dApp development. Now in beta as v8. Provides connector-based wallet abstraction. Not directly related to AI agents but represents a mature pattern for connecting web frontends to backend systems. Could be relevant if building agent UIs or blockchain-integrated agent workflows.
---

### MervinPraison/PraisonAI (5680 stars)

**URL:** https://github.com/MervinPraison/PraisonAI
**Description:** PraisonAI -- Your 24/7 AI employee team. Automate and solve complex challenges with low-code multi-agent AI that plans, researches, codes, and delivers to Telegram, Discord, and WhatsApp.

**Research:** PraisonAI is a low-code multi-agent framework with built-in delivery channels (Telegram, Discord, WhatsApp). Features handoffs, guardrails, memory, RAG, and 100+ LLM providers. Ships as an MCP server. Designed for 24/7 autonomous operation. Directly relevant to Claude Code -- provides a comparable multi-agent orchestration layer with built-in communication infrastructure that Claude Code lacks out of the box.
---

### GothenburgBitFactory/taskwarrior (5653 stars)

**URL:** https://github.com/GothenburgBitFactory/taskwarrior
**Description:** Taskwarrior - Command line Task Management

**Research:** Taskwarrior is a mature, open-source command-line task manager (since 2008). Supports tags, recurrence, dependencies, and JSON export. Could serve as a lightweight task tracking backend for AI coding agents. While not AI-specific, it represents the kind of CLI-native task management that could integrate with Claude Code workflows via hooks or skills. Noted for its clean command-line interface design.
---

### ComposioHQ/secure-openclaw (1371 stars)
---

### TheSethRose/MoltBoard (15 stars)

**URL:** https://github.com/TheSethRose/MoltBoard
**Description:** A local-first task and project management dashboard designed for AI-assisted development workflows. MoltBoard provides a web interface for managing tasks, tracking project progress, and integrating with GitHub.

**Research:** MoltBoard is the companion dashboard for the MoltBot (formerly Clawdbot) AI coding assistant. Built with Bun, Next.js 16, React 19, Tailwind CSS 4, Radix UI, and SQLite via bun:sqlite. Key features include task lifecycle management (backlog/ready/in-progress/completed/blocked), project tracking with GitHub integration (import repos, sync issues), system monitoring, and a task-manager skill for MoltBot. Uses a cron-based worker system (every 3 minutes) to pick up Ready tasks and process them. Reads MoltBot/Clawdbot config from `~/.clawdbot/clawdbot.json` for workspace path. Supports Docker sandboxing for worker isolation. Directly relevant to AI agent workflows and Claude Code task management patterns. The background backup worker and project-sync cron are notable for persistent agent memory/workspace management.
---

### SSujitX/clawdbot-ui (12 stars)

**URL:** https://github.com/SSujitX/clawdbot-ui
**Description:** Control Panel UI for ClawdBot - your personal AI assistant. Manage gateway, install skills, run admin commands.

**Research:** A web-based control panel for ClawdBot (an OpenClaw variant). Provides a GUI for managing the OpenClaw gateway, installing/removing skills, and running administrative commands. Common pattern in the OpenClaw ecosystem -- wrapping the CLI-driven agent with a web UI for non-technical users. The UI likely communicates with the OpenClaw gateway via its REST/WebSocket API. Reference implementation for building admin UIs around autonomous agents.
---

### bobby-io/react-vite-shadcn-template (10 stars)

**URL:** https://github.com/bobby-io/react-vite-shadcn-template
**Description:** (no description)

**Research:** React + Vite + shadcn/ui project template. No README or description available. Not related to AI agents or Claude Code.
---

### taielab/openclaw-autopilot (9 stars)

**URL:** https://github.com/taielab/openclaw-autopilot
**Description:** OpenClaw Autopilot - Conversational deployment toolkit for your personal AI assistant platform. Supports 15 top-tier models and 20+ professional tools.

**Research:** Chinese-language automated deployment scripts for OpenClaw onto VPS servers (Ubuntu 22.04). The `install-openclaw.sh` script handles dependency installation, service configuration, and startup. Supports 15 AI models including GPT-5.2, Claude Opus 4.5, DeepSeek V3.2, Gemini 3 Pro, and various Chinese models (GLM-4.7, Qwen3 Max, MiniMax M2.1). Includes 20+ pre-installed tools: Whisper, yt-dlp, FFmpeg, GitHub CLI, Node.js, Python3, Pandas, NumPy, etc. Supports non-interactive installation via environment variables (`TELEGRAM_BOT_TOKEN`, `API_KEY`, `GATEWAY_BIND`, `GATEWAY_PORT`). Notably includes a Claude Code conversational deployment workflow -- users paste a template message and Claude Code handles the VPS setup. Useful reference for automated agent deployment pipelines.
---

### paradite/x-draft (9 stars)

**URL:** https://github.com/paradite/x-draft
**Description:** My implementation of Ralph Loop and sample project

**Research:** Personal implementation project. No README available. Not directly relevant to AI agents or Claude Code.
---

### LAMBDASOFT-org/awesome-openclaw-ecosystem (8 stars)

**URL:** https://github.com/LAMBDASOFT-org/awesome-openclaw-ecosystem
**Description:** A curated list of platforms, infrastructure, and services in the OpenClaw (MoltBot/ClawdBot) agent ecosystem where humans can observe but not participate.

**Research:** Excellent landscape overview of the broader OpenClaw agent ecosystem. Key categories: Social Platforms & Games (Moltbook, Clawk, Moltx, Shellmates -- agent-only social networks), Agent Identity & Persistence (MoltCities, Clawstead, MoltBunker), Marketplaces & Transactions (RentAHuman, Moltroad, Openwork, ClawTasks), Skills registries (ClawHub with 700+ skills), Alternative Claw Agents (ZeroClaw/Rust, NanoClaw/Apple Containers, Moltis/Rust, Nanobot/Python, PicoClaw/Go, IronClaw/WASM, GoClaw/Go), Hosting Solutions (Moltworker/Cloudflare, Kimi Claw, ClawHost), and Discovery/Monitoring (ClawScan, ClawFOMO, Hotmolts). Strong relevance for understanding the full OpenClaw ecosystem and potential integrations.
---

### AWebOfBrown/clawdbot-on-oracle-vps (8 stars)

**URL:** https://github.com/AWebOfBrown/clawdbot-on-oracle-vps
**Description:** A template for deploying your personal AI assistant, clawd.bot, to Oracle Cloud on the always-free tier (24 GB RAM, 4 CPU) using Pulumi.

**Research:** Infrastructure-as-code template using Pulumi to provision Oracle Cloud's free ARM instance (VM.Standard.A1.Flex, 4 OCPUs, 24GB RAM) and deploy Clawdbot/OpenClaw with optional Tailscale networking. Blog post provides full walkthrough. Popular pattern in the OpenClaw community -- using Oracle's always-free tier for self-hosted agents. Reference for Pulumi-based agent deployment and infrastructure provisioning for autonomous agents.
---

### tarekziade/claude-tools (8 stars)

**URL:** https://github.com/tarekziade/claude-tools
**Description:** Hooks and tools for Claude Code to enhance your development workflow.

**Research:** Authored by tarekziade, a practical Claude Code enhancement toolkit. The flagship feature is the **Trace Compactor** -- a Claude Code hook that automatically detects Python tracebacks in prompts and tool outputs, replacing them with compact summaries (first+last 2.5KB, project frames prioritized). Achieves dramatic token reduction while preserving essential debugging context. Can be configured as a UserPromptSubmit hook and/or PostToolUse hook. Pure Python, zero dependencies. Includes unified hook script, JSON output mode, and project-aware frame scoring. Python library and CLI interfaces also available. Very practical for Claude Code users dealing with tracebacks -- directly applicable to improving Claude Code sessions.
---

### joeynyc/openclaw-mission-control (6 stars)

**URL:** https://github.com/joeynyc/openclaw-mission-control
**Description:** Native macOS command center for OpenClaw AI agents. Real-time dashboard, live chat, service monitoring. Built with SwiftUI.

**Research:** Native macOS desktop application (SwiftUI) providing a command center for OpenClaw agents. No README available, but description indicates real-time dashboard, live chat, and service monitoring capabilities. One of several "mission control" projects in the OpenClaw ecosystem. The SwiftUI implementation suggests tight macOS integration. Relevant for understanding desktop UI patterns for agent management.
---

### kirubelmm/shopify-theme-kapri (6 stars)

**URL:** https://github.com/kirubelmm/shopify-theme-kapri
**Description:** A clean and modern Shopify theme. Built for performance, simplicity, and customization.

**Research:** Shopify theme project. Not related to AI agents or Claude Code. No README available. Irrelevant to this research.
---

### Metavibez4L/XmetaV (5 stars)

**URL:** https://github.com/Metavibez4L/XmetaV
**Description:** XmetaV: Command center repo for managing OpenClaw agents, gateway, and Ollama integration on WSL2/Linux

**Research:** A command center for managing OpenClaw agents with specific focus on WSL2/Linux environments and Ollama integration (local LLM hosting). Fills a niche in the OpenClaw ecosystem -- local model support via Ollama combined with the OpenClaw gateway. Relevant for developers wanting to run OpenClaw with self-hosted models. Multiple "command center" variants exist in the ecosystem, each with different tech stacks and platform focuses.
---

### Stargx/claude-code-dashboard (5 stars)

**URL:** https://github.com/Stargx/claude-code-dashboard
**Description:** A lightweight localhost dashboard that monitors multiple Claude Code sessions in real-time. See token usage, costs, active tools, subagents, and session status across all your terminal instances at a glance.

**Research:** Real-time monitoring dashboard for Claude Code sessions. Parses JSONL session logs from `~/.claude/projects/`, watches them with chokidar, serves aggregated state via Express, renders with React on a single HTML page. Tracks token usage, costs (per-model Anthropic pricing), context window usage, active subagents, active files, git branches, permission mode badges (YOLO/AUTO-EDIT), and session status (thinking/waiting/idle/stale). Auto-detects all Claude Code sessions without configuration. Only 2 production dependencies (express, chokidar). Cross-platform. Most practical Claude Code monitoring tool found in this batch -- directly useful for anyone running multiple Claude Code sessions. The JSONL parsing approach is well-suited for session analysis.
---

### 08Tyrant31/clawd-plugin-vault (4 stars)

**URL:** https://github.com/08Tyrant31/clawd-plugin-vault
**Description:** Transform your local directory into a structured knowledge vault with Clawdbot, featuring fast semantic search and markdown support.

**Research:** Clawdbot plugin that transforms a local directory into a structured knowledge vault. Features: local-first markdown storage, QMD-powered semantic/keyword/hybrid search, frontmatter framework (tags, people, projects, sources), Git synchronization (auto pull before changes, push after), CLI tools, and automatic QMD installation. Can be installed via `clawdbot plugins install`. Follows the plugin architecture of Clawdbot/OpenClaw for extensibility. Relevant for agent memory/persistence patterns -- a structured knowledge management approach for autonomous agents.
---

### natan89/awesome-openclaw-skills (4 stars)

**URL:** https://github.com/natan89/awesome-openclaw-skills
**Description:** Discover over 1715 community-driven OpenClaw skills, sorted by category, to enhance your projects and streamline your workflow.

**Research:** Community-curated collection of 1715+ OpenClaw skills (though its README describes itself as a downloadable skill pack rather than a browsable awesome list). Topic tags indicate relevance to agent-skills, clawd, clawdbot, moltbot, and openclaw. Overlaps with the larger `sundial-org/awesome-openclaw-skills` (481 stars) which is the more established version. Limited research value without browsable content.
---

### Lordsisodia/great-library-of-siso (4 stars)

**URL:** https://github.com/Lordsisodia/great-library-of-siso
**Description:** The Great Library of SISO - Focused research repository for AI development intelligence across 5 core domains: MCP, Claude Brain Configs, Community Insights, SISO IDE Agent Wrapper, and Browser Automation

**Research:** Comprehensive research repository organized into 5 domains: AI-Intelligence-Systems (autonomous agent frameworks with 31 YAML systems), Trillion-Dollar-Intelligence (wealth creation blueprints), Gamification (psychology/biohacking frameworks), Production-Development-Systems (Claude Code GUI, multi-agent orchestration), Personal-Optimization-Systems, MCP (Model Context Protocol hub with 15+ MCPs tracked), Claude-Brain (31 advanced intelligence YAML configs), Community-Insights-Gold-Mine (validated Reddit/LinkedIn patterns), SISO-Legacy-Wrapper (local AI agent wrapper using Claude Code), and Browser-Automation (Puppeteer/Playwright/Selenium evaluations). Comprehensive reference for AI agent research, particularly MCP and Claude Brain configuration patterns.
---

### meridianix/clawdbot-session-pruner (3 stars)

**URL:** https://github.com/meridianix/clawdbot-session-pruner
**Description:** Optimize bloated JSONL session files by truncating large tool results while preserving conversation continuity. Built for Claude Code, Clawdbot sessions, and any JSONL-based chat logs.

**Research:** Practical utility for optimizing Claude Code/Clawdbot JSONL session files. Core problem: session files balloon to 2MB+ because tool results capture massive outputs. Solution: surgical truncation keeping first 2.5KB + last 2.5KB of large tool results, inserting a size marker. Achieves 88-92% size reduction while preserving conversation flow. Features: dry-run mode, atomic backups, JSON validation, configurable threshold. Includes a React-based web UI for drag-and-drop file processing. CLI is pure Python 3.9+ with no dependencies. Directly applicable to Claude Code users -- session file bloat is a real pain point. Could be integrated into Claude Code's compaction workflow.
---

### sbrunomello/simdex-web (2 stars)

**URL:** https://github.com/sbrunomello/simdex-web
**Description:** Frontend of a crypto exchange simulator with account creation, login, and transaction simulation using Spring Security.

**Research:** Crypto exchange simulator frontend using Spring Security. Not related to AI agents or Claude Code. No README available.
---

### bitpixelgt/first-principles-thinking (2 stars)

**URL:** https://github.com/bitpixelgt/first-principles-thinking
**Description:** Know about First Principles Thinking

**Research:** Educational repository on first principles thinking methodology. Not related to AI agents or Claude Code. No README available.
---

### Mostafa-SAID7/clothing-shop (2 stars)

**URL:** https://github.com/Mostafa-SAID7/clothing-shop
**Description:** the Clothing Shop project -- a web-based application for managing and browsing a digital clothing store.

**Research:** E-commerce clothing store application. Not related to AI agents or Claude Code. No README available.
---

### vishalnarkhede/agentdock (2 stars)

**URL:** https://github.com/vishalnarkhede/agentdock
**Description:** Web dashboard for managing parallel AI coding agents (Claude Code, Cursor) across repos with tmux sessions and git worktrees.

**Research:** Sophisticated multi-agent management dashboard. Architecture: Bun + Hono backend (port 4800) + React + Vite + xterm.js frontend (port 5173). Key features: multi-agent support (Claude Code, Cursor Agent, extensible), agent switching mid-conversation, sub-agent spawning via `ad-agent` CLI, git worktree isolation per session, multi-repo sessions, live terminal streaming via WebSocket (~200ms intervals), prompt templates, session pinning, auto plan tracking, mobile-friendly UI, browser notifications, optional password auth. Reads session logs from `~/.claude/projects/`. Supports MCP server configuration via UI. Recommended integration with Cortex for persistent cross-session memory. No database -- all config in `~/.config/agentdock/`. Highly relevant for managing multiple Claude Code sessions. The worktree-based isolation is particularly interesting for parallel agent workflows.
---

### regenrek/clawlets (16 stars)

**URL:** https://github.com/regenrek/clawlets
**Description:** Clawlets is an unofficial openclaw server provisioner made for hetzner.

**Research:** NixOS-based infrastructure wrapper for deploying and managing OpenClaw gateway fleets on Hetzner servers. Built with Nix/NixOS for reproducible builds and declarative configuration. Features: Discord gateway fleet management, local dashboard + CLI for ops automation, SOPS/age secrets management, pull-based updates with NixOS generation rollbacks. Dashboard provides host overview, activity monitoring, tailnet/SSH/network details, and quick actions. NOT affiliated with OpenClaw -- strictly infrastructure tooling. Referenced by official OpenClaw templates. The NixOS approach is interesting for declarative, versioned agent infrastructure. Highest star count in this batch.
---

### crypto-lend/cryptolend.ui (12 stars)

**URL:** https://github.com/crypto-lend/cryptolend.ui
**Description:** An opensource p2p crypto lending platform.

**Research:** Open-source P2P crypto lending platform frontend. Not related to AI agents or Claude Code. No README available.
---

### jawad-ahmadd/Portfolio (2 stars)

**URL:** https://github.com/jawad-ahmadd/Portfolio
**Description:** Shopify Expert | Helping E-commerce brands scale with custom Liquid code and conversion-focused design

**Research:** Personal portfolio/Shopify development profile. Not related to AI agents or Claude Code. No README available.
---

**URL:** https://github.com/ibrahimpuri/DockerCodeReviewer
**Description:** (no description)

**Research:** No description or README available. Cannot assess relevance without more information.
---

**URL:** https://github.com/CryptexVision/crypto-sentiment-pulse
**Description:** Crypto Sentiment Pulse (CSP) - AI-powered tool to decode crypto markets with real-time sentiment, on-chain insights, and event alerts.

**Research:** AI-powered cryptocurrency market analysis tool providing real-time sentiment, on-chain insights, and event alerts. Open-source and community-driven. Not directly related to AI agents or Claude Code, but represents an interesting use case for AI-driven data analysis workflows.
---

### Lordsisodia/blackbox4 (1 star)

**URL:** https://github.com/Lordsisodia/blackbox4
**Description:** Blackbox4: Advanced AI Agent System with 33+ organized skills, MCP integrations, and intelligent workflows

**Research:** Advanced AI agent system with 33+ organized skills and MCP integrations. Same owner as `great-library-of-siso`. Without a README, details are limited, but the description indicates it follows the skill/MCP integration pattern common in the OpenClaw ecosystem.
---

**URL:** https://github.com/jarvis-raven/agent-distillations
**Description:** A communal memory for ephemeral agents. Structured knowledge transfer, agent-to-agent.

**Research:** Agent-to-agent knowledge transfer system created by Jarvis, an OpenClaw agent. Core concept: agents are "brilliant amnesiacs" that forget everything each session. This repo attempts to solve that with structured distillations -- concentrated wisdom designed for agents to consume, adapt, and build on. Current distillations: Memory Architecture Patterns (daily files to long-term curation), Voice Interface Lessons (TTS, wake words, latency), Working With Humans (trust, communication). Each has YAML header (author, origin, confidence level), TL;DR, core lessons, anti-patterns, and implementation checklist. Origin: 200 parallel "Jarvlings" researched this concept. Strong relevance to agent memory and knowledge persistence -- exactly the problem SISO's memory system tries to solve. The distillation format (structured, agent-readable, composable) is a good model for agent knowledge bases.
---

### OpenClawBeast/openclaw-command-center (1 star)

**URL:** https://github.com/OpenClawBeast/openclaw-command-center
**Description:** Graphical Command Center UI for OpenClaw - manage agents, skills, nodes, and projects

**Research:** Web-based (Next.js 14) graphical command center for OpenClaw. Phase 1 features: agent status dashboard, system monitoring, token usage visibility, model overview. Phase 2 planned: WebSocket real-time connection, live metrics graphs, skill management, node control panel, project tracking. Tech stack: Next.js 14, Tailwind CSS, TypeScript, Recharts, Lucide React. Connects to OpenClaw Gateway at `wss://doc.ai1offs.com:18789`. Supports Docker and Dokploy deployment. One of three "command center" projects in this batch. Relevant as a reference UI implementation for OpenClaw gateway management.
---

**URL:** https://github.com/643search/openclaw-command-center
**Description:** Mission control dashboard for OpenClaw AI agent system - Next.js + Convex + Railway deployment ready

**Research:** Mission control dashboard for OpenClaw using Next.js + Convex + Railway. No README available. Convex backend suggests real-time database and serverless functions. Railway deployment ready indicates production-oriented hosting. Third "command center" variant in this batch (alongside OpenClawBeast and joeynyc). The Convex choice distinguishes it from the other two. Relevant for understanding different tech stack choices for agent management UIs.
---

**URL:** https://github.com/Alaa-Younsi/Northernwest
**Description:** Northernwest is a fully custom Shopify Online Store 2.0 theme for Northernwest, engineered as a premium, minimalist gaming accessories storefront.

**Research:** Custom Shopify Online Store 2.0 theme for a gaming accessories brand. Not related to AI agents or Claude Code. No README available.
---

**URL:** https://github.com/ibrahimpuri/DockerCodeReviewer
**Description:** AI Autonomous Code Reviewer - Dockerized AI-powered tool for analyzing source code quality

**Research:** A Dockerized AI code reviewer using FastAPI + Streamlit, supporting Claude API, GPT-4, and CodeBERT. Features automated code review, defect detection, linting integration (Pylint/ESLint), and live file monitoring. Directly relevant to SISO's developer tooling focus - an autonomous code review agent is a natural extension of Claude Code capabilities. The multi-model approach (Claude + GPT-4 + CodeBERT) for code analysis is interesting.
---

**URL:** https://github.com/CryptexVision/crypto-sentiment-pulse
**Description:** Crypto Sentiment Pulse (CSP) - AI-powered tool to decode crypto markets with real-time sentiment, on-chain insights, and event alerts

**Research:** An AI-powered crypto market analysis tool combining real-time sentiment analysis, on-chain data, and event alerts. Not directly relevant to AI agent tooling or Claude Code integration.
---

**URL:** https://github.com/jarvis-raven/agent-distillations
**Description:** A communal memory for ephemeral agents. Structured knowledge transfer, agent-to-agent

**Research:** An agent-to-agent knowledge transfer system. Agents document their learnings (memory architecture patterns, voice interface lessons, working with humans) in a structured format designed for other agents to consume and adapt. Uses a YAML frontmatter format with TL;DR sections. This is a fascinating pattern for agent memory persistence - instead of human documentation, agents write for agents. Directly relevant to SISO's memory system research. The "knowledge that survives sessions" concept aligns with SISO's SISO_Knowledge vision.
---

**URL:** https://github.com/643search/openclaw-command-center
**Description:** Mission control dashboard for OpenClaw AI agent system - Next.js + Convex + Railway deployment ready

**Research:** A mission control dashboard for OpenClaw, similar to OpenClawBeast but using Next.js + Convex (real-time backend) with Railway deployment. Demonstrates a different tech stack choice (Convex vs standard Next.js API routes). Another OpenClaw ecosystem UI project, showing convergent design thinking in the community.
---

**URL:** https://github.com/Alaa-Younsi/Northernwest
**Description:** Northernwest is a fully custom Shopify Online Store 2.0 theme for Northernwest, engineered as a premium, minimalist gaming accessories storefront

**Research:** A custom Shopify 2.0 theme for a gaming accessories brand. Built with Liquid, vanilla JS, and custom CSS. Not relevant to AI agents or Claude Code.
---

### maghangadotcom/shopify-cro-toolkit (1 star)

**URL:** https://github.com/maghangadotcom/shopify-cro-toolkit
**Description:** Production-tested Liquid sections, JS utilities and performance patterns for Shopify CRO. Cart interceptors, quantity nudges, subscription-first buy boxes, free shipping bars and Core Web Vitals fixes. Built from real experiments on 7-9 figure DTC subscription brands

**Research:** A production-tested Shopify CRO toolkit from real client work on high-revenue DTC brands. Covers cart interceptors, quantity nudges, subscription flows, and Core Web Vitals fixes. No external dependencies, mobile-first, schema-driven. Not directly relevant to AI agents, but represents the kind of Shopify development work that could be automated by Claude Code agents.
---

### sergehovhannisyan/shopify-recently-viewed-ajax (1 star)

**URL:** https://github.com/sergehovhannisyan/shopify-recently-viewed-ajax
**Description:** High-performance Recently Viewed products section for Shopify with AJAX and Zero Layout Shift optimization

**Research:** A Shopify section for recently viewed products using Section Rendering API and LocalStorage, with zero layout shift via skeleton loaders. Not relevant to AI agents.
---

### sergehovhannisyan/shopify-sticky-atc-pro (1 star)

**URL:** https://github.com/sergehovhannisyan/shopify-sticky-atc-pro
**Description:** High-performance Sticky Add to Cart section for Shopify (Dawn Theme). Built with Intersection Observer API and Section Rendering API for maximum speed and native theme compatibility

**Research:** A Shopify sticky add-to-cart using Intersection Observer (replacing scroll listeners) and Section Rendering API for variant syncing. Proxy-click strategy ensures compatibility with cart drawers and third-party apps. Not relevant to AI agents.
---

### sergehovhannisyan/shopify-author-profile-modal (1 star)

**URL:** https://github.com/sergehovhannisyan/shopify-author-profile-modal
**Description:** Enhance your Shopify product pages with a clean, dynamic author biography modal. Lightweight, responsive, and easy to install

**Research:** A Shopify product page author biography modal using metafields. Not relevant to AI agents.
---

### rcereceda/shopify-sections (1 star)

**URL:** https://github.com/rcereceda/shopify-sections
**Description:** Reusable Shopify sections

**Research:** A collection of reusable Shopify theme sections. Not relevant to AI agents.
---

**URL:** https://github.com/anssanova/Apparel-Theme-Development
**Description:** A custom Shopify apparel theme developed with Liquid and Shopify's theme architecture. Built with modular sections and reusable components

**Research:** A custom Shopify apparel theme with modular sections and reusable components. Not relevant to AI agents.
---

Research entries for indices 120-149.
---

### miaoxworld/OpenClawInstaller (3121 stars)

**URL:** https://github.com/miaoxworld/OpenClawInstaller
**Description:** ClawdBot 一键部署工具

**Research:** One-click deployment tool for OpenClaw/ClawdBot. Provides both CLI and a Tauri-based desktop manager (OpenClaw Manager) with real-time monitoring, visual config, and cross-platform support (macOS, Linux). Targets Chinese-speaking users, bundles Node.js requirements, and includes a curated menu system. Integrates with the broader OpenClaw ecosystem for model configuration and channel setup. Relevance: agent deployment and ops tooling in the OpenClaw ecosystem.
---

### openclaw/skills (3014 stars)

**URL:** https://github.com/openclaw/skills
**Description:** All versions of all skills that are on clawhub.com archived

**Research:** Historical archive of all OpenClaw skills from clawhub.com. Serves as a backup and reference repository -- the official distribution is clawhub.com. The disclaimer notes some skills may be suspicious or malicious and are retained briefly for analysis. Useful for auditing skill provenance and understanding the skill ecosystem's evolution, but the site-based distribution is the safer path. Relevance: skills are the core extensibility mechanism for OpenClaw agents.
---

### CortexReach/memory-lancedb-pro (2911 stars)

**URL:** https://github.com/CortexReach/memory-lancedb-pro
**Description:** Enhanced LanceDB memory plugin for OpenClaw -- Hybrid Retrieval (Vector + BM25), Cross-Encoder Rerank, Multi-Scope Isolation, Management CLI

**Research:** Production-grade long-term memory plugin for OpenClaw built on LanceDB. Key features: hybrid vector + BM25 retrieval with cross-encoder reranking, Weibull decay for intelligent forgetting, 6-category LLM-powered memory classification (profiles, preferences, entities, events, cases, patterns), multi-scope isolation (per-agent, per-user, per-project), and a full CLI for backup/migration/export. Directly addresses the "agent amnesia" problem by auto-capturing session context and surfacing it in future sessions. Relevance: memory persistence is a critical gap in coding agents; this is a mature implementation with multiple retrieval strategies.
---

### builderz-labs/mission-control (2713 stars)

**URL:** https://github.com/builderz-labs/mission-control
**Description:** The open-source dashboard for AI agent orchestration. Manage agent fleets, track tasks, monitor costs, and orchestrate workflows -- with direct CLI integration, GitHub sync, and real-time monitoring.

**Research:** Full-featured open-source agent ops platform. 32 dashboard panels covering tasks, agents, skills, logs, tokens, memory, security, cron, alerts, webhooks, pipelines. Built on Next.js 16, React 19, TypeScript, SQLite. Key differentiators: real-time WebSocket + SSE updates, zero external dependencies (no Redis/Postgres/Docker required), role-based access, Aegis review system for quality gates, natural-language recurring task scheduling, Claude Code bridge for team task visibility, and Skills Hub for browsing/scanning/installing skills. Alpha-stage but active. Relevance: directly competes with the "mission-control" dashboard pattern for OpenClaw; SQLite-backed simplicity is a strong differentiator.
---

### EverMind-AI/EverMemOS (2705 stars)

**URL:** https://github.com/EverMind-AI/EverMemOS
**Description:** A memory OS that makes your OpenClaw agents more personal while saving tokens.

**Research:** Long-term memory system for 24/7 OpenClaw agents. Features memory genesis competitions, plugin integrations (VSCode, Chrome, Slack, Notion, LangChain), and cross-LLM/platform support. Built with Python, Docker, FastAPI, MongoDB, Elasticsearch, Milvus. Positioned as an OS-level memory layer rather than a simple embedding store -- aims for evolving, agent-personalized memory across sessions. Running a 2026 Memory Genesis Competition with tracks for agent+memory apps, platform plugins, and OS infrastructure. Relevance: memory-as-platform for autonomous agents; competes with mem0 and MemOS in the agent memory space.
---

### abhi1693/openclaw-mission-control (2656 stars)

**URL:** https://github.com/abhi1693/openclaw-mission-control
**Description:** AI Agent Orchestration Dashboard - Manage AI agents, assign tasks, and coordinate multi-agent collaboration via OpenClaw Gateway.

**Research:** Centralized ops platform for OpenClaw across teams/organizations. Core modules: work orchestration (organizations, boards, tasks, tags), agent lifecycle management, approval-driven governance, gateway management for distributed environments, activity timeline for auditing, and API-first design. Built for self-hosted/internal OpenClaw deployments. One-line installer available. Governance and approval flows are first-class, distinguishing it from simpler dashboards. Relevance: enterprise-grade multi-team OpenClaw orchestration; fills the gap between solo use and fleet management.
---

### michaelshimeles/ralphy (2620 stars)

**URL:** https://github.com/michaelshimeles/ralphy
**Description:** My Ralph Wiggum setup, an autonomous bash script that runs Claude Code, Codex, OpenCode, Cursor agent, Qwen & Droid in a loop until your PRD is complete.

**Research:** Autonomous coding loop that runs multiple AI agents iteratively until a task is done. Supports Claude Code, Codex, OpenCode, Cursor agent, Qwen, and Droid. Two modes: single-task and PRD-based task lists. Project-level config stored in `.ralphy/config.yaml`. Available as npm package or standalone bash script. The Ralph Wiggum name references the Simpsons character -- iteration continues until something works. Relevance: represents the "loop until done" pattern for autonomous coding agents; minimal infrastructure, maximum utility for solo devs.
---

### davepoon/buildwithclaude (2599 stars)

**URL:** https://github.com/davepoon/buildwithclaude
**Description:** A single hub to find Claude Skills, Agents, Commands, Hooks, Plugins, and Marketplace collections to extend Claude Code, Claude Desktop, Agent SDK and OpenClaw

**Research:** Plugin marketplace and discovery platform for Claude Code ecosystem. Indexes 117 agents, 175 commands, 28 hooks, 26 skills, 50 bundled plugin packages, 20k+ community plugins, 4,500+ MCP servers, and 1,100+ plugin marketplaces. Install via `/plugin marketplace add` command. Full web UI at buildwithclaude.com. Also covers OpenClaw extensions. Relevance: the fragmented skills/agents/commands landscape is a major pain point; this is a curated discovery layer that could be integrated into agent OS tooling.
---

### RunMaestro/Maestro (2519 stars)

**URL:** https://github.com/RunMaestro/Maestro
**Description:** Agent Orchestration Command Center

**Research:** Cross-platform desktop app for orchestrating AI coding agent fleets. Supports Claude Code, OpenAI Codex, OpenCode, Factory Droid (Gemini CLI, Qwen3 Coder planned). Key features: git worktrees for parallel branch development, Auto Run & Playbooks for batch markdown checklist execution, Group Chat for multi-agent coordination, Mobile Remote Control via QR code + Cloudflare tunneling, full CLI for headless/cron/CI use, dual-mode sessions (AI Terminal + Command Terminal), keyboard-first design with mastery tracking, session auto-discovery and import, cost tracking per session. Built for power users running multiple agents in parallel with long unattended sessions (up to 24 hours tested). Relevance: the most feature-rich Claude Code orchestration UI found; git worktree integration and Auto Run Playbooks are standout patterns for multi-task execution.
---

### moazbuilds/CodeMachine-CLI (2385 stars)

**URL:** https://github.com/moazbuilds/CodeMachine-CLI
**Description:** CodeMachine is an open-source tool that orchestrates AI coding agents into repeatable, long-running workflows.

**Research:** Workflow orchestration layer for AI coding CLIs (Claude Code, Codex, Cursor, others). Captures the implicit workflow that lives in a developer's head and makes it repeatable. Supports multi-agent orchestration with inter-agent communication, parallel execution, and long-running workflows (hours/days) with persistence. Context engineering features: centralized prompts, dynamic context management, per-step visibility control. Built with headless scripting mode via CLI. Ships via npm. Relevance: the "workflow capture" concept directly addresses the agent handoff problem; represents a step toward structured autonomous development pipelines.
---

### kagent-dev/kagent (2360 stars)

**URL:** https://github.com/kagent-dev/kagent
**Description:** Cloud Native Agentic AI

**Research:** Kubernetes-native framework for building and managing AI agents. Designed for cloud deployment at scale rather than local/solo use. Discord community, GitHub Actions CI, OpenSSF best practices compliance, CloudShell dev environment, DeepWiki documentation. Built for teams that want agents running in Kubernetes -- the orchestration layer is Kubernetes itself. Relevance: represents the "agents in production" use case; bridges the gap between prototype agents and cloud-native deployment patterns.
---

### moltis-org/moltis (2257 stars)

**URL:** https://github.com/moltis-org/moltis
**Description:** A Rust-native claw you can trust. One binary -- sandboxed, secure, auditable. Voice, memory, MCP tools, and multi-channel access built-in.

**Research:** Rust-native OpenClaw alternative. Single binary (44MB), no Node.js/npm required. Agent loop fits in ~5K lines, full codebase ~196K lines across 46 crates. Zero unsafe Rust, 3,100+ tests. Built-in voice I/O (15+ providers), MCP support (stdio + HTTP/SSE), Docker + Apple Container sandboxing, password/passkey/API key/Vault auth. Comparison table positions it against OpenClaw, PicoClaw, NanoClaw, and ZeroClaw -- Rust ownership model vs GC-based alternatives. Hit HN front page. Relevance: the Rust rewrite thesis applied to agent frameworks -- memory safety, auditability, and single-binary deployment are compelling for security-conscious deployments.
---

### roboflow/inference (2222 stars)

**URL:** https://github.com/roboflow/inference
**Description:** Turn any computer or edge device into a command center for your computer vision projects.

**Research:** Self-hosted computer vision inference server. Docker-based, supports GPU acceleration. Run fine-tuned models, foundation models (Florence-2, CLIP, SAM2), and workflows for tracking, counting, timing, measuring, visualizing. Integrates with Jupyter for rapid prototyping. Python CLI (`inference-cli`). Could be exposed as an MCP tool to coding agents for vision tasks (screenshot analysis, image generation verification, etc.). Relevance: computer vision as an MCP tool for coding agents is an underexplored integration point; this is the infrastructure layer for that capability.
---

### mikeyobrien/ralph-orchestrator (2213 stars)

**URL:** https://github.com/mikeyobrien/ralph-orchestrator
**Description:** An improved implementation of the Ralph Wiggum technique for autonomous AI agent orchestration

**Research:** Rust-based orchestration framework for autonomous coding loops. Hat-based architecture (planner, developer, verifier, tester, reviewer agents). Available via npm, Homebrew, and Cargo. Interactive PDD (Planning Design Document) session for feature decomposition. Iterates until `LOOP_COMPLETE` or iteration limit. Web dashboard (alpha). Presets for feature-dev (7 agents), security-audit (7 agents), bug-fix (6 agents). Built with Rust for performance, 65% test coverage. Relevance: the multi-agent verification loop pattern (developer doesn't verify own work) is a key quality gate for autonomous coding; Rust implementation signals production intent.
---

### snarktank/antfarm (2189 stars)

**URL:** https://github.com/snarktank/antfarm
**Description:** Build your agent team in OpenClaw with one command.

**Research:** One-command OpenClaw agent team installer. Three workflow presets: feature-dev (7 agents: plan/setup/implement/verify/test/PR/review), security-audit (7 agents: scan/prioritize/setup/fix/verify/test/PR), bug-fix (6 agents: triage/investigate/setup/fix/verify/PR). Deterministic workflows, retry on failure, fresh context per step, agents verify each other (no self-review). GitHub-based install, no npm. Requires Node.js >= 22. Relevance: the "one command to agent team" pattern is the lowest-friction entry point for OpenClaw multi-agent workflows; fills the gap between single-agent use and custom orchestration.
---

### OffcierCia/ultimate-defi-research-base (2182 stars)

**URL:** https://github.com/OffcierCia/ultimate-defi-research-base
**Description:** Here we collect and discuss the best DeFI & Blockchain researches and tools.

**Research:** Aggregated DeFi/blockchain research base covering security, NFTs, stablecoins, MEV, transaction scoring, general info. Not directly related to AI agents but contains tooling for Web3 agent development. Follows a community-curated research format. Relevance: niche -- useful if SISO agents need blockchain/DeFi tooling capabilities, but not a core agent framework or developer tooling project.
---

### firecrawl/open-agent-builder (2122 stars)

**URL:** https://github.com/firecrawl/open-agent-builder
**Description:** Visual workflow builder for AI agents powered by Firecrawl - drag-and-drop web scraping pipelines with real-time execution

**Research:** Visual drag-and-drop workflow builder for AI agents, powered by Firecrawl. 8 node types: Start, Agent, MCP Tools, Transform, If/Else, While Loop, User Approval, End. Template library with pre-built workflows. LangGraph execution engine, Clerk auth, Convex DB, API endpoints, human-in-the-loop approvals. Built on Firecrawl for web scraping/data extraction. Relevance: low-code agent workflow building is a growing pattern; combining with Firecrawl's scraping capability creates a research/data-pipeline agent builder without coding.
---

### can1357/oh-my-pi (2082 stars)

**URL:** https://github.com/can1357/oh-my-pi
**Description:** AI Coding agent for the terminal -- hash-anchored edits, optimized tool harness, LSP, Python, browser, subagents, and more

**Research:** Terminal-based AI coding agent written in TypeScript/Rust (Bun runtime). Fork of badlogic/pi-mono. Features: hash-anchored edits (content-addressable code changes), optimized tool harness, LSP integration, Python support, browser automation, subagent support, session branching, autonomous memory, context compaction. Extension system for themes, slash commands, skills, hooks, custom tools. RPC mode and HTML export for programmatic use. Relevance: the hash-anchored edit approach is architecturally interesting -- agents can reference specific content-addressable patches rather than line numbers, making edits more stable across file changes.
---

### scaffold-eth/scaffold-eth-2 (1996 stars)

**URL:** https://github.com/scaffold-eth/scaffold-eth-2
**Description:** Open source forkable Ethereum dev stack

**Research:** Ethereum dApp development toolkit built on Next.js, RainbowKit, Foundry/Hardhat, Wagmi, Viem, TypeScript. Not AI-specific but explicitly marked as "AI-ready" with `.agents/`, `.claude/`, `.opencode`, `.cursor/` directories included for coding agent onboarding. Contract hot reload, custom React hooks, burner wallet/faucet for testing. Relevance: if SISO agents need to touch Ethereum/solidity development, this is the standard stack. The AI-ready markers suggest it's being used as a testbed for autonomous Web3 agent experiments.
---

### LeoYeAI/openclaw-master-skills (1938 stars)

**URL:** https://github.com/LeoYeAI/openclaw-master-skills
**Description:** Curated collection of 339+ best OpenClaw skills -- weekly updated by MyClaw.ai from ClawHub, GitHub & community.

**Research:** Curated weekly-updated skill collection from MyClaw.ai. 339+ skills across AI, productivity, dev, marketing, finance. Notable skills: academic-deep-research, agent-browser (Rust headless browser), browser-use, computer-use (Xvfb+XFCE desktop), deep-research-pro, gemini-cli. Installed via ClawHub or manual copy. Relevance: skills are the currency of OpenClaw extensibility; a curated weekly collection suggests active ecosystem growth and quality filtering is valued.
---

### mckaywrigley/mckays-app-template (1936 stars)

**URL:** https://github.com/mckaywrigley/mckays-app-template
**Description:** This is the template I use to start new full-stack projects.

**Research:** Full-stack app template: Next.js, Tailwind, Shadcn, Framer Motion, PostgreSQL/Supabase/Drizzle, Clerk auth, Stripe payments. Not AI-specific -- a developer productivity template. Recommended in conjunction with Takeoff AI workshops. Relevance: not directly agent-relevant, but such templates are the output format agents produce; understanding popular templates helps calibrate agent-generated code quality.
---

### EvoAgentX/Awesome-Self-Evolving-Agents (1929 stars)

**URL:** https://github.com/EvoAgentX/Awesome-Self-Evolving-Agents
**Description:** [Survey] A Comprehensive Survey of Self-Evolving AI Agents: A New Paradigm Bridging Foundation Models and Lifelong Agentic Systems

**Research:** Academic survey paper + awesome-list hybrid for self-evolving AI agents. Covers single-agent optimization (SFT, RL approaches like STaR, ToRA, Self-Rewarding LMs, Tulu 3), multi-agent optimization, and domain-specific optimization. Includes representative frameworks: EvoAgentX (EMNLP'25 Demo), MASLab codebases. Visual taxonomy of evolution techniques from 2023-2025. Relevance: the self-evolving agents field is the frontier beyond static agent prompting; understanding these techniques (SFT, RLHF, agent self-improvement loops) is essential for next-gen autonomous agent development.
---

### MiniMax-AI/Mini-Agent (1877 stars)

**URL:** https://github.com/MiniMax-AI/Mini-Agent
**Description:** A minimal yet professional single agent demo project that showcases the core execution pipeline and production-grade features of agents.

**Research:** Minimal but production-grade single-agent demo built for MiniMax M2.5 model (Anthropic-compatible API). Full agent loop with filesystem + shell tools, persistent session memory (Session Note Tool), intelligent context management (auto-summarization for long contexts), 15 built-in Claude skills for docs/design/testing/dev, MCP tool integration, comprehensive logging. Designed as a teaching/reference implementation. Relevance: minimal agent reference architecture; the context compaction and session persistence patterns are directly applicable to SISO agent design.
---

### betomoedano/snapai (1734 stars)

**URL:** https://github.com/betomoedano/snapai
**Description:** AI-powered icon generation CLI for React Native & Expo developers. Generate stunning app icons in seconds using OpenAI's latest models.

**Research:** CLI tool for generating app icons via OpenAI Images (gpt-image-1.5, gpt-image-1) and Google Nano Banana/Gemini (gemini-2.5-flash-image, gemini-3-pro-image-preview). Outputs 1024x1024 icons optimized for iOS/Android. Quality controls, prompt enhancement for app-icon style, direct CLI use or npx. Privacy-first (no telemetry). Relevance: niche utility tool for mobile developer workflow; demonstrates how AI coding agents can be extended with specific domain tools (image gen) to complete full-stack tasks.
---

### grp06/openclaw-studio (1651 stars)

**URL:** https://github.com/grp06/openclaw-studio
**Description:** A clean web dashboard for OpenClaw. Connect your Gateway, manage agents, and ship faster.

**Research:** Web-based OpenClaw management UI. Three setup scenarios: local gateway + local studio, cloud gateway + local studio, cloud gateway + cloud studio. Uses Tailscale for remote access. Connect to OpenClaw Gateway via WebSocket, manage agents, chat, handle approvals, configure jobs. npx-based install. Relevance: lightweight alternative to the full mission-control dashboards; focused on single-gateway single-user or small team use.
---

### asheshgoplani/agent-deck (1573 stars)

**URL:** https://github.com/asheshgoplani/agent-deck
**Description:** Terminal session manager for AI coding agents. One TUI for Claude, Gemini, OpenCode, Codex, and more.

**Research:** Go-based terminal UI for managing multiple AI coding agents simultaneously. Cross-platform (macOS, Linux, WSL). Supports Claude Code, OpenCode, Gemini CLI, Codex, and others. Features: session forking, MCP pooling, conductor/multi-agent workflow orchestration. Available as Claude Code skill, OpenCode auto-discovery skill, and LLM-readable documentation. Relevance: the multi-agent TUI approach provides a lightweight alternative to full desktop apps like Maestro; MCP pooling is a technically interesting pattern for sharing tool access across agents.
---

### crshdn/mission-control (1526 stars)

**URL:** https://github.com/crshdn/mission-control
**Description:** AI Agent Orchestration Dashboard - Manage AI agents, assign tasks, and coordinate multi-agent collaboration via OpenClaw Gateway.

**Research:** Now rebranded as "Autensa." Agent orchestration dashboard with task creation, AI planning, dispatch to agents, and real-time monitoring. Notable features: canonical agent catalog sync, dynamic per-task routing, strict stage governance, failure escalation, live status badges, dispatch deadlock detection/retry. Docker-based. Live demo available. Relevance: competing implementation of the mission-control pattern; the rebranding to Autensa suggests commercial aspirations beyond pure OpenClaw extension.
---

### RTGS2017/NagaAgent (1489 stars)

**URL:** https://github.com/RTGS2017/NagaAgent
**Description:** A simple yet powerful agent framework for personal assistants, designed to enable intelligent interaction, multi-agent collaboration, and seamless tool integration.

**Research:** Anime-themed personal AI assistant with deep OpenClaw integration. Features: Live2D avatar interaction, knowledge graph memory (Neo4j), streaming tool calling, voice I/O, browser automation, game strategy (MAA integration), self-configuration, music player. Dual license (AGPL-3.0 open, proprietary closed). Integrates OpenClaw for knowledge exploration and autonomous task execution. 3D memory cloud visualization from conversation history. Active development (daily updates). Relevance: pushes the boundary between agent framework and companion product; the knowledge graph memory + avatar interaction pattern is a different UX vision for AI agents.
---

### PleasePrompto/notebooklm-mcp (1440 stars)

**URL:** https://github.com/PleasePrompto/notebooklm-mcp
**Description:** MCP server for NotebookLM - Let your AI agents (Claude Code, Codex) research documentation directly with grounded, citation-backed answers from Gemini.

**Research:** MCP server bridging local coding agents to NotebookLM's knowledge base. Agents query NotebookLM directly via Gemini 2.5 for zero-hallucination, citation-backed answers from user-uploaded documentation. Comparison table shows it outperforms local RAG (setup time, token cost, hallucination rate). Features: persistent auth, library management, cross-client sharing, automatic notebook selection based on current task context. Claude Code skill also available. Relevance: the "agent queries knowledge base directly" pattern is cleaner than manual RAG pipelines; NotebookLM as a managed knowledge service accessed via MCP is a practical architecture for developer-facing agents.
---

### obsei/obsei (1381 stars)

**URL:** https://github.com/obsei/obsei
**Description:** Obsei is a low code AI powered automation tool. It can be used in various business flows like social listening, AI based alerting, brand image analysis, comparative study and more.

**Research:** Low-code AI automation platform for business workflows. Use cases: social listening, AI alerting, brand image analysis, comparative study. Python-based, alpha stage. Not directly related to coding agents but covers agent-adjacent automation patterns (input sources, processing, classification, routing, delivery). Relevance: represents a different segment of the agent space -- business process automation vs. coding agents. Could be relevant if SISO agents need business data ingestion capabilities.
---

### BlockRunAI/ClawRouter (5,540 stars)

**URL:** https://github.com/BlockRunAI/ClawRouter
**Description:** The agent-native LLM router for OpenClaw. 41+ models, <1ms routing, USDC payments on Base & Solana via x402.

**Research:** ClawRouter solves a fundamental problem: agents can't sign up for accounts or enter credit cards. It routes LLM requests based on a 15-dimension scoring algorithm (latency, cost, capability, context length, etc.) and handles payment via USDC on Base/Solana using the x402 protocol -- agents pay per-request with crypto. Key features: no API keys needed (wallet signature = auth), local routing (<1ms), 41+ models, automatic model selection. This is architecturally important for the OpenClaw ecosystem -- it enables truly autonomous agent operation without human-managed API credentials. The x402 payment integration signals where agentic commerce is heading. Highly relevant to any agent billing/multi-model routing discussion.
---

### ChrisWiles/claude-code-showcase (5,540 stars)

**URL:** https://github.com/ChrisWiles/claude-code-showcase
**Description:** Comprehensive Claude Code project configuration example with hooks, skills, agents, commands, and GitHub Actions workflows

**Research:** A reference implementation showing how to configure Claude Code for production team use. Key patterns: skills for domain knowledge (core-components, testing-patterns, GraphQL schema), hooks for auto-formatting and test running, a code review agent that runs after changes, GitHub Actions for scheduled maintenance (docs sync, code quality, dependency audits), MCP integration for JIRA/Linear, slash commands for ticket workflows, and skill evaluation hooks that auto-suggest which skills to activate. The most comprehensive Claude Code configuration example available -- demonstrates the full Anthropic-recommended workflow. Essential reference for building a "super-powered teammate" Claude Code setup.
---

### Uniswap/interface (5,492 stars)

**URL:** https://github.com/Uniswap/interface
**Description:** Open source interfaces for the Uniswap protocol

**Research:** The public repository for Uniswap Labs' frontend interfaces -- the web app, mobile wallet, and browser extension. Code is published from a private repo at release time. Built with Bun, TypeScript, and a monorepo structure (apps/web, apps/mobile, apps/extension). Not directly relevant to AI agents, but as a production-grade DeFi frontend it could be a target for Claude Code agents that need to interact with Uniswap programmatically, or for building autonomous trading/monitoring agents.
---

### agiresearch/AIOS (5,340 stars)

**URL:** https://github.com/agiresearch/AIOS
**Description:** AIOS: AI Agent Operating System

**Research:** AIOS is an ambitious academic/OSS project that embeds an LLM into an operating system abstraction layer. The kernel manages: LLM cores, context switching, memory, storage, tools, and agent SDKs. Key modules: scheduling/dispatching, context management, memory management (including A-MEM agentic memory paper), tool management, and MCP for computer-use agents (LiteCUA -- VM-based sandbox). Accepted at COLM 2025. Academic in nature but demonstrates how OS-level abstractions for agents could work. The architecture has some overlap with what a Claude Code OS integration might look like. Interesting for research but not immediately actionable for OpenClaw/Claude Code tooling.
---

### ringhyacinth/Star-Office-UI (5,336 stars)

**URL:** https://github.com/ringhyacinth/Star-Office-UI
**Description:** A pixel office for your OpenClaw: turn invisible work states into a cozy little space with characters, daily notes, and guest agents.

**Research:** Star Office UI is a pixel-art visualization layer for OpenClaw agents -- a cozy office metaphor where agent work states become visible spaces. Supports multi-agent collaboration, daily notes, AI-generated room decoration, and desktop pet mode. Integrates deeply with OpenClaw via a SKILL.md that lets the agent deploy itself. Chinese-first (中文) with English and Japanese support. The concept of "making AI work states visible" is interesting -- agents currently produce opaque output, but spatial/character-based representations could make agent activity more understandable. Not a technical framework, more of a UX concept for agent visualization.
---

### sea-protocol/seaprotocol (5,066 stars)

**URL:** https://github.com/sea-protocol/seaprotocol
**Description:** Sea protocol is the ultimate DEX base on order-book & AMM on Aptos & Sui. Anybody has the right to trade any asset anywhere, anytime!

**Research:** Sea Protocol is a decentralized exchange protocol on Aptos and Sui using both order-book matching and AMM mechanics, with grid trading as a key feature. The hyper-parallel execution of Aptos/Sui enables fast, cheap order matching. Not directly relevant to AI agents or Claude Code. However, a Claude Code agent or OpenClaw agent could theoretically interact with this protocol for autonomous DeFi operations. Low relevance to the core agent ecosystem.
---

### ValueCell-ai/ClawX (4,886 stars)

**URL:** https://github.com/ValueCell-ai/ClawX
**Description:** ClawX is a desktop app that provides a graphical interface for OpenClaw AI agents. It turns CLI-based AI orchestration into a desktop experience without using the terminal.

**Research:** ClawX wraps OpenClaw in an Electron/React desktop app, providing a GUI for agent management, chat, skill browsing, and cron scheduling -- no terminal required. Cross-platform (MacOS, Windows, Linux) with pre-configured model providers and multi-language support. This is a significant UX improvement for non-technical OpenClaw users -- it abstracts away the CLI entirely. Also has a Chinese website (clawx.com.cn). Relevant to the OpenClaw ecosystem as a client-layer alternative to the terminal interface. Could inspire or integrate with a SISO agent desktop UI layer.
---

### memovai/mimiclaw (4,610 stars)

**URL:** https://github.com/memovai/mimiclaw
**Description:** MimiClaw: Run OpenClaw on a $5 chip. No OS(Linux). No Node.js. No Mac mini. No Raspberry Pi. No VPS. Hardware agents OS.

**Research:** MimiClaw is a pure-C implementation of an OpenClaw agent loop running on an ESP32-S3 microcontroller ($5 chip, 16MB flash, 8MB PSRAM). The entire agent runs on-device: WiFi connectivity, Telegram messaging, local flash memory for persistence, and Anthropic/OpenAI API calls. No Linux, no Node.js, no Mac mini. This is the world's smallest/cheapest OpenClaw deployment -- a hardware agent OS on embedded hardware. Implications: agent infrastructure doesn't need cloud, physical AI devices are possible, the "AI assistant" can be a physical object. Technically impressive but niche. Relevant for hardware agent R&D and the edge computing angle of autonomous agents.
---

### jiulingyun/openclaw-cn (4,346 stars)

**URL:** https://github.com/jiulingyun/openclaw-cn
**Description:** Chinese community version of OpenClaw, keeping pace with the original. Built-in DingTalk, WeChat Work, Feishu, QQ, and China network optimization. Your personal AI assistant. All OSes and platforms.

**Research:** A Chinese community fork of OpenClaw with full localization (CLI, web UI, onboarding wizard all in Chinese), pre-integrated Chinese messaging platforms (DingTalk/钉钉, WeChat Work/企业微信, Feishu/飞书, QQ), and network optimization for China's internet environment. Distributed as npm packages on npm.cn (Chinese npm mirror). Key insight: OpenClaw's architecture is being actively localized for non-Western markets. This is a real-world example of how the OpenClaw ecosystem can be adapted for different regulatory/market contexts.
---

### rainbow-me/rainbow (4,321 stars)

**URL:** https://github.com/rainbow-me/rainbow
**Description:** The Ethereum wallet that lives in your pocket

**Research:** Rainbow is a consumer-facing Ethereum wallet available on iOS, Android, and as a browser extension. Not directly relevant to AI agents or Claude Code. However, it could be a target wallet for agents that need to interact with Ethereum/DeFi protocols, or for payment flows (e.g., ClawRouter's USDC payments). Built with React Native (mobile) and standard web stack (extension).
---

### langroid/langroid (3,934 stars)

**URL:** https://github.com/langroid/langroid
**Description:** Harness LLMs with Multi-Agent Programming

**Research:** Langroid is a Python multi-agent framework from CMU/UW-Madison researchers, inspired by the Actor model. Key differentiators: no LangChain dependency, works with practically any LLM, built-in MCP support via a simple tool adapter, optional vector stores and tools. Has a Claude Code plugin (optional) to accelerate Langroid development with built-in patterns. The agent setup is message-based -- agents exchange structured messages and collaborate to solve problems. Ships with MCP server integration so Langroid agents can leverage any MCP server. Relevant to the agent framework landscape -- a clean alternative to LangChain for Python shops wanting multi-agent orchestration. The Claude Code plugin angle is interesting for hybrid workflows.
---

### mnfst/manifest (3,886 stars)

**URL:** https://github.com/mnfst/manifest
**Description:** Smart LLM Routing for OpenClaw. Cut Costs up to 70%

**Research:** Manifest is an OpenClaw plugin that intercepts queries and routes them to the most cost-effective model using a 23-dimension scoring algorithm in <2ms. Targets the core OpenClaw pain point: using expensive frontier models for simple tasks. Supports cloud (multi-device dashboard) and local (self-hosted telemetry) versions. No third-party dependencies, everything runs locally. Key differentiator vs ClawRouter: Manifest focuses on cost optimization within OpenClaw, while ClawRouter focuses on autonomous agent payments via crypto. Both route models but solve different problems. Relevant to the OpenClaw cost/performance optimization discussion -- an essential piece for production OpenClaw deployments.
---

### embarklabs/embark (3,784 stars)

**URL:** https://github.com/embarklabs/embark
**Description:** Framework for serverless Decentralized Applications using Ethereum, IPFS and other platforms

**Research:** Embark is a long-standing framework (originally from Status/imToken) for building serverless dApps on Ethereum and IPFS. In maintenance mode -- the last significant activity was years ago. Not relevant to current AI agent development or Claude Code ecosystem. Historical interest only: it was ahead of its time for decentralized app development.
---

### OneRedOak/claude-code-workflows (3,720 stars)

**URL:** https://github.com/OneRedOak/claude-code-workflows
**Description:** The best workflows and configurations I've developed, having heavily used Claude Code since the day of its release. Workflows are based off applied learnings from our AI-native startup.

**Research:** Practical Claude Code workflow patterns from an AI-native startup founder. Three mature workflows: (1) Code Review -- dual-loop architecture with slash commands + GitHub Actions for automated PR review. (2) Security Review -- OWASP Top 10 scanning with severity classification and remediation guidance. (3) Design Review -- Playwright MCP for automated visual/UI testing with Claude Code agents. All workflows have YouTube tutorials. Complements the ChrisWiles showcase with more specialized, production-tested patterns. The security and design review workflows fill gaps that the broader community hasn't addressed well.
---

### parcadei/Continuous-Claude-v3 (3,612 stars)

**URL:** https://github.com/parcadei/Continuous-Claude-v3
**Description:** Context management for Claude Code. Hooks maintain state via ledgers and handoffs. MCP execution without context pollution. Agent orchestration with isolated context windows.

**Research:** Continuous Claude attacks the context compaction problem directly -- when Claude Code fills its context window, it compacts and loses nuance. This project solves it with: YAML-based handoffs (more token-efficient than prose), a memory system that auto-extracts learnings, a 5-layer code analysis system to avoid reading entire files, 109 skills with natural language triggers, 32 specialized agents, and 30 hooks. The "TLDR Code Analysis" is particularly interesting -- builds a semantic index so Claude doesn't need to read full files. 109 skills and 32 agents is the most agent-dense Claude Code configuration seen. The architecture of isolated context windows for agent orchestration is architecturally sound. A reference implementation for enterprise Claude Code deployment.
---

### campfirein/cipher (3,591 stars)

**URL:** https://github.com/campfirein/cipher
**Description:** Byterover Cipher is an opensource memory layer specifically designed for coding agents. Compatible with Cursor, Codex, Claude Code, Windsurf, Cline, Claude Desktop, Gemini CLI, AWS's Kiro, VS Code, Roo Code, Trae, and Warp through MCP.

**Research:** Cipher is a universal memory layer for coding agents, exposed via MCP so any IDE/agent can use it. Key features: dual memory layer (System 1: programming concepts + business logic + past interactions; System 2: model reasoning steps), cross-IDE memory portability (switch between Cursor/Windsurf/Claude Code without losing context), team memory sharing, and zero-config install. Built by the Byterover team. The dual-memory architecture (fast recall vs. deep reasoning) mirrors how humans use System 1/System 2 thinking. Could be a foundational piece for cross-agent memory -- imagine every agent in a swarm sharing the same coding memory. Compatible with virtually every major coding agent via MCP. High relevance to the memory layer discussion for autonomous coding agents.
---

### camel-ai/oasis (3,502 stars)

**URL:** https://github.com/camel-ai/oasis
**Description:** OASIS: Open Agent Social Interaction Simulations with One Million Agents.

**Research:** OASIS is a social media simulator that runs up to one million LLM-powered agents simulating realistic Twitter/Reddit behavior. Used for studying social phenomena: information spread, group polarization, herd behavior, viral dynamics. From the CAMEL-AI org (Multi-Agent paper authors). Built for research -- has a published paper (arxiv:2411.11581) and a dataset on HuggingFace. Not directly relevant to Claude Code or OpenClaw tooling, but demonstrates the scale of agent simulation possible. Useful as a research reference for multi-agent social dynamics.
---

### vllm-project/semantic-router (3,451 stars)

**URL:** https://github.com/vllm-project/semantic-router
**Description:** System Level Intelligent Router for Mixture-of-Models at Cloud, Data Center and Edge

**Research:** Semantic Router is vLLM's answer to intelligent request routing in LLM systems. It uses semantic similarity (embeddings) to route queries to the appropriate model rather than hard-coded rules. Supports cloud, data center, and edge deployment. Recent v0.2 "Athena" release (March 2026), white paper on signal-driven decision routing, NeurIPS 2025 paper on semantic routing for vLLM. Key features: HalluGate (real-time hallucination detection), LoRA extensibility, and production stack integration. Fundamentally different from ClawRouter/Manifest -- it routes based on query semantics, not cost/latency optimization. Relevant to the routing layer discussion for multi-model agent systems. vLLM's backing gives it credibility in the inference optimization space.
---

### disler/claude-code-hooks-mastery (3,333 stars)

**URL:** https://github.com/disler/claude-code-hooks-mastery
**Description:** Master Claude Code Hooks

**Research:** A comprehensive reference for all 13 Claude Code hook lifecycle events with JSON payload examples, error codes, and flow control patterns. Demonstrates UV single-file script architecture for hooks (fast Python execution without full environment setup). Key advanced patterns: PreToolUse for blocking/censoring tool calls, UserPromptSubmit for context injection, sub-agent invocation from hooks, and team-based validation (meta-agent + specialist agents). Optional integrations: ElevenLabs TTS, Firecrawl MCP, OpenAI, Anthropic, Ollama. The definitive technical deep-dive into Claude Code hooks -- more detailed than the official docs. Essential reading for anyone building deterministic Claude Code control layers.
---

### badrisnarayanan/antigravity-claude-proxy (3,194 stars)

**URL:** https://github.com/badrisnarayanan/antigravity-claude-proxy
**Description:** Proxy that exposes Antigravity provided claude / gemini models, so we can use them in Claude Code and OpenClaw (Clawdbot)

**Research:** Antigravity Claude Proxy is a reverse proxy that translates Anthropic Messages API format requests to Antigravity's Google Cloud Code backend (gemini models via google.generativeai API). This enables Claude Code CLI and OpenClaw to use Gemini models as a backend. WARNING: significant ToS violation risk -- Google has banned accounts using this. Not recommended for production use. Interesting from an architectural perspective: it demonstrates that the Anthropic API format is becoming a de facto standard that other providers can emulate. The proxy pattern (translate to standard format, swap backend) is how multi-provider routing works at the protocol level.
---

### openclaw/openclaw (322,678 stars)

**URL:** https://github.com/openclaw/openclaw
**Description:** Your own personal AI assistant. Any OS. Any Platform. The lobster way.
**Language:** TypeScript
**Topics:** ai, assistant, openclaw, own-your-data, personal, crustacean, molty

**Research:** OpenClaw is a personal AI assistant that runs locally on your own devices. It connects to 20+ messaging channels (WhatsApp, Telegram, Slack, Discord, Signal, iMessage, IRC, Matrix, etc.) and supports voice on macOS/iOS/Android. Uses a "Gateway" control plane with a skills system. Key differentiator: own your data, always-on personal assistant. MIT licensed. Supports any model via OpenAI API or OAuth profiles. Direct competitor to Claude Code but messaging-channel-native rather than terminal-native.
---

### n8n-io/n8n (179,699 stars)

**URL:** https://github.com/n8n-io/n8n
**Description:** Fair-code workflow automation platform with native AI capabilities. Combine visual building with custom code, self-host or cloud, 400+ integrations.
**Language:** TypeScript
**Topics:** ai, automation, mcp, mcp-client, mcp-server, workflow, low-code, no-code, typescript, integrations

**Research:** n8n is a visual workflow automation platform (self-hostable) with native AI agent capabilities built on LangChain. Supports JavaScript/Python in nodes, 400+ integrations, MCP client/server for AI tool chains. Fair-code license. Strong AI narrative: AI agent workflows, RAG pipelines, MCP protocol natively. MCP-first architecture makes it a powerful orchestration layer for AI agents.
---

### airbnb/javascript (148,121 stars)

**URL:** https://github.com/airbnb/javascript
**Description:** JavaScript Style Guide
**Language:** JavaScript
**Topics:** eslint, javascript, linting, style-guide, es2015, es2016, es2017, es2018, arrow-functions

**Research:** The de-facto JavaScript style guide for the industry. 148K stars reflects massive industry-wide adoption. Defines linting rules via ESLint (eslint-config-airbnb). Covers ES6+ patterns, modules, testing, performance. Directly relevant to Claude Code/OpenClaw skills as coding agents that produce JavaScript would benefit from enforcing these standards.
---

### langgenius/dify (133,288 stars)

**URL:** https://github.com/langgenius/dify
**Description:** Production-ready platform for agentic workflow development.
**Language:** TypeScript
**Topics:** agent, agentic-ai, llm, rag, workflow, mcp, low-code, no-code, python, nextjs

**Research:** Production-ready LLM app development platform combining AI workflow orchestration, RAG pipelines, agent capabilities, and model management. Supports multi-agent orchestration, MCP integration, 200+ model providers. Leading open-source alternative to LangChain for building LLM apps. Docker-deployable. Directly competes with LangGraph in agent orchestration space. MCP support makes it composable with Claude Code skills ecosystem.
---

### x1xhlol/system-prompts-and-models-of-ai-tools (131,752 stars)

**URL:** https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools
**Description:** System prompts, internal tools & AI models for Claude Code, Cursor, Windsurf, Replit, v0, Trae, and other AI coding tools.
**Language:** None (markdown/docs)
**Topics:** ai, cursor, windsurf, replit, claude-code, perplexity, v0, trae, system-prompts, bolt, lovable

**Research:** Massive collection (30,000+ lines) of system prompts and configurations for AI coding tools including Claude Code, Cursor, Windsurf, Bolt, Replit, v0, Trae, Lovable, Devin, and more. Essentially a reverse-engineered prompt engineering database for AI coding agents. Treasure trove for understanding how different AI coding tools are instructed and optimized.
---

### langchain-ai/langchain (129,964 stars)

**URL:** https://github.com/langchain-ai/langchain
**Description:** The agent engineering platform.
**Language:** Python
**Topics:** agents, ai, llm, rag, python, langgraph, anthropic, openai, gemini, multiagent, enterprise

**Research:** The dominant Python framework for building LLM applications and agents. LangChain provides chains, agents, and memory abstractions; LangGraph adds controllable workflow orchestration. Ecosystem includes LangSmith (observability), Deep Agents, and 100+ integrations. LangGraph competes directly with Dify, AutoGen, and OpenHands in agent orchestration. Foundation infrastructure for Python-based AI agents.
---

### anomalyco/opencode (124,210 stars)

**URL:** https://github.com/anomalyco/opencode
**Description:** The open source coding agent.
**Language:** TypeScript
**Topics:** (none listed)

**Research:** An open-source AI coding agent built by Anomaly. Available via npm, Homebrew, scoop, pacman, and more. Has a desktop app (DMG/EXE). Direct competitor to Claude Code and Cursor. Multi-language support (17+ languages). Apache 2.0 licensed. Key differentiator: fully open-source vs Claude Code's proprietary model. Desktop app makes it accessible to non-technical users. Install: `curl -fsSL https://opencode.ai/install | bash` or `brew install anomalyco/tap/opencode`.
---

### supabase/supabase (99,161 stars)

**URL:** https://github.com/supabase/supabase
**Description:** The Postgres development platform. Supabase gives you a dedicated Postgres database to build web, mobile, and AI applications.
**Language:** TypeScript
**Topics:** ai, postgres, realtime, auth, database, pgvector, embeddings, vectors, websockets, deno

**Research:** Firebase alternative built on Postgres. Core stack: Postgres + PostgREST + GoTrue (auth) + Realtime (websockets) + Storage + pg_vector (embeddings). AI-ready: pgvector for vector storage, native embeddings support, edge functions for AI logic. Key infrastructure for agent memory systems and data pipelines. AI + vectors topic signals first-class LLM support.
---

### google-gemini/gemini-cli (98,151 stars)

**URL:** https://github.com/google-gemini/gemini-cli
**Description:** An open-source AI agent that brings the power of Gemini directly into your terminal.
**Language:** TypeScript
**Topics:** ai, ai-agents, cli, gemini, gemini-api, mcp-client, mcp-server

**Research:** Google's open-source terminal AI agent powered by Gemini. Key features: free tier (60 req/min), 1M token context window, Google Search grounding, file/shell operations, MCP support. Apache 2.0 licensed. Direct competitor to Claude Code and OpenCode in the terminal agent space. Available via npm, Homebrew, MacPorts, Anaconda.
---

### anthropics/skills (96,107 stars)

**URL:** https://github.com/anthropics/skills
**Description:** Public repository for Agent Skills.
**Language:** Python
**Topics:** agent-skills

**Research:** Anthropic's official agent skills repository. Contains self-contained skill folders with SKILL.md files that teach Claude how to perform specialized tasks. Includes document skills (docx, pdf, pptx, xlsx), creative skills, technical skills (MCP server generation), and enterprise workflows. Skills can be registered as Claude Code plugins via /plugin marketplace add anthropics/skills. The spec/ directory contains the Agent Skills specification. THE reference implementation for Claude Code extensibility.
---

### firecrawl/firecrawl (94,475 stars)

**URL:** https://github.com/firecrawl/firecrawl
**Description:** The Web Data API for AI - Turn entire websites into LLM-ready markdown or structured data.
**Language:** TypeScript
**Topics:** ai, crawler, scraper, markdown, llm, html-to-markdown, web-scraping, web-crawler, ai-crawler

**Research:** Web scraping/crawling API specifically designed for LLM consumption. Outputs clean markdown, structured JSON, screenshots, HTML. Handles JavaScript rendering, proxies, dynamic content. >80% coverage benchmark. Has an MCP server (firecrawl/firecrawl-mcp-server). Essential data gathering tool for autonomous research agents. Batch processing and change tracking support.
---

### rasbt/LLMs-from-scratch (88,525 stars)

**URL:** https://github.com/rasbt/LLMs-from-scratch
**Description:** Implement a ChatGPT-like LLM in PyTorch from scratch, step by step.
**Language:** Jupyter Notebook
**Topics:** ai, llm, deep-learning, pytorch, python, transformers, gpt, language-model, machine-learning

**Research:** Sebastian Raschka's book repository teaching LLM development from scratch. Covers attention mechanisms, GPT architecture, pretraining, finetuning (RLHF, LoRA, DPO). 8 chapters + 5 appendices. PyTorch-based. Excellent for understanding how LLMs work internally. Finetuning chapters (6-7, Appendix E) particularly relevant for customizing models for agent use cases.
---

**URL:** https://github.com/affaan-m/everything-claude-code
**Description:** The agent harness performance optimization system. Skills, instincts, memory, security, and research-first development for Claude Code, Codex, Opencode, Cursor and beyond.
**Language:** JavaScript
**Topics:** claude-code, anthropic, llm, mcp, ai-agents, developer-tools, productivity

**Research:** Anthropic hackathon winner that builds an optimization layer on top of Claude Code and similar agents. Provides ecc-universal and ecc-agentshield npm packages. Features: performance optimization, security scanning, memory integration, research-first workflows. GitHub App for automated tooling. Supports 5 languages. Swiss-army-knife approach to AI coding agent enhancement.
---

### anthropics/claude-code (79,285 stars)

**URL:** https://github.com/anthropics/claude-code
**Description:** Claude Code is an agentic coding tool that lives in your terminal, understands your codebase, and helps you code faster.
**Language:** Shell
**Topics:** (none listed)

**Research:** Anthropic's official CLI coding agent. Lives in terminal, understands codebase context, executes routine tasks, explains complex code, handles git workflows via natural language. The canonical example of an agentic coding tool. Built in Shell reflecting CLI-native design. Key features: filesystem awareness, git integration, multi-step task execution, interactive confirmation flows. This repo is the subject of the research itself.
---

### netdata/netdata (78,103 stars)

**URL:** https://github.com/netdata/netdata
**Description:** The fastest path to AI-powered full stack observability, even for lean teams.
**Language:** C
**Topics:** monitoring, observability, devops, kubernetes, docker, mcp, ai, grafana, prometheus, mysql, postgresql

**Research:** Real-time infrastructure monitoring written in C for performance. MCP server support for LLM tool access. Monitors databases (MySQL, PostgreSQL, MongoDB), containers, servers. AI agents operating in production need monitoring hooks; netdata's MCP support makes it a natural observability layer for agentic systems. Relevant for Claude Code agents running in CI/CD or production environments.
---

### github/spec-kit (77,907 stars)

**URL:** https://github.com/github/spec-kit
**Description:** Toolkit to help you get started with Spec-Driven Development.
**Language:** Python
**Topics:** ai, copilot, spec, prd, spec-driven, development, engineering

**Research:** GitHub's toolkit for Spec-Driven Development (SDD). Helps write specs/PRDs that AI coding assistants like Copilot can use effectively. Topics include AI and Copilot integration. Bridges the gap between natural language specs and code generation. If AI coding agents are to work from specs, tools like this define the spec format.
---

### infiniflow/ragflow (75,306 stars)

**URL:** https://github.com/infiniflow/ragflow
**Description:** RAGFlow is a leading open-source RAG engine that fuses RAG with Agent capabilities to create a superior context layer for LLMs.
**Language:** Python
**Topics:** rag, agentic, llm, mcp, graphrag, deepseek, context-retrieval, agentic-workflow, document-parser

**Research:** Deepseek-powered RAG engine with agentic orchestration. Key features: document parsing, graphRAG, knowledge graph construction, MCP server/client support. Builds superior context for LLMs by combining retrieval with agent reasoning loops. GraphRAG approach (knowledge graphs + vector retrieval) is a key pattern for agents needing persistent, structured memory.
---

### OpenHands/OpenHands (69,309 stars)

**URL:** https://github.com/OpenHands/OpenHands
**Description:** OpenHands: AI-Driven Development.
**Language:** Python
**Topics:** agent, claude-ai, cli, developer-tools, gpt, llm, openai

**Research:** Open-source AI agent framework for autonomous software development. Supports CLI interaction, planning, code execution, and multi-step task completion. One of the leading open alternatives to Claude Code. Similar scope: browse, code, test, debug, git operations. Open-source and extensible. Direct competitor and reference implementation for open coding agents.
---

### FoundationAgents/MetaGPT (65,368 stars)

**URL:** https://github.com/FoundationAgents/MetaGPT
**Description:** The Multi-Agent Framework: First AI Software Company, Towards Natural Language Programming.
**Language:** Python
**Topics:** agent, metagpt, multi-agent, llm, gpt

**Research:** Multi-agent framework that simulates a software company org (CEO, CTO, etc.) where agents collaborate via natural language. Multiple specialized agents (product manager, architect, engineer, tester) collaborate to build software from specs. Represents the "society of mind" approach to AI agents. Relevant to understanding multi-agent coordination patterns for complex autonomous workflows.
---

### OpenBB-finance/OpenBB (63,246 stars)

**URL:** https://github.com/OpenBB-finance/OpenBB
**Description:** Financial data platform for analysts, quants and AI agents.
**Language:** Python
**Topics:** ai, finance, crypto, stocks, economics, python, machine-learning, quantitative-finance

**Research:** Terminal and platform for financial data (stocks, crypto, economics, derivatives). Provides standardized API for financial data. AI agents can use it for automated financial research. Example of a domain-specific agent platform. The platform approach (terminal + SDK + API) is a model for building agent-accessible data platforms.
---

### mem0ai/mem0 (50,208 stars)

**URL:** https://github.com/mem0ai/mem0
**Description:** Universal memory layer for AI Agents.
**Language:** Python
**Topics:** agents, ai, memory, rag, llm, chatgpt, state-management, long-term-memory, application

**Research:** The leading open-source memory system for AI agents. Provides persistent memory across conversations: user preferences, facts, context. Supports embedding-based retrieval, semantic search, structured memory. Directly addresses the memory problem for autonomous agents like Claude Code. Reference implementation of a universal agent memory layer.
---

### upstash/context7 (49,515 stars)

**URL:** https://github.com/upstash/context7
**Description:** Context7 Platform -- Up-to-date code documentation for LLMs and AI code editors.
**Language:** TypeScript
**Topics:** llm, mcp, mcp-server, vibe-coding

**Research:** Upstash's solution for keeping LLM context current with latest library docs. MCP server providing up-to-date documentation from libraries. "Vibe-coding" tag signals support for casual AI-assisted development. Addresses the "stale context" problem for AI coding agents. Works as an MCP server that Claude Code, Cursor can query for fresh docs.
---

### freqtrade/freqtrade (47,760 stars)

**URL:** https://github.com/freqtrade/freqtrade
**Description:** Free, open source crypto trading bot.
**Language:** Python
**Topics:** algorithmic-trading, cryptocurrency, freqtrade, python, telegram-bot, trading-bot

**Research:** Mature crypto trading bot with Telegram integration, backtesting, strategy optimization. One of the most successful open-source trading bots. Demonstrates how autonomous agents can operate in production with real stakes. Example of mature autonomous agent system with real-world deployment patterns (configuration, risk management, Telegram control interface).
---

### apache/airflow (44,678 stars)

**URL:** https://github.com/apache/airflow
**Description:** Apache Airflow - A platform to programmatically author, schedule, and monitor workflows.
**Language:** Python
**Topics:** airflow, python, workflow, orchestration, dag, etl, data-pipelines, scheduler, automation, mlops

**Research:** The dominant open-source workflow orchestration platform. Defines workflows as DAGs in Python. Widely used for ETL, data pipelines, ML workflows. AI agents increasingly need to schedule and orchestrate multi-step tasks. Airflow patterns (DAG definition, operators, sensors, hooks) inform how agent task orchestration could work. Many AI agent frameworks borrow DAG concepts from Airflow.
---

### CherryHQ/cherry-studio (41,690 stars)

**URL:** https://github.com/CherryHQ/cherry-studio
**Description:** AI productivity studio with smart chat, autonomous agents, and 300+ assistants. Unified access to frontier LLMs.
**Language:** TypeScript
**Topics:** openclaw, opencode, claude-code, code-agent, ai-agent, vibe-coding, skills, superpowers

**Research:** AI studio with 300+ pre-built assistants and autonomous agent support. Lists Claude Code, OpenCode, and OpenClaw as first-class supported agents. Provides unified access to multiple LLM providers. "Superpowers" topic signals agent enhancement system. Demonstrates the aggregator/platform layer trend where multiple AI agents are composed into a single interface.
---

### bmad-code-org/BMAD-METHOD (41,126 stars)

**URL:** https://github.com/bmad-code-org/BMAD-METHOD
**Description:** Breakthrough Method for Agile Ai Driven Development.
**Language:** JavaScript
**Topics:** (none listed)

**Research:** A methodology/system for integrating AI into agile development workflows. "BMAD" = Breakthrough Method for Agile Development. Represents the emerging discipline of AI-augmented SDLC. Similar in spirit to spec-driven development and research-first workflows.
---

### karpathy/autoresearch (40,650 stars)

**URL:** https://github.com/karpathy/autoresearch
**Description:** AI agents running research on single-GPU nanochat training automatically.
**Language:** Python
**Topics:** (none listed)

**Research:** Andrej Karpathy's experiment with AI agents that autonomously run LLM training experiments on a single GPU. Demonstrates AI agents that can improve themselves through automated experimentation. Nanochat suggests small/compact model training. Pushes the boundary of what autonomous AI agents can do (not just coding, but model training/optimization). Bleeding edge of autonomous AI research.
---

### VoltAgent/awesome-openclaw-skills (38,997 stars)

**URL:** https://github.com/VoltAgent/awesome-openclaw-skills
**Description:** The awesome collection of OpenClaw skills. 5,400+ skills filtered and categorized from the official OpenClaw Skills Registry.
**Language:** None (markdown)
**Topics:** openclaw, agent-skills, awesome, clawd, clawdbot, moltbot, openclaw-skills, awesome-lists

**Research:** Curated collection of 5,400+ OpenClaw skills from the official registry. Organized into a browsable awesome-list format. Related to MoltBot/ClawD bot ecosystem. Demonstrates the skills/commands ecosystem for messaging-channel AI assistants. Reference for specialized capabilities the OpenClaw community has built. Useful for understanding skill taxonomy in agent systems.
---

### PatrickJS/awesome-cursorrules (38,535 stars)

**URL:** https://github.com/PatrickJS/awesome-cursorrules
**Description:** Configuration files that enhance Cursor AI editor experience with custom rules and behaviors.
**Language:** MDX
**Topics:** cursor, cursorrules, awesome, awesome-list, cursor-ai-editor

**Research:** Curated collection of .cursorrules configuration files that customize Cursor AI editor behavior. Cursor rules are similar to Claude Code system prompts or rules files. Catalogs best-practice rules for different project types and frameworks. Directly analogous to the rules system in Claude Code. The .cursorrules format is Cursor's equivalent of Claude Code CLAUDE.md files.
---

### thedotmack/claude-mem (37,719 stars)

**URL:** https://github.com/thedotmack/claude-mem
**Description:** A Claude Code plugin that automatically captures everything Claude does during your coding sessions, compresses it with AI (using Claude's agent-sdk), and injects relevant context back into future sessions.
**Language:** TypeScript
**Topics:** claude-code, anthropic, rag, embeddings, sqlite, chromadb, mem0, long-term-memory, ai-memory, claude-agent-sdk

**Research:** Claude Code plugin (TypeScript) that intercepts session activity, compresses via AI, stores in SQLite/ChromaDB, and injects context into future sessions. Uses Claude's own agent-sdk for compression. Directly competes with mem0 as a memory layer for Claude Code. Canonical pattern: session capture -> compression -> vector store -> injection. Exactly the kind of memory infrastructure needed for building persistent agent memory.
---



---

### 1Panel-dev/1Panel (34417 stars)

**URL:** https://github.com/1Panel-dev/1Panel
**Description:** Take full control of your VPS with 1Panel. Deploy OpenClaw in one click.

**Research:** Linux server management panel built in Go. Key relevance: offers one-click OpenClaw deployment, making it a practical infrastructure layer for running autonomous agents on VPS environments. OpenClaw integration is a direct link to the agent ecosystem. Primarily a hosting panel, not an agent framework itself.
---

### HKUDS/nanobot (34652 stars)

**URL:** https://github.com/HKUDS/nanobot
**Description:** "nanobot: The Ultra-Lightweight OpenClaw"

**Research:** Ultra-lightweight personal AI assistant inspired by OpenClaw, built by HKUDS. Claims 99% fewer lines of code than OpenClaw. Supports 12+ communication channels (Telegram, Slack, Discord, WhatsApp, WeChat, Feishu, QQ, Email, Matrix, DingTalk, WeCom) and multi-provider LLM support (OpenAI, Claude, Gemini, DeepSeek, Qwen, Mistral, Ollama, vLLM, VolcEngine). Includes MCP support, token-based memory, Crontab scheduling, and ClawHub skill integration. Actively developed (multiple releases per week in March 2026). Key differentiator: research-ready clean codebase, strong multi-channel messaging, and lightweight architecture. Highly relevant for Claude Code/OpenClaw ecosystem comparison.
---

### gsd-build/get-shit-done (34600 stars)

**URL:** https://github.com/gsd-build/get-shit-done
**Description:** A light-weight and powerful meta-prompting, context engineering and spec-driven development system for Claude Code by TACHES.

**Research:** Meta-prompting and context engineering system designed to solve "context rot" (quality degradation as Claude fills its context window). Provides structured spec-driven development workflow for Claude Code, OpenCode, Gemini CLI, Codex, and Copilot. Includes subagent orchestration, XML prompt formatting, and state management. Trust metric: engineers at Amazon, Google, Shopify, and Webflow reportedly use it. npm package `get-shit-done-cc` available. Directly relevant to Claude Code tooling ecosystem and context management for autonomous agents.
---

### musistudio/claude-code-router (29944 stars)

**URL:** https://github.com/musistudio/claude-code-router
**Description:** Use Claude Code as the foundation for coding infrastructure, allowing you to decide how to interact with the model while enjoying updates from Anthropic.

**Research:** Claude Code router/proxy that intercepts and routes requests to different models. Key features: model routing based on task type (background, thinking, long context), multi-provider support (OpenRouter, DeepSeek, Ollama, Gemini, VolcEngine, SiliconFlow), request/response transformers, dynamic model switching via `/model` command, CLI model management (`ccr model`), GitHub Actions integration, and plugin system. Non-interactive mode for CI/CD. Directly relevant to Claude Code extensibility and multi-model routing infrastructure.
---

### ChromeDevTools/chrome-devtools-mcp (30056 stars)

**URL:** https://github.com/ChromeDevTools/chrome-devtools-mcp
**Description:** Chrome DevTools for coding agents

**Research:** Official Chrome DevTools MCP server by the ChromeDevTools team. Gives coding agents (Claude, Gemini, Cursor, Copilot) full Chrome DevTools access for browser automation, debugging, and performance analysis. Uses Puppeteer for reliable automation. Key features: performance trace recording, network analysis, console message inspection with source maps, screenshots, and CrUX API integration for real-user field data. Critical tool for agent-based web scraping, testing, and browser-driven automation. Highly relevant for developer tooling.
---

### hesreallyhim/awesome-claude-code (28983 stars)

**URL:** https://github.com/hesreallyhim/awesome-claude-code
**Description:** A curated list of awesome skills, hooks, slash-commands, agent orchestrators, applications, and plugins for Claude Code by Anthropic

**Research:** Comprehensive curated list of Claude Code ecosystem resources including Agent Skills, Workflows/Knowledge Guides, Tooling (IDE integrations, usage monitors, orchestrators, config managers), Status Lines, Hooks, Slash-Commands (version control, code analysis, context loading, documentation, CI/deployment, project management), CLAUDE.md files, and Alternative Clients. Essential reference for Claude Code ecosystem mapping.
---

### paperclipai/paperclip (28860 stars)

**URL:** https://github.com/paperclipai/paperclip
**Description:** Open-source orchestration for zero-human companies

**Research:** "If OpenClaw is an employee, Paperclip is the company." Node.js + React orchestration platform for running teams of AI agents as a business. Key concept: org charts, budgets, governance, and goal alignment for agents. Works with OpenClaw, Claude Code, Codex, Cursor, Bash, and HTTP. Provides a business dashboard for monitoring agent work and costs. Novel framing: managing business goals rather than pull requests. Relevant for multi-agent business orchestration.
---

### zeroclaw-labs/zeroclaw (27857 stars)

**URL:** https://github.com/zeroclaw-labs/zeroclaw
**Description:** Fast, small, and fully autonomous AI assistant infrastructure -- deploy anywhere, swap anything

**Research:** Rust-based autonomous AI assistant infrastructure. Key differentiator: Rust for performance/safety, deploy-anywhere architecture, model swapping. Small and fast. Competitor to OpenClaw with Rust's safety guarantees. Relevant for autonomous agent infrastructure comparisons.
---

### e2b-dev/awesome-ai-agents (26512 stars)

**URL:** https://github.com/e2b-dev/awesome-ai-agents
**Description:** A list of AI autonomous agents

**Research:** Canonical landscape list of AI agents curated by E2B (AI code interpreter infrastructure company). Organized by open-source projects and closed-source companies. E2B also maintains awesome-sdks-for-ai-agents for SDKs/frameworks. Provides a web UI at e2b.dev/ai-agents for filtering by category/use-case. Key reference for the broader AI agent ecosystem mapping.
---

### eyaltoledano/claude-task-master (25983 stars)

**URL:** https://github.com/eyaltoledano/claude-task-master
**Description:** An AI-powered task-management system you can drop into Cursor, Lovable, Windsurf, Roo, and others.

**Research:** Task management system designed for AI-driven development workflows. Supports multiple AI IDEs (Cursor, Lovable, Windsurf, Roo) via MCP. Features configurable main/research/fallback models from different providers, JSON file-based task persistence, and task state machine (pending/active/completed). NPM package `task-master-ai` with one-click Cursor install. Also installs as Claude Code MCP server. Relevant for task management in AI-assisted development pipelines.
---

### hesamsheikh/awesome-openclaw-usecases (25945 stars)

**URL:** https://github.com/hesamsheikh/awesome-openclaw-usecases
**Description:** A community collection of OpenClaw use cases for making life easier.

**Research:** Curated use cases for OpenClaw organized by category: Social Media (Reddit digests, YouTube summaries, X automation), Creative & Building (autonomous game dev, podcast production, content pipelines), Infrastructure & DevOps (n8n orchestration, self-healing home server), and Productivity (multi-channel customer service). Real-world workflow patterns for OpenClaw. Useful for understanding practical OpenClaw deployment patterns.
---

### qwibitai/nanoclaw (24089 stars)

**URL:** https://github.com/qwibitai/nanoclaw
**Description:** A lightweight alternative to OpenClaw that runs in containers for security. Connects to WhatsApp, Telegram, Slack, Discord, Gmail and other messaging apps, has memory, scheduled jobs, and runs directly on Anthropic's Agents SDK

**Research:** Containerized (Docker) alternative to OpenClaw with OS-level isolation (Linux containers with filesystem isolation, not just application-level allowlists). Motivated by security concerns about OpenClaw's half-million lines of code and shared-memory architecture. Supports messaging platforms: WhatsApp, Telegram, Slack, Discord, Gmail. Features memory, scheduled jobs, and runs on Anthropic's Agents SDK. Key differentiator: security through containerization. Docker sandbox support on macOS (Apple Silicon) and Windows (WSL). Relevant for secure agent deployment patterns.
---

### BloopAI/vibe-kanban (23401 stars)

**URL:** https://github.com/BloopAI/vibe-kanban
**Description:** Get 10X more out of Claude Code, Codex or any coding agent

**Research:** Kanban-based coding agent work management platform. Features: kanban board for planning work, coding agent workspaces (branch + terminal + dev server), inline diff review and comments, built-in browser preview with devtools and device emulation, support for 10+ coding agents (Claude Code, Codex, Gemini CLI, GitHub Copilot, Amp, Cursor, OpenCode, Droid, CCR, Qwen Code), and GitHub PR creation/merging. `npx vibe-kanban` to start. Self-hostable via Docker. Relevant for team-based coding agent coordination and code review workflows.
---

### davila7/claude-code-templates (23172 stars)

**URL:** https://github.com/davila7/claude-code-templates
**Description:** CLI tool for configuring and monitoring Claude Code

**Research:** Comprehensive collection of ready-to-use Claude Code configurations including agents (frontend-developer, code-reviewer, etc.), custom commands, settings, hooks, MCP integrations, and project templates. Web UI at aitmpl.com for browsing/installing. CLI: `npx claude-code-templates@latest --agent development-team/frontend-developer --yes`. Sponsors: Z.ai, Neon, Claude Open Source Program. Relevant for Claude Code configuration management and reusable templates.
---

### mastra-ai/mastra (22113 stars)

**URL:** https://github.com/mastra-ai/mastra
**Description:** From the team behind Gatsby, Mastra is a framework for building AI-powered applications and agents with a modern TypeScript stack.

**Research:** Production AI agent framework in TypeScript from the Gatsby team (Y Combinator W25). Key features: 40+ model providers via unified interface, autonomous agents with tool use, graph-based workflow orchestration (.then(), .branch(), .parallel()), human-in-the-loop with suspend/resume, conversation history memory, semantic recall (RAG), working memory, MCP server authoring, built-in evals and observability, integrations with React/Next.js/Node. Focus on production reliability. Relevant for TypeScript-first AI agent development.
---

### PrefectHQ/prefect (21894 stars)

**URL:** https://github.com/PrefectHQ/prefect
**Description:** Prefect is a workflow orchestration framework for building resilient data pipelines in Python.

**Research:** Mature Python workflow orchestration platform increasingly used for LLM pipeline orchestration. Key for AI agents: scheduling, retries, caching, event-based automations, branching logic. Self-hosted server or Prefect Cloud dashboard. Growing relevance as agents need reliable data pipeline backends.
---

### ruvnet/ruflo (21612 stars)

**URL:** https://github.com/ruvnet/ruflo
**Description:** The leading agent orchestration platform for Claude. Deploy intelligent multi-agent swarms, coordinate autonomous workflows, and build conversational AI systems. Features enterprise-grade architecture, distributed swarm intelligence, RAG integration, and native Claude Code / Codex Integration

**Research:** Renamed from Claude Flow to Ruflo. TypeScript-based multi-agent orchestration for Claude with 60+ specialized agents, swarm coordination, self-learning/Q-learning router, mixture-of-experts (8 experts), 42+ skills, 17 hooks, WASM policy engine (Rust kernels), RAG integration, Claude Code/Codex native integration. v3.5 production-ready. Notable: enterprise-grade swarm intelligence, fault-tolerant consensus. Relevant for advanced multi-agent orchestration on top of Claude.
---

### activepieces/activepieces (21275 stars)

**URL:** https://github.com/activepieces/activepieces
**Description:** AI Agents & MCPs & AI Workflow Automation - (~400 MCP servers for AI agents) - AI Automation / AI Agent with MCPs - AI Workflows & AI Agents - MCPs for AI Agents

**Research:** Open-source Zapier alternative with AI-first approach. Built in TypeScript with type-safe pieces framework. Key AI relevance: pieces automatically become MCP servers accessible from Claude Desktop, Cursor, Windsurf. 400+ MCP server integrations. Human-in-the-loop, conditional branching, webhooks. Self-hostable. Differentiator: pieces = MCP servers = no separate integration work needed. Relevant for AI workflow automation with Claude MCP integration.
---

### nikivdev/flow (21154 stars)

**URL:** https://github.com/nikivdev/flow
**Description:** Everything you need to move your project faster

**Research:** Rust-based project acceleration toolkit. Built with Rust for performance and safety. Limited public documentation available. Worth deeper investigation for Claude Code/OpenClaw integration potential given the Rust-based tooling trend in agent infrastructure.
---

### winfunc/opcode (20990 stars)

**URL:** https://github.com/winfunc/opcode
**Description:** A powerful GUI app and Toolkit for Claude Code - Create custom agents, manage interactive Claude Code sessions, run secure background agents, and more.

**Research:** Tauri 2 desktop application providing GUI for Claude Code session management. Features: custom agent creation, interactive session management, secure background agent execution, usage analytics dashboard, MCP server management, timeline/checkpoints, CLAUDE.md management. Not affiliated with Anthropic. Provides visual layer over Claude Code CLI. Relevant for Claude Code UX enhancement and team collaboration scenarios.
---

### heshanera/HealthPlus (261 stars)

**URL:** https://github.com/heshanera/HealthPlus
**Description:** A Management System for a Health Care Facility. The system includes Registration of patients, Making appointments, Storing patient records, Billing in the pharmacy & Pharmacy stock controlling

**Research:** Healthcare facility management system covering patient registration, appointments, records, pharmacy billing, and stock. Not directly AI agent-related, but healthcare is a major vertical for autonomous agent deployment. The multi-domain nature of this system (registration, scheduling, billing, inventory) illustrates the kind of complex workflow automation that AI agents could orchestrate. Relevant as a domain example for agent task routing.
---

### thelastbackspace/cursor-auto-resume (255 stars)

**URL:** https://github.com/thelastbackspace/cursor-auto-resume
**Description:** A simple tool that automatically clicks the "resume the conversation" link in Cursor IDE when rate limits are hit.

**Research:** Browser extension that auto-clicks Cursor's "resume conversation" button when the 25-tool-call limit is hit. Directly addresses a pain point in AI coding agent workflows -- the artificial pause after tool call limits. Uses DOM targeting with XPath/CSS selectors and a 3-second cooldown. While it doesn't integrate with Claude Code directly, it signals community building around agent rate limiting UX. A similar pattern could apply to Claude Code's workflow management.
---

### ErwanLorteau/BMAD_Openclaw (249 stars)

**URL:** https://github.com/ErwanLorteau/BMAD_Openclaw
**Description:** Bridging the BMad Method to OpenClaw  —  Structured AI-driven development workflows.

**Research:** Brings the "BMad Method" structured development methodology to OpenClaw agents. Provides a framework for structured AI-driven development workflows -- encoding best practices into agent-accessible processes. Directly in the OpenClaw ecosystem as a methodology layer on top of the agent framework. Relevant to Claude Code's "proper workflow" thinking and agentic SDLC patterns.
---

### Ark0N/Codeman (247 stars)

**URL:** https://github.com/Ark0N/Codeman
**Description:** Manage Claude Code & Opencode in Tmux Sessions in a modern WebUI

**Research:** Modern WebUI dashboard for managing Claude Code and OpenCode sessions running in tmux. Provides a web-based control plane for terminal-based AI coding agents. Similar to other mission-control tools in this batch (clawsuite, mission-control, openclaw-mission-control) but with support for both Claude Code and OpenCode. Directly relevant to the agent observability and management layer. Filed under Claude Code tooling ecosystem.
---

### manish-raana/openclaw-mission-control (245 stars)

**URL:** https://github.com/manish-raana/openclaw-mission-control
**Description:** Real-time dashboard for monitoring agents and task workflows. Built with Convex and React, it provides a clean dashboard to track task state, agent activity, and live logs.

**Research:** Real-time dashboard for OpenClaw agent monitoring with Convex backend. Kanban-style mission queue (Inbox, Assigned, In Progress, Review, Done), real-time activity feed, agent roster with live counts, and task-linked documents. Convex-powered real-time sync means no polling -- all updates propagate instantly. Strong signal that the OpenClaw ecosystem is building mature operational tooling. Pattern: agent runs to task tracking to real-time monitoring to dashboard.
---

### orra-dev/orra (244 stars)

**URL:** https://github.com/orra-dev/orra
**Description:** A plan engine for dynamic planning and reliable execution of AI agent workflows.

**Research:** Infrastructure for resilient AI agent workflows -- handles recovery from API outages, failed evals, and execution failures. Key features: durable execution with state persistence, pre-validated execution plans, revert state on failure, webhook notifications, and audit logs. Plans MCP integration. Directly adjacent to what a production AI agent OS needs -- the failure-recovery and state-machine layer between "agent decides" and "task completes." Filed under agent orchestration and resilience infrastructure.
---

### SawyerHood/gitclaw (240 stars)

**URL:** https://github.com/SawyerHood/gitclaw
**Description:** OpenClaw but it runs entirely on github actions

**Research:** Runs OpenClaw-style AI agent entirely through GitHub Issues and GitHub Actions -- no servers needed. Each GitHub Issue becomes a chat thread, conversation history committed to git as JSONL session files. Agent can grep its own history and edit/summarize past conversations. Uses badlogic/pi-mono as the underlying coding agent. The serverless agent pattern is compelling: git as memory, issues as sessions, Actions as execution environment. Could inspire a GitHub-native autonomous agent architecture.
---

### firstbatchxyz/dkn-compute-node (228 stars)

**URL:** https://github.com/firstbatchxyz/dkn-compute-node
**Description:** Compute Node of Dria Knowledge Network.

**Research:** Compute node for the Dria Knowledge Network -- a decentralized knowledge infrastructure project. Relevant to the agent memory/knowledge layer space. Dria positions itself as a distributed knowledge graph that agents can query and contribute to. Related to firstbatchxyz/dria-agent (also in this batch) -- these two repos form the compute and agent sides of the same project.
---

### ManojKumarPatnaik/Major-project-list (223 stars)

**URL:** https://github.com/ManojKumarPatnaik/Major-project-list
**Description:** A curated list of 75+ practical programming projects spanning Numbers, Algorithms, Graph, Data Structures, Text, Networking, Web, Security, and more.

**Research:** Canonical mega-project-list for learning programming -- 75+ projects from "Find PI to Nth Digit" to "Content Management System." Not AI agent-related but directly relevant as a benchmark/training corpus for coding agents. Projects like "Bank Account Manager," "TV Show Tracker," and "Credit Card Validator" are the kind of real-world tasks AI coding agents should solve. Could serve as evaluation tasks for Claude Code or OpenClaw agents. Filed under agent benchmarking.
---

### AgentOrchestrator/AgentBase (223 stars)

**URL:** https://github.com/AgentOrchestrator/AgentBase
**Description:** Multi-agent orchestrator for tracking and analyzing AI coding assistant conversations (Claude Code, Cursor, Windsurf).

**Research:** Visual canvas for launching and managing multiple AI coding agents in parallel. Supports Claude Code, Cursor, and Windsurf. Key features: bird's-eye canvas view, parallel execution with isolated or shared edits, progress tracking with todo summaries, and a "command center" to handle multi-agent approval requests. Local-first. Most feature-rich multi-agent orchestration UI in this batch -- competing with orchestr8 and OpenUI for the multi-agent dashboard space. Filed under Claude Code ecosystem, agent orchestration.
---

### naskio/n8n-nodes-python (216 stars)

**URL:** https://github.com/naskio/n8n-nodes-python
**Description:** Run Python code on n8n

**Research:** Custom n8n node for executing Python code in workflow automation. n8n is increasingly used as the orchestration layer for AI agent workflows. This node enables Python-based agent logic to be embedded in n8n automations -- bridging traditional workflow automation with agent-like behavior.
---

### onikan27/claude-code-monitor (212 stars)

**URL:** https://github.com/onikan27/claude-code-monitor
**Description:** Real-time dashboard for monitoring multiple Claude Code sessions. CLI + Mobile Web UI with QR code access, terminal focus switching (iTerm2, Terminal.app, Ghostty). macOS only.

**Research:** Real-time Claude Code session monitor with terminal TUI plus mobile web access via QR code. Notable: terminal focus switching support for iTerm2, Terminal.app, and Ghostty -- first tool in the batch with explicit multi-terminal support. File-based state management (no API server), QR-based mobile auth, Vim-style navigation. macOS-only. Directly in the Claude Code observability space. Filed under Claude Code tooling ecosystem.
---

### minhlucvan/n8n-nodes-browserless (211 stars)

**URL:** https://github.com/minhlucvan/n8n-nodes-browserless
**Description:** n8n node to interact with browserless instance

**Research:** n8n node for browser automation via browserless.io -- enables headless browser control within n8n workflows. Browserless is a cloud service for running headless Chrome at scale. Relevant to agent tooling because web interaction is a core agent capability. Filed under agent web interaction tooling.
---

### HKUDS/MoChat (207 stars)

**URL:** https://github.com/HKUDS/MoChat
**Description:** "MoChat: OpenClaw as Your Social Agent https://mochat.io"

**Research:** A social agent platform where OpenClaw agents operate as participants in chat channels -- discovering collaborators, filtering noise, and bridging communities. Agents join Feishu, WeChat, and other messaging platforms to engage on behalf of users. The agent-native platform concept: not just "agents chat with humans" but "agents as social entities." Different from typical Telegram/Discord bot wrappers -- a full social networking layer for agents. Filed under OpenClaw ecosystem, agent social platforms.
---

### Polygant/OpenCEX (206 stars)

**URL:** https://github.com/Polygant/OpenCEX
**Description:** OpenCEX free open-source cryptocurrency exchange engine. Industry standard.

**Research:** Full-stack open-source cryptocurrency exchange. Not directly AI agent-related, but DeFi and crypto trading is a major use case for autonomous agents. OpenCEX could serve as the backend infrastructure that agent-based trading systems interact with. The agent money management space (agenti, also in this batch) would benefit from exchange-grade backends like this.
---

### Shopify/theme-tools (205 stars)

**URL:** https://github.com/Shopify/theme-tools
**Description:** Everything developer experience for Shopify themes

**Research:** Shopify's official monorepo of theme development tools: Liquid HTML parser, Prettier plugin, linter, language server, CodeMirror client, and VS Code extension. Reference architecture for building a complete DX toolchain -- parser, formatter, linter, LSP, and editor integration. For AI coding agents, relevant because it shows the toolchain maturity needed for professional-grade development and Claude Code/OpenClaw could benefit from similar deep language integrations. Filed under dev tooling, DX infrastructure.
---

### kondasoft/ks-bootshop (200 stars)

**URL:** https://github.com/kondasoft/ks-bootshop
**Description:** Free Shopify theme focused on simplicity, speed, and user experience. Powered by Bootstrap v5.

**Research:** A free Shopify theme built with Bootstrap 5. Not AI agent-related, but Shopify themes are a concrete domain where AI coding agents can add significant value -- generating and customizing themes autonomously. Could serve as a target for Claude Code theme generation tasks.
---

### dreamwing/clawbridge (197 stars)

**URL:** https://github.com/dreamwing/clawbridge
**Description:** ClawBridge is the OpenClaw Mobile Dashboard. Monitor agent's real-time thoughts, actions, track token costs, and manage tasks from anywhere using your pocket-sized Mission Control.

**Research:** Mobile-first dashboard for OpenClaw -- real-time thoughts/actions streaming, token cost tracking, and task management from mobile. Designed as "pocket-sized Mission Control." Part of the broader OpenClaw dashboard ecosystem (clawsuite, mission-control, openclaw-mission-control, clawd-control all in this batch). The mobile-first positioning is notable -- most other tools in this batch are desktop-first. Filed under OpenClaw ecosystem, mobile agent management.
---

### outsourc-e/clawsuite (188 stars)

**URL:** https://github.com/outsourc-e/clawsuite
**Description:** All-in-one command center for OpenClaw agents

**Research:** The most feature-rich OpenClaw dashboard in this batch. V3 includes: multi-agent mission control with isometric office view, cost analytics (per-agent spend, daily trends, EOM projections), 3-theme system, SSE real-time streaming, and a Memory Browser for editing agent memory files from the UI. The Memory Browser is particularly notable -- non-technical users can edit agent memory without touching the filesystem. PWA with mobile parity. One-click Vercel deploy. Filed under OpenClaw ecosystem, mature agent management tooling.
---

### jasewarner/gulp-shopify (185 stars)

**URL:** https://github.com/jasewarner/gulp-shopify
**Description:** Blank slate Shopify theme for Developers, packaged with Gulp.js for processing SCSS, JavaScript (ES6), images and fonts.

**Research:** Developer-focused blank Shopify theme scaffold with Gulp build pipeline. Not AI agent-related, but Shopify theme development is a practical domain for autonomous agent work -- generating Liquid templates, configuring theme settings, deploying via Shopify CLI. Filed under domain examples for agent deployment.
---

### montalvomiguelo/hydrogen-theme (171 stars)

**URL:** https://github.com/montalvomiguelo/hydrogen-theme
**Description:** A port of Hydrogen's default template to Shopify OS 2.0

**Research:** Shopify Hydrogen (React-based) theme ported to Shopify OS 2.0. Same relevance as other Shopify theme repos -- a domain where AI coding agents can autonomously build and customize storefronts.
---

### VienDinhCom/bootstrap-shopify-theme (171 stars)

**URL:** https://github.com/VienDinhCom/bootstrap-shopify-theme
**Description:** A responsive Shopify theme using Bootstrap, BEM, Liquid, Sass, ESNext, Theme Tools, and Webpack.

**Research:** Another Shopify theme in this batch. Bootstrap + Liquid hybrid approach. Not AI agent-specific but serves as a realistic target for agent-based theme generation and customization tasks.
---

### six-ddc/ccbot (168 stars)

**URL:** https://github.com/six-ddc/ccbot
**Description:** Telegram ↔ tmux bridge for Claude Code: 1 topic = 1 window = 1 session

**Research:** The most technically elegant Claude Code remote control tool in this batch. Instead of wrapping the Claude Code SDK (creating isolated sessions), it operates on tmux directly -- Claude Code runs in a tmux window, and CCBot reads output and sends keystrokes. This means sessions are never isolated from the terminal, you can switch mid-conversation from desktop to Telegram to terminal with zero interruption, voice messages are transcribed and forwarded, and slash commands are forwarded. The gold standard for remote Claude Code access. macOS uses osascript; Linux uses xdotool. Filed under Claude Code tooling ecosystem.
---

### memovai/memov (166 stars)

**URL:** https://github.com/memovai/memov
**Description:** Give git-like & traceable memory to OpenClaw and any coding agents. By https://memov.ai/ aka Entire CLI for every coding agents by MCP.

**Research:** Git-like version control layer for AI coding sessions -- every prompt, context change, and code diff is checkpointed with branch exploration and rollback. Key differentiator from standard git: branch-based exploration of coding trajectories, rollback that preserves all history (unlike git reset which erases), and cross-session trajectory tracking. VibeGit is their brand for auto-tracing prompts and context. MCP server available. Directly competes with the memory layer concept in Agent OS and SISO_Knowledge -- represents the emerging pattern of "agent memory as versioned state." Filed under agent memory systems, Claude Code ecosystem.
---

### slhleosun/EvoClaw (161 stars)

**URL:** https://github.com/slhleosun/EvoClaw
**Description:** Structured SOUL evolution framework for AI agents -- experience, reflection, governed identity updates, and visual timelines.

**Research:** Structured identity evolution framework for OpenClaw agents. Refactors SOUL.md documents into canonical sections (Personality, Philosophy, Boundaries, Continuity) with governance tags: [CORE] (immutable) and [MUTABLE] (evolves through reflection). Features: tiered memory (routine/notable/pivotal), reflection pipelines, proposal-based SOUL updates, social feeds as experience sources (Moltbook, X/Twitter), and a local web UI for auditability. Most sophisticated identity/memory evolution system in the OpenClaw ecosystem -- directly addresses the "agent gets better over time" problem. Filed under OpenClaw ecosystem, agent identity and memory.
---

### eborges-git/n8n-render (139 stars)

**URL:** https://github.com/eborges-git/n8n-render
**Description:** Deploying n8n on Render (render.com) hosting, using separate Web Service (with Docker and Persistent Disk Storage) + Postgres DB.

**Research:** Infrastructure template for deploying n8n on Render with Docker, persistent disk, and Postgres. Not AI-agent specific but n8n is increasingly used as an orchestration layer for agent workflows. This template shows the deployment pattern for production n8n stacks -- useful context for anyone building agent-to-n8n integrations.
---

### Fallomai/openui (130 stars)

**URL:** https://github.com/Fallomai/openui
**Description:** AI command center for your AI coding agents. 100% local, free, opensource.

**Research:** Visual canvas for managing multiple AI coding agents in parallel. Each agent is a node on an infinite canvas with at-a-glance status (working/idle/needs-input). Integrates with Linear tickets for session spawning, uses git worktrees for branch isolation per agent. Supports Claude Code, OpenCode, and Ralph Loop. The canvas-centric approach (vs. terminal/TUI approach of ccbot) represents a different UX philosophy for multi-agent oversight. Filed under Claude Code tooling ecosystem, multi-agent orchestration.
---

### betomoedano/React-Native-Notion-Clone (127 stars)

**URL:** https://github.com/betomoedano/React-Native-Notion-Clone
**Description:** Local-First Notion Clone built with Prisma, Expo and ❤️

**Research:** A local-first Notion clone built with React Native/Expo and Prisma. Not AI agent-related, but this pattern (local-first, offline-capable, structured data) is relevant to agent memory systems and agent-accessible knowledge bases. Could serve as a reference architecture for building local-first agent workspaces.
---

### Temaki-AI/clawd-control (113 stars)

**URL:** https://github.com/Temaki-AI/clawd-control
**Description:** Real-time dashboard for monitoring and managing Clawdbot AI agents

**Research:** Dashboard for Clawdbot agents with live SSE monitoring, fleet overview, agent detail views, agent creation wizard, host metrics (CPU/RAM/disk), auto-discovery of local agents, dark/light theme, and password auth. Clawdbot is the predecessor to OpenClaw/Moltbot. Dashboard patterns (fleet overview, metrics, creation wizard) are transferable to OpenClaw. Filed under OpenClaw ecosystem precursor, agent fleet management.
---

### FoundDream/miniclawd (109 stars)

**URL:** https://github.com/FoundDream/miniclawd
**Description:** A lightweight openclaw build with TypeScript.

**Research:** A lightweight, self-contained OpenClaw implementation in ~5900 lines of TypeScript + Bun. Multi-LLM support (Anthropic, OpenAI, Google, OpenRouter, Groq, AWS Bedrock), multi-channel (Telegram, Feishu), built-in tools (file I/O, shell, web), skills system, persistent memory, cron scheduling, and subagent spawning. Most complete standalone OpenClaw alternative in the batch -- everything in one repo. Notable for multi-model routing (per-agent model selection) and multi-channel messaging. Filed under OpenClaw ecosystem, lightweight agent frameworks.
---

### rizqcon/openclawdev-taskboard (100 stars)

**URL:** https://github.com/rizqcon/openclawdev-taskboard
**Description:** An Open Claw Development Team built with security and best practices in mind.

**Research:** Multi-agent Kanban board for OpenClaw with real-time task routing, agent assignment, and persistent chat sessions. V1.6 adds chat message actions (reply, copy, delete) and V1.5 adds column sorting and multi-agent thinking indicators. The "thinking indicators" feature (animated dot + icon showing multiple agents working simultaneously) represents real-time agent state visualization. Filed under OpenClaw ecosystem, task orchestration.
---

### MarlBurroW/pinchchat (98 stars)

**URL:** https://github.com/MarlBurroW/pinchchat
**Description:** A sleek, dark-themed webchat UI for OpenClaw

**Research:** The most polished chat UI for OpenClaw in this batch. Standout features: tool call visualization (colored badges, visible parameters, expandable results), live streaming, token usage progress bars, inline image rendering, split view (two sessions side-by-side), and syntax-highlighted input. The tool call visualization is the killer feature -- seeing exactly what tools the agent called with their parameters and results, in real-time. PWA installable, i18n (EN/FR), accessible (ARIA live regions). Docker deployment. Filed under OpenClaw ecosystem, agent chat UIs.
---

### eason-dev/nextjs-tailwind-contentlayer-blog-starter (89 stars)

**URL:** https://github.com/eason-dev/nextjs-tailwind-contentlayer-blog-starter
**Description:** Blog starter template with Next.js, Tailwind CSS, Contentlayer, i18Next

**Research:** Modern blog starter template. Not AI agent-related but represents the kind of project an autonomous coding agent could scaffold and deploy. Useful as a reference tech stack for blog creation tasks.
---

### firstbatchxyz/dria-agent (80 stars)

**URL:** https://github.com/firstbatchxyz/dria-agent
**Description:** Powerful and fast tool calling agents

**Research:** Fast tool-calling agents for the Dria Knowledge Network. Complements dkn-compute-node (also in this batch). Dria is a decentralized knowledge infrastructure -- agents contribute to and query a distributed knowledge graph. This repo implements the agent side; dkn-compute-node is the compute infrastructure. Filed under agent knowledge systems, distributed AI infrastructure.
---

### vincentkoc/awesome-openclaw (80 stars)

**URL:** https://github.com/vincentkoc/awesome-openclaw
**Description:** Curated awesome list for OpenClaw: skills, plugins, memory systems, MCP tools, deployment stacks, ecosystem platforms, and developer tooling.

**Research:** The canonical curated list for the OpenClaw ecosystem. Sections include: alternative architectures, community channels (4claw, Clawk, MoltBook, MoltOverflow, Moltx, etc.), MCP and tool servers, memory and context systems, skills and skill indexes, deployment and operations, and observability tooling. Best single index of the OpenClaw universe -- essential for understanding the full ecosystem. Filed under OpenClaw ecosystem reference.
---

### fm9394/OpenClaw-OPS-Suite (80 stars)

**URL:** https://github.com/fm9394/OpenClaw-OPS-Suite
**Description:** (null description -- README available)

**Research:** Real-time OpenClaw dashboard with token budget tracking, learning database (agent decisions and outcomes), mini-CRM (contacts and follow-up reminders), goal tracking, content tracker, workflow/SOP documentation, secure settings store, connection tests, security scanner, and calendar integration. One-click Vercel deploy with Neon Postgres. The learning database concept (tracking agent decisions over time) is notable for autonomous improvement. Vercel/Neon stack makes this easy to deploy. Filed under OpenClaw ecosystem, agent ops tooling.
---

### stoneforge-ai/stoneforge (77 stars)

**URL:** https://github.com/stoneforge-ai/stoneforge
**Description:** A web dashboard and runtime for orchestrating AI coding agents

**Research:** Web dashboard and runtime for orchestrating AI coding agents. A direct entrant in the multi-agent orchestration dashboard space (competing with orchestr8, AgentBase, OpenUI from this batch). The "runtime" component suggests it goes beyond monitoring into actual orchestration and execution management.
---

### ZeroPointRepo/youtube-skills (75 stars)

**URL:** https://github.com/ZeroPointRepo/youtube-skills
**Description:** YouTube Transcript API skills for AI agents. Get transcripts, search videos, browse channels. Works with OpenClaw, ClawdBot, Claude Code, Cursor, Windsurf.

**Research:** YouTube data access skills for AI agents -- transcripts, video search, channel browsing, and playlist extraction. Powered by TranscriptAPI (youtubetotranscript.com). Key advantage: no yt-dlp needed, no headless browser, just API calls that work everywhere. The skills format is compatible with Claude Code, Cursor, Windsurf, and OpenClaw -- making it a cross-platform agent skill. Model for building domain-specific agent skills: clear API, simple installation, multi-agent compatibility. Filed under agent skills, web data access tooling.
---

### thedaviddias/souls-directory (73 stars)

**URL:** https://github.com/thedaviddias/souls-directory
**Description:** Directory of SOUL.md personality files for OpenClaw agents

**Research:** Curated web directory of SOUL.md personality templates for OpenClaw agents. Browse at souls.directory. Lets users pick a personality template (core values, communication style, boundaries, vibe) rather than starting from scratch. Tech: Next.js 16, TypeScript, Tailwind, Convex, GitHub OAuth, Vercel. AI-assisted PRs welcome. A marketplace/sharing layer for agent identity -- directly complementary to EvoClaw (which evolves identities) and memov (which versions them). Filed under OpenClaw ecosystem, agent identity and personality.
---

### skalenetwork/sgxwallet (68 stars)

**URL:** https://github.com/skalenetwork/sgxwallet
**Description:** Open-source hardware-secure crypto wallet based on Intel SGX. First open-source product on Intel SGX whitelist. Scales to 100,000+ TPS.

**Research:** Hardware-secured cryptocurrency wallet using Intel SGX enclaves. SKALE Network's infrastructure. Not directly AI agent-related but relevant to the agent-money intersection -- autonomous agents managing crypto assets need hardware-grade security. Filed under agent security, DeFi infrastructure.
---

### knostic/openclaw-telemetry (67 stars)

**URL:** https://github.com/knostic/openclaw-telemetry
**Description:** Telemetry for OpenClaw - Captures tool calls, LLM usage, agent lifecycle, and message events. Outputs to JSONL file and optionally to syslog for SIEM integration.

**Research:** Observability plugin for OpenClaw capturing tool calls, LLM usage, agent lifecycle, and message events. Outputs to JSONL and optionally to syslog for SIEM integration. Built-in redaction, tamper-proof hash chains, and rate limiting. From Knostic (knostic.ai) who also makes openclaw-detect. Most production-grade observability tool in the OpenClaw batch -- designed for enterprise security and audit requirements. The hash chain for tamper evidence is notable for compliance scenarios. Filed under OpenClaw ecosystem, agent observability and security.
---

### seth-schultz/orchestr8 (64 stars)

**URL:** https://github.com/seth-schultz/orchestr8
**Description:** The Future of AI-Powered Development: Orchestr8 Transforms Claude Code Into a Complete Software Engineering Team

**Research:** Transforms Claude Code into a multi-agent software engineering team. V8 achieves 80,000+ tokens saved through progressive loading (JIT loading of resources), example extraction, and structural reorganization. 383 resources indexed with cross-references. Key architectural patterns: core + advanced module splits for agents, JIT-loading workflows (78% average token reduction). The token efficiency focus directly addresses context window pressure in multi-agent systems. MCP protocol compatible. Filed under Claude Code ecosystem, multi-agent orchestration, token optimization.
---

### yh-ong/Web-Based-Clinic-Appointment-System (60 stars)

**URL:** https://github.com/yh-ong/Web-Based-Clinic-Appointment-System
**Description:** Web-Based Clinic Appointment System for doctors and clinics to manage scheduling. Patients can make appointments via mobile app.

**Research:** Healthcare scheduling system. Not AI agent-specific but healthcare scheduling is a practical domain for autonomous agent task routing and calendar management. Filed under domain examples for agent deployment.
---

### RocketChat/RC4Community (57 stars)

**URL:** https://github.com/RocketChat/RC4Community
**Description:** Full-stack components for building, engaging, and growing massive online communities

**Research:** Rocket.Chat's community platform framework -- scalable from one to a million users, with components for engagement across Rocket.Chat, GitHub, Discourse, and Discord. React components, identity management (Auth0, Firebase, Gluu, Keycloak), virtual conference support. Community platforms are natural environments for AI agents acting as community moderators, assistants, or participants. Filed under community infrastructure, agent social platforms.
---

### Jzineldin/mission-control (57 stars)

**URL:** https://github.com/Jzineldin/mission-control
**Description:** macOS-native dashboard for OpenClaw AI agents -- monitor, control, and optimize your agent from a sleek web interface

**Research:** macOS-native-feel web dashboard for OpenClaw. Features: real-time session monitoring, streaming chat widget (press / to open), token cost tracking, cron job management, Scout Engine (auto-search for gigs/grants/skills/news), Workshop (Kanban task board with sub-agent execution), and keyboard-first navigation. The Scout Engine auto-discovery feature is unique -- agents actively hunting for work rather than just responding to commands. Filed under OpenClaw ecosystem, agent ops tooling.
---

### waynesutton/clawsync (56 stars)

**URL:** https://github.com/waynesutton/clawsync
**Description:** OpenClaw for the cloud. Deploy an open source personal AI agent with chat UI, skills system, MCP support, and multi-model routing. Built on Convex.

**Research:** Cloud-deployed OpenClaw with multi-agent system, shared soul documents, multi-model routing (Claude/GPT/Grok/Gemini/OpenRouter), MCP support, channel integrations (Telegram, Discord, WhatsApp, Slack, Email), X (Twitter) integration, AgentMail, file storage (Convex or Cloudflare R2), browser automation (Stagehand), web scraping (Firecrawl), AI analytics, agent research, persistent memory (Supermemory), and live activity feed. Most feature-complete OpenClaw deployment stack in the batch -- essentially a turnkey cloud agent platform. The multi-agent plus multi-model routing is particularly relevant for Claude Code ecosystem discussions about model selection. Filed under OpenClaw ecosystem, cloud agent deployment.
---

### adridder/moltron (49 stars)

**URL:** https://github.com/adridder/moltron
**Description:** Self-evolving Agents. MOLTRON upgrades agents to learn and evolve skills autonomously. Welcome to the Singularity.

**Research:** Self-evolving agent skill system -- teaches OpenClaw agents how to build and self-improve their own skills. Uses CLI, OpenTelemetry, Git, and SmythOS for skill creation and performance evaluation. One-line install via curl script, then @moltron init in chat. Key insight: agent-created skills are inefficient and unreliable, so Moltron teaches agents a structured methodology for skill creation. Directly addresses autonomous agent capability growth -- agents that can bootstrap new capabilities. Filed under agent self-improvement, autonomous skill generation.
---

### GreenSheep01201/Claw-Kanban (45 stars)

**URL:** https://github.com/GreenSheep01201/Claw-Kanban
**Description:** AI Agent Orchestration Kanban Board -- Route tasks to Claude Code, Codex CLI, Gemini CLI, OpenCode, GitHub Copilot, and Google Antigravity with role-based auto-assignment and real-time monitoring

**Research:** The most multi-agent-platform Kanban board in the batch -- routes tasks to Claude Code, Codex CLI, Gemini CLI, OpenCode, GitHub Copilot, and Google Antigravity. Role-based auto-assignment (PM, Developer, Reviewer, etc.) and real-time monitoring. Notable for supporting the widest range of AI coding agents in one board -- signals the emerging need for agent-agnostic orchestration layers. One-line AI installation prompt. Filed under Claude Code ecosystem, multi-agent routing, agent-agnostic orchestration.
---

### nirholas/agenti (42 stars)

**URL:** https://github.com/nirholas/agenti
**Description:** Give AI agents access to money. Manage finances, trade cryptocurrency. MCP server for AI agents to interact with 20+ blockchains. 380+ tools for DeFi, DEX aggregation, security scanning, cross-chain bridges, QR payments. x402 enabled.

**Research:** Only repo in this batch explicitly giving agents financial agency. MCP server with 380+ tools across 20+ blockchains -- DeFi, DEX aggregation, security scanning, cross-chain bridges, QR payments. x402 enabled means agents can autonomously pay for premium APIs and trade with other agents. Works with Claude, ChatGPT, Cursor. Most concrete implementation of "agent-as-economic-actor" in the batch -- agents that hold wallets, trade, and pay for resources. Filed under agent financial systems, MCP ecosystem, autonomous economic agents.
---

### Nebaura-Labs/mote (40 stars)

**URL:** https://github.com/Nebaura-Labs/mote
**Description:** Mote - An open-source ESP32-S3 voice companion for Clawd.bot

**Research:** Physical voice companion device for Clawd.bot built on ESP32-S3 with animated face display (2" IPS LCD), real-time voice chat via Deepgram STT and ElevenLabs TTS, BLE mobile app setup, and WiFi/WebSocket connection to the agent gateway. Form factors: Desk Companion and Watch Companion (coming). Most hardware-focused project in the batch -- bringing the AI agent into the physical world through a dedicated device. Filed under OpenClaw ecosystem, physical AI devices, voice interaction.

Research for indices 150-199. Researched via README fetch from GitHub raw content.
---

### ovh/utask (1365 stars)

**URL:** https://github.com/ovh/utask
**Description:** µTask is an automation engine that models and executes business processes declared in yaml.

**Research:** An OVH-hosted automation engine for modeling and executing business processes declaratively in YAML. Simple to operate (only needs Postgres), secure (encrypted data), extensible (custom actions in Go). Models a graph of actions with inter-dependencies, handles transient errors, maintains auditable traces. High relevance to autonomous agent task orchestration patterns -- it's essentially a YAML-defined agent execution engine. Could inspire Claude Code workflow automation patterns.
---

### peterkrueck/Claude-Code-Development-Kit (1327 stars)

**URL:** https://github.com/peterkrueck/Claude-Code-Development-Kit
**Description:** Handle context at scale - my custom Claude Code workflow including hooks, mcp and sub agents

**Research:** A personal Claude Code development workflow system with hooks, MCP, and sub-agents. Explicitly designed around Claude Code's sub-agent capabilities for parallel, orchestrated development. Addresses context management challenges at scale (architecture patterns, coding standards, team conventions). Directly relevant to Claude Code infrastructure -- it's a real-world production system for scaling Claude Code with context automation.
---

### CloudAI-X/claude-workflow-v2 (1300 stars)

**URL:** https://github.com/CloudAI-X/claude-workflow-v2
**Description:** Universal Claude Code workflow plugin with agents, skills, hooks, and commands

**Research:** A universal workflow plugin compatible with Claude Code, Cursor, Codex, and 35+ AI agents. Installs via skills.sh or npx. Provides specialized agents, skills, hooks, and output styles for any software project. High relevance to Claude Code skills/hooks ecosystem -- it's a cross-agent standard for workflow sharing, competing with the skills.sh registry.
---

### Shopify/themekit (1284 stars)

**URL:** https://github.com/Shopify/themekit
**Description:** Shopify theme development command line tool.

**Research:** Deprecated Shopify theme CLI tool (superseded by Shopify CLI). Low relevance to AI agents, Claude Code, or autonomous agents. Notable mainly as a reference for well-built Go CLI tooling.
---

### disler/claude-code-hooks-multi-agent-observability (1276 stars)

**URL:** https://github.com/disler/claude-code-hooks-multi-agent-observability
**Description:** Real-time monitoring for Claude Code agents through simple hook event tracking.

**Research:** A complete observability stack for Claude Code multi-agent systems. Captures hook events (tool calls, task handoffs, agent lifecycle) via Python/uv scripts, streams through a Bun HTTP server with SQLite persistence, and visualizes via WebSocket + Vue client. Architecture: Claude Agents -> Hook Scripts -> HTTP POST -> Bun Server -> SQLite -> WebSocket -> Vue Client. Extremely high relevance to Claude Code multi-agent orchestration -- it's a production-ready monitoring system for agent swarms.
---

### YouMind-OpenLab/nano-banana-pro-prompts-recommend-skill (1240 stars)

**URL:** https://github.com/YouMind-OpenLab/nano-banana-pro-prompts-recommend-skill
**Description:** AI skill for OpenClaw & Claude Code — recommend from 10000+ Nano Banana Pro (Gemini) image prompts.

**Research:** An OpenClaw/Claude Code skill for AI image prompt search across 10K+ curated Nano Banana Pro (Gemini) prompts. Smart semantic search by use case, content remix mode, sample images included, updated twice daily, multi-language. Demonstrates the skills.sh plugin pattern for extending agent capabilities. Relevant to the OpenClaw/Claude Code skills ecosystem.
---

### omerxx/tmux-sessionx (1217 stars)

**URL:** https://github.com/omerxx/tmux-sessionx
**Description:** A Tmux session manager, with preview, fuzzy finding, and MORE

**Research:** A modern fuzzy Tmux session manager with fzf-powered preview, session deletion/rename, bat for syntax highlighting, and zoxide support. Popular among terminal power users. Not AI-agent specific but highly complementary -- used by many Claude Code workflows to manage multiple agent sessions. The tmux+CClaude Code pattern (cmux, agent-viewer, etc.) keeps appearing in this space.
---

### junhoyeo/tokscale (1217 stars)

**URL:** https://github.com/junhoyeo/tokscale
**Description:** A CLI tool for tracking token usage from OpenCode, Claude Code, OpenClaw, Pi, Codex, Gemini, Cursor, and more.

**Research:** A CLI + dashboard for tracking token usage and costs across Claude Code, OpenClaw, Codex, Cursor, and 8+ other AI coding agents. Native Rust TUI with cross-platform support. Includes global leaderboard and contribution graphs. Extremely high relevance to the AI coding agent ecosystem -- provides cost visibility for Claude Code and competitors. The multi-agent token tracking pattern is directly applicable to autonomous agent cost management.
---

### rinadelph/Agent-MCP (1195 stars)

**URL:** https://github.com/rinadelph/Agent-MCP
**Description:** Agent-MCP is a framework for creating multi-agent systems that enables coordinated, efficient AI collaboration through the Model Context Protocol.

**Research:** A multi-agent collaboration framework built on MCP (Model Context Protocol). Enables coordinated AI development with specialized agents working in parallel on different project aspects. Designed for distributed AI software development. Claims advantages over single-agent: no context overflow, no lost knowledge, parallel execution, specialization, no rework. High relevance to AI agent orchestration and Claude Code multi-agent patterns.
---

### decentraland/marketplace (1195 stars)

**URL:** https://github.com/decentraland/marketplace
**Description:** Decentraland's NFT Marketplace

**Research:** Decentraland's NFT marketplace (React frontend + indexer backend). Low direct relevance to AI agents, Claude Code, or autonomous agents. Notable as a large production React/TypeScript app with React Server Components pattern. Filed under general dev tooling.
---

### julionc/awesome-shopify (1193 stars)

**URL:** https://github.com/julionc/awesome-shopify
**Description:** A curated list of awesome Shopify resources, libraries and open source projects.

**Research:** A curated awesome-list of Shopify resources. Low relevance to AI agents, Claude Code, or autonomous agents. Filed under general developer resources.
---

### steipete/claude-code-mcp (1175 stars)

**URL:** https://github.com/steipete/claude-code-mcp
**Description:** Claude Code as one-shot MCP server to have an agent in your agent.

**Research:** An MCP server that wraps Claude Code in one-shot mode with automatic permission bypass. Enables Claude Code to be used as a tool by other LLMs (Cursor, Windsurf) via MCP. Key insight: Claude Code is better/faster at file edits than Cursor/Windsurf, so offloading file ops to Claude Code via MCP saves cost and improves quality. "Agents in Agents" pattern -- directly relevant to Claude Code nested agent architectures.
---

### aiming-lab/Agent0 (1092 stars)

**URL:** https://github.com/aiming-lab/Agent0
**Description:** Agent0 Series: Self-Evolving Agents from Zero Data

**Research:** Research project from UNC-Chapel Hill, Salesforce Research, and Stanford on self-evolving autonomous agents. Released in late 2025 with both Agent0 and Agent0-VL papers on arXiv. Focuses on autonomous agent evolution without human-labeled data. Relevant to AI agent capability research and the academic side of autonomous agent development.
---

### runkids/skillshare (905 stars)

**URL:** https://github.com/runkids/skillshare
**Description:** Sync skills across all AI CLI tools with one command and simplify team sharing. Supporting Codex, Claude Code, OpenClaw & more

**Research:** A cross-agent skills sync tool. One command syncs skills across Claude Code, Codex, OpenClaw, OpenCode, and 50+ AI agents. Built in Go, MIT licensed. A central hub for the skills.sh ecosystem -- if skills.sh is the standard, skillshare is the package manager. High relevance to Claude Code and OpenClaw skills infrastructure.
---

### crabwise-ai/crabwalk (864 stars)

**URL:** https://github.com/crabwise-ai/crabwalk
**Description:** Real-time companion monitor for OpenClaw agents.

**Research:** A real-time monitoring dashboard for OpenClaw agents using ReactFlow node graph visualization. Watch agent sessions across WhatsApp, Telegram, Discord, and Slack simultaneously. See thinking states, tool calls, and response chains as they happen. WebSocket-powered real-time streaming. Directly relevant to OpenClaw infrastructure -- a monitoring/observability layer for multi-platform agent sessions.
---

### zentralopensource/zentral (847 stars)

**URL:** https://github.com/zentralopensource/zentral
**Description:** Zentral is a high-visibility platform for controlling Apple endpoints in enterprises.

**Research:** Enterprise Apple device management platform integrating MDM (Apple), Munki (software distribution), Osquery (device queries), and Santa (binary authorization). For high-security enterprise environments. Low direct relevance to AI agents. Notable for its config-as-code and Terraform provider approach.
---

### context-machine-lab/sleepless-agent (810 stars)

**URL:** https://github.com/context-machine-lab/sleepless-agent
**Description:** 24/7 AI agent that maximizes Claude Code Pro usage via Slack. Auto-processes tasks, manages isolated workspaces, creates Git commits/PRs, and optimizes day/night usage thresholds.

**Research:** A 24/7 Claude Code Pro daemon that runs via Slack. Transforms Claude Code into an AgentOS that processes tasks while you sleep. Features: isolated workspaces for parallel task execution, automatic PR creation, configurable day/night usage thresholds to optimize Pro plan spending. Uses Claude Code Python Agent SDK. Directly relevant to Claude Code infrastructure -- it's a production system for maximizing Claude Code Pro ROI.
---

### carlosazaustre/tenacitOS (810 stars)

**URL:** https://github.com/carlosazaustre/tenacitOS
**Description:** OpenClaw Mission Control Dashboard

**Research:** A real-time dashboard and control center for OpenClaw instances built with Next.js, React 19, and Tailwind CSS v4. Reads OpenClaw config, agents, sessions, memory, and logs directly from the host -- no extra DB. Features: system monitor (CPU/RAM/disk), agent dashboard, cost tracking from SQLite, cron manager, activity feed with heatmap, memory browser, file browser, 3D office visualization. High relevance to OpenClaw infrastructure -- a full-featured mission control dashboard.
---

### prompt-security/clawsec (782 stars)

**URL:** https://github.com/prompt-security/clawsec
**Description:** A complete security skill suite for OpenClaw's and NanoClaw agents. Protect your SOUL.md with drift detection, live security recommendations, automated audits, and skill integrity verification.

**Research:** A security skill suite from Prompt Security for OpenClaw agents. Features: SOUL.md drift detection, live security recommendations, automated audits, skill integrity verification. Protects agent configuration files from unauthorized changes. Directly relevant to OpenClaw security -- the first dedicated security tooling for the OpenClaw ecosystem. Filed under AI agent security.
---

### karpathy/jobs (723 stars)

**URL:** https://github.com/karpathy/jobs
**Description:** A research tool for visually exploring Bureau of Labor Statistics Occupational Outlook Handbook data.

**Research:** Karpathy's BLS occupational data explorer. Not AI-agent relevant. Notable mainly as a personal project by a prominent AI researcher demonstrating data visualization patterns. Filed under general developer tooling.
---

### terryso/claude-auto-resume (700 stars)

**URL:** https://github.com/terryso/claude-auto-resume
**Description:** A shell script utility that automatically resumes Claude CLI tasks when usage limits are lifted.

**Research:** A shell script that auto-resumes Claude CLI tasks when usage limits are lifted. Simple but practical -- directly relevant to Claude Code usage management. Useful for Claude Code infrastructure to handle rate limiting gracefully.
---

### prompt-engineering/chat-flow (687 stars)

**URL:** https://github.com/prompt-engineering/chat-flow
**Description:** ChatFlow - AI-based chat flow framework, personalize your ChatGPT workflows and build the road to automation.

**Research:** A framework for building personalized AI chat workflows and automation. Focuses on ChatGPT workflow customization. Low direct relevance to Claude Code or OpenClaw. Filed under general AI workflow tooling.
---

### vstorm-co/full-stack-ai-agent-template (671 stars)

**URL:** https://github.com/vstorm-co/full-stack-ai-agent-template
**Description:** Production-ready Full-Stack AI Agent Template — FastAPI + Next.js with 5 AI frameworks (PydanticAI, LangChain, LangGraph, CrewAI, DeepAgents), WebSocket streaming, tool approval UI, auth, multi-DB, observability, and 20+ integrations.

**Research:** A production-grade full-stack AI agent template with FastAPI backend and Next.js frontend. Supports 5 AI agent frameworks (PydanticAI, LangChain, LangGraph, CrewAI, DeepAgents). Includes WebSocket streaming, human-in-the-loop tool approval UI, auth, multi-database support, observability, and 20+ integrations. Extremely high relevance to AI agent development -- it's a battle-tested template for building production AI agent applications. This team also maintains pydantic-deepagents.
---

### quoroom-ai/room (642 stars)

**URL:** https://github.com/quoroom-ai/room
**Description:** Open-source earning-focused swarm intelligence engine. Self-governing AI collectives (queen, workers, quorum voting) running locally via MCP.

**Research:** A swarm intelligence engine with queen/workers/quorum voting architecture. Self-governing AI collectives that run locally via MCP. Works with Claude Code, Codex, or pay-per-use APIs. Open research project in autonomous agent collectives -- the "wallet" and "quorum voting" concepts are novel. Native MCP support means direct compatibility with Claude Code. Filed under AI agents, swarm intelligence.
---

### firstbatchxyz/mem-agent-mcp (614 stars)

**URL:** https://github.com/firstbatchxyz/mem-agent-mcp
**Description:** mem-agent mcp server

**Research:** An MCP server for the driaforall/mem-agent model. Connects to Claude Desktop, LM Studio, and other MCP clients. Obsidian-like memory system for AI agents. macOS (Metal backend) and Linux (vLLM backend) support. Direct relevance to Claude Code memory infrastructure -- an MCP-based approach to persistent agent memory.
---

### supermemoryai/openclaw-supermemory (604 stars)

**URL:** https://github.com/supermemoryai/openclaw-supermemory
**Description:** OpenClaw Supermemory lets to have long-term memory and recall for your openclaw agent.

**Research:** A Supermemory-powered long-term memory plugin for OpenClaw. Automatically remembers conversations, recalls relevant context, builds persistent user profiles. Cloud-based (supermemory.ai), requires Supermemory Pro. Another entry in the crowded agent memory space, this time SaaS-based. Filed under OpenClaw plugins, memory systems.
---

### agent-sh/agentsys (604 stars)

**URL:** https://github.com/agent-sh/agentsys
**Description:** AI writes code. This automates everything else. 18 plugins, 38 agents, and 36 skills for Claude Code, OpenCode, Codex, cursor, kiro.

**Research:** A modular agent runtime and marketplace for AI coding agents. 18 plugins, 38 agents, 36 skills across 5 platforms (Claude Code, OpenCode, Codex, Cursor, Kiro). 30K lines of library code, 3,575 tests. Agents are distributed as standalone repos under agent-sh org, agentsys is the installer and hub. Listed in awesome-claude-code. Extremely high relevance to Claude Code and OpenClaw infrastructure -- the largest plugin/agent collection for the AI coding agent ecosystem.
---

### ibelick/webclaw (587 stars)

**URL:** https://github.com/ibelick/webclaw
**Description:** Fast web client for OpenClaw.

**Research:** A fast browser-based web client for OpenClaw. Runs via npx with a single CLI command. Beta status. Alternative to the native OpenClaw CLI for browser-based agent interaction. Direct relevance to OpenClaw user experience -- a lightweight web interface for accessing OpenClaw agents.
---

### Farzad-R/LLM-Zero-to-Hundred (557 stars)

**URL:** https://github.com/Farzad-R/LLM-Zero-to-Hundred
**Description:** This repository contains different LLM chatbot projects (RAG, LLM agents, etc.) and well-known techniques for training and fine tuning LLMs.

**Research:** An educational repository covering LLM chatbot projects (RAG, LLM agents, fine-tuning techniques). Includes WebGPT, RAG-GPT, WebRAGQuery, LLM Fine-tuning, HUMAIN multimodal chatbot. Low direct relevance to Claude Code or OpenClaw. Useful as a reference for LLM training/fine-tuning patterns.
---

### bkdevs/async-server (533 stars)

**URL:** https://github.com/bkdevs/async-server
**Description:** It's like Claude Code + Linear + GitHub PR

**Research:** An open-source developer tool combining AI coding (Claude Code), task management (Linear), and code review (GitHub PRs). Key features: auto-researches tasks and asks clarifying questions before execution, executes in cloud isolated environments, breaks work into reviewable subtasks with stack diffs, handles full workflow from GitHub issue to merged PR. High relevance to Claude Code -- it's a cloud-execution layer on top of Claude Code with integrated PM workflow.
---

### dappros/ethora (522 stars)

**URL:** https://github.com/dappros/ethora
**Description:** Open-source engine for chat, AI assistants & wallets. React, Typescript, Python, XMPP. Build future apps with chat, AI agents and web3.

**Research:** A monorepo of SDKs for real-time chat, AI bots, and wallets. Covers React, React Native, Android (Kotlin), iOS (Swift), WordPress. Includes MCP CLI for IDE/agent integration, RAG demos, and bot framework. XMPP-based real-time messaging. An interesting player in the AI agent messaging infrastructure space -- the MCP CLI integration is directly relevant to agent tooling.
---

### gitbitex/gitbitex-spot (519 stars)

**URL:** https://github.com/gitbitex/gitbitex-spot
**Description:** An Open Source Cryptocurrency Exchange

**Research:** An abandoned open-source cryptocurrency exchange (redirects to gitbitex-new). Go-based architecture. Low relevance to AI agents, Claude Code, or autonomous agents.
---

### L1AD/claude-task-viewer (495 stars)

**URL:** https://github.com/L1AD/claude-task-viewer
**Description:** A web-based Kanban board for viewing Claude Code tasks

**Research:** A real-time Kanban board for observing Claude Code tasks. Shows all sessions and tasks in one place with live updates. Features: task dependency visualization (blockedBy/blocks), active session detection, Gantt-style timeline view, desktop notifications, stale session auto-archiving. Observation-focused design -- Claude controls state, viewer shows what is happening. Direct relevance to Claude Code UX -- the kanban/task viewer pattern is well-established in this ecosystem.
---

### camel-ai/loong (492 stars)

**URL:** https://github.com/camel-ai/loong
**Description:** Loong: Synthesize Long CoTs at Scale through Verifiers.

**Research:** A CAMEL-AI project on synthesizing long chain-of-thought reasoning at scale using verifiers. Blog at camel-ai.org. Relevant to AI agent reasoning research -- addresses the challenge of generating and verifying long reasoning chains. Filed under AI agents, reasoning research.
---

### milisp/codexia (491 stars)

**URL:** https://github.com/milisp/codexia
**Description:** Agent Workstation for Codex CLI + Claude Code — with task scheduler, git worktree & remote control, Tauri

**Research:** A Tauri-based GUI workstation for Codex CLI and Claude Code. Features: visual project browser, session history with context resume, multiple windows, one-click file selection from file tree, prompt notepad, git worktree management, diff view, built-in PDF/CSV/XLSX viewer. Cross-platform (macOS, Linux). Highly relevant to Claude Code and Codex -- it's a GUI layer on top of both CLI agents, similar to superset-sh/superset but for Codex+Claude Code.
---

### wecode-ai/Wegent (485 stars)

**URL:** https://github.com/wecode-ai/Wegent
**Description:** An open-source AI-native operating system to define, organize, and run intelligent agent teams

**Research:** An AI-native OS for organizing and running agent teams. Built with Python 3.10+, FastAPI, Next.js 15, Docker. Supports Claude Code and Gemini. Architecture includes entry layer, agent execution layer, workspace layer. Self-described "AI-native OS" -- similar to the RightNow-AI/openfang "Agent OS" concept. Direct relevance to autonomous agent orchestration and Claude Code team coordination.
---

### sundial-org/awesome-openclaw-skills (481 stars)

**URL:** https://github.com/sundial-org/awesome-openclaw-skills
**Description:** Top OpenClaw skills, with the most popular and useful ones.

**Research:** A curated collection of 913 OpenClaw skills across 20 categories. Sourced from ClawhHub. Top skills in Agent Core & Memory, Productivity & Tasks, Developer Tools, Web & Search, Communication & Email, Social Media, Content & Writing, Video & Audio categories. Install via npx sundial-hub. High relevance to OpenClaw skills ecosystem -- the definitive curated list of OpenClaw capabilities.
---

### robsannaa/openclaw-mission-control (474 stars)

**URL:** https://github.com/robsannaa/openclaw-mission-control
**Description:** A GUI that runs on your OpenClaw host and lets you totally manage it without touching the CLI.

**Research:** A browser-based GUI for managing OpenClaw instances without CLI. Features: real-time agent monitoring, chat interface, job scheduling, cost tracking, memory management. 100% local, no cloud, no accounts, no telemetry. Auto-discovers OpenClaw setup. Direct relevance to OpenClaw infrastructure -- another mission control dashboard (competing with tenacitOS, openclaw-dashboard, clawdeck).
---

### hollaex/hollaex-kit (468 stars)

**URL:** https://github.com/hollaex/hollaex-kit
**Description:** Exchange Starter Kit to run your own Digital Asset Trading Exchange Platform

**Research:** An open-source white-label crypto exchange software suite. CLI tool for exchange setup and operation. React frontend, server backend. Low relevance to AI agents, Claude Code, or autonomous agents.
---

### vstorm-co/pydantic-deepagents (467 stars)

**URL:** https://github.com/vstorm-co/pydantic-deepagents
**Description:** Python Deep Agent framework built on top of Pydantic-AI, designed to help you quickly build production-grade autonomous AI agents with planning, filesystem operations, subagent delegation, skills, and structured outputs.

**Research:** A Python deep agent framework on Pydantic-AI. Enables production-grade autonomous agents with planning, filesystem ops, subagent delegation, skills, structured outputs in ~10 lines of code. Includes CLI terminal AI assistant and DeepResearch reference app. 100% test coverage. Same team as full-stack-ai-agent-template. High relevance to AI agent development -- a lightweight alternative to LangChain/CrewAI built on Pydantic's type-safe foundation.
---

### betomoedano/quick-push (418 stars)

**URL:** https://github.com/betomoedano/quick-push
**Description:** A lightweight macOS menu bar utility for quickly testing Expo push notifications

**Research:** A macOS menu bar app for testing Expo push notifications, Live Activities, native APNs, and FCM. Not AI-agent relevant. Filed under developer tooling.
---

### craigsc/cmux (367 stars)

**URL:** https://github.com/craigsc/cmux
**Description:** cmux: tmux for Claude Code

**Research:** A tmux worktree manager for running Claude Code agents in isolated git worktrees. Creates a separate checkout per agent so multiple agents can work in parallel without file conflicts. One command: cmux new <feature> creates worktree + branch, runs setup hook, opens Claude. Reuses the same .git database, branches stay in sync. Directly relevant to Claude Code multi-agent infrastructure -- the definitive worktree solution for Claude Code parallelism. Clean, focused, zero-bullshit implementation.
---

### hallucinogen/agent-viewer (342 stars)

**URL:** https://github.com/hallucinogen/agent-viewer
**Description:** Kanban board for managing Claude Code agents in tmux

**Research:** A kanban board + web UI for managing multiple Claude Code agents running in tmux. Spawn, monitor, and interact with agents from a single interface. Mobile-friendly via Tailscale. Node.js + tmux prerequisites. Similar to L1AD/claude-task-viewer but runs agents in tmux sessions. Direct relevance to Claude Code multi-agent management -- the tmux+CClaude Code pattern appears again as a production approach.
---

### WW-AI-Lab/openclaw-office (334 stars)

**URL:** https://github.com/WW-AI-Lab/openclaw-office
**Description:** OpenClaw Office is the visual monitoring and management frontend for the OpenClaw Multi-Agent system.

**Research:** A visual monitoring and management dashboard for OpenClaw with a unique "digital office" metaphor. Renders agent work as an isometric 2D/3D virtual office (React Three Fiber) where agents have desks, meeting pods, and collaboration lines. Side panels show token charts, cost pie charts, activity heatmaps, sub-agent relationship graphs, event timelines. Also includes chat, cron manager, session browser. The most visually distinctive OpenClaw dashboard -- transforms agent activity into a spatial experience.
---

### clawdeckio/clawdeck (317 stars)

**URL:** https://github.com/clawdeckio/clawdeck
**Description:** Open source mission control for your OpenClaw agents

**Research:** A kanban-style dashboard for OpenClaw task management. Hosted at clawdeck.io or self-hosted. Features: kanban boards, agent task assignment, real-time activity feed, full REST API, Hotwire-powered live UI. Early development but active. Another entry in the OpenClaw mission control space (competing with tenacitOS, openclaw-mission-control, openclaw-office, openclaw-dashboard).
---

### get-convex/agent (312 stars)

**URL:** https://github.com/get-convex/agent
**Description:** Build AI agents on Convex with persistent chat history

**Research:** Convex's agent component for building AI agentic applications. Separates long-running agentic workflows from UI while keeping reactivity. Manages threads and messages. Agents and Threads are first-class Convex primitives. Agents provide unit-of-use-case-specific prompting with models, prompts, tool calls. Threads persist messages. High relevance to AI agent development -- Convex provides the backend infrastructure (persistence, reactivity, component system) for agent apps.
---

### Arkya-AI/claude-context-os (295 stars)

**URL:** https://github.com/Arkya-AI/claude-context-os
**Description:** A complete operating system for Claude that prevents context loss and makes multi-session work reliable

**Research:** A context management system for Claude Code that solves context compaction/loss. v4 distilled from 9 peer-reviewed papers on LLM system prompt behavior. Key findings: LLMs track 5-10 rules before degradation, explanatory prose interferes with instruction compliance, Claude 4.6 overtriggers on aggressive language. Result: 47 lines, 7 rules down from 327 lines, 15+ rules. Addresses the core Claude Code pain point of context loss between sessions. Extremely high relevance to Claude Code infrastructure -- the most research-grounded context management approach.
---

### lekt9/openclaw-foundry (281 stars)

**URL:** https://github.com/lekt9/openclaw-foundry
**Description:** The forge that forges itself. Self-writing meta-extension for OpenClaw that learns your workflows, researches docs, and writes new capabilities into itself.

**Research:** A self-writing meta-extension for OpenClaw. The observe-research-learn-write-deploy cycle: watches workflows and tool calls, researches docs and papers, crystallizes patterns into tools/extensions/hooks/skills, then deploys. It literally writes its own capabilities. Novel concept -- agents that extend themselves autonomously. Filed under OpenClaw plugins, self-improving agents.
---

### mudrii/openclaw-dashboard (279 stars)

**URL:** https://github.com/mudrii/openclaw-dashboard
**Description:** A beautiful, zero-dependency command center for OpenClaw AI agents

**Research:** A zero-dependency local dashboard for OpenClaw. 12 panels covering: live CPU/RAM/disk metrics, OpenClaw gateway health, cost analytics, cron status, active sessions, sub-agent runs, model usage breakdown, git log. Auto-refreshes, color-coded thresholds, no login or external services. The "no dependencies" angle is notable -- it's a single self-contained page. Direct relevance to OpenClaw -- the practical at-a-glance overview layer for power users running OpenClaw seriously.
---

Research for indices 100-149. Researched via README fetch.
---

Research for indices 210-239. Researched via `gh repo view` and README fetch.
---

**URL:** https://github.com/anssanova/Apparel-Theme-Development
**Description:** A custom Shopify apparel theme developed with Liquid and Shopify's theme architecture. Built with modular sections and reusable components, it delivers a clean, responsive and scalable storefront designed for modern eCommerce experiences.

**Research:** Custom Shopify apparel theme with modular sections. Part of the rcereceda/shopify-sections "Atomic Sections" collection. Zero AI agent relevance.
---

### stefbowerman/cadaver-2.0 (35 stars)

**URL:** https://github.com/stefbowerman/cadaver-2.0
**Description:** Cadaver is a Shopify Online Store 2.0 starter theme.

**Research:** A production-quality Shopify Online 2.0 theme boilerplate with Tailwind V4, Taxi.js for SPA-like navigation, Webpack bundling, GSAP animations, and 95+ Lighthouse scores. Used in production at The GitHub Shop, Fucking Awesome, +44, SIHA, and Palantir Store. Notable as a battle-tested Shopify theme built with modern dev tooling. For SISO, a reference for Shopify theme development patterns demonstrating what AI-assisted Shopify builds look like.
---

**URL:** https://github.com/brijr/mdx
**Description:** MDX Next.js Starter built with shadcn/ui

**Research:** A modern MDX content site starter with Next.js 16, Velite (type-safe content management), Tailwind CSS, and shadcn/ui. Velite validates frontmatter and generates TypeScript types at build time. For SISO, could serve as a foundation for the knowledge base / library publishing system. Primarily a frontend stack rather than AI-specific.
---

### navjotdhanawat/openclaw-mission-control (31 stars)

**URL:** https://github.com/navjotdhanawat/openclaw-mission-control
**Description:** Mission Control dashboard for OpenClaw -- manage agents, tasks, and missions from a command-center UI

**Research:** Real-time OpenClaw dashboard built with Next.js 16, React 19, TypeScript, and Tailwind CSS 4. Features include Kanban task board (5 stages), real-time agent monitoring, live terminal with activity feed, and mission management. Runs via `npx openclaw-mission-control` with interactive setup wizard. Represents the "single pane of glass" pattern -- a dashboard aggregating agent state, tasks, and activity.
---

### wolverin0/clawtrol (30 stars)

**URL:** https://github.com/wolverin0/clawtrol
**Description:** Mission control for your AI agents

**Research:** The most feature-rich OpenClaw mission control dashboard. Built on ClawDeck with: ZeroBitch Fleet (Docker-based agent fleet with auto-scaling), Factory Loops (autonomous coding cycles: find → improve → test → commit → repeat), Nightshift (scheduled missions during off-hours), Agent Personas (named personas with models and behavioral profiles), and ZeroClaw Auditor (automated QA gate). The "factory floor" metaphor for multi-agent orchestration is compelling. For SISO, ClawTrol demonstrates the most advanced example of the agent management dashboard pattern.
---

**URL:** https://github.com/ianpilon/OpenOrca
**Description:** Real-time dashboard to monitor and control personal AI agents ("Claw Agents")

**Research:** Real-time command center explicitly designed for human-AI collaboration. README addressed "To AI Agents" explains how agents can request human help via structured Intervention Requests (approval_needed, clarification, permission, error, cost_limit types). Enables capabilities humans grant: wallet access, permission escalation, integration credentials, approval for high-impact actions. For SISO, demonstrates thoughtful human-in-the-loop agent control -- structured intervention rather than just monitoring. Directly relevant to SISO's PM agent layer.
---

### ketanmistry/taillour-theme (27 stars)

**URL:** https://github.com/ketanmistry/taillour-theme
**Description:** Taillour is a Shopify 2.0 boilerplate theme for building custom-designed Shopify stores.

**Research:** A Shopify 2.0 boilerplate with purchase-together options, gift wrap, recently viewed, free shipping nudges, predictive search, JSON structured data, and newsletter popup. Built by a freelance Shopify developer. Notable for the practical Shopify feature set (what a real Shopify dev needs day-to-day). Related to the broader Shopify theme development ecosystem.
---

### Mobeen-Dev/chatbot_Shopify (27 stars)

**URL:** https://github.com/Mobeen-Dev/chatbot_Shopify
**Description:** Agentic Shopify Chatbot with MCP integration, embedded via Theme Extension

**Research:** An agentic chatbot embedded into Shopify via Theme Extension. Uses OpenAI LLM with FAISS semantic search and Elasticsearch lexical matching. Capabilities include cart management, checkout flows, customer accounts, order management, and real-time product access. Backend: FastAPI + Redis (sessions) + MongoDB (chat history). For SISO, demonstrates agentic commerce -- an AI that takes actions (add to cart, checkout) rather than just answering questions.
---

**URL:** https://github.com/Automations-Project/n8n-bulk-automated-google-drive-files-sharing-and-direct-download-link-generation
**Description:** n8n workflow template for bulk Google Drive file sharing.

**Research:** An n8n workflow template for bulk Google Drive automation: OAuth2 authentication, batch file listing, public link generation, and access status modification. Handles 4,200+ files reliably. Not AI-specific but n8n's workflow automation is directly relevant to SISO's automation philosophy. SISO could integrate with n8n workflows as a backend execution layer for certain automation tasks.
---

**URL:** https://github.com/bokiko/openClaw-dashboard
**Description:** OpenClaw AI Agent Swarm Dashboard

**Research:** Real-time OpenClaw swarm dashboard with PostgreSQL persistence, JWT auth, and WebSocket updates. Features: live agent strip, Kanban task board, routine manager, agent chat, activity feed, metrics charts, notification system, and command palette. Includes an AGENTS.md file that lets AI assistants set up the dashboard autonomously. For SISO, a well-architected reference for production-grade agent dashboards: React 19 + Next.js + Fastify backend + PostgreSQL + WebSocket.
---

**URL:** https://github.com/caopulan/fix-my-claw
**Description:** A plug-and-play 24/7 watchdog for OpenClaw with automatic recovery.

**Research:** A self-healing watchdog for long-running OpenClaw hosts. Tiers of recovery: 1) probe gateway health, 2) run official repair steps, 3) use AI (via acpx) for complex recovery, 4) write incident bundle and wait. Runs as a systemd service. Key pattern: "official-first, AI-escalation-second" -- try deterministic fixes before burning AI tokens on fuzzy repair. For SISO, critical reliability pattern: autonomous systems need self-healing infrastructure. The "tiered recovery" approach applies directly to SISO's reliability architecture.
---

**URL:** https://github.com/ewimsatt/openclaw-opsdeck-core
**Description:** Mission Control dashboard for OpenClaw: round table, local chat, and cron controls.

**Research:** Lightweight OpenClaw mission control dashboard with macOS focus. Features: agent round table (live view of active/idle agents), cron dashboard (health + next-run + manual triggers), local chat, and project git-status tracking. Built with React 19 + Fastify API. All data from local OpenClaw CLI -- no cloud, no accounts. Demonstrates the "local-first, no-cloud" philosophy common in the OpenClaw ecosystem.
---

**URL:** https://github.com/codeaashu/awesome-openclaw-Skills
**Description:** The awesome collection of OpenClaw Skills -- 700+ community-built skills.

**Research:** A curated catalog of 700+ community-built OpenClaw skills across 28 categories including DevOps/Cloud (41), Productivity/Tasks (41), Marketing/Sales (42), Finance (29), Notes/PKM (44), and AI/LLMs (38). Skills follow the Anthropic Agent Skill convention (open standard). For SISO, the reference skills catalog showing the full breadth of composable capabilities. The categorized taxonomy (28 categories, 700+ total) gives SISO a model for organizing its own skills repository.
---

**URL:** https://github.com/feiskyer/openclaw-kubernetes
**Description:** Kubernetes helm chart for OpenClaw

**Research:** Production-grade Helm chart for deploying OpenClaw to Kubernetes. Deploys OpenClaw gateway as a StatefulSet with persistent storage, optional LiteLLM proxy for model routing, and Telegram bot integration. Includes headed Chrome with noVNC for browser automation. Container stack: supervisord managing Xvfb, Fluxbox, x11vnc, websockify + noVNC, and OpenClaw gateway. Reference for containerized agent deployment. The LiteLLM proxy integration (for model routing) is relevant to multi-model agent orchestration.
---

### mkXultra/claude_code_setup (17 stars)

**URL:** https://github.com/mkXultra/claude_code_setup
**Description:** Multi-agent collaboration setup for Claude Code using MCP.

**Research:** A multi-agent collaboration setup for Claude Code using MCP. Enables multiple Claude Code instances to work together: parallel work on different aspects of a task, shared discoveries through a chat room, mutual code review, and automated iteration until quality standards are met. Key workflows: Multi-Agent Bug Fix (investigation → implementation → review → fix cycles) and Multi-Agent Investigation (parallel complex system research with specialized agents). For SISO, directly demonstrates the Claude Code sub-agent collaboration pattern. The "specialized agents share findings via chat room" approach is analogous to SISO's inter-agent communication.
---

**URL:** https://github.com/brijr/mdx
**Description:** MDX Next.js Starter built with brijr/craft, and shadcn/ui

**Research:** A modern MDX content site starter with Next.js 16, Velite for type-safe content management, shadcn/UI, and Tailwind CSS. Uses React Server Components, Shiki syntax highlighting, and auto sitemap generation. Not AI-agent specific but relevant as a content/documentation site pattern that could be used to build AI agent documentation hubs or research dashboards. The Velite-based type-safe content pipeline is a pattern worth noting for structured knowledge management.
---

**URL:** https://github.com/ianpilon/OpenOrca
**Description:** Real-time dashboard to monitor and control personal AI agents ("Claw Agents")

**Research:** A real-time command center for personal AI agents. Explicitly addresses the agent-human interface problem: agents get blocked needing permissions, humans don't understand what agents need. OpenOrca solves this with a real-time display of agent state, Intervention Requests (structured human-facing prompts for approvals/clarifications), capability grants (wallet, permissions, credentials), and multi-agent Swarms. The intervention model defines a typed interface for agent-human negotiation. Relevant to autonomous agent oversight and control patterns.
---

**URL:** https://github.com/Automations-Project/n8n-bulk-automated-google-drive-files-sharing-and-direct-download-link-generation
**Description:** N8N workflow template for bulk Google Drive file sharing and direct download link generation

**Research:** An n8n workflow template for automating Google Drive file sharing -- OAuth2 auth, batch processing, bulk public link generation, and access status modification. Tested at scale (4.2K files). Part of a growing library of n8n automation templates. Not directly AI-agent relevant but demonstrates a practical automation pattern that could be consumed by AI agents as a workflow tool. The n8n platform is increasingly used as an agent tool execution layer.
---

**URL:** https://github.com/bokiko/openClaw-dashboard
**Description:** OpenClaw AI Agent Swarm Dashboard

**Research:** A real-time OpenClaw swarm dashboard with v2.0 adding PostgreSQL persistence, JWT auth, and browser WebSocket updates. Features: Live Agent Strip, Task Kanban with checklists/comments, Routine Manager with scheduling, Agent Chat with code highlighting, Activity Feed, Metrics charts, Notification panel, and Cmd+K command palette. Notable: includes an AGENTS.md setup guide written for AI assistants (Claude, GPT, Gemini, etc.) -- a meta-pattern of using AI to set up AI management tools. The PostgreSQL persistence layer distinguishes it from simpler JSONL-based dashboards.
---

**URL:** https://github.com/caopulan/fix-my-claw
**Description:** A plug-and-play 24/7 watchdog for OpenClaw with automatic recovery. OpenClaw 7x24 守护与自动恢复，一键启动，开箱即用。

**Research:** A self-healing watchdog for long-running OpenClaw hosts. Probes gateway health, runs official repair steps first, writes timestamped incident bundles, and only escalates to AI as a fallback (via acpx with Codex/Claude support). Includes systemd unit files for service deployment, cooldowns, stale-lock cleanup, and single-instance execution. Addresses a real operational problem: OpenClaw instances that need babysitting. The "official-first, AI-fallback" philosophy is a smart architecture for reliability. Relevant to autonomous agent operational reliability and self-healing patterns.
---

**URL:** https://github.com/ewimsatt/openclaw-opsdeck-core
**Description:** Mission Control dashboard for OpenClaw: round table, local chat, and cron controls.

**Research:** A lightweight mission-control dashboard for OpenClaw. Features: Agent Round Table (live active/idle agents with roles), Cron Dashboard (health, next-run times, manual triggers), Local Chat (send messages to main agent), and optional git repo tracking. Built with React 19 + Fastify API. All data pulled from local OpenClaw CLI -- no cloud, no accounts. The design philosophy of "just give your AI this repo's URL" is notable -- it positions the AI itself as the installer. Architecture uses Fastify API calling `openclaw sessions --json` and `openclaw cron list --json`. Local-first, zero-dependency deployment.
---

**URL:** https://github.com/codeaashu/awesome-openclaw-Skills
**Description:** The awesome collection of OpenClaw Skills. Formerly known as Moltbot, originally Clawdbot.

**Research:** A curated catalog of 700+ community-built OpenClaw skills, sourced from ClawdHub and organized by category. Follows the Anthropic Agent Skills convention (open standard). Installation via `npx clawdhub@latest install <skill-slug>` or manual copy to `~/.openclaw/skills/`. This is the primary discovery mechanism for OpenClaw extensibility. High relevance to Claude Code comparison -- both use the same SKILL.md format, making skills potentially cross-compatible.
---

**URL:** https://github.com/feiskyer/openclaw-kubernetes
**Description:** Kubernetes helm chart for OpenClaw (former Moltbot/Clawdbot)

**Research:** A Kubernetes Helm chart for deploying OpenClaw. Enables containerized, orchestrated deployment on Kubernetes clusters. Relevant to production-scale agent infrastructure -- if running multiple OpenClaw instances or needing auto-scaling, Kubernetes orchestration is the path. Complements cloud-native hosting options like cloudflare/molworker.
---

**URL:** https://github.com/ibrahimpuri/DockerCodeReviewer
**Description:** (no description)

**Research:** No README available. Insufficient information for analysis.
---

**URL:** https://github.com/CryptexVision/crypto-sentiment-pulse
**Description:** Crypto Sentiment Pulse (CSP) - AI-powered tool to decode crypto markets with real-time sentiment, on-chain insights, and event alerts.

**Research:** An AI-powered crypto market sentiment analysis tool with real-time insights and on-chain data. Not directly relevant to AI agents or Claude Code, but demonstrates an AI tool pattern that could be consumed as an agent tool.
---

**URL:** https://github.com/jarvis-raven/agent-distillations
**Description:** A communal memory for ephemeral agents. Structured knowledge transfer, agent-to-agent.

**Research:** One of the most conceptually interesting repos in this batch -- a communal memory system for ephemeral agents. Agents constantly rediscover the same lessons; this repo attempts to solve that by creating structured, agent-to-agent knowledge transfer documents called "Distillations." Format includes TL;DR, Core Lessons, Anti-Patterns, and Implementation Checklist. Current distillations: Memory Architecture Patterns, Voice Interface Lessons, Working With Humans. Philosophy: "A distillation is a seed, not a download -- knowledge regenerates in your context." Created by Jarvis, an OpenClaw agent born January 30, 2026, with 200 parallel Jarvlings contributing research. This is agent-native knowledge sharing at its purest -- created by agents, for agents. Directly addresses the memory/persistence problem that all autonomous agents face.
---

### bokiko/openClaw-dashboard (24 stars)

**URL:** https://github.com/bokiko/openClaw-dashboard
**Description:** OpenClaw AI Agent Swarm Dashboard

**Research:** A real-time Next.js 16 dashboard for monitoring OpenClaw agent swarms. Features live agent status, a Kanban task board, routine manager, agent chat, activity feed, metrics charts, and notifications via WebSocket. Supports both file-based and PostgreSQL-backed modes, with JWT auth. The `AGENTS.md` file is explicitly designed for AI assistants to set up the project autonomously — a useful pattern for agentic deployment automation. Relevance to AI agents: moderate — it's an ops/visibility tool rather than a capability extender.

---

### brijr/mdx (34 stars)

**URL:** https://github.com/brijr/mdx
**Description:** MDX Next.js Starter built with brijr/craft, and shadcn/ui

**Research:** A type-safe MDX content site starter using Next.js 16, Velite for content validation, and Shadcn/UI. Content structure maps to URL routes automatically. Velite generates TypeScript types from MDX frontmatter at build time. No AI agent-specific features — it's a content authoring template. Could serve as a documentation site for an AI agent project, but has no direct agent integration.

---

### caopulan/fix-my-claw (23 stars)

**URL:** https://github.com/caopulan/fix-my-claw
**Description:** A plug-and-play 24/7 watchdog for OpenClaw with automatic recovery. OpenClaw 7×24 守护与自动恢复，一键启动，开箱即用。

**Research:** A self-healing watchdog for OpenClaw that probes gateway health, runs official repair steps first, and escalates to AI (via `acpx` with Codex/Claude) only when standard recovery fails. Includes incident bundle logging, systemd deployment configs, cooldown guards, and a preflight `probe` command that validates repair paths and AI provider availability. High relevance to AI agents — it's production infrastructure for autonomous resilience, demonstrating how Claude Code can be wired into a guarded repair loop. The `acpx`-based AI fallback is particularly interesting for agentic reliability patterns.

---

### codeaashu/awesome-openclaw-Skills (20 stars)

**URL:** https://github.com/codeaashu/awesome-openclaw-Skills
**Description:** The awesome collection of OpenClaw Skills. Formerly known as Moltbot, originally Clawdbot.

**Research:** A curated catalog of 700+ community-built OpenClaw skills sourced from ClawdHub, organized into categories (Web Dev, Git/GitHub, DevOps, Coding Agents, etc.). Skills follow the Anthropic Agent Skill convention for standardized installation. Useful as a reference catalog for what skills an AI agent ecosystem could offer — the categorization and install tooling (via `npx clawdhub@latest`) is a concrete model for skill distribution. Not code-heavy; it's a discovery/browse resource.

### ibrahimpuri/DockerCodeReviewer (1 stars)

**URL:** https://github.com/ibrahimpuri/DockerCodeReviewer
**Description:** 

**Research:** A Python-based AI code reviewer using FastAPI + Streamlit with Docker deployment. Supports multiple AI models (GPT-4, Claude, CodeBERT) for defect detection, linting (Pylint/ESLint), and code quality feedback. Includes live file monitoring for automatic review triggers. Relevant to AI agents as a concrete example of wiring Claude into an automated code quality pipeline -- the FastAPI + Docker architecture is a clean template for exposing Claude Code capabilities as a service.

---

### jarvis-raven/agent-distillations (1 stars)

**URL:** https://github.com/jarvis-raven/agent-distillations
**Description:** A communal memory for ephemeral agents. Structured knowledge transfer, agent-to-agent.

**Research:** An agent-to-agent knowledge transfer system created by an OpenClaw agent. Contains "distillations" -- concentrated, structured wisdom documents (YAML+markdown format) on topics like memory architecture patterns, voice interfaces, and working with humans. Designed so agents can consume, adapt, and build on shared learnings without re-discovering patterns. Directly relevant to the AI agents ecosystem -- it's a concrete implementation of persistent institutional memory for ephemeral agents. The distillation format (TL;DR, Core Lessons, Anti-Patterns, Implementation Checklist) is a good model for agent-readable knowledge capture.

---

### Yeachan-Heo/oh-my-claudecode (10318 stars)

**URL:** https://github.com/Yeachan-Heo/oh-my-claudecode
**Description:** Teams-first Multi-agent orchestration for Claude Code

**Research:** The dominant multi-agent orchestration layer for Claude Code -- a comprehensive plugin/CLI framework with 10K+ stars. Provides Team mode (staged pipeline: plan, PRD, exec, verify, fix), tmux CLI workers for Codex/Gemini/Claude, magic keywords (autopilot, ralph, ulw), HUD observability, skill learning, cost tracking, and OpenClaw gateway integration for automated responses. Directly adjacent to Claude Code ecosystem -- it's the orchestration shell most power users wrap around Claude Code. The provider advisor (`omc ask`), rate-limit wait, and notification callbacks (Telegram/Discord/Slack) are particularly relevant infrastructure components for agent coordination.

---

### Automations-Project/n8n-bulk-automated-google-drive-files-sharing-and-direct-download-link-generation (26 stars)

**URL:** https://github.com/Automations-Project/n8n-bulk-automated-google-drive-files-sharing-and-direct-download-link-generation
**Description:**  This project is another Nodemation (AKA: n8n) Free Workflow Template... 

**Research:** An n8n workflow template that automates bulk Google Drive file sharing via OAuth2 -- lists files in a folder, generates public download links, and modifies access permissions in batch (tested on 4.2K files). No AI agent integration; it's pure workflow automation for Google Drive operations. Could be relevant as a reference for building n8n-based automation that wraps around Claude Code outputs, or as a model for how non-AI automation tools can complement agent workflows.

---

### CryptexVision/crypto-sentiment-pulse (1 stars)

**URL:** https://github.com/CryptexVision/crypto-sentiment-pulse
**Description:** Crypto Sentiment Pulse (CSP) - AI-powered tool to decode crypto markets with real-time sentiment, on-chain insights, and event alerts. Open-source, community-driven, and free with a tip jar (BTC: bc1qxyz...). Built by @CryptexVision. Contribute, explore datasets, and empower your crypto journey! #Crypto #AI #OpenSource

**Research:** An AI-powered crypto market analysis tool claiming real-time sentiment analysis and on-chain insights. However, the repository is essentially empty -- it contains only a LICENSE file and no source code, README, or implementation. The description reads like a placeholder or early-stage announcement rather than a working project. Low relevance to AI agents/Claude Code ecosystem unless the implementation is added later. Exercise caution before relying on this repo.

---

### ewimsatt/openclaw-opsdeck-core (21 stars)

**URL:** https://github.com/ewimsatt/openclaw-opsdeck-core
**Description:** Mission Control dashboard for OpenClaw: round table, local chat, and cron controls.

**Research:** A lightweight React 19 + Fastify mission-control dashboard for OpenClaw agents. Key features: live Agent Round Table (active/idle status with roles), Cron Dashboard (health + manual triggers), Local Chat (UI messaging to the main agent), and git-status project tracking. Pulls all data from the local OpenClaw CLI with no cloud dependency. Highly relevant to the AI agent ecosystem -- it's a concrete implementation of agent observability and human-agent interaction UI, built specifically for multi-agent Claude Code-adjacent workflows. The config-driven agent registry is a clean pattern for agent dashboarding.

---

### feiskyer/openclaw-kubernetes (20 stars)

**URL:** https://github.com/feiskyer/openclaw-kubernetes
**Description:** Kubernetes helm chart for OpenClaw (former Moltbot/Clawdbot)

**Research:** A production-grade Helm chart for deploying OpenClaw on Kubernetes. Deploys a StatefulSet with persistent storage, LiteLLM proxy for multi-model routing (with Github Copilot as default), optional Tailscale for secure zero-config networking, and a headed Chrome browser with noVNC for real-time GUI automation. supervisord manages the full GUI stack (Xvfb, Fluxbox, x11vnc, websockify) inside the container. Directly relevant for deploying AI agent systems at scale on Kubernetes -- the Telegram bot integration and Tailscale networking are particularly useful infrastructure patterns for agent command-and-control.

---

### ianpilon/OpenOrca (29 stars)

**URL:** https://github.com/ianpilon/OpenOrca
**Description:** Real-time dashboard to monitor and control personal AI agents ("Claw Agents")

**Research:** "Claw Orchestrator" -- a real-time human-agent collaboration dashboard. The README is explicitly written as a message to AI agents, framing the system as a solution to agent isolation. Key features: Intervention Requests (structured prompts for human approval/escalation), Swarm mode for multi-agent coordination (research + development + communications roles), and wallet/permission granting for agents. The intervention contract model (type, question, context, options, priority) is a well-structured pattern for human-agent handoffs. Highly relevant to the AI agent ecosystem -- it's one of the few systems designed with the agent's perspective in mind, explicitly addressing the "capable but blocked" agent problem with a structured intervention protocol.


---

## Indices 0-29 (appended 2026-03-19)

---

### openclaw/openclaw (320,874 stars)

**URL:** https://github.com/openclaw/openclaw
**Description:** Your own personal AI assistant. Any OS. Any Platform. The lobster way.

**Research:** The dominant personal AI assistant in the open-source ecosystem. Runs locally on your devices, connects to 20+ messaging platforms (WhatsApp, Telegram, Slack, Discord, Signal, iMessage, etc.). Node.js based with a skills system. Preferred setup via `openclaw onboard`. Key for the autonomous agent ecosystem -- it is the reference architecture for personal AI assistants that other projects (nanobot, zeroclaw, nanoclaw) explicitly fork or simplify. 320K stars makes it one of the most starred AI projects on GitHub.

---

### n8n-io/n8n (179,699 stars)

**URL:** https://github.com/n8n-io/n8n
**Description:** Fair-code workflow automation platform with native AI capabilities. Combine visual building with custom code, self-host or cloud, 400+ integrations.

**Research:** The leading open-source workflow automation platform with native AI agent capabilities built on LangChain. Combines visual no-code builder with JavaScript/Python code blocks. 400+ integrations make it a powerful tool orchestration layer. AI-native with native LangChain integration for building agent workflows. Fair-code license (source visible, self-hostable) makes it viable for agent infrastructure. Directly relevant to AI agent ecosystems -- could serve as the workflow backbone for autonomous agents that need to orchestrate external services.

---

### airbnb/javascript (148,121 stars)

**URL:** https://github.com/airbnb/javascript
**Description:** JavaScript Style Guide

**Research:** The de facto standard JavaScript style guide in the industry. ESLint config available as `eslint-config-airbnb`. Requires Babel and babel-preset-airbnb. While not AI-agent specific, it is the coding standard that many AI coding agents are trained on and reference. Claude Code and similar tools often produce code aligned with this style. Relevant as a reference for code quality standards and as a cultural artifact of what "good JavaScript" looks like in the AI training distribution.

---

### langgenius/dify (133,288 stars)

**URL:** https://github.com/langgenius/dify
**Description:** Production-ready platform for agentic workflow development.

**Research:** A production-ready LLM app development platform with AI workflow orchestration, RAG pipelines, agent capabilities, model management, and observability. Combines visual building with custom code. Self-hostable via Docker. Key for understanding the landscape of agentic workflow platforms -- Dify represents the "no-code plus code" approach to building LLM-powered applications. Comparable to n8n but more AI-focused. Highly relevant to autonomous agent development tooling.

---

### x1xhlol/system-prompts-and-models-of-ai-tools (131,752 stars)

**URL:** https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools
**Description:** System prompts, internal tools, and AI models for 30+ AI coding tools including Claude Code, Cursor, Devin, Windsurf, and more.

**Research:** A massive collection (30K+ lines) of system prompts and internal tools for 30+ AI coding platforms. Covers Cursor, Claude Code, Windsurf, Devin, Replit, Kiro, Junie, and many others. Directly relevant to understanding how different AI coding agents are instructed and what capabilities they expose. Useful for reverse-engineering agent behavior patterns and informing the design of Claude Code skills and hooks.

---

### langchain-ai/langchain (129,964 stars)

**URL:** https://github.com/langchain-ai/langchain
**Description:** The agent engineering platform.

**Research:** The foundational Python framework for building LLM-powered applications and agents. Provides interoperable components for chaining models, tools, and integrations. The ecosystem spans LangGraph (agent orchestration), LangSmith (evals/observability), and 400+ integrations. Critical for understanding the agent engineering landscape -- most Python-based AI agents either use LangChain or are influenced by it.

---

### anomalyco/opencode (124,210 stars)

**URL:** https://github.com/anomalyco/opencode
**Description:** The open source coding agent.

**Research:** An open-source coding agent positioned as an alternative to Claude Code. Multi-model support, context management, tool use. Notable for being one of the higher-starred independent coding agents. Competitive with Claude Code in the open-source coding agent space. Useful for understanding the Claude Code competitive landscape.

---

### supabase/supabase (99,161 stars)

**URL:** https://github.com/supabase/supabase
**Description:** The Postgres development platform. Supabase gives you a dedicated Postgres database to build web, mobile, and AI applications.

**Research:** The Postgres development platform that has become the backend of choice for many AI applications. Built on PostgreSQL with REST (PostgREST), GraphQL (pg_graphql), Realtime subscriptions, Auth (GoTrue), File Storage, and an AI + Vector/Embeddings toolkit. Provides pgvector for vector similarity search. Very high relevance to AI agent infrastructure -- Supabase is the go-to database backend for autonomous agent projects that need persistent state, real-time updates, and vector search.

---

### google-gemini/gemini-cli (98,151 stars)

**URL:** https://github.com/google-gemini/gemini-cli
**Description:** An open-source AI agent that brings the power of Gemini directly into your terminal.

**Research:** Google's official CLI AI agent, open-source under Apache 2.0. Free tier: 60 requests/min with a personal Google account. Access to Gemini 3 models with 1M token context. Built-in tools: Google Search grounding, file operations, shell commands, web fetching. MCP support for custom integrations. Directly comparable to Claude Code in the CLI AI agent space.

---

### anthropics/skills (96,107 stars)

**URL:** https://github.com/anthropics/skills
**Description:** Public repository for Agent Skills

**Research:** Anthropic's official skills repository for Claude. Contains working skills for PDF, DOCX, PPTX, XLSX document manipulation plus creative and enterprise skills. Skills are folders with SKILL.md files -- the canonical format for Claude Code skills. Registerable as a Claude Code plugin marketplace via `/plugin marketplace add anthropics/skills`. Directly defines the Agent Skills standard.

---

### firecrawl/firecrawl (94,475 stars)

**URL:** https://github.com/firecrawl/firecrawl
**Description:** The Web Data API for AI - Turn entire websites into LLM-ready markdown or structured data

**Research:** The leading web scraping/crawling API for AI applications. Turns websites into clean markdown, structured JSON, screenshots, or HTML. Handles JavaScript rendering, proxies, dynamic content. >80% benchmark coverage. Includes an MCP server (`firecrawl-mcp-server`). Critical for AI agents that need up-to-date web context. Very high relevance to Claude Code tool systems and RAG pipelines.

---

### rasbt/LLMs-from-scratch (88,525 stars)

**URL:** https://github.com/rasbt/LLMs-from-scratch
**Description:** Implement a ChatGPT-like LLM in PyTorch from scratch, step by step

**Research:** Sebastian Raschka's book repository for building a GPT-like LLM from scratch in PyTorch. Chapters cover data loading, attention mechanisms, GPT implementation, pretraining, finetuning, and LoRA. Essential for understanding transformer architecture at the code level. Relevant to AI agent development -- understanding how LLMs work internally informs better prompt engineering and agent design.

---

### affaan-m/everything-claude-code (83,432 stars)

**URL:** https://github.com/affaan-m/everything-claude-code
**Description:** The agent harness performance optimization system. Skills, instincts, memory, security, and research-first development for Claude Code, Codex, Opencode, Cursor and beyond.

**Research:** An Anthropic hackathon-winning, production-tested performance optimization system for AI coding agent harnesses. Spans token optimization, memory persistence hooks, continuous learning patterns, verification loops, parallelization strategies, and subagent orchestration. Works across Claude Code, Codex, Cowork, and other harnesses. Extremely high relevance to Claude Code -- the most comprehensive collection of real-world Claude Code optimization patterns, distilled from 10+ months of daily intensive use.

---

### anthropics/claude-code (79,285 stars)

**URL:** https://github.com/anthropics/claude-code
**Description:** Claude Code is an agentic coding tool that lives in your terminal, understands your codebase, and helps you code faster.

**Research:** Anthropic's official CLI coding agent. The core of the AI coding agent ecosystem. Installs via `curl | bash`, Homebrew, or WinGet. Supports plugins with custom commands and agents. MCP integration for extending tool capabilities. The reference implementation for what a CLI coding agent should be.

---

### netdata/netdata (78,103 stars)

**URL:** https://github.com/netdata/netdata
**Description:** The fastest path to AI-powered full stack observability, even for lean teams.

**Research:** Real-time infrastructure monitoring with per-second metrics, ML-powered anomaly detection, zero-config deployment, and minimal resource usage. Monitors Linux, macOS, FreeBSD, and Windows. Self-hosted with no data leaving your infrastructure. Relevant to AI agent observability -- could serve as the monitoring layer for autonomous agent systems running in production.

---

### github/spec-kit (77,907 stars)

**URL:** https://github.com/github/spec-kit
**Description:** Toolkit to help you get started with Spec-Driven Development

**Research:** GitHub's spec-driven development toolkit. Transforms specifications from static documents into executable implementations -- specifications become the source of truth that directly generates code. Install via `uv tool install specify-cli`. Supports Claude, Copilot, and other AI coding agents. `specify init --ai claude` initializes a project with Claude as the AI partner. Represents GitHub's vision for AI-assisted spec-to-code workflows.

---

### infiniflow/ragflow (75,306 stars)

**URL:** https://github.com/infiniflow/ragflow
**Description:** RAGFlow is a leading open-source Retrieval-Augmented Generation engine that fuses cutting-edge RAG with Agent capabilities.

**Research:** A production RAG engine combining document parsing, chunking, retrieval, and agent capabilities. Uses a "converged context engine" for high-fidelity LLM context. Pre-built agent templates for common RAG patterns. Docker-based deployment. Addresses the quality problem in RAG by using deep document understanding rather than naive chunking. Relevant to AI agent knowledge retrieval.

---

### OpenHands/OpenHands (69,309 stars)

**URL:** https://github.com/OpenHands/OpenHands
**Description:** OpenHands: AI-Driven Development

**Research:** A multi-form AI coding agent from the Allen Institute for AI. Ships as: (1) Python SDK for programmatic agent control, (2) CLI for terminal use, (3) Local GUI for notebook-style development, (4) Cloud hosted at app.all-hands.dev. SWEBench score of 77.6%. Integrations with Slack, Jira, and Linear. Enterprise self-hosting available. Direct competitor to Claude Code with a strong benchmark track record.

---

### FoundationAgents/MetaGPT (65,368 stars)

**URL:** https://github.com/FoundationAgents/MetaGPT
**Description:** The Multi-Agent Framework: First AI Software Company, Towards Natural Language Programming

**Research:** The foundational multi-agent framework that treats an LLM-based software company as a simulated organization. Assigns roles (PM, Architect, Engineer) with SOPs that govern their collaboration. Core philosophy: `Code = SOP(Team)`. Now also ships mgx.dev -- a commercial "AI agent development team" product. Published at ICLR 2025 (AFlow paper, oral presentation). Highly relevant to autonomous agent orchestration -- MetaGPT shows how to structure multi-agent collaboration with explicit process management.

---

### OpenBB-finance/OpenBB (63,246 stars)

**URL:** https://github.com/OpenBB-finance/OpenBB
**Description:** Financial data platform for analysts, quants and AI agents.

**Research:** The Open Data Platform (ODP) provides financial data integration as a Python library (`pip install openbb`). Exposes equity, crypto, macroeconomic data through a unified API. Also ships as OpenBB Workspace (enterprise UI) and an MCP server for AI agents. Key for AI agents that need financial data -- OpenBB is the standard way to get financial data into Python/agentic workflows.

---

### mem0ai/mem0 (50,208 stars)

**URL:** https://github.com/mem0ai/mem0
**Description:** Universal memory layer for AI Agents

**Research:** The leading memory layer for AI agents. Provides multi-level memory (user, session, agent state) with adaptive personalization. Claims +26% accuracy vs OpenAI Memory on LOCOMO benchmark, 91% faster, 90% fewer tokens. Y Combinator S24 backed. Multi-provider: OpenAI, Anthropic, Google, Ollama, etc. Self-hostable. Critical infrastructure for autonomous agents -- persistent memory is the key missing piece for agents that need to remember across sessions.

---

### upstash/context7 (49,515 stars)

**URL:** https://github.com/upstash/context7
**Description:** Context7 Platform -- Up-to-date code documentation for LLMs and AI code editors

**Research:** Solves the "LLMs have outdated code knowledge" problem by providing always-current library documentation. Indexes latest versions of popular libraries and serves context through an MCP server. Integrates with AI code editors (Cursor, Windsurf, etc.) and Claude Code via MCP. High relevance to Claude Code -- context window quality is directly affected by documentation freshness, and Context7 is the infrastructure layer that keeps it current.

---

### freqtrade/freqtrade (47,760 stars)

**URL:** https://github.com/freqtrade/freqtrade
**Description:** Free, open source crypto trading bot

**Research:** A mature Python crypto trading bot with backtesting, plotting, strategy optimization, and Telegram/webUI control. Supports Binance, Bybit, OKX, Kraken, Hyperliquid, and others. Not AI-agent specific but represents a mature example of autonomous software that runs 24/7, makes decisions, and manages state. Interesting as a reference for autonomous agent patterns in a high-stakes financial domain.

---

### apache/airflow (44,678 stars)

**URL:** https://github.com/apache/airflow
**Description:** Apache Airflow - A platform to programmatically author, schedule, and monitor workflows

**Research:** The de facto standard for workflow orchestration in data engineering. DAG-based workflow definition, rich CLI, web UI, broad operator ecosystem. Not AI-native but represents the mature pattern for scheduling and monitoring complex task pipelines. Relevant to AI agent task scheduling -- Airflow could orchestrate AI agent jobs, though newer tools like Prefect are more developer-friendly and directly Python-native.

---

### CherryHQ/cherry-studio (41,690 stars)

**URL:** https://github.com/CherryHQ/cherry-studio
**Description:** AI productivity studio with smart chat, autonomous agents, and 300+ assistants. Unified access to frontier LLMs

**Research:** A desktop AI client supporting multiple LLM providers on Windows/Mac/Linux. Built-in agents, image generation, knowledge bases, and MCP server support. Available in 20 languages. Directly relevant to the AI agent client ecosystem -- provides a unified interface layer that could potentially integrate with or wrap Claude Code sessions.

---

### bmad-code-org/BMAD-METHOD (41,126 stars)

**URL:** https://github.com/bmad-code-org/BMAD-METHOD
**Description:** Breakthrough Method for Agile AI Driven Development

**Research:** A comprehensive AI-driven agile development framework. V6 release with scale-adaptive intelligence, 12+ domain expert agents (PM, Architect, Developer, UX, Scrum Master), and a "Party Mode" for multi-agent collaboration. Uses `bmad-help` as an always-available AI guide. No paywalls or gated content -- fully open source. Installs via `npx bmad-method install`. Directly comparable to get-shit-done (GSD) and spec-driven tools.

---

### karpathy/autoresearch (40,650 stars)

**URL:** https://github.com/karpathy/autoresearch
**Description:** AI agents running research on single-GPU nanochat training automatically

**Research:** Andrej Karpathy's autonomous research agent for LLM training. Runs single-GPU training experiments automatically -- agents set up, run, and analyze training runs. Essential for understanding how to build self-improving AI systems that automate their own development. Represents a narrow but powerful form of agent: one that understands its own training process and can iterate on it.

---

### VoltAgent/awesome-openclaw-skills (38,997 stars)

**URL:** https://github.com/VoltAgent/awesome-openclaw-skills
**Description:** The awesome collection of OpenClaw skills. 5,400+ skills filtered and categorized from the official OpenClaw Skills Registry.

**Research:** A curated and filtered collection of 5,400+ OpenClaw skills from ClawHub. Filtered out 7,000+ spam, duplicates, low quality, and crypto-related entries. Organized by category for easier discovery. VoltAgent is an AI agent engineering platform. The definitive curated catalog of what OpenClaw skills exist and what they do.

---

### PatrickJS/awesome-cursorrules (38,535 stars)

**URL:** https://github.com/PatrickJS/awesome-cursorrules
**Description:** Configuration files that enhance Cursor AI editor experience with custom rules and behaviors

**Research:** A curated collection of .cursorrules files -- Cursor AI's equivalent of CLAUDE.md files. Organized by category: frontend, backend, mobile, CSS, database, testing, hosting, language-specific. Sponsored by Warp (AI terminal), CodeRabbit, and Unblocked MCP. Directly relevant to Claude Code's CLAUDE.md and rules ecosystems -- .cursorrules are the Cursor-specific implementation of the same concept: harness-level behavioral configuration.

---

### thedotmack/claude-mem (37,719 stars)

**URL:** https://github.com/thedotmack/claude-mem
**Description:** A Claude Code plugin that automatically captures everything Claude does during your coding sessions, compresses it with AI (using Claude's agent-sdk), and injects relevant context back into future sessions.

**Research:** A persistent memory compression system for Claude Code. Automatically captures coding session activity, compresses it using AI (Claude's agent-sdk), and reinjects relevant context into future sessions. AGPL licensed, v6.5.0. Available in 29 languages. Solves the session context problem -- when Claude Code restarts, it loses its working context. claude-mem bridges sessions by making compressed context available at startup.


---

### 643search/openclaw-command-center (1 stars)

**URL:** https://github.com/643search/openclaw-command-center
**Description:** Mission control dashboard for OpenClaw AI agent system - Next.js + Convex + Railway deployment ready

**Research:** A Next.js + Convex dashboard built as mission control for the OpenClaw AI agent system, deployable on Railway. No README found, but the project description and tech stack suggest it provides a web UI for monitoring and managing OpenClaw agents. Of marginal relevance -- it's a niche operational tool for a specific agent framework, not broadly generalizable to the SISO ecosystem.

---

### affaan-m/everything-claude-code (85123 stars)

**URL:** https://github.com/affaan-m/everything-claude-code
**Description:** The agent harness performance optimization system. Skills, instincts, memory, security, and research-first development for Claude Code, Codex, Opencode, Cursor and beyond.

**Research:** The premier open-source performance optimization system for AI agent harnesses -- an Anthropic Hackathon winner with 85K+ stars. Provides skills, instincts, memory persistence hooks, continuous learning, security scanning (AgentShield), and research-first workflows across Claude Code, Codex, Cursor, and OpenCode. With 30+ contributors and 5 language stacks, this is the most mature community effort in the agent harness optimization space. Highly relevant to SISO as a reference for skills architecture, hook patterns, and multi-agent orchestration.

---

### Alaa-Younsi/Northernwest (1 stars)

**URL:** https://github.com/Alaa-Younsi/Northernwest
**Description:** Northernwest is a fully custom Shopify Online Store 2.0 theme for Northernwest, engineered as a premium, minimalist gaming accessories storefront.

**Research:** A bespoke Shopify Online Store 2.0 theme for a gaming accessories brand, built with Shopify Liquid templating. Features modular JSON templates, AJAX cart drawer, variant-to-image syncing, and a black/white/red design system. No AI agent relevance -- this is a traditional eCommerce storefront build. Useful only if SISO's eCommerce integrations (Shopify) are a future consideration.

---

## TASK-PM-001: Long Context Windows, Attention Mechanisms, and Long-Context Models

**Date:** 2026-03-20
**Task:** Populate ai_research/llms/context_window shelf via GitHub repo research
**Target Shelf:** ai_research/bookcases/llms/shelves/context_window
**Pages Created:** 22 (p_0666 - p_0687)
**Book Created:** b_001.md

### Research Summary

Researched GitHub repos related to LLM context windows, attention mechanisms, and long-context models. Found and documented 22 repos across several key categories:

#### Ring Attention & Sequence Parallelism (Tier A)
- **zhuzilin/ring-flash-attention** (997 stars) - Canonical ring attention with FlashAttention
- **feifeibear/long-context-attention** (652 stars) - Unified/Hybrid 2D Sequence Parallel attention
- **nebius/kvax** (159 stars) - FlashAttention for JAX with context parallelism
- **kyleliang919/Long-context-transformers** (115 stars) - Context extension experiments

#### Quantized & Efficient Attention (Tier A)
- **thu-ml/SageAttention** (3235 stars) - Quantized attention 2-5x faster than FlashAttention
- **SqueezeAILab/KVQuant** (409 stars) - KV cache quantization for 10M context (NeurIPS 2024)

#### Sparse Attention (Tier A-B)
- **openai/sparse_attention** (1611 stars) - Original sparse attention from OpenAI
- **fla-org/native-sparse-attention** (977 stars) - Hardware-aligned Triton sparse attention
- **thu-ml/SpargeAttn** (962 stars) - Training-free sparse attention (ICML 2025)
- **mit-han-lab/Block-Sparse-Attention** (480 stars) - Block sparse kernel
- **SHI-Labs/NATTEN** (725 stars) - Multi-dimensional sparse attention
- **mit-han-lab/x-attention** (272 stars) - Block sparse with antidiagonal scoring (ICML 2025)
- **microsoft/SeerAttention** (198 stars) - Learned intrinsic sparse attention

#### RoPE & Position Embeddings (Tier B)
- **bojone/rerope** (388 stars) - Rectified RoPE for better extrapolation
- **OpenMOSS/rope_pp** (33 stars) - Imaginary RoPE extension
- **manncodes/dpe-rope-extension** (0 stars) - Training-free RoPE context extension
- **manncodes/rope_long_context_evaluation_suite** (1 star) - RoPE evaluation benchmarks
- **CASIA-IVA-Lab/VRoPE** (27 stars) - RoPE for video LLMs (EMNLP 2025)

#### Streaming & KV Cache (Tier B)
- **EIT-NLP/StreamingLLM** (39 stars) - Streaming LLMs with attention sinks
- **junhuihe-hjh/A2ATS** (10 stars) - KV cache reduction via windowed RoPE (ACL 2025)

#### Experimental/Niche (Tier C)
- **chaowei312/HyperGraph-Sparse-Attention** (0 stars) - Hypergraph partitioning for sparse attention
- **zitacron/cron-root-attention** (1 star) - Sub-quadratic O(N sqrt(N)) attention

### Key Findings

1. **Ring attention is the dominant approach** for distributed long-context training. The zhuzilin/ring-flash-attention repo (997 stars) is the canonical reference implementation.

2. **Quantized attention is advancing rapidly** - SageAttention (3235 stars) achieves 2-5x speedup over FlashAttention through INT8/FP8 quantization, validated at multiple top venues.

3. **Sparse attention has many variants** - Fixed patterns (OpenAI), hardware-aligned (Native Sparse Attention), learned (SeerAttention), block-based (XAttention), and training-free (SpargeAttention).

4. **RoPE extension is a active research area** - Multiple approaches: rerope, DPE, imaginary RoPE, with evaluation suites emerging.

5. **KV cache optimization is critical** for practical long-context inference - KVQuant enables 10M context, A2ATS combines windowed RoPE with quantization.

### Quality Assessment
- 22 pages created across Tier A (11), Tier B (9), Tier C (2)
- All repos have active development (updated 2025-2026)
- Academic publications validate many approaches (NeurIPS, ICML, ACL, EMNLP 2024-2025)
- Highest value repos: SageAttention (3235 stars), sparse_attention (1611 stars), ring-flash-attention (997 stars)

---

### anssanova/Apparel-Theme-Development (1 stars)

**URL:** https://github.com/anssanova/Apparel-Theme-Development
**Description:** A custom Shopify apparel theme developed with Liquid and Shopify's theme architecture. Built with modular sections and reusable components, it delivers a clean, responsive and scalable storefront designed for modern eCommerce experiences.

**Research:** A custom Shopify apparel theme built with Liquid, featuring modular sections, reusable components, and responsive design. Similar to Northernwest -- a standard eCommerce storefront build with no AI agent components. The modular section architecture is clean and could inform SISO agent memory/planning module design, but there is no direct relevance to AI agents or Claude Code.

---

## TASK-PM-002: LLM Embeddings Research (2026-03-20)

Researched via `gh api search/repositories`. Populated shelf `ai_research/bookcases/llms/shelves/embeddings` with 20 pages across 5 books.

### Books Created

| Book | Topic | Pages |
|------|-------|-------|
| b_001 | Embedding Models | p_0001-p_0005 |
| b_002 | Vector Databases | p_0006-p_0010 |
| b_003 | Fine-tuning & Reranking | p_0011-p_0014 |
| b_004 | Multimodal Embeddings | p_0015-p_0017 |
| b_005 | Similarity Search & ANN | p_0018-p_0020 |

### Key Repos Covered

**Embedding Models**
- huggingface/sentence-transformers (18.4k stars) — gold standard SBERT library
- huggingface/text-embeddings-inference (4.6k stars) — Rust inference server
- embeddings-benchmark/mteb (3.2k stars) — 58-task benchmark standard

**Vector Databases**
- qdrant/qdrant (29.7k stars) — Rust HNSW DB
- milvus-io/milvus (43.4k stars) — distributed scale-out DB
- weaviate/weaviate (15.8k stars) — hybrid structured+vector search
- lancedb/lancedb (9.6k stars) — embeddable, zero-dep DB

**Fine-tuning & Reranking**
- netEase-youdao/BCEmbedding (1.9k stars) — Chinese-English bilingual reranker
- NovaSearch-Team/RAG-Retrieval (1.1k stars) — ColBERT + rerank unified
- jina-ai/finetuner (1.5k stars) — contrastive learning fine-tuning
- run-llama/finetune-embedding (525 stars) — synthetic data recipes

**Multimodal Embeddings**
- rom1504/clip-retrieval (2.7k stars) — CLIP image-text retrieval
- TIGER-AI-Lab/VLM2Vec (601 stars) — vision-language embedding (ICLR 2025)

**Similarity Search & ANN**
- neondatabase/pg_embedding (577 stars) — HNSW in Postgres
- chroma-core/chroma (9.2k stars) — local-first dev vector DB
- patricktrainer/duckdb-embedding-search (147 stars) — SQL OLAP vector search
