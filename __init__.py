def grader_fn(*args):
    try:
        # --- Case 1: Hackathon validator (output, expected) ---
        if len(args) == 2:
            output, expected = args

            if not isinstance(output, dict) or not isinstance(expected, dict):
                return 0.0

            if (
                output.get("category") == expected.get("category") and
                output.get("priority") == expected.get("priority")
            ):
                return 1.0

            return 0.0

        # --- Case 2: RL trajectory ---
        if len(args) == 1:
            trajectory = args[0]

            if not isinstance(trajectory, dict):
                return 0.0

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


TASKS = [
    {
        "id": "task_1",
        "env": "v1",
        "input": {
            "email": "Win a free iPhone!!! Click now!!! Limited offer!!!"
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