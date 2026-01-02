def is_time_overlap(a_start, a_end, b_start, b_end):
    return max(a_start, b_start) < min(a_end, b_end)

def detect_schedule_conflict(schedules):
    conflicts = []
    for i in range(len(schedules)):
        for j in range(i + 1, len(schedules)):
            s1 = schedules[i]
            s2 = schedules[j]
            if s1.hari == s2.hari and is_time_overlap(
                s1.jam_mulai, s1.jam_selesai,
                s2.jam_mulai, s2.jam_selesai
            ):
                if s1.ruangan == s2.ruangan:
                    conflicts.append({
                        "type": "room_conflict",
                        "affected": [s1.id, s2.id]
                    })
                if s1.dosen == s2.dosen:
                    conflicts.append({
                        "type": "lecturer_conflict",
                        "affected": [s1.id, s2.id]
                    })
    return conflicts