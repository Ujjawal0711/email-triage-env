email-triage-env is an OpenEnv-compatible reinforcement learning environment that simulates a real-world customer support email routing system.
An RL agent receives an inbound email as an observation and must act as an intelligent routing system — predicting both the category and the priority of the email.
The key differentiator: the dataset is bilingual, covering both English and Hinglish (Hindi-English code-switching), making this environment uniquely relevant for AI systems deployed in the Indian tech ecosystem. Most NLP benchmarks and RL environments are English-only. This project challenges that by forcing agents to generalize across languages that real users actually write in.

The Task
The agent operates as a 3-step sequential decision pipeline:
StepTaskDescription1Email AnalysisParse and understand the inbound email content2Category ClassificationRoute to one of: urgent · billing · spam · support · info3Priority AssignmentAssign one of: high · medium · low
Example Tasks
python# From tasks.py
{"email": "Win a free iPhone!!!"}           → category: spam,    priority: low
{"email": "Production server is down ASAP!"} → category: urgent,  priority: high
{"email": "Invoice overdue payment pending"} → category: billing, priority: medium

Reward Function
The grader evaluates the agent's trajectory output against ground truth:
OutcomeScoreCorrect category AND priority+1.0Correct category OR priority (partial match)+0.5Incorrect classification0.0Exception / malformed output0.0
The grader is implemented in graders.py and is dual-mode compatible — it works with both the OpenEnv hackathon validator API and standard RL trajectory evaluation conventions.

Architecture
email-triage-env/
├── server/
│   ├── email_triage_env.py   # EmailTriageEnvironment class (OpenEnv core)
│   ├── models.py             # EmailTriageObservation, EmailTriageAction (Pydantic)
│   └── client.py             # HTTP client for the environment server
├── graders.py                # Dual-mode grader function
├── tasks.py                  # TASKS list with ground truth + grader bindings
├── models.py                 # Re-exports from server/models.py
├── client.py                 # Re-exports from server/client.py
├── openenv.yaml              # OpenEnv spec (entry points, categories, schema)
├── pyproject.toml            # Package config with openenv entry points
├── Dockerfile                # Docker deployment
└── push_it.py                # HuggingFace Space push script
Key Components
EmailTriageEnvironment
The core OpenEnv environment class. Exposes reset() and step(action) following the OpenEnv interface. Accepts an EmailTriageObservation and expects an EmailTriageAction containing predicted category and priority.
email_grader
A trajectory-based grader that inspects the last step of an RL trajectory, extracts the agent's output, and performs substring matching against the ground truth. Handles malformed trajectories gracefully by returning score: 0.0.
openenv.yaml
The environment spec file that registers the environment and task list with the OpenEnv ecosystem under the workflow and nlp categories.

Quickstart
1. Install
bashgit clone https://github.com/Ujjawal0711/email-triage-env.git
cd email-triage-env
pip install -e .
2. Run with Docker
bashdocker build -t email-triage-env .
docker run -p 8000:8000 email-triage-env
3. Use the environment directly
pythonfrom email_triage_env.server.email_triage_env import EmailTriageEnvironment
from email_triage_env.server.models import EmailTriageAction

env = EmailTriageEnvironment()
obs = env.reset(options={"email": "Mera bill kyun double aaya? Please help!"})

action = EmailTriageAction(category="billing", priority="high")
obs, reward, done, info = env.step(action)

print(f"Reward: {reward}")  # 1.0, 0.5, or 0.0
4. Run the grader manually
pythonfrom email_triage_env.graders import email_grader

trajectory = [{"output": "category: billing, priority: high"}]
ground_truth = {"category": "billing", "priority": "high"}

result = email_grader(trajectory, ground_truth)
print(result)  # {"score": 1.0}

OpenEnv Integration
This environment is fully spec-compliant with OpenEnv. The openenv.yaml registers:
yamlname: email-triage-env
version: 0.1.0
tasks:
  entry_point: email_triage_env.tasks:TASKS
envs:
  v1:
    entry_point: email_triage_env.server.email_triage_env:EmailTriageEnvironment
    action: EmailTriageAction
    observation: EmailTriageObservation
Entry points are also declared in pyproject.toml for discovery by the OpenEnv CLI.

Dependencies
PackagePurposefastapiHTTP server for the environmentuvicornASGI serverpydanticObservation/Action schema validationopenenv-core >= 0.2.0OpenEnv base classes and spec

Requires Python 3.10+


Why Bilingual?
India has over 500 million English-Hindi code-switchers. Phrases like "yaar mera bill kyun aaya" or "server down ho gaya ASAP fix karo" are completely normal in real customer support queues — but most RL environments and NLP benchmarks are built exclusively on clean English data.
This environment is a small step toward evaluation infrastructure that reflects how people in India actually communicate. Agents that score well here have genuinely learned to handle linguistic diversity, not just English pattern matching.

Built With

Python + PyTorch ecosystem
FastAPI + Uvicorn — environment server
Pydantic — typed observation/action schemas
OpenEnv — RL environment spec
Docker — containerized deployment


Author
Ujjawal Chaudhary — B.Tech Computer Science
