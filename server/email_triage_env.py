import random

EMAILS = [
    {"subject": "URGENT: Production server down!", "body": "Server crashed. Fix ASAP.", "sender": "ops@company.com", "category": "urgent", "priority": "high"},
    {"subject": "Invoice overdue", "body": "Payment pending ₹4999", "sender": "billing@saas.io", "category": "billing", "priority": "medium"},
    {"subject": "You won ₹10,00,000!", "body": "Click to claim prize", "sender": "spam@fake.com", "category": "spam", "priority": "low"},
    {"subject": "App crash ho raha hai", "body": "Android app crash", "sender": "user@gmail.com", "category": "support", "priority": "medium"},
    {"subject": "Monthly report", "body": "Usage summary", "sender": "reports@company.com", "category": "info", "priority": "low"},
    {"subject": "bhai payment kar diya but still not working", "body": "pls check asap", "sender": "user2@gmail.com", "category": "support", "priority": "high"},
    {"subject": "FREE offer just for you!!!", "body": "limited time bro claim now", "sender": "spam2@fake.com", "category": "spam", "priority": "low"},
]


class EmailTriageEnvironment:
    def __init__(self):
        self.current_email = None
        self.state = None
        self.total_reward = 0
        self.episodes = 0
        self.max_steps = 5

    def reset(self):
        self.current_email = random.choice(EMAILS) or {}

        self.true_category = self.current_email.get("category", "")
        self.true_priority = self.current_email.get("priority", "")

        self.state = {
            "analyzed": False,
            "category": None,
            "priority": None,
            "analysis": None,
            "step_count": 0,
            "done": False
        }

        return self._get_obs()

    def step(self, action):
        if self.current_email is None or self.state is None:
            self.reset()
            return self._get_obs(), 0.0, False

        try:
            # normalize
            if isinstance(action, dict):
                action = action.get("action")

            if not isinstance(action, str):
                return self._get_obs(), -1.0, False

            if self.state["done"]:
                return self._get_obs(), 0.0, True

            reward = -0.05

            # step limit
            if self.state["step_count"] >= self.max_steps:
                self.state["done"] = True
                return self._get_obs(), reward - 1.0, True

            # penalties
            if action.startswith("classify") and not self.state["analyzed"]:
                reward -= 0.7

            if action.startswith("set_priority") and self.state["category"] is None:
                reward -= 0.7

            # analyze
            if action == "analyze":
                if not self.state["analyzed"]:
                    self.state["analyzed"] = True

                    text = (
                        self.current_email.get("subject", "") + " " +
                        self.current_email.get("body", "")
                    ).lower()

                    if "urgent" in text or "asap" in text:
                        self.state["analysis"] = "high urgency detected"
                    elif "invoice" in text or "payment" in text:
                        self.state["analysis"] = "billing related"
                    elif "crash" in text or "error" in text:
                        self.state["analysis"] = "technical issue"
                    else:
                        self.state["analysis"] = "general inquiry"

                    reward += 0.2
                else:
                    reward -= 0.2

            # classify
            elif action.startswith("classify"):
                if self.state["analyzed"]:
                    pred = action.split("_")[1] if "_" in action else None
                    if pred:
                        self.state["category"] = pred
                        reward += 0.5 if pred == self.true_category else -0.5

            # priority
            elif action.startswith("set_priority"):
                if self.state["category"] is not None:
                    pr = action.split("_")[-1] if "_" in action else None
                    if pr:
                        self.state["priority"] = pr
                        reward += 0.5 if pr == self.true_priority else -0.3

            # resolve
            elif action == "resolve":
                self.state["done"] = True

                if (
                    self.state["category"] == self.true_category and
                    self.state["priority"] == self.true_priority
                ):
                    reward += 1.0
                else:
                    reward -= 1.0

                self.total_reward += reward
                self.episodes += 1

            else:
                reward -= 0.2

            self.state["step_count"] += 1

            return self._get_obs(), reward, self.state["done"]

        except Exception:
            return self._get_obs(), -1.0, True

    def _get_obs(self):
        if self.current_email is None or self.state is None:
            return {
                "message": "env not initialized",
                "valid_actions": ["analyze"]
            }

        return {
            "email_subject": self.current_email.get("subject", ""),
            "email_body": self.current_email.get("body", ""),
            "sender": self.current_email.get("sender", ""),
            "language": "hi-en" if "ho raha" in self.current_email.get("body", "") else "en",

            "analyzed": self.state.get("analyzed"),
            "analysis": self.state.get("analysis"),
            "category": self.state.get("category"),
            "priority": self.state.get("priority"),

            "step_count": self.state.get("step_count"),
            "done": self.state.get("done"),

            "valid_actions": self._get_valid_actions()
        }

    def _get_valid_actions(self):
        if self.state is None:
            return ["analyze"]

        if not self.state["analyzed"]:
            return ["analyze"]

        if self.state["category"] is None:
            return [
                "classify_urgent",
                "classify_billing",
                "classify_support",
                "classify_spam",
                "classify_info"
            ]

        if self.state["priority"] is None:
            return [
                "set_priority_high",
                "set_priority_medium",
                "set_priority_low"
            ]

        return ["resolve"]