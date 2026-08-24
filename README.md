# Trendly Support Agent

> Agentic customer-support assistant for Trendly, built with Gemini tool calling and deterministic Python business logic.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Gemini](https://img.shields.io/badge/LLM-Google%20Gemini-4285F4)](https://ai.google.dev/)
[![Tests](https://img.shields.io/badge/tests-14%2F14%20passing-success)](#testing)

## Overview

Trendly is a direct-to-consumer fashion retailer handling a large volume of customer-support conversations. A significant portion of those conversations involve repetitive questions about orders, returns, exchanges, shipping, and refunds.

This project implements an **agentic support assistant** that can:

- Look up orders and explain their status
- Answer policy questions using the provided Trendly policy
- Determine return eligibility
- Determine exchange eligibility
- Handle damaged or wrong items
- Handle lost parcels
- Escalate cases to human support
- Refuse unsupported or unauthorized requests
- Use real tool/function calling rather than keyword matching

The core design separates **LLM reasoning and orchestration** from **deterministic business decisions**.

Gemini decides what the customer is asking and which tool should be used. Python tools retrieve data and enforce business rules. The resulting structured data is then returned to Gemini to generate the final customer-facing response.

---

## What This Project Demonstrates

The assignment focuses on two major areas:

### Orchestration

The agent can decide what to do, call multiple tools when required, use tool results to continue the workflow, and escalate cases that should not be handled automatically.

### Prompt Engineering

The agent is instructed to:

- Ground policy answers in the provided policy document
- Avoid inventing policies or discounts
- Use tools for order-specific decisions
- Treat tool results as the source of truth for eligibility
- Escalate when human intervention is required
- Avoid exposing internal implementation details
- Handle uncertainty conservatively

---

## Architecture

```text
                         Customer
                            |
                            v
                     Gemini Agent
                            |
                    Intent / Tool Selection
                            |
          +-----------------+------------------+
          |                 |                  |
          v                 v                  v
     get_order()      search_policy()     Eligibility Tools
                                                |
                                      +---------+---------+
                                      |                   |
                                      v                   v
                               Return Tool        Exchange Tool
                                      |                   |
                                      +---------+---------+
                                                |
                                                v
                                         Structured Result
                                                |
                                                v
                                          Gemini Agent
                                                |
                                      +---------+---------+
                                      |                   |
                                      v                   v
                               Final Response       Escalation
                                                        |
                                                        v
                                                  Human Support
```

### Core Principle

```text
Natural-language reasoning
          |
          v
       Gemini
          |
     Tool selection
          |
          v
    Python tools
          |
   Deterministic rules
          |
          v
 Structured result
          |
          v
       Gemini
          |
          v
 Customer response
```

The LLM does **not** independently decide whether a return or exchange is allowed. Those decisions are made by deterministic Python tools using order data and policy rules.

---

## How It Works

### 1. Customer Request

```text
Customer:
Can I return TR-4530?
```

### 2. Agent Identifies Required Actions

Gemini determines that the request requires order information and return eligibility checking.

```text
get_order()
     |
     v
check_return_eligibility()
```

### 3. Tools Execute Business Logic

The return tool checks the order against the applicable rules, including:

- Delivery date
- Return window
- Item category
- Final-sale status
- Order status

### 4. Tool Returns Structured Data

```json
{
  "eligible": true,
  "action": "return_eligible",
  "order_id": "TR-4530",
  "delivered_date": "2026-07-26",
  "days_since_delivery": 29
}
```

### 5. Gemini Generates the Response

The verified result is passed back to Gemini, which turns it into a concise customer-facing response.

```text
Trendly Agent:

Yes, your order TR-4530 is eligible for a return.

It was delivered on July 26, 2026, which is within
Trendly's 30-calendar-day return window.
```

---

## Tooling

### Order Lookup

`get_order()`

Retrieves order information from the provided order dataset.

Used for:

- Order status
- Items
- Delivery date
- Carrier
- Tracking information

### Policy Search

`search_policy()`

Retrieves relevant information from:

```text
data/trendly_policy.md
```

The policy document is treated as the source of truth for policy questions.

### Return Eligibility

`check_return_eligibility()`

Determines whether an order can be returned using deterministic business rules.

Possible outcomes include:

```text
return_eligible
not_eligible
not_found
invalid_date
escalate
```

### Exchange Eligibility

`check_exchange_eligibility()`

Handles size exchanges and checks:

- Exchange window
- Requested size
- Size availability
- Previous exchange count
- Order status

Possible outcomes include:

```text
exchange_eligible
refund
escalate
not_eligible
clarification_needed
```

### Human Escalation

`escalate_to_human()`

Creates a structured human-support case when the issue requires manual handling.

Example:

```json
{
  "status": "escalated",
  "case_id": "CASE-602D1914",
  "reason": "lost_parcel",
  "order_id": "TR-4526",
  "assigned_to": "human_support"
}
```

---

## Policy Grounding

The agent uses:

```text
data/trendly_policy.md
```

as the source of truth for policy questions.

Examples of policy-controlled behavior include:

- 30-calendar-day return window
- Non-returnable product categories
- Final-sale restrictions
- Exchange rules
- Damaged-item handling
- Lost-parcel handling
- Refund processing rules

The agent should not invent a policy when the provided policy does not support the answer.

For example:

```text
Customer:
Can I get a birthday discount?

Agent:
Our available Trendly policy does not cover birthday discounts.
A human support agent can assist with promotion or discount inquiries.
```

---

## Human Escalation

Not every support case should be resolved automatically.

For example, a lost parcel follows this flow:

```text
Customer
   |
   v
"What should I do about TR-4526?"
   |
   v
get_order()
   |
   v
Order is lost in transit
   |
   v
Escalation tool
   |
   v
Human support case
   |
   v
Case ID
   |
   v
Customer receives escalation confirmation
```

This keeps human-in-the-loop handling explicit instead of pretending that an action was completed when it was not.

---

## Example Scenarios

### Valid Return

```text
Customer:
Can I return TR-4530?

Agent:
Yes, your order TR-4530 is eligible for a return.

It was delivered on July 26, 2026, which is within
Trendly's 30-calendar-day return window.
```

### Non-Returnable Jewellery

```text
Customer:
Can I return TR-4527?

Agent:
Order TR-4527 is not eligible for return.

The Pearl Drop Earrings are jewellery, which is a
non-returnable category under Trendly's policy.
```

### Expired Return

```text
Customer:
Can I return TR-4528?

Agent:
Order TR-4528 is not eligible for return.

The 30-calendar-day return window has expired.
```

### Lost Parcel

```text
Customer:
What should I do about TR-4526?

Agent:
Order TR-4526 is marked as lost in transit.

This requires human-support handling, so I have
escalated the case and created a support case ID.
```

### Damaged Item

```text
Customer:
My jewellery from TR-4527 arrived damaged. What can I do?

Agent:
Although jewellery is normally non-returnable, damaged
items are covered by the damaged-item policy.

The customer can provide photographs and choose between
a replacement or a full refund, subject to the policy.
```

---

## Project Structure

```text
trendly-support-agent/
│
├── app/
│   ├── agent.py
│   ├── __init__.py
│   │
│   ├── guardrails/
│   │
│   ├── prompts/
│   │
│   └── tools/
│       ├── orders.py
│       ├── policy.py
│       ├── returns.py
│       ├── exchanges.py
│       ├── escalation.py
│       └── __init__.py
│
├── data/
│   ├── orders.json
│   └── trendly_policy.md
│
├── tests/
│   ├── test_returns.py
│   ├── test_exchanges.py
│   └── test_escalation.py
│
├── .env.example
├── .gitignore
├── pytest.ini
├── requirements.txt
├── PROMPTS.md
├── SOLUTION.md
└── README.md
```

---

## Testing

The deterministic business logic is tested independently of the Gemini API.

### Test Coverage

| Test Suite | Tests | Status |
|---|---:|---|
| Return eligibility | 5 | ✅ Passing |
| Exchange eligibility | 7 | ✅ Passing |
| Human escalation | 2 | ✅ Passing |
| **Total** | **14** | **✅ 14/14 Passing** |

### Run Tests

From the project root:

```powershell
$env:PYTHONPATH = (Get-Location).Path
pytest -v
```

Expected:

```text
14 passed
```

The tests cover cases including:

- Valid returns
- Non-returnable jewellery
- Expired returns
- Cancelled orders
- Final-sale items
- Valid exchanges
- Unavailable sizes
- Second exchanges
- Expired exchanges
- Lost-parcel escalation
- Missing requested sizes

---

## Setup

### Requirements

- Python 3.10+
- Gemini API key
- Internet connection

### Clone

```bash
git clone https://github.com/ritusagar225/trendly-support-agent.git
cd trendly-support-agent
```

### Create Virtual Environment

```powershell
python -m venv .venv
```

### Activate

```powershell
.venv\Scripts\Activate.ps1
```

### Install Dependencies

```powershell
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_actual_gemini_api_key
```

A safe `.env.example` file is included in the repository.

> Never commit the real `.env` file or expose the API key.

---

## Run Locally

The application can be started from the project root with:

```powershell
python -m app.agent
```

Example:

```text
Customer: Can I return TR-4530?
```

The agent then performs tool selection, executes the required business logic, and generates the response.

---

## Running the Project for Evaluation

The project is intentionally structured so that it can be run locally without a separate frontend.

### Start Command

```text
python -m app.agent
```

### Test Command

```powershell
$env:PYTHONPATH = (Get-Location).Path
pytest -v
```

---

## Error Handling

The system is designed to handle failures from both the LLM layer and tool layer.

Examples include:

- Gemini service unavailable
- Gemini quota/rate-limit errors
- Invalid model configuration
- Missing order
- Invalid dates
- Unsupported requests
- Tool failures

Business tools return structured results rather than allowing errors or uncertainty to become invented customer-facing answers.

---

## Safety and Guardrails

The agent is designed to:

- Avoid inventing policy
- Avoid unauthorized discounts
- Avoid claiming an action was completed when it was not
- Avoid exposing internal implementation details
- Avoid collecting sensitive financial information
- Escalate cases that require human intervention
- Use provided policy and tool results as sources of truth

---

## AI Usage Note

AI tools were used during development for:

- Brainstorming agent architecture
- Drafting and refining prompts
- Debugging implementation issues
- Improving documentation
- Reviewing edge cases and test scenarios

The final implementation, tool design, business logic, tests, guardrails, and project structure were reviewed and modified as part of the development process.

The author is prepared to explain and modify the implementation during evaluation.

More detail about prompt development and iteration is documented in [`PROMPTS.md`](PROMPTS.md).

---

## Known Limitations

- The current order dataset is a fixed local JSON dataset provided for the assignment.
- Human-support escalation is represented by a local tool rather than a production ticketing system.
- The current application is primarily a CLI application.
- There is no persistent conversation database.
- Production authentication and authorization are not implemented.
- Gemini availability and free-tier quota can affect live LLM calls.
- Inventory availability is represented through the tool inputs/data available to the prototype rather than a production inventory service.

---

## Future Improvements

If this were moved toward production, the next improvements would include:

- Persistent conversation state
- Production database integration
- Real ticketing-system integration
- Real return and exchange creation
- Authentication and authorization
- Observability and tracing
- Retry and backoff strategies
- Rate-limit handling
- Production inventory integration
- Customer-facing web interface
- Automated evaluation against scripted conversations
- Analytics for escalation and resolution rates

---

## Repository

GitHub:

https://github.com/ritusagar225/trendly-support-agent

---

## Submission

This repository is structured to support the assignment deliverables:

- Source code
- README
- Prompt documentation
- Solution note
- Automated tests
- Local start command

The assignment also requires a public demo video and either a live endpoint or a repository that can be started with one command.

---

## License

This project was created as a screening-assignment demonstration of an agentic customer-support architecture using Gemini tool calling and deterministic Python business logic.
