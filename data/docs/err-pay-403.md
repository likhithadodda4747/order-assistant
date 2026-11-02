---
doc_id: err-pay-403
version: 1
doc_type: error_catalog
region: ALL
effective_date: 2026-01-15
allowed_roles: [associate, manager]
---
# Error Catalog > ERR_PAY_403: Fraud Check Hold

**Meaning:** The payment was held by the fraud screening service for manual review.

**Order status:** `PAYMENT_PENDING` until the fraud team approves or rejects the payment, usually within **24 hours**.

**What to do:**
1. Tell the customer the order is under a routine security review.
2. Do not share details of the fraud check.
3. Do not cancel or re-place the order; a second order would be held too.

**Automatic retries:** None. The fraud team's decision updates the order.
