from dataclasses import dataclass

from .cli import server_parser


@dataclass
class ServerConfiguration:
    host: str = "0.0.0.0"
    port: str = "5000"


__all__ = [
    "server_parser",
    "ServerConfiguration",
]
