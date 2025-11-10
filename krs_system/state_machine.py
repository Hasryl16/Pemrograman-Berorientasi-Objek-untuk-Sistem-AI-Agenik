from enum import Enum, auto

class KRSStatus(Enum):
    DRAFT = auto()
    SUBMITTED = auto()
    APPROVED = auto()
    REVISION = auto()


class InvalidTransitionError(Exception):
    pass


class KRSStateMachine:
    valid_transitions = {
        KRSStatus.DRAFT: [KRSStatus.SUBMITTED],
        KRSStatus.SUBMITTED: [KRSStatus.APPROVED, KRSStatus.REVISION],
        KRSStatus.REVISION: [KRSStatus.SUBMITTED],
        KRSStatus.APPROVED: []
    }

    def __init__(self, state=KRSStatus.DRAFT):
        self.state = state

    def transition(self, new_state):
        allowed = self.valid_transitions.get(self.state, [])
        if new_state not in allowed:
            raise InvalidTransitionError(f"Transisi tidak valid: {self.state.name} → {new_state.name}")
        print(f"✅ Transisi berhasil: {self.state.name} → {new_state.name}")
        self.state = new_state

    def __str__(self):
        return f"Status KRS saat ini: {self.state.name}"
