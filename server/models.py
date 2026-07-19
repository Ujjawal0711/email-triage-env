from openenv.core.models import Action, Observation

class EmailTriageAction(Action):
    action: str

class EmailTriageObservation(Observation):
    email_subject: str
    email_body: str
    sender: str
    language: str

    analyzed: bool
    category: str | None
    priority: str | None

    step_count: int
    done: bool

    # Fields the environment also emits in its observation dict. Kept optional
    # so the model stays constructible from a partial/uninitialized observation.
    stage: str | None = None
    analysis: str | None = None
    valid_actions: list[str] = []