from openenv.core.env_client import EnvClient
from email_triage_env.server.models import EmailTriageAction, EmailTriageObservation

class EmailTriageEnv(EnvClient):
    action_class = EmailTriageAction
    observation_class = EmailTriageObservation