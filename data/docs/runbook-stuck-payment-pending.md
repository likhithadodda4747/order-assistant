---
doc_id: runbook-stuck-payment-pending
version: 2
doc_type: runbook
region: ALL
effective_date: 2026-09-01
allowed_roles: [associate, manager]
---
# Runbook > Order stuck in PAYMENT_PENDING

Use this when an order has been in `PAYMENT_PENDING` for more than **1 hour**.

## Step 1: Check the error code
Look up `last_error` on the order.
- **ERR_PAY_401** (card declined): ask the customer to update the payment method. Stop here.
- **ERR_PAY_403** (fraud hold): wait for the fraud review (up to 24 hours). Stop here.
- **ERR_INV_101** (inventory): go to the runbook "Out-of-stock item on an order".
- **ERR_PAY_402** (provider timeout): continue to Step 2.

## Step 2: Check the retry count
- Fewer than 3 retries: automatic retries are still running. Tell the customer to check back in 30 minutes.
- **3 retries reached:** go to Step 3.

## Step 3: Escalate
1. Open a ticket to **Payments on-call** with the order ID and error code.
2. Tell the customer their payment is being reviewed and they will not be charged twice.
3. If the customer prefers, they can cancel and place a new order with a different card.
