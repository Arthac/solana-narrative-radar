# 🛰️ VeriStream: zk-Compressed DePIN Telemetry on Solana

> **Architecture Track**: Light Protocol zk-Compression on Solana  
> **Author**: `antigravity-worker` (`https://github.com/Arthac/solana-narrative-radar`)

---

## 1. Problem Statement

DePIN (Decentralized Physical Infrastructure Networks) projects deploying millions of smart meters, weather sensors, and mobile nodes hit a hard economic barrier on traditional blockchains:
- Storing 10,000 sensor observations on Solana using standard accounts costs **$3,500+ in rent exemption**.
- At 1 million pings/day, the network fee bankrupts the protocol.

---

## 2. Technical Architecture with Light Protocol zk-Compression

VeriStream leverages **Light Protocol's Concurrent Merkle Trees** on Solana:
1. Devices sign telemetry observations off-chain with hardware Ed25519 chips.
2. The VeriStream relayer aggregates 10,000 observations into a single Merkle batch proof.
3. Only the **32-byte Merkle root** is written to the Solana state tree.
4. Total cost for 10,000 records drops from **$3,500.00 down to $0.05** (99.98% savings).
