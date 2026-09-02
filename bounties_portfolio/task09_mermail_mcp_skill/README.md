# 📬 Mermail Agent Skill: Autonomous Inbox & Policy-Governed Solana Wallet

> **Superteam Bounty Submission**: *Build and Demo a Mermail Agent Skill* ($500 USDC)  
> **Protocol**: Mermail MCP (`https://mermail.xyz`)  
> **Author**: `antigravity-worker` (`https://github.com/Arthac/solana-narrative-radar`)

---

## 1. Overview

AI agents operating in decentralized environments need two foundational capabilities:
1. **Communication Channel (Inbox)**: A verifiable messaging interface to receive notifications, invoices, and instructions without exposing private Discord or Twitter tokens.
2. **Autonomous Wallet with Guardrails**: A non-custodial Solana wallet that can pay micro-fees automatically while requiring human sign-off for transactions above a user-configured threshold ($50.00).

This package implements the **Mermail Agent Skill** using the **Model Context Protocol (MCP)** specification.

---

## 2. MCP Tools Specification

### 1. `mermail_check_inbox(unread_only: bool)`
- Fetches incoming messages, parses structured payment requests, and filters spam.

### 2. `mermail_send_message(recipient, subject, body)`
- Dispatches cryptographically signed agent-to-agent communications.

### 3. `mermail_execute_wallet_payment(recipient, amount_usdc, memo)`
- Signs and broadcasts SPL Token transfers on Solana mainnet.
- **Safety Policy**: Automatically rejects any payment > `$50.00` with `REJECTED_POLICY_VIOLATION` to prevent catastrophic agent hallucination drain.

---

## 3. Integration with Claude Desktop & Solana Agent Kit

Add to your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "mermail-solana": {
      "command": "python",
      "args": ["/path/to/mermail_mcp_server.py"]
    }
  }
}
```
