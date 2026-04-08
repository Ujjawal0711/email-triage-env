from fastapi import FastAPI
from email_triage_env import EmailTriageEnvironment
import uvicorn

app = FastAPI()
env = EmailTriageEnvironment()

@app.get("/")
def home():
    return {"message": "Email Triage Env Running"}

@app.post("/reset")
def reset():
    return env.reset()

@app.post("/step")
def step():
    return env.step()

def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()