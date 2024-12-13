import yaml

from app.schemas import SerialSchemas, ServerSchemas

with open("app/config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

serial_config = SerialSchemas(**config["Robot-config"]["serial"])
qr_serial_config = SerialSchemas(**config["Robot-config"]["qr_serial"])
cam_serial_config = SerialSchemas(**config["Robot-config"]["cam_serial"])
server_config = ServerSchemas(**config["Robot-config"]["server"])
camera_config = config["Robot-config"]["camera"]
distance_config = config["Robot-config"]["distance"]
raybot_config = config["Robot-config"]["raybot"]
