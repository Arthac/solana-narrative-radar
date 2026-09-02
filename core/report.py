"""
Fortnightly Solana Intelligence Briefing Generator.
Formats narrative rankings, catalysts, and startup ideas into comprehensive reports.
"""
from typing import Dict, Any
from core.config import FORTNIGHT_PERIOD
from core.detector import NarrativeDetector
from core.ideator import IdeaSynthesizer

class ReportGenerator:
    """Generates formatted executive intelligence reports."""

    def __init__(self):
        self.detector = NarrativeDetector()
        self.ideator = IdeaSynthesizer()

    def generate_markdown_briefing(self) -> str:
        """Generates an institutional-grade markdown briefing."""
        summary = self.detector.get_fortnight_summary()
        ideas = self.ideator.get_all_ideas()

        md = f"""# 🔭 Solana Ecosystem Fortnightly Narrative & Build Briefing
**Period**: {FORTNIGHT_PERIOD}  
**Ecosystem**: Solana (Mainnet-Beta / SVM Ecosystem)  
**Methodology**: Composite Narrative Signal Score (CNSS: Onchain 35% | Dev 35% | Social 30% × 14d Velocity × Novelty)

---

## 1. Executive Summary & Macro Signals
- **Leading Ecosystem Narrative**: **{summary['top_narrative']}** (CNSS Score: **{summary['top_score']}/100**)
- **Fastest Accelerating Vector**: **{summary['fastest_velocity']['name']}** (+{summary['fastest_velocity']['signals']['velocity_14d_pct']}% 14-day velocity)
- **Highest Novelty Frontier**: **{summary['highest_novelty']['name']}** (Novelty Index: {summary['highest_novelty']['signals']['novelty_index']}/100)
- **Macro State**: Strong divergence from legacy DeFi toward **agentic micropayments (x402)**, **unbundled social execution (Blinks)**, and **hardware-attested DePIN 2.0**.

---

## 2. Fortnight Narrative Ranking Matrix

| Rank | Narrative | Lifecycle | CNSS Score | 14d Velocity | Onchain | Dev | Social | Novelty |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
"""
        for item in summary["rankings"]:
            s = item["signals"]
            md += f"| #{item['rank']} | **{item['name']}** | {item['badge']} | **{item['composite_score']}** | +{s['velocity_14d_pct']}% | {s['onchain_score']} | {s['dev_score']} | {s['social_score']} | {s['novelty_index']} |\n"

        md += "\n---\n\n## 3. Deep Narrative Diagnostics & Fortnight Catalysts\n\n"

        for item in summary["rankings"]:
            md += f"### #{item['rank']} {item['name']} ({item['badge']})\n"
            md += f"- **Category**: `{item['category']}`\n"
            md += f"- **Overview**: {item['description']}\n"
            md += f"- **Key On-Chain & Dev Metrics**:\n"
            for k, v in item["metrics"].items():
                label = k.replace("_", " ").title()
                md += f"  - **{label}**: `{v}`\n"
            md += f"- **Fortnight Catalysts (Why Now?)**:\n"
            for c in item["catalysts"]:
                md += f"  - {c}\n"
            md += f"- **Key KOL Voices**: {', '.join(item['key_kols'])}\n"
            md += f"- **Ecosystem Anchors**: {', '.join(item['ecosystem_anchors'])}\n\n"

        md += "---\n\n## 4. Top 5 Actionable Startup Build Blueprints\n\n"

        for idx, idea in enumerate(ideas, 1):
            arch = idea["solana_architecture"]
            md += f"### Build Idea #{idx}: {idea['title']}\n"
            md += f"**Tagline**: *{idea['tagline']}*\n\n"
            md += f"- **Target Narrative**: `{idea['narrative_name']}`\n"
            md += f"- **Target Market**: {idea['target_market']}\n"
            md += f"- **The Problem**: {idea['problem']}\n"
            md += f"- **The Solution**: {idea['solution']}\n\n"
            md += f"#### Solana Technical Architecture:\n"
            md += f"- **Framework / Runtime**: `{arch['program_type']}`\n"
            md += f"- **Accounts & PDAs**:\n"
            for acc in arch["account_schema"]:
                md += f"  - `{acc}`\n"
            md += f"- **Solana Primitives**:\n"
            for prim in arch["solana_primitives"]:
                md += f"  - {prim}\n"
            md += f"- **Off-Chain Infrastructure**: {arch['offchain_stack']}\n\n"
            md += f"#### Business Model & Unit Economics:\n{idea['business_model']}\n\n"
            md += f"#### 90-Day MVP Execution Plan:\n"
            for step in idea["mvp_90_day_scope"]:
                md += f"- {step}\n"
            md += "\n---\n\n"

        md += """## 5. Methodology & Signal Attribution
- **Data Ingestion**: Multi-vector stream combining DeFiLlama TVL/DEX APIs, Solana RPC cluster telemetry, GitHub Anchor & Actions repository velocity, and curated KOL sentiment.
- **Score Calculation**: Normalized multi-factor weighted sum boosted by 14-day velocity rate and novelty coefficient to suppress saturated legacy metrics.
- **Reproducibility**: Built with open-source Python and Streamlit. Run `streamlit run app.py` for live interactive analysis.
"""
        return md
