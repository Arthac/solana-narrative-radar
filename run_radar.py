"""
Solana Narrative Radar & Idea Generator - CLI Execution Interface
Allows running the analytical agent directly from the command line,
generating instant terminal summaries and JSON / Markdown exports.
"""
import sys
import argparse
import json

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from core.config import FORTNIGHT_PERIOD
from core.collector import SignalCollector
from core.detector import NarrativeDetector
from core.ideator import IdeaSynthesizer
from core.report import ReportGenerator

def main():
    parser = argparse.ArgumentParser(description="Solana Ecosystem Narrative Radar & Idea Generator")
    parser.add_argument("--export-md", type=str, default="Solana_Fortnight_Report.md", help="Export report to markdown file")
    parser.add_argument("--export-json", type=str, default="", help="Export telemetry to JSON file")
    parser.add_argument("--w-onchain", type=float, default=0.35, help="Weight for On-Chain Activity")
    parser.add_argument("--w-dev", type=float, default=0.35, help="Weight for Developer Activity")
    parser.add_argument("--w-social", type=float, default=0.30, help="Weight for Social / Research Signals")
    parser.add_argument("--alpha-vel", type=float, default=0.25, help="Velocity boost multiplier")
    args = parser.parse_args()

    print("=" * 70)
    print("🔭 SOLANA NARRATIVE RADAR & STARTUP IDEA GENERATOR (CLI AGENT)")
    print(f"📅 Fortnight: {FORTNIGHT_PERIOD}")
    print("=" * 70)

    # Ingest & Evaluate
    detector = NarrativeDetector(alpha_velocity=args.alpha_vel)
    custom_w = {"onchain": args.w_onchain, "dev": args.w_dev, "social": args.w_social}
    
    print("\n[+] Ingesting multi-source signals (Onchain, GitHub, KOL feeds)...")
    rankings = detector.detect_and_rank_all(custom_weights=custom_w)
    
    print("\n[+] FORTNIGHT NARRATIVE RANKINGS:")
    print("-" * 70)
    print(f"{'Rank':<5} | {'Narrative':<35} | {'Score':<7} | {'Velocity':<10} | {'Status'}")
    print("-" * 70)
    for r in rankings:
        print(f"#{r['rank']:<4} | {r['name'][:35]:<35} | {r['composite_score']:<7} | +{r['signals']['velocity_14d_pct']}%{'':<5} | {r['badge']}")

    # Ideator
    ideator = IdeaSynthesizer()
    ideas = ideator.get_all_ideas()
    print("\n" + "=" * 70)
    print(f"💡 SYNTHESIZED STARTUP BUILD BLUEPRINTS ({len(ideas)} Ideas)")
    print("=" * 70)
    for idx, idea in enumerate(ideas, 1):
        print(f"\n[Idea #{idx}] {idea['title']}")
        print(f"  Narrative : {idea['narrative_name']}")
        print(f"  Tagline   : {idea['tagline']}")
        print(f"  Program   : {idea['solana_architecture']['program_type']}")
        print(f"  Primitives: {', '.join(idea['solana_architecture']['solana_primitives'][:2])}")

    # Export Report
    if args.export_md:
        reporter = ReportGenerator()
        briefing = reporter.generate_markdown_briefing()
        with open(args.export_md, "w", encoding="utf-8") as f:
            f.write(briefing)
        print(f"\n[✓] Exported complete markdown briefing to: {args.export_md}")

    if args.export_json:
        summary = detector.get_fortnight_summary()
        with open(args.export_json, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)
        print(f"[✓] Exported telemetry JSON to: {args.export_json}")

    print("\n[✓] Execution completed successfully.\n")

if __name__ == "__main__":
    main()
