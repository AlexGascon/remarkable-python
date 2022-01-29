from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path

from yaml import BaseLoader
from yaml import load as yml_load
from yaml import dump as yml_dump


@dataclass
class AuthCredentials:
    device_token: str
    user_token: str

    CONFIG_FILE_PATH = Path.joinpath(Path.home(), ".rmapi")

    @classmethod
    def create_from_file(cls) -> AuthCredentials:
        if Path.exists(cls.CONFIG_FILE_PATH):
            with open(cls.CONFIG_FILE_PATH, 'r') as config_file:
                config = dict(yml_load(config_file.read(), Loader=BaseLoader))
        
        return cls(config["devicetoken"], config["usertoken"])


    def save_to_file(self) -> None:
        """Saves itself to the .rmapy config file"""

        config = {"devicetoken": self.device_token, "usertoken": self.user_token}
        with open(self.CONFIG_FILE_PATH, 'w') as config_file:
            config_file.write(yml_dump(config))


