#!/usr/bin/env python3
"""Shared topic routing: maps content signals to library shelves."""
import re
from typing import Optional

# shelf format: section/bookcase/shelf
TOPIC_SHELF_MAP: dict[str, str] = {
    # AI Research - Agents
    "multi_agent": "ai_research/agents/multi_agent",
    "multiagent": "ai_research/agents/multi_agent",
    "agents": "ai_research/agents/multi_agent",
    "agent": "ai_research/agents/multi_agent",
    "autonomous": "ai_research/agents/autonomous",
    "autonomous_agents": "ai_research/agents/autonomous",

    # AI Research - Code Agents
    "code_agent": "ai_research/agents/code_agents",
    "code_agents": "ai_research/agents/code_agents",
    "coding_agent": "ai_research/agents/code_agents",
    "claude_code": "ai_research/agents/code_agents",
    "cursor": "ai_research/agents/code_agents",
    "aider": "ai_research/agents/code_agents",
    "devin": "ai_research/agents/code_agents",
    "swe_agent": "ai_research/agents/code_agents",
    "opencode": "ai_research/agents/code_agents",
    "codex": "ai_research/agents/code_agents",
    "copilot": "ai_research/agents/code_agents",

    # AI Research - LLMs
    "llm": "ai_research/llms/reasoning",
    "llms": "ai_research/llms/reasoning",
    "reasoning": "ai_research/llms/reasoning",
    "chain_of_thought": "ai_research/llms/reasoning",
    "cot": "ai_research/llms/reasoning",
    "o1": "ai_research/llms/reasoning",
    "o3": "ai_research/llms/reasoning",
    "claude": "ai_research/llms/reasoning",
    "gpt": "ai_research/llms/reasoning",
    "gemini": "ai_research/llms/reasoning",
    "context_window": "ai_research/llms/context_window",
    "embeddings": "ai_research/llms/embeddings",

    # AI Research - RAG
    "rag": "ai_research/rag/retrieval",
    "retrieval": "ai_research/rag/retrieval",
    "vector_db": "ai_research/rag/vector_db",
    "vector_search": "ai_research/rag/retrieval",
    "chunking": "ai_research/rag/retrieval",
    "reranking": "ai_research/rag/retrieval",

    # AI Research - Claude Code
    "claude_code_patterns": "ai_research/claude_code/patterns",

    # AI Research - Evals
    "eval": "ai_research/evals/benchmarks",
    "evals": "ai_research/evals/benchmarks",
    "benchmark": "ai_research/evals/benchmarks",
    "benchmarks": "ai_research/evals/benchmarks",
    "evaluation": "ai_research/evals/benchmarks",
    "methodology": "ai_research/evals/methodology",

    # Infrastructure - LLM Serving
    "inference": "infrastructure/llm_serving/inference",
    "llm_serving": "infrastructure/llm_serving/inference",
    "serving": "infrastructure/llm_serving/inference",
    "vllm": "infrastructure/llm_serving/inference",
    "tensorrt": "infrastructure/llm_serving/inference",
    "ollama": "infrastructure/llm_serving/inference",
    "lmstudio": "infrastructure/llm_serving/inference",
    "quantization": "infrastructure/llm_serving/inference",
    "batch_inference": "infrastructure/llm_serving/inference",

    # Infrastructure - DevOps
    "devops": "infrastructure/devops/ci_cd",
    "ci_cd": "infrastructure/devops/ci_cd",
    "github_actions": "infrastructure/devops/ci_cd",
    "gitlab_ci": "infrastructure/devops/ci_cd",
    "jenkins": "infrastructure/devops/ci_cd",
    "containers": "infrastructure/devops/containers",
    "docker": "infrastructure/devops/containers",
    "containerization": "infrastructure/devops/containers",

    # Infrastructure - Kubernetes
    "kubernetes": "infrastructure/kubernetes/patterns",
    "k8s": "infrastructure/kubernetes/patterns",
    "kubectl": "infrastructure/kubernetes/patterns",
    "helm": "infrastructure/kubernetes/patterns",
    "kubeflow": "infrastructure/kubernetes/patterns",

    # Infrastructure - Frontend
    "web_agents": "infrastructure/frontend/web_agents",
    "browser_agent": "infrastructure/frontend/web_agents",
    "browser_agents": "infrastructure/frontend/web_agents",
    "playwright": "infrastructure/frontend/web_agents",
    "automation": "infrastructure/frontend/web_agents",
    "frontend": "infrastructure/frontend/web_agents",
    "ui": "infrastructure/frontend/web_agents",
    "gui": "infrastructure/frontend/web_agents",

    # Ecosystem
    "open_source": "ecosystem/opensource/models",
    "opensource": "ecosystem/opensource/models",
    "open_weights": "ecosystem/opensource/models",
    "llama": "ecosystem/opensource/models",
    "mistral": "ecosystem/opensource/models",
    "anthropic": "ecosystem/anthropic/models",
    "openai": "ecosystem/openai/models",
    "gemini_eco": "ecosystem/opensource/models",

    # Product
    "business": "product/business_automation/automation",
    "automation": "product/business_automation/automation",
    "product": "product/business_automation/automation",
    "saas": "product/business_automation/automation",

    # Discovery - Social
    "twitter": "discovery/social/twitter",
    "x": "discovery/social/twitter",
    "tweet": "discovery/social/twitter",
    "tweets": "discovery/social/twitter",
    "x_com": "discovery/social/twitter",
    "reddit": "discovery/social/reddit",
    "subreddit": "discovery/social/reddit",
    "r_machineLearning": "discovery/social/reddit",
    "hacker_news": "discovery/social/hacker_news",
    "hn": "discovery/social/hacker_news",
    "ycombinator": "discovery/social/hacker_news",

    # Discovery - Web
    "web_search": "discovery/web/search",
    "search_engine": "discovery/web/search",
    "google_search": "discovery/web/search",
    "newsletter": "discovery/web/newsletter",
    "rss": "discovery/web/rss",
    "rss_feed": "discovery/web/rss",
    "atom_feed": "discovery/web/rss",
    "papers": "discovery/web/papers",
    "arxiv": "discovery/web/papers",
    "research_paper": "discovery/web/papers",
    "articles": "discovery/web/articles",
    "article": "discovery/web/articles",
    "blogs": "discovery/web/blogs",
    "blog_post": "discovery/web/blogs",
    "blogging": "discovery/web/blogs",
}

