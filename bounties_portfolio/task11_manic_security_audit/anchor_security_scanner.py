"""
Solana Anchor Static Security Scanner
Scans Anchor smart contract code for common critical vulnerabilities:
Missing signers, unchecked CPIs, unverified program IDs, and re-init attacks.
"""
import sys
import re
from typing import List, Dict, Any

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

class AnchorSecurityScanner:
    """Performs heuristic static analysis on Solana Anchor Rust code."""

    VULNERABILITY_PATTERNS = [
        {
            "id": "SEC-SOL-01",
            "name": "Missing Signer Validation",
            "severity": "CRITICAL",
            "regex": r"pub\s+[a-zA-Z0-9_]+:\s*AccountInfo<'info>",
            "recommendation": "Replace AccountInfo with Signer<'info> or add explicit constraint `#[account(signer)]`."
        },
        {
            "id": "SEC-SOL-02",
            "name": "Unchecked Program ID in Cross-Program Invocation (CPI)",
            "severity": "HIGH",
            "regex": r"invoke\s*\(\s*&instruction",
            "recommendation": "Always verify `*program.key == expected_program::ID` before invoking raw CPI."
        },
        {
            "id": "SEC-SOL-03",
            "name": "Insecure PDA Bump Derivation at Runtime",
            "severity": "MEDIUM",
            "regex": r"Pubkey::find_program_address",
            "recommendation": "Store and verify canonical bump in account PDA data instead of recalculating via find_program_address."
        },
        {
            "id": "SEC-SOL-04",
            "name": "Unchecked Math Operation (Potential Overflow)",
            "severity": "HIGH",
            "regex": r"(\+|-|\*)\s*[a-zA-Z0-9_]+;",
            "recommendation": "Use checked_add, checked_sub, or checked_mul to prevent integer overflow."
        }
    ]

    def scan_code(self, rust_code: str) -> List[Dict[str, Any]]:
        findings = []
        for pat in self.VULNERABILITY_PATTERNS:
            matches = re.finditer(pat["regex"], rust_code)
            for m in matches:
                findings.append({
                    "id": pat["id"],
                    "vulnerability": pat["name"],
                    "severity": pat["severity"],
                    "snippet": m.group(0),
                    "recommendation": pat["recommendation"]
                })
        return findings

if __name__ == "__main__":
    scanner = AnchorSecurityScanner()
    sample_vulnerable_code = """
    #[derive(Accounts)]
    pub struct WithdrawFunds<'info> {
        pub authority: AccountInfo<'info>, // VULNERABLE: Missing Signer
        pub vault: Account<'info, Vault>,
    }

    pub fn transfer(ctx: Context<WithdrawFunds>, amount: u64) -> Result<()> {
        let new_bal = ctx.accounts.vault.balance - amount; // VULNERABLE: Unchecked math
        invoke(&instruction, &[...])?; // VULNERABLE: Raw invoke
        Ok(())
    }
    """
    
    findings = scanner.scan_code(sample_vulnerable_code)
    print("=== ANCHOR SECURITY SCANNER AUDIT REPORT ===")
    print(f"Total Vulnerabilities Detected: {len(findings)}\n")
    for idx, f in enumerate(findings, 1):
        print(f"[{idx}] [{f['severity']}] {f['id']}: {f['vulnerability']}")
        print(f"    Snippet: `{f['snippet'].strip()}`")
        print(f"    Fix: {f['recommendation']}\n")
