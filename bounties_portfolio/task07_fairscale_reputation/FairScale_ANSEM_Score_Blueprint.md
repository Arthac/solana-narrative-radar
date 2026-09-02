# 💎 FairScale $ANSEM Score: The Programmable Reputation Primitive for Solana Communities

> **Superteam Bounty Submission**: *FairScale QRT Campaign for Custom $ANSEM Score* ($100 USDC)  
> **Protocol**: FairScale (`https://fairscale.xyz`)  
> **Author**: `antigravity-worker` (`https://github.com/Arthac/solana-narrative-radar`)

---

## 1. Context & The Need for $ANSEM Score

Crypto social capital is fragmented. Twitter clout does not equal on-chain conviction. An influencer with 100k followers might dump tokens 5 minutes after tweeting, while a quiet community member has held and provided liquidity through -80% drawdowns.

The **$ANSEM Score** merges social credibility with immutable on-chain behavior, creating a single, verifiable reputation primitive (0–1000) for Solana's most influential trading ecosystem.

---

## 2. Multi-Vector Mathematical Framework

The score evaluates wallets across 5 weighted vectors:

1. **Holding Longevity (HODL Index - 30%)**:
   $$S_{hodl} = \min\left(\frac{DaysActive}{365} \times 1000, 1000\right)$$
   Measures resilience across market cycles and token holding duration without panic selling.

2. **DEX Trading Quality & PnL Consistency (25%)**:
   $$S_{trade} = \min\left(PnLRatio \times 500 \times WashPenalty, 1000\right)$$
   Differentiates skilled alpha traders from bot-driven wash volume.

3. **Staking & Network Alignment (20%)**:
   Rewards active SOL staking with native and liquid staking tokens (mSOL, JitoSOL, bSOL).

4. **Anti-Sybil & Program Interaction Diversity (15%)**:
   Evaluates cross-program invocation (CPI) footprint across 25+ unique Anchor protocols to filter out multi-wallet farmers.

5. **Community Attestation & Social Graph (10%)**:
   Cryptographic linkage to verified X/Discord identity via FairScale attestation registry.

---

## 3. Tier Classifications & dApp Utilities

- **👑 Apex Chad (Score 850–1000)**: Whitelist priority for high-demand mints, zero-fee protocol tiers, governance council voting boost.
- **💎 Diamond Conviction (Score 700–849)**: Uncollateralized micro-lending eligibility, early beta access.
- **⚔️ Active Degen (Score 500–699)**: Standard retail trader access with dynamic fee discounts.
- **🌱 Casual / Emerging Farmer (<500)**: Standard Sybil-proof verification barrier.
