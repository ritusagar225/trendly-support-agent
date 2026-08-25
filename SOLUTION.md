# Trendly Support Agent - Technical Solution Document

## 1. System Architecture

The **Trendly Support Agent** combines Large Language Model (LLM) natural-language processing with deterministic Python business logic:

```
                            [ Customer / API Client ]
                                        |
                                        v
                            FastAPI Server (`app/api.py`)
                                        |
                                        v
                           Gemini Agent (`app/agent.py`)
                          - Model: `gemini-3.6-flash`
                          - Tool Selection & NLU Synthesis
                                        |
                 +----------------------+----------------------+
                 |                      |                      |
                 v                      v                      v
           Order Lookup           Policy Search        Eligibility Tools
         (`tools/orders.py`)   (`tools/policy.py`)   (`tools/returns.py`)
                 |                      |            (`tools/exchanges.py`)
           `orders.json`      `trendly_policy.md`    (`tools/escalation.py`)
                 |                      |                      |
                 +----------------------+----------------------+
                                        |
                                        v
                              Deterministic Output
                                        |
                                        v
                               LLM Final Response
```

### Architecture Components
- **API Server (`app/api.py`)**: Built on FastAPI and Uvicorn. Exposes REST endpoints (`GET /`, `GET /health`, `POST /chat`).
- **Agent Orchestrator (`app/agent.py`)**: Wraps the Google Gemini API (`google-genai`). Manages conversation context, handles function calling loops, injects runtime variables (e.g., current date), and returns safe, grounded responses.
- **Business Logic Tools (`app/tools/`)**:
  - `orders.py`: Queries fixed customer order database (`data/orders.json`).
  - `policy.py`: Searches policy document sections using normalized keyword matching (`data/trendly_policy.md`).
  - `returns.py`: Evaluates 30-day return windows, cancellation status, lost parcel status, category non-returnability, and final-sale restrictions.
  - `exchanges.py`: Evaluates size exchange eligibility, 30-day window, inventory size availability, and enforces human escalation for repeat exchanges.
  - `escalation.py`: Generates structured human escalation tickets (`CASE-XXXXXXXX`).

---

## 2. Key Technical Trade-offs

1. **Deterministic Python Rules vs. Pure LLM Reasoning**:
   - *Trade-off*: All eligibility, policy matching, and escalation rules are enforced by strict Python code rather than LLM prompts.
   - *Benefit*: Guarantees zero hallucinations on policy, return windows, or financial commitments.
   - *Cost*: Adding new business policies requires code changes and unit tests rather than simple prompt tweaks.

2. **File-Based JSON & Markdown Storage vs. Database & RAG**:
   - *Trade-off*: Orders and policies are stored in local `orders.json` and `trendly_policy.md` files.
   - *Benefit*: Zero database overhead, instant test suite execution (<0.1s), simple single-command local run.
   - *Cost*: Cannot handle high-concurrency writes, real-time inventory updates, or large-scale document collections without database backing.

3. **In-Memory Escalation Tracking vs. External CRM Integration**:
   - *Trade-off*: Escalations generate a local tracking ID string.
   - *Benefit*: Runs isolated without external dependencies or third-party API credentials.
   - *Cost*: Tickets are not persisted to an external helpdesk (e.g., Zendesk, Freshdesk).

---

## 3. Known Limitations

1. **ReadOnly Eligibility Checking**:
   - The agent determines return/exchange eligibility, but does not initiate return shipping labels or mutate order status.
2. **Keyword Policy Retrieval**:
   - Policy retrieval relies on keyword matching. Highly complex or multi-intent questions may benefit from vector embeddings (RAG) in future iterations.
3. **Stateless Request Context**:
   - The `/chat` endpoint processes each request independently. Multi-turn context within a single request is handled by the function calling loop, but cross-request conversational state requires external session storage.

---

## 4. Five Discovery Questions for Trendly's Operations Team

1. **Partial & Multi-Item Order Handling**:
   - *How should the system handle partial returns when an order contains both returnable apparel and non-returnable items (e.g., innerwear or final-sale items)?*
2. **CRM & Ticketing Integration**:
   - *Which helpdesk system (e.g., Zendesk, Freshdesk, Kustomer, Salesforce) should `escalate_to_human()` connect to, and what routing tags or priority levels should be assigned to lost-parcel vs. policy-exception cases?*
3. **Damaged / Defective Item Verification**:
   - *What is the standard operating procedure for photo verification on damaged items, and should the agent automatically issue replacement requests or always route through human approval?*
4. **COD Refund Disbursement Protocol**:
   - *What secure gateway (e.g., Razorpay X, Cashfree) should be integrated for collecting and validating customer bank accounts/UPI IDs for Cash on Delivery refunds?*
5. **Real-time Inventory & Stock Restock Integration**:
   - *How should the size exchange tool query live inventory, and what rule should apply if a requested size is currently out of stock but scheduled for restock within 5 business days?*
