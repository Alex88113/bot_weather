from loguru import logger

logger.remove(0)


def create_debug_logger(filename: str) -> int:
    return logger.add(
        filename,
        rotation='500 MB',
        retention='10 days',
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        filter=lambda record: record['level'].name == "DEBUG",
    )


def create_info_logger(filename: str) -> int:
    return logger.add(
        filename,
        rotation='500 MB',
        retention='10 days',
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        filter=lambda record: record['level'].name == "INFO",
    )


def create_error_logger(filename: str) -> int:
    return logger.add(
        filename,
        rotation='500 MB',
        retention='10 days',
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        filter=lambda record: record['level'].name == "ERROR",
    )


def create_critical_error_logger(filename: str) -> int:
    return logger.add(
        filename,
        rotation='500 MB',
        retention='10 days',
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        filter=lambda record: record['level'].name == "CRITICAL",
    )


create_debug_logger('logs/debug.log')
create_info_logger("logs/app.log")
create_error_logger('logs/error.log')
create_critical_error_logger("logs/critical_error.log")

