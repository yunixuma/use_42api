import sys, os, json
import datetime
from typing import Dict, Optional
import yaml
# from dotenv import load_dotenv

class _const(object):
    class ConstError(TypeError):
        pass
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError()
        self.__dict__[name] = value
sys.modules[__name__] = _const()

def __load_param(param_file: Optional[str] = None) -> Dict:
    if not param_file:
        param_file = f"{os.environ.get('PWD', '')}/param.yml"
    try:
        with open(param_file, "r") as file_stream:
            return yaml.load(file_stream, Loader=yaml.BaseLoader)
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file not found: {param_file}")
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing config file: {e}")

k = __load_param()
print(f"Loaded param: {k}")