"""
Template for config.yml:

    x_api_token: {your_x_api_token}
    owner_name: {your_owner_name}
    app_name: {your_app_name}
    ipa: {your_ipa}

Note: use ipa key even if you have Android app
"""

from appcenterlib import AppCenterAPI
import yaml
import os
import zipfile
import wget

CONFIG_PATH = os.path.abspath('config.yml')


def download_app(app):
    download_uri = app.get_download_uri()
    build_path = wget.download(download_uri)
    try:
        with zipfile.ZipFile(build_path, 'r') as z:
            z.extract(f'build/{app.ipa}', os.curdir)
    except Exception as e:
        raise e
    finally:
        os.remove(build_path)


if __name__ == '__main__':
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError("File config.yml not found.")

    with open(CONFIG_PATH) as config_file:
        api_config = yaml.load(config_file)

    api = AppCenterAPI(**api_config)
    download_app(api)
