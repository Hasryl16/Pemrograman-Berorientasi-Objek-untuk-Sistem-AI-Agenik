from abc import ABC, abstractmethod

class ValidationResult:
    def __init__(self, success, message=""):
        self.success = success
        self.message = message

    def __str__(self):
        status = "PASS" if self.success else "FAIL"
        return f"[{status}] {self.message}"


class Validator(ABC):
    def __init__(self, next_validator=None):
        self._next = next_validator

    def set_next(self, next_validator):
        self._next = next_validator
        return next_validator

    def handle(self, krs):
        result = self.validate(krs)
        if not result.success:
            return result
        if self._next:
            return self._next.handle(krs)
        return ValidationResult(True, "Semua validasi berhasil!")

    @abstractmethod
    def validate(self, krs):
        pass


class SKSValidator(Validator):
    def validate(self, krs):
        total = krs.total_sks()
        if total > 24:
            return ValidationResult(False, f"Total SKS {total} > 24!")
        return ValidationResult(True, "Total SKS valid")


class PrerequisiteValidator(Validator):
    def validate(self, krs):
        for course in krs.courses:
            prasyarats = course.prasyarat if isinstance(course.prasyarat, list) else [course.prasyarat] if course.prasyarat else []
            for prasyarat in prasyarats:
                if prasyarat not in krs.student.lulus:
                    return ValidationResult(False, f"Belum lulus prasyarat {prasyarat} untuk {course.nama}")
        return ValidationResult(True, "Semua prasyarat terpenuhi")


class ConflictValidator(Validator):
    def validate(self, krs):
        jadwals = [c.jadwal for c in krs.courses]
        if len(jadwals) != len(set(jadwals)):
            return ValidationResult(False, "Terdapat bentrok jadwal!")
        return ValidationResult(True, "Tidak ada bentrok jadwal")


class DuplicateValidator(Validator):
    def validate(self, krs):
        names = [c.nama for c in krs.courses]
        if len(names) != len(set(names)):
            return ValidationResult(False, "Terdapat mata kuliah duplikat!")
        return ValidationResult(True, "Tidak ada duplikasi mata kuliah")
