"""
Payment Service
A simple dummy payment processing service for demonstration purposes.
"""

import uuid
from datetime import datetime


SUPPORTED_CURRENCIES = {"USD", "EUR", "GBP", "CAD", "AUD"}
SUPPORTED_METHODS = {"credit_card", "debit_card", "paypal", "bank_transfer"}


class PaymentError(Exception):
    """Raised when a payment cannot be processed."""
    pass


def validate_payment(amount: float, currency: str, method: str) -> None:
    """Validate payment parameters before processing."""
    if amount <= 0:
        raise PaymentError(f"Invalid amount: {amount}. Must be greater than 0.")
    if currency not in SUPPORTED_CURRENCIES:
        raise PaymentError(
            f"Unsupported currency: {currency}. Supported: {SUPPORTED_CURRENCIES}"
        )
    if method not in SUPPORTED_METHODS:
        raise PaymentError(
            f"Unsupported payment method: {method}. Supported: {SUPPORTED_METHODS}"
        )


def process_payment(
    amount: float,
    currency: str = "USD",
    method: str = "credit_card",
    description: str = "",
) -> dict:
    """
    Process a payment transaction.

    Args:
        amount:      The payment amount (must be > 0).
        currency:    ISO 4217 currency code (e.g. "USD", "EUR").
        method:      Payment method ("credit_card", "debit_card", "paypal", "bank_transfer").
        description: Optional description for the transaction.

    Returns:
        A dict containing the transaction details and status.

    Raises:
        PaymentError: If the payment parameters are invalid.
    """
    validate_payment(amount, currency, method)

    transaction_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat() + "Z"

    transaction = {
        "transaction_id": transaction_id,
        "status": "success",
        "amount": round(amount, 2),
        "currency": currency,
        "method": method,
        "description": description,
        "timestamp": timestamp,
    }

    print(f"[{timestamp}] Payment processed: {transaction_id} | "
          f"{currency} {amount:.2f} via {method}")

    return transaction


def refund_payment(transaction_id: str, amount: float = None) -> dict:
    """
    Issue a refund for a previous transaction.

    Args:
        transaction_id: The ID of the original transaction.
        amount:         Partial refund amount. If None, full refund is assumed.

    Returns:
        A dict containing the refund details.
    """
    if not transaction_id:
        raise PaymentError("transaction_id is required for a refund.")

    refund_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat() + "Z"

    refund = {
        "refund_id": refund_id,
        "original_transaction_id": transaction_id,
        "status": "refunded",
        "amount": round(amount, 2) if amount is not None else "full",
        "timestamp": timestamp,
    }

    print(f"[{timestamp}] Refund issued: {refund_id} for transaction {transaction_id}")

    return refund


# ---------------------------------------------------------------------------
# Quick demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== Payment Service Demo ===\n")

    # Successful payment
    result = process_payment(49.99, currency="USD", method="credit_card",
                             description="Subscription renewal")
    print("Transaction result:", result)

    print()

    # Refund
    refund = refund_payment(result["transaction_id"])
    print("Refund result:", refund)

    print()

    # Validation error
    try:
        process_payment(-10, currency="XYZ", method="crypto")
    except PaymentError as e:
        print(f"PaymentError caught: {e}")
