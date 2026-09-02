"""
FairScale $ANSEM Score Calculation Engine
Calculates contextual, programmatic on-chain reputation scores for Solana wallets.
"""
import sys
from typing import Dict, Any

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

class AnsemScoreEngine:
    """
    Computes custom $ANSEM reputation score (0 - 1000) based on:
    1. Holding Longevity (HODL Index) - 30%
    2. DEX Trading Quality & PnL Consistency - 25%
    3. Staking & Long-Term Network Alignment - 20%
    4. Anti-Sybil Clustering & Transaction Velocity - 15%
    5. Ecosystem Protocol Diversity - 10%
    """

    def calculate_score(self, telemetry: Dict[str, Any]) -> Dict[str, Any]:
        # Vector 1: Longevity (days held)
        days_active = telemetry.get("wallet_age_days", 30)
        hodl_subscore = min((days_active / 365.0) * 1000, 1000.0)

        # Vector 2: Trading Quality (organic vs wash)
        pnl_ratio = telemetry.get("realized_pnl_ratio", 1.0) # > 1.0 = net profitable
        trade_count = telemetry.get("dex_trade_count", 10)
        wash_penalty = 0.5 if trade_count > 500 and pnl_ratio < 0.9 else 1.0
        trade_subscore = min(pnl_ratio * 500 * wash_penalty, 1000.0)

        # Vector 3: Staking & Network Alignment
        sol_staked = telemetry.get("sol_staked", 0.0)
        stake_subscore = min((sol_staked / 50.0) * 1000, 1000.0)

        # Vector 4: Anti-Sybil (diversity of funding sources)
        unique_cpi_programs = telemetry.get("unique_programs_interacted", 5)
        sybil_subscore = min((unique_cpi_programs / 25.0) * 1000, 1000.0)

        # Vector 5: Community Attestation / Social
        social_verified = telemetry.get("social_link_verified", False)
        social_subscore = 1000.0 if social_verified else 300.0

        # Composite $ANSEM Score
        ansem_score = round(
            0.30 * hodl_subscore +
            0.25 * trade_subscore +
            0.20 * stake_subscore +
            0.15 * sybil_subscore +
            0.10 * social_subscore,
            1
        )

        # Tier Classification
        if ansem_score >= 850:
            tier = "👑 Apex Chad (Top 1%)"
            badge = "APEX_CHAD"
        elif ansem_score >= 700:
            tier = "💎 Diamond Conviction (Top 10%)"
            badge = "DIAMOND_CONVICTION"
        elif ansem_score >= 500:
            tier = "⚔️ Active Degen (Top 30%)"
            badge = "ACTIVE_DEGEN"
        else:
            tier = "🌱 Casual / Emerging Farmer"
            badge = "CASUAL_FARMER"

        return {
            "ansem_score": ansem_score,
            "tier": tier,
            "badge": badge,
            "breakdown": {
                "longevity": round(hodl_subscore, 1),
                "trading_quality": round(trade_subscore, 1),
                "network_alignment": round(stake_subscore, 1),
                "sybil_resistance": round(sybil_subscore, 1),
                "social_attestation": round(social_subscore, 1)
            }
        }

if __name__ == "__main__":
    engine = AnsemScoreEngine()
    mock_wallet = {
        "wallet_age_days": 420,
        "realized_pnl_ratio": 2.4,
        "dex_trade_count": 140,
        "sol_staked": 125.0,
        "unique_programs_interacted": 32,
        "social_link_verified": True
    }
    result = engine.calculate_score(mock_wallet)
    print("=== FAIRSCALE $ANSEM REPUTATION SCORE RESULT ===")
    print(f"Score: {result['ansem_score']} / 1000")
    print(f"Tier: {result['tier']}")
    print("Subscores:", result["breakdown"])
