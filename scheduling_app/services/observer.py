class Observer:
    def update(self, event):
        pass

class ScheduleSubject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self, event_type, data):
        for obs in self._observers:
            obs.update({"type": event_type, "data": data})

class StudentObserver(Observer):
    def update(self, event):
        print(f"[EMAIL] Mahasiswa notified: {event}")

class LecturerObserver(Observer):
    def update(self, event):
        print(f"[PUSH] Dosen notified: {event}")

class AdminObserver(Observer):
    def update(self, event):
        print(f"[LOG] Admin notified: {event}")