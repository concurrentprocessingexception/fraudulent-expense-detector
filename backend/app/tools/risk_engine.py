from app.database.repositories import (
    get_user_avg_amount,
    get_user_category_stats,
    get_recent_transactions_count,
    get_user_by_id
)


class FraudRiskEngine:

    def __init__(self, db):
        self.db = db

    def analyze_transaction(self, txn):

        risk_score = 0
        reasons = []

        user_id = txn.user_id

        # ---------- AMOUNT ----------
        avg_amount = get_user_avg_amount(self.db, user_id)

        if avg_amount and txn.amount > avg_amount * 3:
            risk_score += 30
            reasons.append(
                f"Transaction amount {txn.amount:.2f} exceeds user average {avg_amount:.2f}"
            )

        # ---------- LOCATION ----------
        user = get_user_by_id(self.db, user_id)

        if txn.country != user.home_country:
            risk_score += 25
            reasons.append(
                f"Transaction outside home country ({txn.country})"
            )

        # ---------- CATEGORY ----------
        category_stats = get_user_category_stats(self.db, user_id)
        categories = [c[0] for c in category_stats]

        if txn.merchant_category not in categories:
            risk_score += 20
            reasons.append(
                f"Unusual merchant category ({txn.merchant_category})"
            )

        # ---------- VELOCITY ----------
        recent_count = get_recent_transactions_count(self.db, user_id)

        if recent_count > 5:
            risk_score += 15
            reasons.append("High transaction frequency")

        # ---------- CLASSIFICATION ----------
        if risk_score >= 70:
            level = "HIGH"
        elif risk_score >= 40:
            level = "MEDIUM"
        else:
            level = "LOW"

        return {
            "risk_score": risk_score,
            "risk_level": level,
            "reasons": reasons
        }