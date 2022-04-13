from typing import NamedTuple, Optional

class Device(NamedTuple):
    name: str
    device_type: str
    host: str
    username: str
    password: str
    secret: Optional[str]
    port: int


