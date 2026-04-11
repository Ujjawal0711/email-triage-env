import os
from openai import OpenAI
from server.email_triage_env import EmailTriageEnvironment

API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")

TASK_NAME = "email-triage"
BENCHMARK = "v1"

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY
)

env = EmailTriageEnvironment()

rewards = []
steps = 0

print(f"[START] task={TASK_NAME} env={BENCHMARK} model={MODEL_NAME}")

obs = env.reset()
done = False

while not done and steps < 5:
    valid_actions = obs.get("valid_actions", ["analyze"])

    try:
        prompt = f"""
You are an email triage agent.

Current state:
{obs}

Valid actions:
{valid_actions}

Choose EXACTLY one action from valid_actions.
Return ONLY the action string.
"""

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a precise decision-making agent."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        action = response.choices[0].message.content.strip()

    except Exception:
        # fallback (IMPORTANT: still safe)
        action = valid_actions[0]

    if action not in valid_actions:
        action = valid_actions[0]

    obs, reward, done = env.step(action)

    steps += 1
    reward = round(float(reward), 2)
    rewards.append(reward)

    print(
        f"[STEP] step={steps} action={action} "
        f"reward={reward:.2f} done={done} error=None"
    )

# compute score
score = sum(rewards) / len(rewards) if rewards else 0.0
score = max(0.0, min(score, 1.0))

success = done

rewards_str = "[" + ",".join(f"{r:.2f}" for r in rewards) + "]"

print(
    f"[END] success={success} "
    f"steps={steps} score={score:.2f} rewards={rewards_str}"
)