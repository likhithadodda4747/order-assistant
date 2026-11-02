---
doc_id: err-pay-401
version: 1
doc_type: error_catalog
region: ALL
effective_date: 2026-01-15
allowed_roles: [associate, manager]
---
# Error Catalog > ERR_PAY_401: Card Declined

**Meaning:** The customer's bank declined the payment card. The payment provider responded and the decline is final for this card.

**Order status:** The order stays in `PAYMENT_PENDING` until the customer updates the payment method.

**What to do:**
1. Tell the customer the bank declined the card. Do not share the decline reason code with the customer.
2. Ask the customer to update the payment method in their account or at the register.
3. Do not retry the same card. Retrying a declined card will not succeed.

**Automatic retries:** None. ERR_PAY_401 is never retried automatically.
