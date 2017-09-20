import yaml

PARAMS_CONFIG_SCHEMA = {
    'nameplates-path': './data/names',
    'debug-image-size': [320, 240]
}


def read_config(filename):
    config = PARAMS_CONFIG_SCHEMA.copy()
    try:
        with open(filename, 'r') as yml_config:
            config.update(yaml.load(yml_config))
        params_config = ParamsConfig(nameplates_path=config['nameplates-path'],
                                     debug_image_size=config['debug-image-size'])
        return params_config
    except:
        print("ERROR - no such file: " + filename)
        return DEFAULT_PARAMS_CONFIG


class ParamsConfig:
    def __init__(self,
                 nameplates_path=None,
                 debug_image_size=None
                 ):
        self.nameplates_path = nameplates_path
        self.debug_image_size = debug_image_size


DEFAULT_PARAMS_CONFIG = ParamsConfig()
