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

How It Works

The agent follows a tool-based workflow.

1. Customer Request

The customer sends a natural-language request.

Customer:
Can I return TR-4530?

2. Gemini Understands the Request

Gemini identifies the customer's intent and selects the appropriate tool.

For example:

get_order()
check_return_eligibility()

3. Python Executes the Tool

The selected Python function applies the actual Trendly business rules.

check_return_eligibility(
order_id="TR-4530",
current_date="2026-08-24"
)

4. Deterministic Result

The tool returns a structured result.

{
"eligible": true,
"action": "return_eligible",
"order_id": "TR-4530",
"days_since_delivery": 29
}

5. Gemini Generates the Response

Gemini converts the tool result into a customer-friendly response.

Yes, your order TR-4530 is eligible for a return.
It was delivered within the 30-day return window.

6. Human Escalation

Requests that require human intervention are passed to the escalation tool.

Customer
|
v
Lost Parcel
|
v
Escalation Tool
|
v
Case Created
|
v
Human Support

Project Structure
trendly-support-agent/
│
├── app/
│ ├── agent.py
│ ├── **init**.py
│ │
│ ├── guardrails/
│ │
│ ├── prompts/
│ │
│ └── tools/
│ ├── orders.py
│ ├── policy.py
│ ├── returns.py
│ ├── exchanges.py
│ ├── escalation.py
│ └── **init**.py
│
├── data/
│ ├── orders.json
│ └── trendly_policy.md
│
├── tests/
│ ├── test_returns.py
│ ├── test_exchanges.py
│ └── test_escalation.py
│
├── .env.example
├── .gitignore
├── pytest.ini
└── README.md

Main Components
Component Purpose
app/agent.py Main Gemini agent and tool-calling workflow
app/tools/orders.py Order lookup
app/tools/policy.py Trendly policy search
app/tools/returns.py Return eligibility
app/tools/exchanges.py Exchange eligibility
app/tools/escalation.py Human-support escalation
data/orders.json Order data
data/trendly_policy.md Trendly policy
tests/ Automated business-logic tests
.env.example Environment-variable template
.gitignore Protects secrets and generated files
Tools
get_order()

Retrieves order information using an order ID.

It is used for questions involving:

Order status
Items
Delivery
Carrier
Tracking information
search_policy()

Searches the Trendly policy stored in:

data/trendly_policy.md

It is used for questions about:

Shipping
Returns
Refunds
Damaged or wrong items
Lost parcels
Address changes

If the policy does not cover a question, the agent does not invent an answer.

check_return_eligibility()

Determines whether an order is eligible for a return.

It checks:

Delivery date
30-day return window
Non-returnable categories
Final-sale status
Cancelled orders
Lost parcels
check_exchange_eligibility()

Determines whether an item is eligible for a size exchange.

It checks:

30-day exchange window
Requested size
Size availability
Previous exchange count
Cancelled orders
Lost parcels
Missing requested size

Possible outcomes include:

exchange_eligible
refund
escalate
not_eligible
clarification_needed
escalate_to_human()

Creates a human-support case when a request requires human intervention.

Example:

{
"status": "escalated",
"case_id": "CASE-XXXXXXXX",
"reason": "lost_parcel",
"order_id": "TR-4526",
"assigned_to": "human_support"
}
Policy and Business Rules

The agent follows the rules defined in:

data/trendly_policy.md
Returns
Return window: 30 calendar days from delivery.
Items must be unworn and unwashed.
Original tags must be attached.
Original packaging must be included where provided.
Innerwear and socks are non-returnable.
Jewellery is non-returnable.
Beauty and fragrance products are non-returnable.
Face masks are non-returnable.
Gift cards are non-returnable.
Final-sale items are eligible for size exchange only.
Cancelled orders cannot have a return raised.
Footwear must be returned with the original shoe box.
Refunds

Refund timing starts after warehouse inspection.

