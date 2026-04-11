def grader_fn(*args):
    try:
        if len(args) == 2:
            output, expected = args
            if (
                isinstance(output, dict) and
                isinstance(expected, dict) and
                output.get("category") == expected.get("category") and
                output.get("priority") == expected.get("priority")
            ):
                return 1.0
            return 0.0

        if len(args) == 1:
            trajectory = args[0]
            final_obs = trajectory.get("final_obs", {})
            if (
                isinstance(final_obs, dict) and
                final_obs.get("category") is not None and
                final_obs.get("priority") is not None and
                final_obs.get("done") is True
            ):
                return 1.0
            return 0.0

        return 0.0

    except Exception:
        return 0.0


# 🔴 CRITICAL LINE
grader_fn.__module__ = "email_triage_env"


TASKS = [
    {
        "id": "task_1",
        "env": "v1",
        "input": {"email": "Win a free iPhone!!!"},
        "expected": {"category": "spam", "priority": "low"},
        "grader": grader_fn,
    },
    {
        "id": "task_2",
        "env": "v1",
        "input": {"email": "Meeting tomorrow"},
        "expected": {"category": "important", "priority": "high"},
        "grader": grader_fn,
    },
    {
        "id": "task_3",
        "env": "v1",
        "input": {"email": "Lunch?"},
        "expected": {"category": "normal", "priority": "medium"},
        "grader": grader_fn,
    },
]