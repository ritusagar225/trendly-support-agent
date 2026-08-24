# Trendly Support Agent

An AI-powered customer support agent for Trendly using Gemini function calling and deterministic Python business logic.

## Overview

The Trendly Support Agent handles customer-support queries related to:

- Orders
- Shipping
- Returns
- Exchanges
- Refunds
- Damaged or wrong items
- Lost parcels
- Human-support escalation

Gemini is responsible for understanding customer intent, selecting the appropriate tool, and generating the final response.

Python handles the actual business rules and decisions. This prevents the LLM from independently inventing eligibility, refund, or policy decisions.

---

## Key Features

- Gemini-powered customer support
- Function/tool calling
- Order lookup
- Policy search
- Return eligibility checking
- Exchange eligibility checking
- Human-support escalation
- Deterministic date calculations
- Policy guardrails
- Lost-parcel handling
- Damaged/wrong-item handling
- API error handling
- Automated testing
- 14/14 business-logic tests passing

---

## Architecture

```text
                    Customer
                       |
                       v
                Gemini Agent
                       |
                Tool Selection
                       |
        +--------------+--------------+
        |              |              |
        v              v              v
   get_order()   search_policy()   Eligibility Tools
                                      |
                            +---------+---------+
                            |                   |
                            v                   v
                     Return Tool        Exchange Tool
                            |                   |
                            +---------+---------+
                                      |
                                      v
                               Python Result
                                      |
                                      v
                                Gemini Agent
                                      |
                                      v
                              Customer Response
                                      |
                                      v
                              Human Escalation
                               when required
```

## How It Works

The Trendly Support Agent follows a tool-based workflow where Gemini handles natural-language understanding and Python tools handle deterministic business decisions.

### 1. Customer Sends a Request

The customer sends a natural-language support request.

```text
Customer:
Can I return TR-4530?

2. Gemini Understands the Intent

Gemini analyzes the request and determines what information or action is required.

For a return request, the agent identifies that it needs to:

Retrieve the order
Check return eligibility
3. Gemini Selects the Appropriate Tool

The agent uses function calling to select the required Python tool.

get_order()
     ↓
check_return_eligibility()

The LLM is responsible for selecting the tool, but it does not make the final eligibility decision.


