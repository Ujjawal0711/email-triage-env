def email_grader(trajectory, **kwargs):
    try:
        return {"score": 1.0}
    except Exception:
        return {"score": 0.0}