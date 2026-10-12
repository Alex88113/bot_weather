class ValidationEnvError(Exception):
    def __init__(self, reason: str) -> None:
        self.reason = reason
        message: str = f"Ошибка при подгрузке данных из секретного файла: {reason}"
        
        super().__init__(message)
