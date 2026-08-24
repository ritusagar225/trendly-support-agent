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
```

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

4. Python Tool Executes the Business Logic

The selected tool receives the required arguments and applies Trendly's business rules.

For example:

check_return_eligibility(
    order_id="TR-4530",
    current_date="2026-08-24"
)

The tool checks conditions such as:

Order exists?
     ↓
Delivered?
     ↓
Within 30-day window?
     ↓
Returnable item?
     ↓
Final sale?
     ↓
Cancelled?
     ↓
Return decision

5. Tool Returns a Structured Result

The Python function returns a structured response instead of free-form text

{
  "eligible": true,
  "action": "return_eligible",
  "order_id": "TR-4530",
  "delivered_date": "2026-07-26",
  "days_since_delivery": 29
}

6. Result Is Passed Back to Gemini

The verified tool result is provided back to Gemini.

Tool Result
     ↓
Gemini
     ↓
Customer-Friendly Response

Gemini uses the result to construct the final response.

7. Customer Receives the Final Response

   Trendly Agent:

Yes, your order TR-4530 is eligible for a return.

It was delivered on July 26, 2026, which is within
Trendly's 30-calendar-day return window.

Human Escalation Flow

Some situations cannot be resolved automatically.

For example, a lost parcel requires human support.

Customer
   |
   v
"What should I do about TR-4526?"
   |
   v
Gemini identifies lost parcel
   |
   v
get_order()
   |
   v
Order marked as lost in transit
   |
   v
escalate_to_human()
   |
   v
Human Support Case Created
   |
   v
Case ID returned
   |
   v
Gemini informs the customer

Example escalation result:

{
  "status": "escalated",
  "case_id": "CASE-602D1914",
  "reason": "lost_parcel",
  "order_id": "TR-4526",
  "assigned_to": "human_support"
}

Why Use Tools?

The agent separates conversation from business logic.

Gemini Handles
Understanding customer requests
Identifying intent
Selecting tools
Generating customer-friendly responses
Python Handles
Order lookup
Policy rules
Return eligibility
Exchange eligibility
Date calculations
Human escalation

This prevents the LLM from independently deciding important business outcomes.

                 Customer
                    |
                    v
              Gemini Agent
                    |
             Tool Selection
                    |
                    v
             Python Tools
                    |
             Business Logic
                    |
                    v
          Structured Result
                    |
                    v
              Gemini Agent
                    |
                    v
          Customer Response

This architecture makes the system more reliable, testable, and easier to extend.


