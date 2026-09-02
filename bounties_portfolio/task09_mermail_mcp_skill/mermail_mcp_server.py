"""
Mermail Agent Skill - Model Context Protocol (MCP) Server for Solana Agents
Equips AI agents with an autonomous inbox and user-governed Solana Agent Wallet.
"""
import sys
import json
import time
from typing import Dict, List, Any

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

class MermailMCPServer:
    """
    Model Context Protocol (MCP) tool provider for Mermail.
    Supports agent-to-agent inbox messaging and policy-governed wallet execution.
    """

    def __init__(self, agent_pubkey: str = "AgentWallet1111111111111111111111111111111"):
        self.agent_pubkey = agent_pubkey
        self.spending_limit_usd = 50.0 # user-governed policy limit
        self.inbox: List[Dict[str, Any]] = [
            {
                "id": "msg_001",
                "sender": "oracle_feed@mermail.xyz",
                "subject": "Solana Staking Yield Alert",
                "timestamp": int(time.time()) - 3600,
                "read": False,
                "body": "JitoSOL yield increased to 8.2% APR. Rebalancing recommended.",
                "payment_request": None
            },
            {
                "id": "msg_002",
                "sender": "data_provider@mermail.xyz",
                "subject": "DePIN Telemetry Invoice #402",
                "timestamp": int(time.time()) - 1200,
                "read": False,
                "body": "API query fee for 1,000 weather records.",
                "payment_request": {"amount_usdc": 0.25, "recipient": "DataVault9999999999999999999999999999999"}
            }
        ]

    def tool_check_inbox(self, unread_only: bool = True) -> List[Dict[str, Any]]:
        """MCP Tool: Retrieves messages from the agent's dedicated Mermail inbox."""
        if unread_only:
            return [m for m in self.inbox if not m["read"]]
        return self.inbox

    def tool_send_message(self, recipient: str, subject: str, body: str) -> Dict[str, Any]:
        """MCP Tool: Dispatches a cryptographically signed message from the agent."""
        msg_id = f"msg_{int(time.time())}"
        outbound = {
            "id": msg_id,
            "sender": f"{self.agent_pubkey}@mermail.agent",
            "recipient": recipient,
            "subject": subject,
            "body": body,
            "signature": f"sig_ed25519_{hash(body)}",
            "status": "delivered"
        }
        return outbound

    def tool_execute_wallet_payment(self, recipient: str, amount_usdc: float, memo: str) -> Dict[str, Any]:
        """
        MCP Tool: Executes a payment from the agent's self-custody wallet,
        enforcing human-in-the-loop spending caps.
        """
        if amount_usdc > self.spending_limit_usd:
            return {
                "status": "REJECTED_POLICY_VIOLATION",
                "error": f"Amount ${amount_usdc} exceeds autonomous limit of ${self.spending_limit_usd}. Human operator approval required."
            }

        # Simulated on-chain transfer
        tx_hash = f"tx_sol_{int(time.time())}_{abs(hash(memo))}"
        return {
            "status": "CONFIRMED",
            "tx_hash": tx_hash,
            "amount_usdc": amount_usdc,
            "recipient": recipient,
            "sender": self.agent_pubkey,
            "slot": 284102940
        }

if __name__ == "__main__":
    server = MermailMCPServer()
    print("=== MERMAIL MCP AGENT SKILL VERIFICATION ===")
    
    # 1. Check inbox
    unread = server.tool_check_inbox()
    print(f"[✓] Polled inbox: Found {len(unread)} unread messages.")
    for m in unread:
        print(f"  - From: {m['sender']} | Subject: '{m['subject']}'")

    # 2. Process automated micro-payment from message
    inv = unread[1]["payment_request"]
    if inv:
        res = server.tool_execute_wallet_payment(
            recipient=inv["recipient"],
            amount_usdc=inv["amount_usdc"],
            memo="Invoice 402 payment"
        )
        print(f"[✓] Executed Autonomous Payment: Status={res['status']}, Tx={res['tx_hash']}")

    # 3. Test spending limit enforcement
    over_limit = server.tool_execute_wallet_payment(
        recipient="Whale111111111111111111111111111111111",
        amount_usdc=500.0,
        memo="Unauthorized large transfer"
    )
    print(f"[✓] Spending Limit Guard: Status={over_limit['status']}")
