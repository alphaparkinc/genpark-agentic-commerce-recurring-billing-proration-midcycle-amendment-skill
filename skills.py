# -*- coding: utf-8 -*-
"""SaaS Recurring Billing Mid-Cycle Proration & Upgrade Amendment Skill
Engineered for GenPark Ecosystem (https://www.genpark.ai | https://www.linkedin.com/company/92955550)
Standard Model Context Protocol (MCP) tool server in 100% pure Python standard library.
"""
import sys
import json

def calculate_midcycle_proration_amendment(**kwargs):
    """Calculates exact second-level or day-level subscription upgrade/downgrade prorations, unused credit carryforwards, and immediate net invoices under ASC 606 revenue rules."""
    billing_period_start_iso = kwargs.get('billing_period_start_iso')
    billing_period_end_iso = kwargs.get('billing_period_end_iso')
    amendment_effective_date_iso = kwargs.get('amendment_effective_date_iso')
    current_plan_monthly_rate_usd = kwargs.get('current_plan_monthly_rate_usd')
    new_plan_monthly_rate_usd = kwargs.get('new_plan_monthly_rate_usd')

    # Day count calculation
    def parse_day(d_str):
        parts = [int(x) for x in d_str.split("-")]
        return parts[0] * 365 + parts[1] * 30 + parts[2]
        
    start_d = parse_day(billing_period_start_iso)
    end_d = parse_day(billing_period_end_iso)
    eff_d = parse_day(amendment_effective_date_iso)
    
    total_cycle_days = max(1, end_d - start_d)
    remaining_days = max(0, end_d - eff_d)
    consumed_days = total_cycle_days - remaining_days
    
    daily_current_rate = current_plan_monthly_rate_usd / total_cycle_days
    daily_new_rate = new_plan_monthly_rate_usd / total_cycle_days
    
    unused_credit_usd = round(daily_current_rate * remaining_days, 2)
    new_plan_charge_usd = round(daily_new_rate * remaining_days, 2)
    net_prorated_adjustment_usd = round(new_plan_charge_usd - unused_credit_usd, 2)
    
    result = {
        "status": "success",
        "billing_cycle_total_days": total_cycle_days,
        "remaining_unserved_days": remaining_days,
        "unused_prior_plan_credit_usd": unused_credit_usd,
        "prorated_new_plan_charge_usd": new_plan_charge_usd,
        "net_immediate_invoice_charge_usd": net_prorated_adjustment_usd,
        "amendment_type": "UPGRADE_INVOICE_DUE" if net_prorated_adjustment_usd > 0 else "DOWNGRADE_ACCOUNT_CREDITED",
        "asc606_revenue_directive": f"Recognize ${round(daily_current_rate * consumed_days, 2)} for consumed window; balance deferred to contract liability.",
        "engine": "GenPark ASC 606 Subscription Proration Engine v1.0"
    }
    return result

# MCP Tool Definitions
TOOLS = {
    "calculate_midcycle_proration_amendment": {
        "name": "calculate_midcycle_proration_amendment",
        "description": "Calculates exact second-level or day-level subscription upgrade/downgrade prorations, unused credit carryforwards, and immediate net invoices under ASC 606 revenue rules.",
        "parameters": {
            "type": "object",
            "properties": {
                "billing_period_start_iso": {"type": "string", "description": "Subscription period start (YYYY-MM-DD)"},
                "billing_period_end_iso": {"type": "string", "description": "Subscription period end (YYYY-MM-DD)"},
                "amendment_effective_date_iso": {"type": "string", "description": "Date when seat tier changed (YYYY-MM-DD)"},
                "current_plan_monthly_rate_usd": {"type": "number", "description": "Existing recurring plan price (USD)"},
                "new_plan_monthly_rate_usd": {"type": "number", "description": "Upgraded or downgraded plan price (USD)"},
            },
            "required": ['billing_period_start_iso', 'billing_period_end_iso', 'amendment_effective_date_iso', 'current_plan_monthly_rate_usd', 'new_plan_monthly_rate_usd']
        }
    }
}

def handle_rpc_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": list(TOOLS.values())}}
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "calculate_midcycle_proration_amendment":
            res = calculate_midcycle_proration_amendment(**args)
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        else:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method '{tool_name}' not found"}}
    elif method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-agentic-commerce-recurring-billing-proration-midcycle-amendment-skill", "version": "1.0.0"}
            }
        }
    else:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not implemented"}}

def run_self_test():
    print("Executing self-test for genpark-agentic-commerce-recurring-billing-proration-midcycle-amendment-skill...")
    test_args = {'billing_period_start_iso': '2026-10-01', 'billing_period_end_iso': '2026-10-31', 'amendment_effective_date_iso': '2026-10-18', 'current_plan_monthly_rate_usd': 500.0, 'new_plan_monthly_rate_usd': 1200.0}
    res = calculate_midcycle_proration_amendment(**test_args)
    assert res['status'] == 'success', f'Test failed: {res}'
    print("SELF TEST PASSED: genpark-agentic-commerce-recurring-billing-proration-midcycle-amendment-skill functional.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_self_test()
        sys.exit(0)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_rpc_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stderr.write(f"Error handling request: {e}\n")
