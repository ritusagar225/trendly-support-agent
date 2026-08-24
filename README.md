# Trendly Support Agent

> An AI-powered customer support agent for Trendly using Gemini function calling and deterministic Python business logic.

---

## Overview

The **Trendly Support Agent** is an AI-powered customer support system designed to handle common e-commerce support requests.

It combines **Google Gemini** for natural-language understanding and tool selection with **deterministic Python business logic** for important customer-support decisions.

The agent can handle:

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

- 🤖 Gemini-powered customer support
- 🔧 Function/tool calling
- 📦 Order lookup
- 📖 Policy search
- ↩️ Return eligibility checking
- 🔄 Exchange eligibility checking
- 👤 Human-support escalation
- 📅 Deterministic date calculations
- 🛡️ Policy guardrails
- 🚚 Lost-parcel handling
- ⚠️ Damaged/wrong-item handling
- 🚨 API error handling
- 🧪 Automated testing
- ✅ 14/14 business-logic tests passing

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
          +-----------------+-----------------+
          |                 |                 |
          v                 v                 v
     get_order()     search_policy()    Eligibility Tools
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

### Architecture Principle

The system separates **natural-language reasoning** from **deterministic business logic**.

```text
Gemini
  |
  | Understand request
  | Select tool
  v
Python Tools
  |
  | Apply business rules
  | Validate data
  | Calculate eligibility
  v
Structured Result
  |
  v
Gemini
  |
  | Generate response
  v
Customer
```

---

## How It Works

The Trendly Support Agent follows a tool-based workflow where Gemini handles natural-language understanding and Python tools handle deterministic business decisions.

### 1. Customer Sends a Request

```text
Customer:
Can I return TR-4530?
```

### 2. Gemini Understands the Intent

Gemini analyzes the request and determines what information or action is required.

For a return request, the agent identifies that it needs to:

1. Retrieve the order
2. Check return eligibility

### 3. Gemini Selects the Appropriate Tool

The agent uses function calling to select the required Python tool.

```text
get_order()
     ↓
check_return_eligibility()
```

The LLM is responsible for selecting the tool, but it does not make the final eligibility decision.

### 4. Python Tool Executes the Business Logic

The selected tool receives the required arguments and applies Trendly's business rules.

```python
check_return_eligibility(
    order_id="TR-4530",
    current_date="2026-08-24"
)
```

The tool checks conditions such as:

```text
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
```

### 5. Tool Returns a Structured Result

The Python function returns a structured response instead of free-form text.

```json
{
  "eligible": true,
  "action": "return_eligible",
  "order_id": "TR-4530",
  "delivered_date": "2026-07-26",
  "days_since_delivery": 29
}
```

### 6. Result Is Passed Back to Gemini

```text
Tool Result
     ↓
Gemini
     ↓
Customer-Friendly Response
```

Gemini uses the verified result to construct the final response.

### 7. Customer Receives the Final Response

```text
Trendly Agent:

Yes, your order TR-4530 is eligible for a return.

It was delivered on July 26, 2026, which is within
Trendly's 30-calendar-day return window.
```

---

## Human Escalation Flow

Some situations cannot be resolved automatically.

For example, a lost parcel requires human support.

```text
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
```

Example escalation result:

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

## Why Use Tools?

The agent separates **conversation** from **business logic**.

### Gemini Handles

- Understanding customer requests
- Identifying intent
- Selecting tools
- Generating customer-friendly responses

### Python Handles

- Order lookup
- Policy rules
- Return eligibility
- Exchange eligibility
- Date calculations
- Human escalation

This prevents the LLM from independently deciding important business outcomes.

The result is a system that is:

