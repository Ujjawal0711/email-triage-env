from email_triage_env.graders import email_grader

TASKS = [
    {
        "id": "task_1",
        "env": "email_triage_env",
        "input": {"email": "Win a free iPhone!!!"},
        "grader": email_grader,
    },
    {
        "id": "task_2",
        "env": "email_triage_env",
        "input": {"email": "Meeting tomorrow"},
        "grader": email_grader,
    },
    {
        "id": "task_3",
        "env": "email_triage_env",
        "input": {"email": "Lunch?"},
        "grader": email_grader,
    },
]