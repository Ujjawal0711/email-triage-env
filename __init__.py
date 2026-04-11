def grader_fn(output, expected):
    try:
        if not isinstance(output, dict) or not isinstance(expected, dict):
            return 0.0

        if (
            output.get("category") == expected.get("category") and
            output.get("priority") == expected.get("priority")
        ):
            return 1.0

        return 0.0

    except Exception:
        return 0.0


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

print("TASKS LOADED:", len(TASKS))