---
doc_id: err-inv-101
version: 1
doc_type: error_catalog
region: ALL
effective_date: 2026-01-15
allowed_roles: [associate, manager]
---
# Error Catalog > ERR_INV_101: Inventory Reservation Failed

**Meaning:** One or more items could not be reserved at the assigned warehouse because stock ran out after the order was placed.

**Order status:** `PAYMENT_PENDING`. The customer is not charged until all items are reserved.

**What to do:**
1. Check stock for the affected items.
2. Offer the customer a substitution, a split shipment, or removal of the item (see runbook "Out-of-stock item on an order").
3. The system retries the reservation once automatically after 15 minutes.
