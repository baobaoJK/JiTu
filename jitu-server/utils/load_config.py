import yaml

CONFIG_FILE = "config.yml"


def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        config_yaml = yaml.safe_load(file)  # 安全加载 YAML
    return config_yaml


def save_config(data):
    """保存配置到 YAML 文件"""
    with open(CONFIG_FILE, "w", encoding="utf-8") as file:
        yaml.dump(data, file, allow_unicode=True, default_flow_style=False, sort_keys=False)


def get_upload_folder():
    config = load_config()
    return config['server']['upload-folder']
