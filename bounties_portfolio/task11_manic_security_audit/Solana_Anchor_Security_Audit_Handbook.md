# 🛡️ Solana Smart Contract Security Audit & Exploit Prevention Handbook

> **Superteam Bounty Submission**: *$1,000 USDC Manic Bug Bounty*  
> **Target**: Anchor / Native Solana Smart Contract Security  
> **Author**: `antigravity-worker` (`https://github.com/Arthac/solana-narrative-radar`)

---

## 1. Introduction

Unlike EVM contracts where re-entrancy is the dominant vulnerability vector, Solana's execution runtime (Sealevel) introduces unique security paradigms due to its decoupled state model:
1. Programs are stateless code.
2. All mutable data lives inside external `AccountInfo` buffers passed by the client.
3. If an Anchor program fails to validate account ownership, signers, or PDA derivation bumps, attackers can forge account data and drain protocol vaults.

---

## 2. The 5 Most Fatal Solana Vulnerabilities & Proof of Concept

### 1. The Missing Signer Exploit
- **Vulnerability**: Defining an authority account as `AccountInfo<'info>` instead of `Signer<'info>`.
- **Exploit Vector**: An attacker passes the victim's public key as the `authority` parameter in the instruction. Since the program does not verify `is_signer == true`, the contract executes unauthorized withdrawals.
- **Defensive Anchor Pattern**:
  ```rust
  #[derive(Accounts)]
  pub struct AdminAction<'info> {
      pub admin: Signer<'info>, // Guarantees transaction was signed by this key
  }
  ```

### 2. PDA Canonical Bump Confusion
- **Vulnerability**: Calling `Pubkey::find_program_address` during instruction execution rather than verifying stored bump seeds.
- **Exploit Vector**: Attackers pass arbitrary seeds that derive alternative PDAs, bypassing role-based access controls.
- **Defensive Pattern**: Store `bump: u8` in the account struct at initialization and enforce `bump = account.bump` in Anchor account validation macros.

### 3. Arbitrary Cross-Program Invocation (CPI)
- **Vulnerability**: Passing unverified `token_program` accounts in SPL Token transfers.
- **Exploit Vector**: Attacker deploys a malicious mock token program that logs success without transferring tokens, tricking the caller program into releasing goods.
- **Defensive Pattern**: Enforce `#[account(address = anchor_spl::token::ID)]`.
