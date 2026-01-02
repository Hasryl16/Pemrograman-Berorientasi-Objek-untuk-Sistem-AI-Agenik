def suggest_alternative(conflict_schedule, available_slots):
    suggestions = []
    for slot in available_slots:
        if slot["kapasitas"] >= conflict_schedule.jumlah_mahasiswa:
            suggestions.append({
                "hari": slot["hari"],
                "jam": slot["jam"],
                "ruangan": slot["ruangan"],
                "reason": "Kapasitas cukup dan minim bentrok"
            })
        if len(suggestions) == 3:
            break
    return suggestions