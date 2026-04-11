from server.email_triage_env import EmailTriageEnvironment


def grader_fn(obs):
    return (
        obs.get("category") is not None and
        obs.get("priority") is not None and
        obs.get("done") is True
    )


TASKS = [
    {
        "name": "email_triage_task_1",
        "env": EmailTriageEnvironment,
        "grader": grader_fn,
    },
    {
        "name": "email_triage_task_2",
        "env": EmailTriageEnvironment,
        "grader": grader_fn,
    },
    {
        "name": "email_triage_task_3",
        "env": EmailTriageEnvironment,
        "grader": grader_fn,
    },
]