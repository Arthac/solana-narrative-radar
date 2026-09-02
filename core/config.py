"""
Configuration, constants, and baseline ecosystem definitions for Solana Narrative Radar.
"""
from typing import Dict, List, Any

# Fortnight configuration
FORTNIGHT_PERIOD = "Current Fortnight (Aug 15 - Sep 02, 2026)"
DEFAULT_RPC_URL = "https://api.mainnet-beta.solana.com"
DEFILLAMA_SOLANA_ENDPOINT = "https://api.llama.fi/v2/chains"
DEFILLAMA_DEXS_ENDPOINT = "https://api.llama.fi/overview/dexs/solana"

# Narrative classification and signal seeds
CORE_NARRATIVES: Dict[str, Dict[str, Any]] = {
    "ai_agents_x402": {
        "name": "Autonomous AI Agents & Agentic Micropayments",
        "category": "AI / Autonomous Infrastructure",
        "description": "On-chain autonomous agents utilizing Solana's sub-second finality and sub-cent fees to execute micro-transactions, x402 HTTP-paywall settlements, and cross-agent coordination.",
        "primary_signals": [
            "Surge in program-to-program invocation (CPI) frequency by automated non-custodial signer keys",
            "Adoption of HTTP 402 Payment Required standard with instant Solana Pay settle hooks",
            "Proliferation of agent identity registries and on-chain verifiable compute attestations"
        ],
        "key_kols": ["@mert_", "@aeyakovenko", "@shawmakesmagic", "@sendaifun"],
        "ecosystem_anchors": ["Eliza / ai16z", "SendAI", "Solana Agent Kit (SendAI / LangChain)", "Sphere"],
        "base_weight": {"onchain": 0.35, "developer": 0.35, "social": 0.30}
    },
    "actions_blinks": {
        "name": "Solana Actions & Blinks (Headless On-Chain UX)",
        "category": "Consumer / UX Primitive",
        "description": "Unbundled decentralized application interactions transforming any URL, tweet, or social card into an interactive on-chain transaction execution portal without dApp hopping.",
        "primary_signals": [
            "Over 180+ new public actions registered across Dialect and independent action registries",
            "Spike in non-dApp transaction originations (X/Twitter, Discord embeds, Telegram mini-apps)",
            "Expansion into e-commerce checkout, decentralized voting, and NFT dynamic mints directly inside feeds"
        ],
        "key_kols": ["@shayne_coplan", "@saydialect", "@mert_", "@heabor"],
        "ecosystem_anchors": ["Dialect", "Phantom Blinks", "Backpack Actions", "Jupiter Blinks"],
        "base_weight": {"onchain": 0.30, "developer": 0.40, "social": 0.30}
    },
    "depin_sensors": {
        "name": "DePIN 2.0: Decentralized Edge Compute & Sensor Networks",
        "category": "Hardware / Physical Infrastructure",
        "description": "Second-generation DePIN on Solana moving from mere reward emission to verifiable machine proof-of-work, real enterprise telemetry, decentralized AI inference nodes, and distributed geospatial indexing.",
        "primary_signals": [
            "Record hardware node onboarding rates across decentralized wireless (5G) and dashcam networks",
            "Integration of Solana State Compression (zk-compressed accounts) for millions of device identities",
            "Transition to burn-and-mint equilibrium tokenomics driven by enterprise data buyers"
        ],
        "key_kols": ["@toly", "@akshaybd", "@helium", "@Hivemapper"],
        "ecosystem_anchors": ["Helium", "Hivemapper", "Render Network", "io.net", "Nosana", "Grass"],
        "base_weight": {"onchain": 0.40, "developer": 0.30, "social": 0.30}
    },
    "token2022_fintech": {
        "name": "Token-2022 & Confidential Balances for Institutional Pay",
        "category": "Fintech / Payments",
        "description": "Massive institutional pilot acceleration utilizing Solana Token Extensions (Token-2022): confidential transfers (ElGamal + ZK zero-knowledge proofs), transfer hooks for KYC/AML compliance, and interest-bearing tokens.",
        "primary_signals": [
            "Corporate treasury and merchant adoption of programmable transfer fees and compliance transfer hooks",
            "Growth in privacy-preserving B2B payroll and merchant settlements via ZK confidential balances",
            "Regulatory-compliant yield token issuances by European and Asian fintech entities on Solana"
        ],
        "key_kols": ["@solana", "@austinvirts", "@rajgokal", "@jerallaire"],
        "ecosystem_anchors": ["Solana Pay", "Stripe Solana Integration", "Paxos USDG / PYUSD", "Squads"],
        "base_weight": {"onchain": 0.45, "developer": 0.35, "social": 0.20}
    },
    "svm_execution": {
        "name": "SVM Layer 2s & Dedicated Appchains",
        "category": "Scaling / Modular Architecture",
        "description": "Horizontal scaling of the Solana Virtual Machine (SVM) into dedicated high-throughput appchains, rollup stacks, and customized execution environments anchored to Solana L1.",
        "primary_signals": [
            "Launch of SVM rollup SDKs and shared sequencer testnets settling state roots back to Solana mainnet",
            "Specialized high-frequency trading and gaming studios deploying isolated SVM rollups",
            "Cross-SVM liquidity aggregation mechanisms and zero-latency bridge protocols"
        ],
        "key_kols": ["@anatoly", "@tarunbabu", "@aeyakovenko", "@jump_firedancer"],
        "ecosystem_anchors": ["Eclipse", "Sonic (SVM on TikTok)", "Firedancer client rollouts", "MagicBlock (Ephemerals)"],
        "base_weight": {"onchain": 0.30, "developer": 0.45, "social": 0.25}
    }
}
