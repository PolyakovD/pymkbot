import yaml

PARAMS_CONFIG_SCHEMA = {
    'nameplates-path': '../../data/names',
    'debug-image-size': [320, 240],
    'moves-lib-path': '../../data/moves',
    'menu-button': '../../data/button',
    'templates-path': '../../data/templates'
}


def read_config(filename):
    config = PARAMS_CONFIG_SCHEMA.copy()
    try:
        with open(filename, 'r') as yml_config:
            config.update(yaml.load(yml_config))
        params_config = ParamsConfig(nameplates_path=config['nameplates-path'],
                                     debug_image_size=config['debug-image-size'],
                                     moves_lib_path=config['moves-lib-path'],
                                     menu_button_path=config['menu-button-path'],
                                     templates_path=config['templates-path'])
        return params_config
    except:
        print("ERROR - no such file: " + filename)
        return DEFAULT_PARAMS_CONFIG


class ParamsConfig:
    def __init__(self,
                 nameplates_path=None,
                 debug_image_size=None,
                 moves_lib_path=None,
                 menu_button_path=None,
                 templates_path=None
                 ):
        self.nameplates_path = nameplates_path
        self.debug_image_size = debug_image_size
        self.moves_lib_path = moves_lib_path
        self.menu_button_path = menu_button_path
        self.templates_path = templates_path


DEFAULT_PARAMS_CONFIG = ParamsConfig()
