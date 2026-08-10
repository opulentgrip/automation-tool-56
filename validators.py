import re

class ValidationError(Exception):
    pass

class EmailValidator:
    def __init__(self):
        self.email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    def validate(self, email):
        if not isinstance(email, str):
            raise ValidationError('Email must be a string')
        if not re.match(self.email_pattern, email):
            raise ValidationError('Invalid email format')
        return True

class AgeValidator:
    def validate(self, age):
        if not isinstance(age, int):
            raise ValidationError('Age must be an integer')
        if age < 0 or age > 120:
            raise ValidationError('Age must be between 0 and 120')
        return True

class RegistrationValidator:
    def __init__(self):
        self.email_validator = EmailValidator()
        self.age_validator = AgeValidator()

    def validate(self, email, age):
        try:
            self.email_validator.validate(email)
            self.age_validator.validate(age)
        except ValidationError as e:
            return str(e)
        return 'Validation successful'

if __name__ == '__main__':
    validator = RegistrationValidator()
    print(validator.validate('test@example.com', 25))
    print(validator.validate('invalid-email', 25))
    print(validator.validate('test@example.com', -5))