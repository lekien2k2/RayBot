from pydantic import BaseModel


class SerialSchemas(BaseModel):
    port: str
    baudrate: int
    timeout: int
    bytesize: int
    parity: str
    stopbits: int


class ServerSchemas(BaseModel):
    host: str
    port: int
    timeout: int
    protocol: str
    path: str
    id: str
