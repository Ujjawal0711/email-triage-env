from fastapi import FastAPI
from email_triage_env import EmailTriageEnvironment

app = FastAPI()
env = EmailTriageEnvironment()

@app.get("/")
def home():
    return {
        "project": "Email Triage RL Environment 🚀",
        "endpoints": {
            "reset": "/reset",
            "step": "/step"
        }
    }

@app.post("/reset")
def reset():
    return env.reset()

@app.post("/step")
def step():
    return env.step()