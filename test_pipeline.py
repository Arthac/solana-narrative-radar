"""
Real verification test for Solana Narrative Radar.
Validates end-to-end data collection, narrative detection, and idea synthesis.
"""
import sys
import json

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
from core.config import CORE_NARRATIVES, FORTNIGHT_PERIOD
from core.collector import SignalCollector
from core.detector import NarrativeDetector
from core.ideator import IdeaSynthesizer
from core.report import ReportGenerator

def test_full_pipeline():
    print("[1/5] Testing SignalCollector...")
    collector = SignalCollector()
    data = collector.collect_all()
    assert "solana_macro" in data, "Missing solana_macro in collector output"
    assert "narratives" in data, "Missing narratives in collector output"
    assert len(data["narratives"]) == len(CORE_NARRATIVES), "Narrative count mismatch"
    print(f" -> Collected {len(data['narratives'])} narratives, Solana TVL: ${data['solana_macro']['tvl']/1e9:.2f}B")

    print("[2/5] Testing NarrativeDetector ranking...")
    detector = NarrativeDetector()
    rankings = detector.detect_and_rank_all()
    assert len(rankings) == len(CORE_NARRATIVES), "Rankings length mismatch"
    assert rankings[0]["composite_score"] >= rankings[1]["composite_score"], "Sorting is not descending"
    for item in rankings:
        assert "rank" in item
        assert "composite_score" in item
        assert "lifecycle" in item
        print(f" -> Rank #{item['rank']}: {item['name']} (CNSS: {item['composite_score']}, {item['badge']})")

    print("[3/5] Testing IdeaSynthesizer...")
    ideator = IdeaSynthesizer()
    ideas = ideator.get_all_ideas()
    assert len(ideas) >= 5, "Fewer than 5 startup build blueprints generated"
    for idea in ideas:
        assert "solana_architecture" in idea
        assert "account_schema" in idea["solana_architecture"]
        assert len(idea["solana_architecture"]["account_schema"]) >= 2
        print(f" -> Validated Idea: '{idea['title']}' for narrative: '{idea['narrative_name']}'")

    print("[4/5] Testing ReportGenerator...")
    reporter = ReportGenerator()
    briefing = reporter.generate_markdown_briefing()
    assert len(briefing) > 1000, "Briefing markdown is too short"
    assert "Solana Ecosystem Fortnightly Narrative & Build Briefing" in briefing
    print(f" -> Generated Briefing ({len(briefing)} characters)")

    print("[5/5] Testing Python syntax compilation for app.py...")
    import py_compile
    py_compile.compile("app.py", doraise=True)
    print(" -> app.py syntax verification passed.")

    print("\n✅ ALL VERIFICATION CHECKS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test_full_pipeline()
