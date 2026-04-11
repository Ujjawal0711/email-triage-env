def grader_fn(trajectory):
    try:
        if not isinstance(trajectory, dict):
            return 0.0

        final_obs = trajectory.get("final_obs", {})
        rewards = trajectory.get("rewards", [])

        # Success condition
        if (
            isinstance(final_obs, dict) and
            final_obs.get("category") is not None and
            final_obs.get("priority") is not None and
            final_obs.get("done") is True
        ):
            return 1.0

        # Fallback: average reward if available
        if isinstance(rewards, list) and len(rewards) > 0:
            return float(sum(rewards) / len(rewards))

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