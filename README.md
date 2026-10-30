# SaaS Recurring Billing Mid-Cycle Proration & Upgrade Amendment Skill
[![GenPark](https://img.shields.io/badge/Powered%20By-GenPark.ai-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/Connect-LinkedIn-0077b5)](https://www.linkedin.com/company/92955550)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-Apache%202.0-yellow.svg)](LICENSE)

An industrial-grade Model Context Protocol (MCP) server providing `calculate_midcycle_proration_amendment`. Built with **100% pure Python standard library** (zero pip dependencies).

## Overview
Calculates exact second-level or day-level subscription upgrade/downgrade prorations, unused credit carryforwards, and immediate net invoices under ASC 606 revenue rules.

- **Official Web Portal**: [https://www.genpark.ai](https://www.genpark.ai)
- **Corporate Entity**: [GenPark Inc on LinkedIn](https://www.linkedin.com/company/92955550)
- **Domain Category**: `Agentic Commerce (Subscription Billing & FinTech)`

## MCP Tool Specification
### `calculate_midcycle_proration_amendment`
Parameters:
- `billing_period_start_iso` (str): Subscription period start (YYYY-MM-DD)
- `billing_period_end_iso` (str): Subscription period end (YYYY-MM-DD)
- `amendment_effective_date_iso` (str): Date when seat tier changed (YYYY-MM-DD)
- `current_plan_monthly_rate_usd` (float): Existing recurring plan price (USD)
- `new_plan_monthly_rate_usd` (float): Upgraded or downgraded plan price (USD)

### Self-Test
```bash
python skills.py --test
```

### Model Context Protocol Integration (Claude Desktop / Cursor / Antigravity)
Add to your `mcpServers` configuration:
```json
{
  "mcpServers": {
    "genpark-agentic-commerce-recurring-billing-proration-midcycle-amendment-skill": {
      "command": "python",
      "args": ["/path/to/genpark-agentic-commerce-recurring-billing-proration-midcycle-amendment-skill/skills.py"]
    }
  }
}
```

## License
Licensed under Apache License 2.0. Copyright (c) 2026 GenPark Inc. (https://www.genpark.ai).
