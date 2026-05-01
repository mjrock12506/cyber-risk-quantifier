"""
ai_advisor.py — AI-powered FAIR input estimator
Sends organization context to Claude, gets back calibrated FAIR ranges.
"""

import json
import anthropic


def estimate_fair_inputs(org_description: str, api_key: str) -> dict:
    """
    Takes a plain-English description of an organization
    and returns estimated FAIR input ranges.
    """
    client = anthropic.Anthropic(api_key=api_key)

    prompt = f"""You are a senior cyber risk analyst using the FAIR 
(Factor Analysis of Information Risk) framework. 

A user has described their organization below. Based on this description, 
estimate realistic FAIR input ranges. Consider their industry, size, 
security maturity, past incidents, and any other relevant factors.

ORGANIZATION DESCRIPTION:
{org_description}

Respond with ONLY valid JSON in this exact format, no other text:
{{
    "tef_low": <number>,
    "tef_mode": <number>,
    "tef_high": <number>,
    "vuln_low": <number between 0 and 1>,
    "vuln_mode": <number between 0 and 1>,
    "vuln_high": <number between 0 and 1>,
    "pl_low": <number in USD>,
    "pl_mode": <number in USD>,
    "pl_high": <number in USD>,
    "slef_low": <number between 0 and 1>,
    "slef_mode": <number between 0 and 1>,
    "slef_high": <number between 0 and 1>,
    "sl_low": <number in USD>,
    "sl_mode": <number in USD>,
    "sl_high": <number in USD>,
    "reasoning": "<2-3 sentence explanation of why you chose these ranges>"
}}

Guidelines for your estimates:
- TEF: Consider industry attack frequency, org size, and public exposure
- Vulnerability: Factor in mentioned security controls (MFA, EDR, training)
- Primary Loss: Scale to org size and industry (healthcare/finance = higher)
- SLEF: Consider regulatory environment (HIPAA, PCI, GDPR)
- Secondary Loss: Scale to potential fines, lawsuits, customer base
- Be realistic, not alarmist. Base estimates on published data like Verizon DBIR."""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    response_text = message.content[0].text
    return json.loads(response_text)