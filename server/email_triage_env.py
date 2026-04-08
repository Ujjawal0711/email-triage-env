import random
from openenv.core.environment import Environment
from models import EmailTriageAction, EmailTriageObservation

EMAILS = [
    # URGENT
    {"subject": "URGENT: Production server down!", "body": "Our main server crashed 10 mins ago. Users cannot login. Need immediate fix.", "sender": "ops@company.com", "category": "urgent", "priority": "high", "language": "en"},
    {"subject": "CRITICAL: Data breach detected", "body": "Security team found unauthorized access in DB logs. Immediate action required.", "sender": "security@company.com", "category": "urgent", "priority": "high", "language": "en"},
    {"subject": "Kal se app band ho jayega!", "body": "Hamara subscription expire ho raha hai kal. Abhi renew karo warna sab users affect honge.", "sender": "admin@startup.in", "category": "urgent", "priority": "high", "language": "hi-en"},
    {"subject": "Website completely down since 2 hours", "body": "All endpoints returning 502. Customers calling non-stop. Fix karo jaldi.", "sender": "cto@mybiz.in", "category": "urgent", "priority": "high", "language": "hi-en"},
    {"subject": "Payment gateway failure - orders stuck", "body": "All transactions failing since 3 PM. Revenue loss happening every minute.", "sender": "finance@shop.com", "category": "urgent", "priority": "high", "language": "en"},

    # BILLING
    {"subject": "Invoice #4521 is overdue", "body": "Your payment of ₹4,999 for the Pro plan was due on April 1st. Please pay to avoid service disruption.", "sender": "billing@saas.io", "category": "billing", "priority": "medium", "language": "en"},
    {"subject": "Subscription renew nahi hua", "body": "Aapka plan auto-renew fail ho gaya. Card update karein ya manually pay karein.", "sender": "accounts@app.in", "category": "billing", "priority": "medium", "language": "hi-en"},
    {"subject": "Refund request for order #8823", "body": "I was charged twice for the same order. Please process refund for ₹1,200 immediately.", "sender": "customer@gmail.com", "category": "billing", "priority": "medium", "language": "en"},
    {"subject": "GST invoice required for March", "body": "Hamein March month ki GST invoice chahiye accounts ke liye. Please send ASAP.", "sender": "accounts@firm.co.in", "category": "billing", "priority": "medium", "language": "hi-en"},
    {"subject": "Failed payment - plan downgraded", "body": "Your card ending in 4242 was declined. Your account has been moved to free tier.", "sender": "noreply@platform.com", "category": "billing", "priority": "high", "language": "en"},

    # SPAM
    {"subject": "You have WON ₹10,00,000!", "body": "Congratulations! Click here to claim your prize money. Limited time offer!!!", "sender": "winner@lotto-india.net", "category": "spam", "priority": "low", "language": "en"},
    {"subject": "Free iPhone 16 Pro - Grab Now!", "body": "First 100 respondents get a FREE iPhone. Just pay ₹99 shipping. Click NOW.", "sender": "promo@freegifts.xyz", "category": "spam", "priority": "low", "language": "en"},
    {"subject": "Lose 10kg in 7 days GUARANTEED", "body": "Doctor-approved fat burn secret. No diet. No exercise. Buy now at 90% off.", "sender": "health@miracle-slim.com", "category": "spam", "priority": "low", "language": "en"},
    {"subject": "Aapke account mein ₹50,000 transfer honge", "body": "SBI ke taraf se aapko selected kiya gaya hai. Link pe click karke claim karein.", "sender": "sbi-reward@phishing.in", "category": "spam", "priority": "low", "language": "hi-en"},
    {"subject": "Make ₹5000/day working from home!", "body": "Join our team and earn without any skills. No investment needed. Guaranteed income.", "sender": "jobs@easy-money.biz", "category": "spam", "priority": "low", "language": "en"},

    # SUPPORT
    {"subject": "Cannot reset my password", "body": "I've been trying to reset my password for 2 hours. The OTP never arrives. Please help.", "sender": "user123@gmail.com", "category": "support", "priority": "medium", "language": "en"},
    {"subject": "App crash ho raha hai", "body": "Android app version 2.3.1 mein open karte hi crash ho jata hai. Screenshot attach hai.", "sender": "priya.sharma@gmail.com", "category": "support", "priority": "medium", "language": "hi-en"},
    {"subject": "How do I export my data?", "body": "I want to download all my account data before deleting my account. Where is the export option?", "sender": "john.doe@outlook.com", "category": "support", "priority": "low", "language": "en"},
    {"subject": "Feature kaam nahi kar raha", "body": "Dashboard mein 'Export CSV' button click karne pe kuch nahi hota. Browser Chrome hai.", "sender": "rahul.v@company.in", "category": "support", "priority": "medium", "language": "hi-en"},
    {"subject": "Two-factor authentication issue", "body": "After enabling 2FA, I can't login anymore. The authenticator app shows wrong codes.", "sender": "techuser@mail.com", "category": "support", "priority": "high", "language": "en"},
    {"subject": "Dark mode nahi aa raha", "body": "Settings mein dark mode toggle ON kiya but UI change nahi hoti. Phone restart bhi kiya.", "sender": "anil.k@yahoo.in", "category": "support", "priority": "low", "language": "hi-en"},

    # INFO
    {"subject": "Q1 Product Roadmap Update", "body": "Here's a summary of what we shipped in Q1 and what's coming in Q2. No action needed.", "sender": "product@company.com", "category": "info", "priority": "low", "language": "en"},
    {"subject": "Maintenance window this Saturday", "body": "Scheduled downtime from 2 AM to 4 AM IST on April 12. No action needed from your end.", "sender": "ops@platform.io", "category": "info", "priority": "low", "language": "en"},
    {"subject": "Naye features aa gaye!", "body": "Is mahine humne 5 naye features launch kiye hain. Blog post aur release notes attached.", "sender": "newsletter@app.in", "category": "info", "priority": "low", "language": "hi-en"},
    {"subject": "Your monthly usage report - March 2026", "body": "You used 4,200 API calls this month. Your limit is 10,000. No action required.", "sender": "reports@api.service.com", "category": "info", "priority": "low", "language": "en"},
    {"subject": "Team ka new member join kiya", "body": "Anjali Mehta hamare design team mein aaj se join kar rahi hain. Welcome message bhej sakte ho!", "sender": "hr@company.in", "category": "info", "priority": "low", "language": "hi-en"},
]

