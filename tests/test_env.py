"""Self-contained smoke tests for the email-triage environment.

These load the modules by file path so they run regardless of how (or whether)
the package is installed, and with no dependency on ``openenv``. Run either:

    python tests/test_env.py        # plain runner, exits non-zero on failure
    pytest tests/test_env.py        # standard pytest
"""

import importlib.util
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent


def _load(name, relpath):
    spec = importlib.util.spec_from_file_location(name, ROOT / relpath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_env_mod = _load("_ete_env", "server/email_triage_env.py")
_grader_mod = _load("_ete_grader", "graders.py")

EmailTriageEnvironment = _env_mod.EmailTriageEnvironment
email_grader = _grader_mod.email_grader

BILLING = {
    "subject": "Invoice overdue",
    "body": "Payment pending",
    "sender": "billing@saas.io",
    "category": "billing",
    "priority": "medium",
}


def _run_pipeline(env, actions):
    reward, done, obs = 0.0, False, None
    for action in actions:
        obs, reward, done = env.step(action)
    return obs, reward, done


def test_penalties_survive_clamp():
    """Regression guard: wrong actions must yield a *negative* reward.

    The old code clamped rewards to [0, 1], erasing every penalty."""
    env = EmailTriageEnvironment()
    env.reset(options={"email": BILLING})
    env.step("analyze")
    _, reward, _ = env.step("classify_spam")  # wrong category
    assert reward < 0, f"expected penalty, got {reward}"
    assert reward >= -1.0, "reward must stay within [-1, 1]"


def test_correct_pipeline_is_positive():
    env = EmailTriageEnvironment()
    env.reset(options={"email": BILLING})
    _, reward, done = _run_pipeline(
        env, ["analyze", "classify_billing", "set_priority_medium", "resolve"]
    )
    assert done is True
    assert reward > 0, f"correct resolution should reward, got {reward}"


def test_reset_uses_provided_email():
    env = EmailTriageEnvironment()
    env.reset(options={"email": "Invoice overdue"})  # matches a known email
    assert env.true_category == "billing"


def test_reset_default_is_random_and_valid():
    env = EmailTriageEnvironment()
    obs = env.reset()
    assert obs["valid_actions"] == ["analyze"]


def test_language_detection():
    env = EmailTriageEnvironment()
    env.reset(options={"email": {"subject": "bhai payment kar diya", "body": "pls check",
                                 "category": "support", "priority": "high"}})
    assert env._get_obs()["language"] == "hi-en"
    env.reset(options={"email": {"subject": "Monthly report", "body": "Usage summary",
                                 "category": "info", "priority": "low"}})
    assert env._get_obs()["language"] == "en"


def test_invalid_action_is_penalized_not_zeroed():
    env = EmailTriageEnvironment()
    env.reset(options={"email": BILLING})
    _, reward, _ = env.step("resolve")  # illegal before analyze
    assert reward < 0


def test_grader_scoring():
    assert email_grader([{"output": "category: billing, priority: medium"}],
                        {"category": "billing", "priority": "medium"}) == {"score": 1.0}
    assert email_grader([{"output": "category: billing"}],
                        {"category": "billing", "priority": "medium"}) == {"score": 0.5}
    assert email_grader([{"output": "nonsense"}],
                        {"category": "billing", "priority": "medium"}) == {"score": 0.0}
    assert email_grader([], {"category": "billing"}) == {"score": 0.0}


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failures = 0
    for test in tests:
        try:
            test()
            print(f"PASS  {test.__name__}")
        except AssertionError as exc:
            failures += 1
            print(f"FAIL  {test.__name__}: {exc}")
    print(f"\n{len(tests) - failures}/{len(tests)} passed")
    raise SystemExit(1 if failures else 0)
