# Whenever we need any random data or mock data, we can simply call this calss

from faker import Faker
import random
import string

class RandomDataUtil:
    def __init__(self):
        self.faker = Faker()

    def get_first_name(self):
        return self.faker.first_name()

    def get_last_name(self):
        return self.faker.last_name()

    def get_full_name(self):
        return self.faker.full_name()

    def get_email(self):
        return self.faker.email()

    def get_phone_number(self):
        return self.faker.phone_number()

    def get_username(self):
        return self.faker.user_name()

    def get_password(self, length: int=10):
        return self.faker.password(length=length)

    def get_random_country(self):
        return self.faker.country()

    def get_random_state(self):
        return self.faker.state()

    def get_random_city(self):
        return self.faker.city()

    def get_random_pin(self):
        return self.faker.postalcode()

    def get_random_address(self):
        return self.faker.street_address()

    def get_random_alphanumeric(self, length:int):
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

    def get_random_numeric(self, length: int) -> str:
        return ''.join(random.choice(string.digits) for _ in range(length))

    def get_random_uuid(self) -> str:
        return str(self.faker.uuid4())