# Keywords per topic for fuzzy detection
TOPIC_KEYWORDS: dict[str, list[str]] = {
    "multi_agent": ["multi-agent", "multi agent", "multiagent", "agentic", "agent orchestration", "agent coordination", "swarm", "crewai", "autogen", "camels"],
    "code_agents": ["coding agent", "code agent", "devin", "claude code", "aider", "cursor", "opencode", "codex cli", "swe-agent", "software engineer agent"],
    "llms": ["large language model", "llm", "gpt", "claude", "gemini", "mistral", "llama", "reasoning", "chain of thought", "thinking model"],
    "rag": ["rag", "retrieval augmented", "vector search", "embeddings", "chunking", "rerank", "pinecone", "weaviate", "chroma"],
    "evals": ["benchmark", "eval", "evaluation", "accuracy", "performance measurement", "human eval", "mmlu", "gpqa"],
    "inference": ["inference", "serving", "vllm", "tensorrt", "ollama", "quantization", "batch inference", "latency", "throughput", "tgi"],
    "devops": ["devops", "ci cd", "github actions", "jenkins", "gitlab ci", "pipeline", "automation", "deployment"],
    "kubernetes": ["kubernetes", "k8s", "kubectl", "helm", "kubeflow", "container orchestration"],
    "web_agents": ["browser agent", "web agent", "playwright", "selenium", "puppeteer", "gui automation", "web automation", "screen use"],
    "opensource": ["open source", "open weights", "llama", "mistral", "phi", "gemma", "qwen", "deepseek"],
    "social_media": ["twitter", "x.com", "tweet", "reddit", "subreddit", "hacker news", "ycombinator", "hn", "social media", "social platform"],
    "web_content": ["web search", "newsletter", "rss feed", "atom feed", "arxiv", "research paper", "article", "blog post", "blogging", "content discovery"],
}

# Tools/frameworks for concept linking
KNOWN_TOOLS = [
    "claude code", "claude-code", "opencode", "codex", "aider", "cursor", "devin",
    "swe-agent", "openclaw", "clawdbot", "cloudbot", "open interpreter",
    "langchain", "langgraph", "llamaindex", "crewai", "autogen", "autogenstudio",
    "vllm", "ollama", "lm studio", "lmstudio", "tensorrt", "tgi", "text generation inference",
    "kubernetes", "k8s", "docker", "github actions", "gitlab ci", "jenkins",
    "playwright", "puppeteer", "selenium", "browserbase",
    "pinecone", "weaviate", "chroma", "qdrant", "milvus",
    "llama", "llama 3", "llama 4", "mistral", "phi", "gemma", "qwen", "deepseek",
    "claude", "claude 3", "claude 4", "gpt-4", "gpt-4o", "gpt-o",
    "react", "next.js", "nextjs", "typescript", "python", "rust", "golang", "go",
    "mcp", "model context protocol", "anthropic mcp",
    "mem0", "memgpt", "open memory",
    "postgres", "postgresql", "redis", "sqlite",
    "aws", "gcp", "azure", "cloudflare",
    "vercel", "netlify", "fly.io",
]


