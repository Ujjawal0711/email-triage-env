def grader_fn(output, expected):
    try:
        if not isinstance(output, dict) or not isinstance(expected, dict):
            return 0.0

        category_match = output.get("category") == expected.get("category")
        priority_match = output.get("priority") == expected.get("priority")

        if category_match and priority_match:
            return 1.0

        return 0.0

    except Exception:
        return 0.0


TASKS = [
    {
        "id": "task_1",
        "env": "v1",
        "input": {
            "email": "Win a free iPhone!!! Click now!!!"
        },
        "expected": {
            "category": "spam",
            "priority": "low"
        },
        "grader": grader_fn,
    },
    {
        "id": "task_2",
        "env": "v1",
        "input": {
            "email": "Reminder: Project meeting tomorrow at 10 AM"
        },
        "expected": {
            "category": "important",
            "priority": "high"
        },
        "grader": grader_fn,
    },
    {
        "id": "task_3",
        "env": "v1",
        "input": {
            "email": "Hey, are we still up for lunch?"
        },
        "expected": {
            "category": "normal",
            "priority": "medium"
        },
        "grader": grader_fn,
    },
]