class EmailTriageEnvironment(Environment):
    def __init__(self):
        self.current_email = None
        self._step_count = 0

    def reset(self) -> EmailTriageObservation:
        self.current_email = random.choice(EMAILS)
        self._step_count = 0
        return EmailTriageObservation(
            email_subject=self.current_email["subject"],
            email_body=self.current_email["body"],
            sender=self.current_email["sender"],
            language=self.current_email["language"],
            step_count=self._step_count,
            done=False,
        )

    def step(self, action: EmailTriageAction):
        self._step_count += 1
        correct_category = action.category == self.current_email["category"]
        correct_priority = action.priority == self.current_email["priority"]

        if correct_category and correct_priority:
            reward = 1.0
        elif correct_category or correct_priority:
            reward = 0.5
        else:
            reward = -1.0

        obs = EmailTriageObservation(
            email_subject=self.current_email["subject"],
            email_body=self.current_email["body"],
            sender=self.current_email["sender"],
            language=self.current_email["language"],
            step_count=self._step_count,
            done=True,
        )
        return obs, reward, True  # (observation, reward, done)

    def state(self):
        return {
            "step_count": self._step_count,
            "current_category": self.current_email["category"] if self.current_email else None,
            "current_priority": self.current_email["priority"] if self.current_email else None,
            "language": self.current_email["language"] if self.current_email else None,
        }