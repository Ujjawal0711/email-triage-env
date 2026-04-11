import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from email_triage_env.server.email_triage_env import EmailTriageEnvironment

TASK_NAME = "email-triage"
BENCHMARK = "v1"

env = EmailTriageEnvironment()

rewards = []
steps = 0

print(f"[START] task={TASK_NAME} env={BENCHMARK}")

try:
    obs = env.reset()
except Exception as e:
    print(f"[ERROR] reset failed: {e}")
    print("[END] success=False steps=0 score=0.00 rewards=[]")
    exit(0)

done = False

while not done and steps < 5:
    try:
        valid_actions = obs.get("valid_actions", ["analyze"])

        #deterministic action selection (CRITICAL)
        action = valid_actions[0] if valid_actions else "analyze"

        obs, reward, done = env.step(action)

        reward = float(reward)
        reward = max(0.0, min(reward, 1.0))  # clamp

    except Exception as e:
        print(f"[ERROR] step failed: {e}")
        break

    steps += 1
    rewards.append(round(reward, 2))

    print(
        f"[STEP] step={steps} action={action} "
        f"reward={reward:.2f} done={done} error=None"
    )

# safe score calculation
score = sum(rewards) / len(rewards) if rewards else 0.0
score = max(0.0, min(score, 1.0))

success = bool(done)

rewards_str = "[" + ",".join(f"{r:.2f}" for r in rewards) + "]"

print(
    f"[END] success={success} "
    f"steps={steps} score={score:.2f} rewards={rewards_str}"
)