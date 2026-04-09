import os
import random
from server.email_triage_env import EmailTriageEnvironment

API_BASE_URL = os.getenv("API_BASE_URL", "local")
MODEL_NAME = os.getenv("MODEL_NAME", "rule-based")
TASK_NAME = "email-triage"
BENCHMARK = "v1"

env = EmailTriageEnvironment()

rewards = []
steps = 0

print(f"[START] task={TASK_NAME} env={BENCHMARK} model={MODEL_NAME}")

obs = env.reset()
done = False

while not done and steps < 5:
    valid_actions = obs.get("valid_actions", ["analyze"])
    action = random.choice(valid_actions)

    obs, reward, done = env.step(action)

    steps += 1
    rewards.append(reward)

    print(
        f"[STEP] step={steps} action={action} "
        f"reward={reward:.2f} done={str(done).lower()} error=None"
    )

# compute score (normalized)
max_possible_reward = 5.0
score = sum(rewards) / max_possible_reward if max_possible_reward > 0 else 0
score = max(0.0, min(score, 1.0))

success = done

rewards_str = "[" + ",".join(f"{r:.2f}" for r in rewards) + "]"

print(
    f"[END] success={str(success)} "
    f"steps={steps} score={score:.2f} rewards={rewards_str}"
)