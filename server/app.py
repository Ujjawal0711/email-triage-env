from openenv.core.env_server import create_app
from server.email_triage_environment import EmailTriageEnvironment
from models import EmailTriageAction, EmailTriageObservation

env = EmailTriageEnvironment()
app = create_app(env, EmailTriageAction, EmailTriageObservation)