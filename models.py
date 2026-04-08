from pydantic import BaseModel
from openenv.core.models import Action, Observation

class EmailTriageAction(Action):
    category: str  # "urgent" | "billing" | "spam" | "support" | "info"
    priority: str  # "high" | "medium" | "low"

class EmailTriageObservation(Observation):
    email_subject: str
    email_body: str
    sender: str
    language: str  # "en" or "hi-en" (Hinglish)
    step_count: int
    done: bool