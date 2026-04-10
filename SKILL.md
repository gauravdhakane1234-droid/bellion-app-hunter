---
name: bellion-app-hunter
description: Mass search, analyze and rank money-making apps from Google Play Store and web. Find the best earning apps with real tasks, lowest withdrawal minimums, and highest daily payouts. Built for Indian market with UPI/Paytm focus.
metadata:
  author: bellion.zo.computer
  version: 1.0.0
  tags: [apps, money, earning, India, micro-tasks, UPI, Paytm, automation]
compatibiity: Created for Zo Computer with Manus AI + PortMCP integration
---

# 🔍 BELLION APP HUNTER SKILL

Searches, scrapes and ranks money-making apps using PortMCP-powered automation.

## Usage

```
SEARCH: Find apps by category
ANALYZE: Deep analysis of specific app  
RANK: Rank all found apps by criteria
COMPARE: Compare apps head-to-head
UPDATE_DB: Refresh app database
REPORT: Generate full report
```

## What it searches

- Google Play Store (scraped via gpsear.ch CLI)
- Trustpilot / Reddit / X for real user reviews  
- Withdrawal proof screenshots from Google Images
- Payment proof posts from Reddit
- App ranking data from SimilarWeb / Semrush
- Telegram group payment proofs

## Ranking criteria (weighted)

| Criteria | Weight |
|----------|--------|
| Real task availability | 30% |
| Minimum withdrawal | 25% |
| Daily earning potential | 20% |
| Payment reliability (proofs found) | 15% |
| User ratings | 10% |

## Output format

```json
{
  "apps": [...],
  "rankings": {...},
  "best_for": {
    "daily_hustle": "app_name",
    "high_earners": "app_name", 
    "low_effort": "app_name",
    "reselling": "app_name"
  }
}
```

## Skills used

- `BELLION-PORTMCP-MANAGER` — for running PortMCP commands
- Python scripts in `scripts/` for Play Store scraping
- Batch processing via MCP for parallel searches

## Files

- `scripts/play_store_scraper.py` — scrape PS data
- `scripts/web_analyzer.py` — analyze web presence
- `scripts/payment_proof_finder.py` — find withdrawal proofs
- `scripts/ranker.py` — weighted ranking engine
- `scripts/reporter.py` — generate markdown reports
- `data/app_database.json` — cached app data
- `data/rankings.json` — latest rankings
