from app.services.api.exceptions import NotFoundException


class ConfigNotFoundException(NotFoundException):
    def __init__(self, section: str):
        super().__init__(f"Section '{section}' not found in configuration")
