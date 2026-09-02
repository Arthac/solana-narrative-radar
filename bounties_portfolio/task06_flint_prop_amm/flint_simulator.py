"""
Simulation Model: Proprietary AMM vs. Flint Multi-Maker Prop AMM on Solana
Compares capital efficiency, toxic flow slippage (LVR), and execution net yield.
"""
from typing import Dict, List

def simulate_quoting_returns(
    daily_volume: float = 10_000_000, # $10M daily volume
    toxic_flow_pct: float = 0.35,      # 35% MEV/Toxic flow
    maker_capital: float = 2_000_000,  # $2M deployed inventory
    days: int = 30
) -> Dict[str, Dict[str, float]]:
    """
    Simulates 30-day net PnL of:
    1. Custom Proprietary AMM (Solo build, FIFO matching, high fixed infra costs)
    2. Flint Multi-Maker Prop AMM (Shared infra, Pro-Rata matching, aggregator priority)
    """
    # Baseline parameters
    base_spread_bps = 8.0 # 8 bps average capture
    
    # 1. Custom Prop AMM:
    # - Fixed infra overhead: Dedicated RPC ($3k/mo), Geyser nodes ($4k/mo), dev ops ($15k/mo amortized) = $22,000/mo
    # - Toxic flow loss: Under FIFO, high-frequency searchers pick off quotes during stale slots -> 18 bps penalty on toxic flow
    # - Aggregator integration: Requires individual routing maintenance; captures ~45% of potential routing volume
    custom_volume = daily_volume * 0.45
    custom_gross_fees = custom_volume * (base_spread_bps / 10_000) * days
    custom_toxic_loss = custom_volume * toxic_flow_pct * (18.0 / 10_000) * days
    custom_fixed_costs = 22_000
    custom_net_pnl = custom_gross_fees - custom_toxic_loss - custom_fixed_costs
    custom_apr = (custom_net_pnl / maker_capital) * (365 / days) * 100

    # 2. Flint Multi-Maker Prop AMM:
    # - Zero fixed infra costs (Flint manages contracts, Geyser indexers, and RPC clusters)
    # - Pro-Rata Matching: Spreads toxic fill across all makers proportionally, reducing individual pick-off impact by 65%
    # - Native Aggregator Integrations (Jupiter, DFlow, Titan, OKX): Captures 100% of optimal routed volume
    flint_volume = daily_volume * 1.0
    # Maker provides 20% of the aggregate pool
    flint_maker_share = 0.20
    flint_gross_fees = (flint_volume * flint_maker_share) * (base_spread_bps / 10_000) * days
    flint_toxic_loss = (flint_volume * flint_maker_share) * toxic_flow_pct * (6.3 / 10_000) * days
    flint_platform_fee = flint_gross_fees * 0.05 # 5% performance fee
    flint_net_pnl = flint_gross_fees - flint_toxic_loss - flint_platform_fee
    flint_apr = (flint_net_pnl / maker_capital) * (365 / days) * 100

    return {
        "custom_solo_amm": {
            "monthly_volume_routed": round(custom_volume * days, 2),
            "gross_fee_revenue": round(custom_gross_fees, 2),
            "toxic_flow_lvr_loss": round(custom_toxic_loss, 2),
            "fixed_infra_costs": custom_fixed_costs,
            "net_monthly_profit": round(custom_net_pnl, 2),
            "annualized_roi_pct": round(custom_apr, 2)
        },
        "flint_prop_amm": {
            "monthly_volume_routed": round(flint_volume * flint_maker_share * days, 2),
            "gross_fee_revenue": round(flint_gross_fees, 2),
            "toxic_flow_lvr_loss": round(flint_toxic_loss, 2),
            "fixed_infra_costs": 0,
            "net_monthly_profit": round(flint_net_pnl, 2),
            "annualized_roi_pct": round(flint_apr, 2)
        },
        "flint_advantage": {
            "net_profit_multiplier": round(flint_net_pnl / max(custom_net_pnl, 1), 2),
            "toxic_loss_reduction_pct": round((1 - (flint_toxic_loss / custom_toxic_loss)) * 100, 2)
        }
    }

if __name__ == "__main__":
    res = simulate_quoting_returns()
    import pprint
    print("=== FLINT PROP AMM VS CUSTOM AMM SIMULATION RESULTS ===")
    pprint.pprint(res)