- More reliable
- Easier to test
- Easier to debug
- Easier to extend
- Less dependent on LLM-generated business decisions

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
└── README.md
```

### Main Components

| Component                 | Purpose                                                   |
| ------------------------- | --------------------------------------------------------- |
| `app/agent.py`            | Main Gemini agent and tool-calling workflow               |
| `app/tools/orders.py`     | Order lookup                                              |
| `app/tools/policy.py`     | Trendly policy search                                     |
| `app/tools/returns.py`    | Return eligibility                                        |
| `app/tools/exchanges.py`  | Exchange eligibility                                      |
| `app/tools/escalation.py` | Human-support escalation                                  |
| `app/guardrails/`         | Agent safety and behavior controls                        |
| `app/prompts/`            | Agent prompt components                                   |
| `data/orders.json`        | Order data                                                |
| `data/trendly_policy.md`  | Trendly policy source                                     |
| `tests/`                  | Automated business-logic tests                            |
| `.env.example`            | Environment-variable template                             |
| `.gitignore`              | Prevents secrets and generated files from being committed |
| `pytest.ini`              | Pytest configuration                                      |

---

## Tools and Components

### `get_order()`

**File:** `app/tools/orders.py`

Retrieves order information using an order ID.

Used for questions involving:

- Order status
- Items
- Delivery information
- Carrier
- Tracking information

### `search_policy()`

**File:** `app/tools/policy.py`

Searches the Trendly policy stored in:

```text
data/trendly_policy.md
```

Used for questions about:

- Shipping
- Returns
- Refunds
- Damaged or wrong items
- Lost parcels
- Address changes

If the policy does not cover a question, the agent does not invent an answer.

### `check_return_eligibility()`

**File:** `app/tools/returns.py`

Determines whether an order is eligible for a return.

The tool checks:

- Delivery date
- 30-day return window
- Non-returnable categories
- Final-sale status
- Cancelled orders
- Lost parcels

Example:

```python
check_return_eligibility(
    order_id="TR-4530",
    current_date="2026-08-24"
)
```

Example result:

```json
{
  "eligible": true,
  "action": "return_eligible",
  "order_id": "TR-4530",
  "days_since_delivery": 29
}
```

### `check_exchange_eligibility()`

**File:** `app/tools/exchanges.py`

Determines whether an item is eligible for a size exchange.

The tool checks:

- 30-day exchange window
- Requested size
- Size availability
- Previous exchange count
- Cancelled orders
- Lost parcels
- Missing requested size

Possible outcomes:

```text
exchange_eligible
refund
escalate
not_eligible
clarification_needed
```

### `escalate_to_human()`

**File:** `app/tools/escalation.py`

Creates a human-support case when a request requires human intervention.

Example result:

```json
{
  "status": "escalated",
  "case_id": "CASE-XXXXXXXX",
  "reason": "lost_parcel",
  "order_id": "TR-4526",
  "assigned_to": "human_support"
}
```

---

## Policy and Business Rules

The agent follows the rules defined in:

```text
data/trendly_policy.md
```

### Returns

- Items can be returned within 30 calendar days of the delivery date.
- Items must be unworn and unwashed.
- Original tags must be attached.
- Original packaging must be included where provided.
- Innerwear and socks are non-returnable.
- Jewellery is non-returnable.
- Beauty and fragrance products are non-returnable.
- Face masks are non-returnable.
- Gift cards are non-returnable.
- Final-sale items are eligible for size exchange only.
- Cancelled orders cannot have a return raised.

### Refunds

| Payment Method      | Refund Destination            | Processing Time    |
| ------------------- | ----------------------------- | ------------------ |
| Credit / Debit Card | Original card                 | 5–7 business days  |
| UPI                 | Original UPI ID               | 3–5 business days  |
| Cash on Delivery    | Bank transfer or store credit | 7–10 business days |
| Store Credit        | Store credit                  | Immediate          |

The assistant must not collect sensitive bank information through chat.

### Exchanges

- Exchanges are for size changes.
- The same 30-day window applies.
- A second exchange requires human approval.
- If the requested size is unavailable, the exchange becomes a refund.

### Damaged or Wrong Items

Damaged, defective, or incorrect items must be reported within 48 hours of delivery with photographs.

The customer can choose:

1. Free replacement
2. Full refund including shipping

### Lost Parcels

Lost parcels are handled as human-support cases.

The resolution can be:

- Free replacement
- Full refund

---

## Example Scenarios

### Valid Return

```text
Customer:
Can I return TR-4530?

Trendly Agent:
Yes, your order TR-4530 is eligible for a return.

It was delivered on July 26, 2026, which is within Trendly's
30-calendar-day return window.
```

### Non-Returnable Jewellery

```text
Customer:
Can I return TR-4527?

Trendly Agent:
Order TR-4527 is not eligible for return.

The Pearl Drop Earrings belong to the jewellery category,
which is non-returnable under Trendly's policy.
```

### Exchange Size Unavailable

```text
Customer:
Can I exchange TR-4530 for size S?

Trendly Agent:
Size S is currently unavailable.

The exchange request will need to be converted to a refund.
```

### Lost Parcel

```text
Customer:
What should I do about TR-4526?

Trendly Agent:
Order TR-4526 is marked as lost in transit.

Lost parcels are handled as lost-parcel claims and require
human support.

I have escalated your case to our human support team.

Case ID: CASE-XXXXXXXX
```

### Damaged Jewellery

```text
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
```

### Unsupported Policy Question

```text
Customer:
Can I get a birthday discount?

Trendly Agent:
Our available Trendly policy does not cover birthday discounts.