def detect_tags(content: str) -> list[str]:
    """Infer tags from content keywords. Preserves priority order — most specific first."""
    content_lower = content.lower()
    found = []

    # Explicit high-priority checks first (before dict iteration)
    high_priority = [
        ("multi_agent", ["multi-agent", "multi agent", "multiagent", "agentic", "agent orchestration", "swarm"]),
        ("code_agents", ["coding agent", "code agent", "devin", "swe-agent", "swe agent"]),
        ("web_agents", ["browser agent", "web agent", "gui automation"]),
    ]
    for topic, keywords in high_priority:
        for kw in keywords:
            if kw in content_lower:
                found.append(topic)
                break

    # General keyword detection
    skip = {"multi_agent", "code_agents", "web_agents"}  # already handled above
    for topic, keywords in TOPIC_KEYWORDS.items():
        if topic in skip:
            continue
        for kw in keywords:
            if kw in content_lower:
                found.append(topic)
                break

    return found


def route_to_shelf(tags: list[str], title: str = "", content: str = "") -> str:
    """Map detected tags to a library shelf. Returns default shelf if no match."""
    title_lower = title.lower()
    content_lower = content.lower()

    # 1. Title-first priority: title mentions are strongest signal
    title_signals = [
        ("multi_agent", ["multi-agent", "multi agent", "multiagent", "agentic", "agent orchestration", "ai agent"]),
        ("code_agents", ["code agent", "coding agent", "claude code", "opencode", "aider", "cursor"]),
        ("web_agents", ["browser agent", "web agent", "gui automation"]),
        ("kubernetes", ["kubernetes", "k8s", "kubectl"]),
        ("evals", ["eval", "benchmark", "evals"]),
        ("llms", ["llm", "reasoning", "chain of thought", "gpt", "gemini"]),
        ("rag", ["rag", "retrieval augmented"]),
        ("inference", ["inference", "serving", "vllm", "ollama"]),
        ("devops", ["devops", "ci cd", "github actions"]),
    ]
    for topic, keywords in title_signals:
        for kw in keywords:
            if kw in title_lower:
                return TOPIC_SHELF_MAP[topic]

    # 2. Content-based detection (body/summary — more careful with short words)
    content_signals = [
        ("multi_agent", ["multi-agent", "multi agent", "multiagent", "agentic swarm", "agent orchestration"]),
        ("code_agents", ["coding agent", "code agent", "claude code", "opencode", "aider", "devin", "swe-agent"]),
        ("web_agents", ["browser agent", "web agent", "gui automation"]),
        ("kubernetes", ["kubernetes", "k8s", "kubectl", "helm", "kubeflow"]),
        ("evals", ["ai eval", "user acceptance testing", "benchmark", "evals", "performance measurement"]),
        ("inference", ["inference", "serving", "vllm", "ollama", "tensorrt", "quantization", "batch inference"]),
        ("rag", ["retrieval augmented", "vector search", "embedding model", "chunking strategy"]),
        ("devops", ["devops", "ci cd", "github actions", "gitlab ci"]),
        ("llms", ["large language model", "chain of thought", "thinking model"]),
        ("opensource", ["open source", "open-weight", "llama", "mistral", "gemma"]),
    ]
    for topic, keywords in content_signals:
        for kw in keywords:
            if kw in content_lower:
                return TOPIC_SHELF_MAP[topic]

    # 3. Tag-based fallback
    for tag in tags:
        tag_lower = tag.lower()
        if tag_lower in TOPIC_SHELF_MAP:
            return TOPIC_SHELF_MAP[tag_lower]
        if tag_lower.rstrip("s") in TOPIC_SHELF_MAP:
            return TOPIC_SHELF_MAP[tag_lower.rstrip("s")]

    # 4. Keyword scan of combined text
    combined = title_lower + " " + content_lower
    detected = detect_tags(combined)
    for topic in detected:
        if topic in TOPIC_SHELF_MAP:
            return TOPIC_SHELF_MAP[topic]

    # Default: route to inference (largest existing shelf)
    return "infrastructure/llm_serving/inference"


def extract_tools(content: str) -> list[str]:
    """Extract known tool/framework names from content."""
    content_lower = content.lower()
    found = []
    for tool in KNOWN_TOOLS:
        # Use word boundary matching
        pattern = re.escape(tool.lower())
        if re.search(r'\b' + pattern + r'\b', content_lower):
            if tool not in found:
                found.append(tool)
    return found


if __name__ == "__main__":
    # Quick smoke test
    shelf = route_to_shelf(["kubernetes"], "K8s deployment patterns", "Using kubernetes with helm")
    print(f"Tags [kubernetes] -> {shelf}")

    shelf2 = route_to_shelf([], "Claude Code Multi-Agent Orchestration", "multi-agent swarm")
    print(f"Auto [claude code multi-agent] -> {shelf2}")

    tools = extract_tools("Using Claude Code with OpenCode and vllm for inference")
    print(f"Tools found: {tools}")
