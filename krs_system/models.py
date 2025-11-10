class Course:
    def __init__(self, nama, sks, jadwal, prasyarat=None):
        self.nama = nama
        self.sks = sks
        self.jadwal = jadwal
        self.prasyarat = prasyarat


class Student:
    def __init__(self, nim, lulus=None):
        self.nim = nim
        self.lulus = lulus or []


class KRS:
    def __init__(self, student, courses=None):
        self.student = student
        self.courses = courses or []

    def total_sks(self):
        return sum(course.sks for course in self.courses)
