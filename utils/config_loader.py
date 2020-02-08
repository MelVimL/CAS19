import yaml

DEFAULT_CONFIG_PATH = "./config/config.yml"


def _loaded_tail():
    return ConfigLoader.config


def _fill_sim_with_default(name, sim, default):
    result = {"name": name}
    for key in default:
        if key not in sim:
            result.update({key: default[key]})
        else:
            result.update({key: sim[key]})

    return result


def _process_config(config):
    result = {}
    sim_conf = []

    for key in config:
        if not key == "simulations":
            result.update({key: config[key]})

    simulations = config["simulations"]

    for group in simulations:
        default = simulations[group]["default"]
        for sim in simulations[group]:
            if not sim == "default":
                sim_name = "{}_{}".format(group, sim)
                sim_conf.append(_fill_sim_with_default(sim_name, simulations[group][sim], default))
    result.update({"simulations": sim_conf})

    return result


def _load_tail():
    with open(DEFAULT_CONFIG_PATH, "r") as f:
        ConfigLoader.config = _process_config(yaml.load(f, Loader=yaml.FullLoader))

    ConfigLoader.load_func = _loaded_tail

    return ConfigLoader.config


class ConfigLoader:
    config = None
    load_func = _load_tail

    @staticmethod
    def load():
        return ConfigLoader.load_func()
