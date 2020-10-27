import pytest
import dataikuapi
import subprocess

from dku_plugin_test_utils.run_config import ScenarioConfiguration
from dku_plugin_test_utils import get_plugin_info


@pytest.fixture(scope="session")
def client():
    run_config = ScenarioConfiguration()
    if run_config.host and run_config.api_key:
        return dataikuapi.DSSClient(run_config.host, run_config.api_key)
    else:
        raise ValueError("Either host[{}] or api_key[{}] is undefined".format(run_config.host, run_config.api_key))


@pytest.fixture(scope="session")
def plugin(client):
    subprocess.run(['make', 'plugin'], stdout=subprocess.PIPE)
    info = get_plugin_info()
    with open('dist/dss-plugin-' + info["id"] + '-' + info["version"] + '.zip', 'rb') as file:
        client.get_plugin(get_plugin_info()["id"]).update_from_zip(file)
