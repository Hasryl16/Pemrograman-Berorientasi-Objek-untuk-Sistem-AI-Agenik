from models import Course, Student, KRS
from validators import SKSValidator, PrerequisiteValidator, ConflictValidator, DuplicateValidator
from state_machine import KRSStateMachine, KRSStatus

def main():
    student = Student(nim="12345", lulus=["Matematika Dasar"])

    courses = [
        Course("Pemrograman Lanjut", 3, "Senin 08:00", "Algoritma"),
        Course("Algoritma", 3, "Senin 08:00"),
        Course("PBO", 3, "Selasa 10:00")
    ]

    krs = KRS(student, courses)

    # Validator chain
    v1 = SKSValidator()
    v2 = v1.set_next(PrerequisiteValidator())
    v3 = v2.set_next(ConflictValidator())
    v4 = v3.set_next(DuplicateValidator())

    result = v1.handle(krs)
    print(result)

    # State transitions
    machine = KRSStateMachine()
    print(machine)
    machine.transition(KRSStatus.SUBMITTED)
    machine.transition(KRSStatus.REVISION)
    machine.transition(KRSStatus.SUBMITTED)
    machine.transition(KRSStatus.APPROVED)
    print(machine)

if __name__ == "__main__":
    main()
