def grader_fn(output, expected):
    try:
        return (
            output.get("category") == expected.get("category") and
            output.get("priority") == expected.get("priority")
        )
    except Exception:
        return False


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