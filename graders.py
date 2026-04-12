def email_grader(trajectory, ground_truth=None, **kwargs):
    try:
        if not trajectory or not isinstance(trajectory, list):
            return {"score": 0.0}
        
        last = trajectory[-1] if trajectory else {}
        output = last.get("output", last.get("content", last.get("action", "")))
        output_str = str(output).lower()

        expected_category = (ground_truth or {}).get("category", "")
        expected_priority = (ground_truth or {}).get("priority", "")

        category_match = expected_category and expected_category in output_str
        priority_match = expected_priority and expected_priority in output_str

        if category_match and priority_match:
            return {"score": 1.0}
        elif category_match or priority_match:
            return {"score": 0.5}
        else:
            return {"score": 0.0}
    except Exception:
        return {"score": 0.0}