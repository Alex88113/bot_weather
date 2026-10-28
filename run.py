class InvalidEmailAddress(Exception):
    def __init__(self, email: str, reason: str) -> None:
        self.email = email
        self.reason = reason
        super().__init__()

    def __str__(self) -> str:
        return f"Указанный email: {self.email} некорректен.\nПричина: {self.reason}"


def _validation_email_address(email: str) -> str:
    if not isinstance(email, str):
        raise InvalidEmailAddress(email, "неверный тип данных")

    clear_strip = email.strip()
    if not clear_strip:
        raise InvalidEmailAddress(email, "Поле с электронным адресом пустое")

    if "@" in clear_strip and "." in clear_strip:
        return clear_strip
    else:
        raise InvalidEmailAddress(email, "Email должен содержать спец символы: [@]  [.] ")


def get_valid_email(email) -> str:
    return _validation_email_address(email)

print(get_valid_email("sanya.kucheryavvk##@hbk.ru"))