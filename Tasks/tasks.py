def grader_fn(trajectory):
    try:
        if not trajectory:
            return 0.0
        
        # safe extraction
        rewards = trajectory.get("rewards", [])
        final_obs = trajectory.get("final_obs", {})

        success = (
            final_obs.get("category") is not None and
            final_obs.get("priority") is not None and
            final_obs.get("done") is True
        )

        if success:
            return 1.0
        
        return float(sum(rewards) / len(rewards)) if rewards else 0.0

    except Exception:
        return 0.0


TASKS = [
    {
        "id": "task_1",
        "env": "v1",
        "grader": grader_fn,
    },
    {
        "id": "task_2",
        "env": "v1",
        "grader": grader_fn,
    },
    {
        "id": "task_3",
        "env": "v1",
        "grader": grader_fn,
    },
]