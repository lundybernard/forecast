from dataclasses import dataclass

from .server import ServerConfiguration


@dataclass
class GlobalConfig:
    # example module with configuration dataclass
    server: ServerConfiguration