A human support agent can assist with promotion or discount inquiries.
```

---

## Error Handling

The agent handles common API and workflow failures.

### Gemini API Errors

The system can encounter:

- `429 RESOURCE_EXHAUSTED` — quota or rate limit exceeded
- `503 UNAVAILABLE` — model temporarily unavailable
- `404 NOT_FOUND` — configured model unavailable

These errors should be handled without exposing internal implementation details to customers.

### Tool Errors

Tools return structured results such as:

```json
{
  "eligible": false,
  "action": "not_eligible",
  "reason": "The 30-calendar-day return window has expired.",
  "order_id": "TR-4523"
}
```

### Human Escalation

Cases requiring human intervention are passed to the escalation tool.

The agent should only tell the customer that an escalation was created after the tool successfully returns a case.

---

## Testing

The deterministic business logic is tested independently of Gemini.

### Test Coverage

| Test Suite           |  Tests | Result               |
| -------------------- | -----: | -------------------- |
| Return eligibility   |      5 | ✅ Passing           |
| Exchange eligibility |      7 | ✅ Passing           |
| Human escalation     |      2 | ✅ Passing           |
| **Total**            | **14** | **✅ 14/14 Passing** |

### Run All Tests

From the project root:

```powershell
$env:PYTHONPATH = (Get-Location).Path
pytest -v
```

Expected:

```text
14 passed
```

### Return Tests

`tests/test_returns.py` covers:

- Valid return
- Non-returnable jewellery
- Expired return
- Cancelled order
- Final-sale item

### Exchange Tests

`tests/test_exchanges.py` covers:

- Valid exchange
- Unavailable size → refund
- Second exchange → escalation
- Expired exchange
- Cancelled order
- Lost parcel → escalation
- Missing requested size

### Escalation Tests

`tests/test_escalation.py` covers:

- Lost-parcel escalation
- Policy escalation
- Case ID generation
- Human-support assignment

---

## Setup and Installation

### Requirements

- Python 3.10+
- Gemini API key
- Internet connection

### 1. Clone the Repository

```bash
git clone https://github.com/ritusagar225/trendly-support-agent.git
cd trendly-support-agent
```

### 2. Create a Virtual Environment

```powershell
python -m venv .venv
```

### 3. Activate the Virtual Environment

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```powershell
pip install -r requirements.txt
```

If `requirements.txt` is not present:

```powershell
pip install google-genai python-dotenv pytest
```

### 5. Configure the Gemini API Key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_actual_gemini_api_key
```

The repository includes a safe `.env.example` file:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

> **Never commit the real `.env` file.**

---

## Running the Agent

From the project root:

```powershell
python -m app.agent
```

The application will prompt:

```text
Customer:
```

Example:

```text
Customer: Can I return TR-4530?
```

The agent identifies the request, selects the required tools, executes the business logic, and generates the response.

---

## Security

### API Key Protection

The Gemini API key is stored in `.env`.

The `.gitignore` excludes:

```text
.env
.venv/
__pycache__/
.pytest_cache/
```

`.env.example` contains only a placeholder and is safe to commit.

### Sensitive Information

The assistant must not collect sensitive financial information through chat, including:

- Bank account numbers
- Card numbers
- CVV
- Passwords

---

## Design Principles

### Deterministic Business Logic

Critical business decisions are implemented in Python rather than delegated entirely to the LLM.

### Tool-Based Actions

Gemini selects tools instead of directly manipulating business data.

### Policy Grounding

Policy questions are answered using the provided Trendly policy.

### Human-in-the-Loop

Cases requiring human intervention are escalated rather than handled autonomously.

### Fail Safely

The system avoids inventing unsupported policies, refunds, discounts, inventory, or completed actions.

### Testability

Business logic is tested independently of the Gemini API.

---

## Current Status

| Component            | Status   |
| -------------------- | -------- |
| Gemini tool calling  | ✅       |
| Policy grounding     | ✅       |
| Order lookup         | ✅       |
| Return eligibility   | ✅       |
| Exchange eligibility | ✅       |
| Human escalation     | ✅       |
| Date handling        | ✅       |
| API error handling   | ✅       |
| Automated testing    | ✅       |
| Business-logic tests | ✅ 14/14 |

### Project Status

**Functional AI Support Agent Prototype**

---

## Future Improvements

- Persistent escalation storage
- Real customer-support ticket integration
- Return creation workflow
- Exchange creation workflow
- Refund processing workflow
- Database-backed order storage
- FastAPI backend
- Authentication
- Conversation logging
- Observability and metrics
- Additional integration tests
- Retry and backoff strategies for transient API failures
- Web-based customer-support interface

---

## Tech Stack

| Technology        | Purpose                                         |
| ----------------- | ----------------------------------------------- |
| Python 3.10       | Core application and business logic             |
| Google Gemini API | Natural-language understanding and tool calling |
| `google-genai`    | Gemini API integration                          |
| `python-dotenv`   | Environment variable management                 |
| pytest            | Automated testing                               |
| JSON              | Order data storage                              |
| Markdown          | Policy storage and documentation                |

---

## Repository

**GitHub:**  
https://github.com/ritusagar225/trendly-support-agent

---

## License

This project was created as a demonstration of an AI-powered customer-support agent architecture using Gemini function calling and deterministic business logic.
