import yaml

from app.schemas import SerialSchemas, ServerSchemas


ALLOWED_KEYS = {
    "serial": ["port", "baudrate", "timeout", "bytesize", "parity", "stopbits"],
    "qr_serial": ["port", "baudrate", "timeout", "bytesize", "parity", "stopbits"],
    "cam_serial": ["port", "baudrate", "timeout", "bytesize", "parity", "stopbits"],
    "server": [
        "port",
        "host",
        "protocol",
        "path",
        "username",
        "password",
        "ssl",
        "id",
        "timeout",
    ],
}


def validate_key(section: str, key: str):
    if section not in ALLOWED_KEYS or key not in ALLOWED_KEYS[section]:
        raise ValueError(
            f"Key '{key}' in section '{section}' is not allowed for modification"
        )


class ConfigService:
    def __init__(self, config_file: str):
        self.config_file = config_file

    def load_config(self) -> dict:
        """Load the YAML configuration file."""
        with open(self.config_file, "r") as file:
            return yaml.safe_load(file)

    def save_config(self, config: dict):
        """Save the updated configuration back to the YAML file."""
        with open(self.config_file, "w") as file:
            yaml.dump(config, file, default_flow_style=False, allow_unicode=True)

    def update_config(self, *, section: str, key: str, value):
        """Update a specific key in the configuration."""
        config = self.load_config()
        if section not in config:
            raise ValueError(f"Section '{section}' not found in configuration")
        if key not in config[section]:
            raise ValueError(f"Key '{key}' not found in section '{section}'")

        # Update the key
        config[section][key] = value
        self.save_config(config)
        config = self.load_config()
        return config

    def get_config(self, *, section: str, key: str = None):
        config = self.load_config()
        if section not in config:
            raise ValueError(f"Section '{section}' not found in configuration")
        if key:
            if key not in config[section]:
                raise ValueError(f"Key '{key}' not found in section '{section}'")
            return config[section][key]
        return config[section]


config_service = ConfigService("app/config.yaml")


with open("app/config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

serial_config = SerialSchemas(**config_service.get_config(section="serial"))
qr_serial_config = SerialSchemas(**config_service.get_config(section="qr_serial"))
cam_serial_config = SerialSchemas(**config_service.get_config(section="cam_serial"))
server_config = ServerSchemas(**config_service.get_config(section="server"))
# raybot_config = config["Robot-config"]["raybot"]
# camera_config = config["Robot-config"]["camera"]
