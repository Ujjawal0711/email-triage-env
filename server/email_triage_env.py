import random

EMAILS = [
    {"subject": "URGENT: Production server down!", "body": "Server crashed. Fix ASAP.", "sender": "ops@company.com", "category": "urgent", "priority": "high"},
    {"subject": "Invoice overdue", "body": "Payment pending ₹4999", "sender": "billing@saas.io", "category": "billing", "priority": "medium"},
    {"subject": "You won ₹10,00,000!", "body": "Click to claim prize", "sender": "spam@fake.com", "category": "spam", "priority": "low"},
    {"subject": "App crash ho raha hai", "body": "Android app crash", "sender": "user@gmail.com", "category": "support", "priority": "medium"},
    {"subject": "Monthly report", "body": "Usage summary", "sender": "reports@company.com", "category": "info", "priority": "low"},
]

def auto_classify(email):
    text = (email["subject"] + " " + email["body"]).lower()

    if any(word in text for word in ["crash", "down", "fail", "error"]):
        return "support", "medium"

    if any(word in text for word in ["urgent", "critical", "immediate"]):
        return "urgent", "high"

    if any(word in text for word in ["invoice", "payment", "refund"]):
        return "billing", "medium"

    if any(word in text for word in ["won", "free", "offer"]):
        return "spam", "low"

    return "info", "low"


class EmailTriageEnvironment:
    def __init__(self):
        self.current_email = None
        self.step_count = 0
        self.total_reward = 0
        self.episodes = 0

    def reset(self):
        self.current_email = random.choice(EMAILS)
        self.step_count = 0

        return {
            "email_subject": self.current_email["subject"],
            "email_body": self.current_email["body"],
            "sender": self.current_email["sender"],
            "step_count": self.step_count,
            "done": False
        }

    def step(self, action=None):
        self.step_count += 1

        # 🔥 AUTO prediction (no manual input needed)
        pred_category, pred_priority = auto_classify(self.current_email)

        correct_category = pred_category == self.current_email["category"]
        correct_priority = pred_priority == self.current_email["priority"]

        if correct_category and correct_priority:
            reward = 1.0
        elif correct_category or correct_priority:
            reward = 0.5
        else:
            reward = -1.0

        # 🔥 Track performance
        self.total_reward += reward
        self.episodes += 1

        return {
            "email": self.current_email,
            "prediction": {
                "category": pred_category,
                "priority": pred_priority
            },
            "actual": {
                "category": self.current_email["category"],
                "priority": self.current_email["priority"]
            },
            "reward": reward,
            "stats": {
                "episodes": self.episodes,
                "total_reward": self.total_reward,
                "avg_reward": self.total_reward / self.episodes
            },
            "done": True
        }