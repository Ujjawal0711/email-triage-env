from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
from email_triage_env.server.email_triage_env import EmailTriageEnvironment
from email_triage_env.server.demo_page import DEMO_HTML
import uvicorn
import random

app = FastAPI()
env = EmailTriageEnvironment()


# ✅ OPTIONAL FIELD (IMPORTANT)
class StepRequest(BaseModel):
    action: Optional[str] = None


@app.get("/", response_class=HTMLResponse)
def home():
    # Interactive web demo (drives /reset, /step, /evaluate). The plain JSON
    # health check lives at /health for the RL harness / uptime probes.
    return DEMO_HTML


@app.get("/health")
def health():
    return {"message": "Email Triage RL Env Running"}


@app.post("/reset")
def reset():
    return {"observation": env.reset()}


@app.post("/step")
async def step(req: StepRequest, request: Request):
    try:
        action = req.action

        # fallback if Swagger / parsing fails
        if action is None:
            try:
                data = await request.json()
                if isinstance(data, dict):
                    action = data.get("action")
            except:
                action = None

        obs, reward, done = env.step(action)

        return {
            "observation": obs,
            "reward": reward,
            "done": done
        }

    except Exception as e:
        return {"error": str(e)}


@app.get("/state")
def state():
    return {"observation": env._get_obs()}


@app.get("/evaluate")
def evaluate():
    ACTIONS = [
        "analyze",
        "classify_urgent",
        "classify_billing",
        "classify_support",
        "classify_spam",
        "classify_info",
        "set_priority_high",
        "set_priority_medium",
        "set_priority_low",
        "resolve"
    ]

    episodes = 50
    rewards = []
    steps_list = []

    for _ in range(episodes):
        env.reset()
        done = False
        total = 0
        steps = 0

        while not done:
            action = random.choice(ACTIONS)
            _, r, done = env.step(action)
            total += r
            steps += 1

        rewards.append(total)
        steps_list.append(steps)

    return {
        "episodes": episodes,
        "avg_reward": sum(rewards) / episodes,
        "avg_steps": sum(steps_list) / episodes
    }


def main():
    uvicorn.run("email_triage_env.server.app:app", host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()