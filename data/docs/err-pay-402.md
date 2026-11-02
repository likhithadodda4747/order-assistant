---
doc_id: err-pay-402
version: 1
doc_type: error_catalog
region: ALL
effective_date: 2026-01-15
allowed_roles: [associate, manager]
---
# Error Catalog > ERR_PAY_402: Payment Provider Timeout

**Meaning:** The payment provider did not respond in time. The card was not declined; the charge result is unknown at the moment of the error.

**Order status:** The order stays in `PAYMENT_PENDING` while the system retries.

**Automatic retries:** The system retries the charge automatically up to **3 times**, about **10 minutes apart**, using the same idempotency key so the customer is never charged twice.

**What to do:**
1. If retries are below 3, tell the customer the payment is being retried and to check back in 30 minutes.
2. If the order has reached **3 retries**, follow the runbook "Order stuck in PAYMENT_PENDING".
3. Do not ask the customer to pay again while retries are in progress.
