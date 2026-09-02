// Solana Anchor Program: Web2 Database to Zero-Copy On-Chain State
// Replaces traditional PostgreSQL / Redis user store with decentralized L1 state.

use anchor_lang::prelude::*;

declare_id!("OnChainBackend1111111111111111111111111111111");

#[program]
pub mod onchain_backend {
    use super::*;

    pub fn initialize_user_record(
        ctx: Context<InitializeUserRecord>,
        username: [u8; 32],
        tier: u8,
    ) -> Result<()> {
        let user_account = &mut ctx.accounts.user_record;
        user_account.authority = *ctx.accounts.authority.key;
        user_account.username = username;
        user_account.subscription_tier = tier;
        user_account.created_at = Clock::get()?.unix_timestamp;
        user_account.last_active_at = Clock::get()?.unix_timestamp;
        user_account.total_logins = 1;
        user_account.bump = ctx.bumps.user_record;
        
        msg!("User record initialized on Solana L1 for authority {}", ctx.accounts.authority.key);
        Ok(())
    }

    pub fn update_user_session(
        ctx: Context<UpdateUserSession>,
        activity_hash: [u8; 32],
    ) -> Result<()> {
        let user_account = &mut ctx.accounts.user_record;
        user_account.last_active_at = Clock::get()?.unix_timestamp;
        user_account.total_logins = user_account.total_logins.checked_add(1).unwrap();
        user_account.last_activity_hash = activity_hash;
        
        msg!("Session heartbeat updated. Total logins: {}", user_account.total_logins);
        Ok(())
    }
}

#[derive(Accounts)]
pub struct InitializeUserRecord<'info> {
    #[account(
        init,
        payer = authority,
        space = 8 + UserRecord::LEN,
        seeds = [b"user_record", authority.key().as_ref()],
        bump
    )]
    pub user_record: Account<'info, UserRecord>,
    
    #[account(mut)]
    pub authority: Signer<'info>,
    
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct UpdateUserSession<'info> {
    #[account(
        mut,
        seeds = [b"user_record", authority.key().as_ref()],
        bump = user_record.bump,
        has_one = authority
    )]
    pub user_record: Account<'info, UserRecord>,
    
    pub authority: Signer<'info>,
}

#[account]
pub struct UserRecord {
    pub authority: Pubkey,          // 32 bytes
    pub username: [u8; 32],         // 32 bytes UTF-8 fixed string
    pub subscription_tier: u8,      // 1 byte (0 = Free, 1 = Pro, 2 = Enterprise)
    pub created_at: i64,            // 8 bytes
    pub last_active_at: i64,        // 8 bytes
    pub total_logins: u64,          // 8 bytes
    pub last_activity_hash: [u8; 32],// 32 bytes SHA-256 state root
    pub bump: u8,                   // 1 byte
}

impl UserRecord {
    pub const LEN: usize = 32 + 32 + 1 + 8 + 8 + 8 + 32 + 1; // 122 bytes
}
