"""
Algorithmic Narrative Detection and Signal Ranking Engine for Solana.
Applies multi-factor weighting, 14-day velocity multipliers, and novelty indices.
"""
from typing import Dict, List, Any
from core.config import CORE_NARRATIVES
from core.collector import SignalCollector

class NarrativeDetector:
    """
    Computes Composite Narrative Signal Score (CNSS) and generates
    explainability breakdowns for emerging Solana ecosystem narratives.
    """

    def __init__(self, alpha_velocity: float = 0.25):
        self.collector = SignalCollector()
        self.alpha_velocity = alpha_velocity

    def evaluate_narrative(self, key: str, telemetry: Dict[str, Any], weights: Dict[str, float]) -> Dict[str, Any]:
        """
        Calculates the normalized composite score and classification for a single narrative.
        """
        cfg = CORE_NARRATIVES.get(key, {})
        name = cfg.get("name", key)
        category = cfg.get("category", "General")
        description = cfg.get("description", "")
        key_kols = cfg.get("key_kols", [])
        anchors = cfg.get("ecosystem_anchors", [])

        onchain = telemetry.get("onchain_score", 50.0)
        dev = telemetry.get("dev_score", 50.0)
        social = telemetry.get("social_score", 50.0)
        velocity = telemetry.get("velocity_14d_pct", 0.0)
        novelty = telemetry.get("novelty_index", 50.0)
        metrics = telemetry.get("metrics", {})
        catalysts = telemetry.get("key_catalysts", [])

        dev_weight = weights.get("dev", weights.get("developer", 0.33))
        onchain_weight = weights.get("onchain", 0.34)
        social_weight = weights.get("social", 0.33)

        # 1. Base Weighted Score
        base_score = (
            onchain_weight * onchain +
            dev_weight * dev +
            social_weight * social
        )

        # 2. Velocity Multiplier: rewarding accelerating momentum
        velocity_factor = 1.0 + self.alpha_velocity * min(velocity / 100.0, 1.0)

        # 3. Novelty Coefficient: favoring early emerging signals over legacy saturated themes
        novelty_multiplier = 0.85 + 0.15 * (novelty / 100.0)

        # 4. Composite Narrative Signal Score (CNSS)
        composite_score = round(min(base_score * velocity_factor * novelty_multiplier, 100.0), 2)

        # 5. Narrative Lifecycle Classification
        if composite_score >= 88.0 and velocity >= 45.0:
            lifecycle = "EXPLOSIVE_BREAKOUT"
            badge = "🔥 Explosive Breakout"
        elif composite_score >= 80.0:
            lifecycle = "HIGH_ACCELERATION"
            badge = "⚡ High Acceleration"
        elif novelty >= 85.0 and composite_score >= 70.0:
            lifecycle = "EMERGING_FRONTIER"
            badge = "🌱 Emerging Frontier"
        else:
            lifecycle = "ESTABLISHED_SCALE"
            badge = "🧱 Established Scale"

        return {
            "key": key,
            "name": name,
            "category": category,
            "description": description,
            "composite_score": composite_score,
            "lifecycle": lifecycle,
            "badge": badge,
            "signals": {
                "onchain_score": onchain,
                "dev_score": dev,
                "social_score": social,
                "velocity_14d_pct": velocity,
                "novelty_index": novelty
            },
            "metrics": metrics,
            "catalysts": catalysts,
            "key_kols": key_kols,
            "ecosystem_anchors": anchors
        }

    def detect_and_rank_all(self, custom_weights: Dict[str, float] = None) -> List[Dict[str, Any]]:
        """
        Gathers all telemetry and ranks all narratives in descending order of CNSS score.
        """
        raw_data = self.collector.collect_all()
        telemetry_map = raw_data["narratives"]

        evaluated_narratives = []
        for key, tel in telemetry_map.items():
            cfg = CORE_NARRATIVES.get(key, {})
            weights = custom_weights or cfg.get("base_weight", {"onchain": 0.34, "dev": 0.33, "social": 0.33})
            evaluated = self.evaluate_narrative(key, tel, weights)
            evaluated_narratives.append(evaluated)

        # Sort descending by composite score
        ranked = sorted(evaluated_narratives, key=lambda x: x["composite_score"], reverse=True)
        for idx, item in enumerate(ranked):
            item["rank"] = idx + 1

        return ranked

    def get_fortnight_summary(self) -> Dict[str, Any]:
        """Provides high-level macro summary for the current fortnight."""
        ranked = self.detect_and_rank_all()
        top_narrative = ranked[0] if ranked else None
        
        return {
            "top_narrative": top_narrative["name"] if top_narrative else "None",
            "top_score": top_narrative["composite_score"] if top_narrative else 0.0,
            "total_tracked": len(ranked),
            "fastest_velocity": max(ranked, key=lambda x: x["signals"]["velocity_14d_pct"]) if ranked else None,
            "highest_novelty": max(ranked, key=lambda x: x["signals"]["novelty_index"]) if ranked else None,
            "rankings": ranked
        }