Payment Method Destination Time
Credit/Debit Card Original card 5–7 business days
UPI Original UPI ID 3–5 business days
Cash on Delivery Bank transfer or store credit 7–10 business days
Store Credit Store credit Immediate

The original ₹99 shipping fee is refunded only when the return is caused by a Trendly error.

The assistant must never collect bank details in chat.

Exchanges
Exchanges are for size changes.
The same 30-day window applies.
A second exchange requires human approval.
If the requested size is unavailable, the exchange becomes a refund.
Damaged or Wrong Items

Damaged, defective, or incorrect items must be reported within 48 hours of delivery with photographs.

The customer can choose:

Free replacement
Full refund including shipping

This also applies to normally non-returnable categories when the item arrives damaged or incorrect.

Lost Parcels

A parcel is treated as lost when:

The carrier marks it as lost, or
There is no tracking movement for 10 consecutive days.

Lost parcels are handled by human support.

The resolution is either:

Free replacement
Full refund

within 5 business days.

Policy Boundaries

The agent does not invent unsupported policies.

For example:

Customer:
Can I get a birthday discount?

Trendly Agent:
Our available Trendly policy does not cover birthday discounts.
A human support agent can assist with promotion or discount inquiries.
Example Scenarios
Valid Return
Customer:
Can I return TR-4530?

Trendly Agent:
Yes, your order TR-4530 is eligible for a return.

It was delivered on July 26, 2026, which is within Trendly's
30-calendar-day return window.
Non-Returnable Jewellery
Customer:
Can I return TR-4527?

Trendly Agent:
Order TR-4527 is not eligible for return.

The Pearl Drop Earrings belong to the jewellery category,
which is non-returnable under Trendly's policy.
Exchange Size Unavailable
Customer:
Can I exchange TR-4530 for size S?

Trendly Agent:
Size S is currently unavailable.

The exchange request will need to be converted to a refund.
Lost Parcel
Customer:
What should I do about TR-4526?

Trendly Agent:
Order TR-4526 is marked as lost in transit.

Lost parcels are handled as lost-parcel claims and require
human support.

I have escalated your case to our human support team.

Case ID: CASE-XXXXXXXX
Damaged Jewellery
Customer:
My jewellery from TR-4527 arrived damaged. What can I do?

Trendly Agent:
Although jewellery is normally non-returnable, damaged items
are covered by Trendly's damaged-item policy.

Please report the damage within 48 hours of delivery and provide
photographs.

You can choose between:

1. A free replacement
2. A full refund including shipping
   Unsupported Policy Question
   Customer:
   Can I get a birthday discount?

Trendly Agent:
Our available Trendly policy does not cover birthday discounts.

A human support agent can assist with promotion or discount inquiries.
Error Handling

The agent handles common API and workflow failures.

Gemini API Errors

The system can encounter:

429 RESOURCE_EXHAUSTED — quota or rate limit exceeded
503 UNAVAILABLE — model temporarily unavailable
404 NOT_FOUND — configured model unavailable

These errors should be handled without exposing internal implementation details to customers.

Tool Errors

Tools return structured results.

Example:

{
"eligible": false,
"action": "not_eligible",
"reason": "The 30-calendar-day return window has expired.",
"order_id": "TR-4523"
}
Human Escalation

Cases requiring human intervention are passed to the escalation tool.

The agent should only tell the customer that an escalation was created after the tool successfully returns a case.

Testing

The deterministic business logic is tested independently of Gemini.

Test Coverage
Test Suite Tests Result
Return eligibility 5 ✅
Exchange eligibility 7 ✅
Human escalation 2 ✅
Total 14 ✅ 14/14
Run All Tests

From the project root:

$env:PYTHONPATH = (Get-Location).Path
pytest -v

Expected:

14 passed
Return Tests

tests/test_returns.py covers:

Valid return
Non-returnable jewellery
Expired return
Cancelled order
Final-sale item
Exchange Tests

