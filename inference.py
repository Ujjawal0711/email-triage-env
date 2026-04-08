from email_triage_env import EmailTriageEnvironment

env = EmailTriageEnvironment()

def predict():
    # simulate one run
    obs = env.reset()
    result = env.step()
    return {
        "observation": obs,
        "result": result
    }


if __name__ == "__main__":
    print(predict())