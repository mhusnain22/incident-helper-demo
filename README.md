# Payment Service

A lightweight, dummy Python payment service for testing and demonstration purposes.
It simulates core payment operations without connecting to any real payment gateway.

## Features

- **Process payments** — validate and record transactions with a unique transaction ID
- **Issue refunds** — full or partial refunds against an existing transaction
- **Input validation** — rejects invalid amounts, unsupported currencies, and unknown payment methods
- **Zero dependencies** — uses only the Python standard library

## Supported Options

| Category         | Values                                              |
|------------------|-----------------------------------------------------|
| **Currencies**   | `USD`, `EUR`, `GBP`, `CAD`, `AUD`,`PKR`                 |
| **Methods**      | `credit_card`, `debit_card`, `paypal`, `bank_transfer`,`virtual_card` |

## Quick Start

```bash
python payment_service.py
```

## Usage

```python
from payment_service import process_payment, refund_payment, PaymentError

# Process a payment
transaction = process_payment(
    amount=99.99,
    currency="USD",
    method="credit_card",
    description="Order #1042",
)
print(transaction["transaction_id"])  # e.g. "3f1a2b4c-..."

# Refund the transaction
refund = refund_payment(transaction["transaction_id"])
print(refund["status"])  # "refunded"

# Handle validation errors
try:
    process_payment(-5, currency="XYZ")
except PaymentError as e:
    print(e)
```

## Response Format

### `process_payment`

```json
{
  "transaction_id": "3f1a2b4c-d5e6-7f8a-9b0c-1d2e3f4a5b6c",
  "status": "success",
  "amount": 99.99,
  "currency": "USD",
  "method": "credit_card",
  "description": "Order #1042",
  "timestamp": "2026-08-25T14:03:00Z"
}
```

### `refund_payment`

```json
{
  "refund_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "original_transaction_id": "3f1a2b4c-d5e6-7f8a-9b0c-1d2e3f4a5b6c",
  "status": "refunded",
  "amount": "full",
  "timestamp": "2026-08-25T14:05:00Z"
}
```

## Project Structure

```
.
├── payment_service.py   # Core payment logic
└── README.md            # Project documentation
```

## License

MIT