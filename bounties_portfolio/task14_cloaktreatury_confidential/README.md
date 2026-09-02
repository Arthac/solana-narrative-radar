# 🔒 CloakTreasury: Token-2022 Confidential Transfers & Compliance Hook

> **Architecture Track**: Solana Token-2022 Extensions  
> **Author**: `antigravity-worker` (`https://github.com/Arthac/solana-narrative-radar`)

---

## 1. Executive Summary

Institutions require two non-negotiable features before moving treasury capital on-chain:
1. **Commercial Confidentiality**: Competitors cannot see payroll, supplier payments, or inventory purchases on public block explorers.
2. **Regulatory Compliance**: Payments must provably avoid sanctioned entities (OFAC/AML) without revealing underlying balances.

CloakTreasury marries **Token-2022 Confidential Transfers** (Twisted ElGamal encryption with Sigma zero-knowledge proofs) with **SPL Transfer Hook Extensions**.

---

## 2. Transfer Hook Execution Flow

Every transfer triggers the on-chain hook program:
1. `source_account` and `destination_account` are checked against the `ComplianceRegistry` PDA.
2. If clean, the transfer proceeds without decrypting the ElGamal ciphertexts.
3. If flagged, the transaction fails atomically at the SVM level before any tokens move.