tests/test_exchanges.py covers:

Valid exchange
Unavailable size → refund
Second exchange → escalation
Expired exchange
Cancelled order
Lost parcel → escalation
Missing requested size
Escalation Tests

tests/test_escalation.py covers:

Lost-parcel escalation
Policy escalation
Case ID generation
Human-support assignment
Setup and Installation
Requirements
Python 3.10+
Gemini API key
Internet connection

1. Clone the Repository
   git clone <YOUR_GITHUB_REPOSITORY_URL>
   cd trendly-support-agent
2. Create a Virtual Environment
   python -m venv .venv
3. Activate the Environment
   .venv\Scripts\Activate.ps1
4. Install Dependencies

If requirements.txt is available:

pip install -r requirements.txt

Otherwise:

pip install google-genai python-dotenv pytest 5. Configure the Gemini API Key

Create a .env file in the project root:

GEMINI_API_KEY=your_actual_gemini_api_key

The repository contains:

.env.example

with:

GEMINI_API_KEY=your_gemini_api_key_here

Never commit the real .env file.

Running the Agent

From the project root:

python -m app.agent

The application will prompt:

Customer:

Example:

Customer: Can I return TR-4530?

The agent identifies the request, selects the required tools, executes the business logic, and generates the response.

Running Tests

Run the complete test suite:

$env:PYTHONPATH = (Get-Location).Path
pytest -v

Run only return tests:

pytest tests/test_returns.py -v

Run only exchange tests:

pytest tests/test_exchanges.py -v

Run only escalation tests:

pytest tests/test_escalation.py -v
Security
API Key Protection

The Gemini API key is stored in .env.

The .gitignore excludes:

.env
.venv/
**pycache**/
.pytest_cache/

.env.example contains only a placeholder and is safe to commit.

Financial Information

The assistant must never collect sensitive financial information through chat, including:

Bank account numbers
Card numbers
CVV
Passwords

COD refund bank details must be handled by a human agent through the approved secure process.

Design Principles
Deterministic Business Logic

Critical business decisions are implemented in Python rather than delegated entirely to the LLM.

Tool-Based Actions

Gemini selects tools instead of directly manipulating business data.

Policy Grounding

Policy questions are answered using the provided Trendly policy.

Human-in-the-Loop

Cases requiring human intervention are escalated rather than handled autonomously.

Fail Safely

The system avoids inventing unsupported policies, refunds, discounts, inventory, or completed actions.

Testability

Business logic is tested independently of the Gemini API.

Current Status
Gemini tool calling ✅
Policy grounding ✅
Order lookup ✅
Return eligibility ✅
Exchange eligibility ✅
Human escalation ✅
Date handling ✅
API error handling ✅
Automated testing ✅
14/14 tests passing ✅

Status: Functional AI Support Agent Prototype

Future Improvements
Persistent escalation storage
Real customer-support ticket integration
Return creation workflow
Exchange creation workflow
Refund processing workflow
Database-backed order storage
FastAPI backend
Authentication
Conversation logging
Observability and metrics
Additional integration tests
Retry/backoff strategies for transient API failures
Web-based customer-support interface
Tech Stack
Python 3.10
Google Gemini API
google-genai
python-dotenv
pytest
JSON
Markdown
Why This Architecture?

The goal of this project is not simply to build a chatbot.

It demonstrates how an AI agent can be connected to deterministic business tools while maintaining control over important customer-support decisions.

The LLM handles:

Language
Intent
Tool Selection
Natural-language Response

Python handles:

Business Rules
Order Data
Eligibility
Date Calculations
Escalation

The tools connect the two layers:

Customer
|
v
Gemini Agent
|
v
Tool Selection
|
v
Python Tools
|
v
Deterministic Result
|
v
Gemini Agent
|
v
Customer Response

This separation makes the system more reliable, testable, and easier to extend into a production customer-support workflow.
