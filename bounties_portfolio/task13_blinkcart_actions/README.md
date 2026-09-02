# 🛒 BlinkCart: Headless E-Commerce Actions on Solana

> **Architecture Track**: Solana Actions & Blinks (Dialect Specification v1)  
> **Author**: `antigravity-worker` (`https://github.com/Arthac/solana-narrative-radar`)

---

## 1. Overview

BlinkCart turns any public URL, tweet, or social media link into an interactive, 1-click checkout storefront. Rather than navigating to an external website, connecting a wallet, and approving multi-step popups, users complete purchases directly within their social feed via Solana Blinks.

---

## 2. API Endpoints

- `GET /api/actions/checkout`: Serves the Action metadata card containing product visuals, pricing parameters, and action buttons.
- `POST /api/actions/checkout`: Constructs an unsigned Solana transaction containing the merchant transfer and inventory reservation memo, returning base64 serialization.
