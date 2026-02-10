def check_gmp(data):
    issues = []
    if not (18 <= data["temperature"] <= 25):
        issues.append("Temperature out of GMP range")
    if not (40 <= data["humidity"] <= 60):
        issues.append("Humidity out of GMP range")
    if data["particle_count"] > 3500:
        issues.append("High particle count")
    return issues
