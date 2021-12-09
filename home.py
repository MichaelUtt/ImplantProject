def separatePatient(name):
    firstName = ""
    lastName = ""
    if "," in name:
        parts = name.split(",", 1)
        lastName = parts[0].strip()
        firstName = parts[1].strip()

    elif " " in name:
        parts = name.split(" ", 1)
        firstName = parts[0].strip()
        lastName = parts[1].strip()
    else:
        lastName = name

    return firstName, lastName

print(separatePatient("Michael Utt"))
