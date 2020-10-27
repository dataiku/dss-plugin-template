import pytest
import dataikuapi
import subprocess

from dku_plugin_test_utils.run_config import ScenarioConfiguration
from dku_plugin_test_utils import get_plugin_info


def idfn(val):
    """
    Utilitary function that will alterate the display of test name.
    Here we will add the target value (DSS7, DSS8, DSSX) to the test name
    in order help recognize test runs against a specific DSS instance.
    You will get the following:
        test_run_read_zendesk_groups[DSS7]
        test_run_read_zendesk_groups[DSS8]

    Args:
        val (any): One value from the parametrization iterable.

    Returns:
        str: The str to display next to the testcase name
    """
    return val["target"]


def pytest_generate_tests(metafunc):
    """
    Pytest exposed hook allowing to dynamically alterate the pytest representation of a test which is metafunc
    Here we use that hook to dynamically paramertrize the "client" fixture of each tests. 
    Therefore, a new client will be instantiated for each DSS instance.

    Args:
        metafunc: pytest object representing a test function
    """
    run_config = ScenarioConfiguration()
    metafunc.parametrize("client", run_config.hosts, indirect=["client"], ids=idfn)


@pytest.fixture(scope="module")
def client(request):
    """
    The client fixture that is used by each of the test that will target a DSS instance.
    The scope of that fixture is set to module, so upon exiting a test module the fixture is destroyed

    Args:
        request: A pytest obejct allowing to introspect the test context. It allows us to access 
        the value of host set in `pytest_generate_tests`

    Returns:
        dssclient: return a instance of a DSS client. It will be the same reference for each test withing the associated context.
    """
    host = request.param
    return dataikuapi.DSSClient(host["url"], host["api_key"])


@pytest.fixture(scope="module")
def plugin(client):
    """
    The plugin fixture that is used by each of the test. It depends on the client fixture, as it needs to be 
    uploaded on the proper DSS instance.
    The scope of that fixture is set to module, so upon exiting a test module the fixture is destroyed

    Args:
        client: A DSS client instance.

    Todo:
        investigate a potential optimization, it seems to upload the plugin for each test.
    """
    subprocess.run(['make', 'plugin'], stdout=subprocess.PIPE)
    info = get_plugin_info()
    with open('dist/dss-plugin-' + info["id"] + '-' + info["version"] + '.zip', 'rb') as file:
        client.get_plugin(get_plugin_info()["id"]).update_from_zip(file)
