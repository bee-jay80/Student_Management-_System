import secrets
def generate_unique_password():
    upperCase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lowerCase = "abcdefghijklmnopqrstuvwxyz"
    numbers = "123456789"
    characters = upperCase + lowerCase + numbers

    from .models import Student
    password = ''
    while True:
        password = ''.join(secrets.choice(characters) for _ in range(12))
        if not Student.objects.filter(password=password).exists():
            break
    return password