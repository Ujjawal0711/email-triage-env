"""email_triage_env package.

Re-export the canonical task list (with ground truth + grader bindings)
defined in tasks.py so ``from email_triage_env import TASKS`` works.
"""

from email_triage_env.graders import email_grader
from email_triage_env.tasks import TASKS

__all__ = ["TASKS", "email_grader"]
