import yaml
DEFAULT_CONFIG_PATH = "./config/config.yml"


def _loaded_tail():
    return ConfigLoader.config


def _load_tail():
    with open(DEFAULT_CONFIG_PATH, "r") as f:
        ConfigLoader.config = yaml.load(f, Loader=yaml.FullLoader)
    ConfigLoader.load_func = _loaded_tail

    return ConfigLoader.config


class ConfigLoader:
    config = None
    load_func = _load_tail

    @staticmethod
    def load():
        return ConfigLoader.load_func()
