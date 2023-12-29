import yaml

def get_config():
    with open("./publisher/config/config.yaml", "r") as yamlFileConfig:
        return yaml.safe_load(yamlFileConfig)
        