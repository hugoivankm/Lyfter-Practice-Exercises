import time
import uuid


class PaymentService:
    @staticmethod
    def process_payment(amount: float, card_number: str) -> tuple[bool, str]:
        if amount <= 0:
            return False, "Invalid payment amount"

        clean_card = card_number.replace("-", "").replace(" ", "")
        if not clean_card.isdigit() or len(clean_card) < 13:
            return False, "Invalid card format"

        time.sleep(0.1)

        if clean_card.endswith("0000"):
            return False, "Card declined: Insufficient funds"

        if clean_card.endswith("9999"):
            return False, "Payment gateway timeout"

        transaction_id = f"txn_{uuid.uuid4().hex[:12]}"
        return True, transaction_id
