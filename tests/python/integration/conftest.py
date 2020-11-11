import pytest
import dataikuapi
import subprocess
import logging

from dku_plugin_test_utils.run_config import ScenarioConfiguration
from dku_plugin_test_utils.run_config import get_plugin_info
from dku_plugin_test_utils.logger import Log


# Entry point for integration test cession, load the logger configuration
Log()

logger = logging.getLogger("dss-plugin-test.zendesk.conftest")


def pytest_generate_tests(metafunc):
    """
    Pytest exposed hook allowing to dynamically alterate the pytest representation of a test which is metafunc
    Here we use that hook to dynamically paramertrize the "client" fixture of each tests. 
    Therefore, a new client will be instantiated for each DSS instance.

    Args:
        metafunc: pytest object representing a test function
    """
    run_config = ScenarioConfiguration()
    metafunc.parametrize("dss_target", run_config.targets, indirect=["dss_target"])


@pytest.fixture(scope="function")
def dss_target(request):
    """
    This is a parameterized fixture. Its value will be set with the different DSS target (DSS7, DSS8 ...) that are specified in the configuration file.
    It returns the value of the considered DSS target for the test. Here it is only used by other fixtures, but one could use it 
    as a test function parameter to access its value inside the test function.

    Args:
        request: The object to introspect the “requesting” test function, class or module context

    Returns:
        The string corresponding to the considered DSS target for the test to be executed
    """
    return request.param


@pytest.fixture(scope="function")
def user_clients(dss_clients, dss_target):
    """
    Fixture that narrows down the dss clients to only the ones that are relevant considering the curent DSS target.

    Args:
        dss_clients (fixture): All the instanciated dss client for each user and dss targets
        dss_target (fixture): The considered DSS target for the test to be executed

    Returns:
        A dict of dss client instances for the current DSS target and each of its specified users.
    """
    return dss_clients[dss_target]


@pytest.fixture(scope="package")
def dss_clients():
    """
    The client fixture that is used by each of the test that will target a DSS instance.
    The scope of that fixture is set to module, so upon exiting a test module the fixture is destroyed

    Args:
        request: A pytest obejct allowing to introspect the test context. It allows us to access 
        the value of host set in `pytest_generate_tests`

    Returns:
        dssclient: return a instance of a DSS client. It will be the same reference for each test withing the associated context.
    """
    dss_clients = {}
    run_config = ScenarioConfiguration()

    logger.info("Instanciating all the DSS clients for each user and DSS instance")
    for host in run_config.hosts:
        target = host["target"]
        dss_clients.update({target: {}})
        url = host["url"]
        for user, api_key in host["users"].items():
            dss_clients[target].update({user: dataikuapi.DSSClient(url, api_key=api_key)})

    return dss_clients


@pytest.fixture(scope="package")
def plugin(dss_clients):
    """
    The plugin fixture that is used by each of the test. It depends on the client fixture, as it needs to be 
    uploaded on the proper DSS instance.
    The scope of that fixture is set to module, so upon exiting a test module the fixture is destroyed

    Args:
        client: A DSS client instance.
    """

    logger.info("Uploading the pluging to each DSS instances [{}]".format(",".join(dss_clients.keys())))
    # TODO : uncomment below, there is an error that i do not understand right now
    # subprocess.run(['make', 'plugin'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # info = get_plugin_info()

    # with open('dist/dss-plugin-' + info["id"] + '-' + info["version"] + '.zip', 'rb') as fd:
    #     for target in dss_clients:
    #         admin_client = dss_clients[target]["admin"]
    #         admin_client.get_plugin(get_plugin_info()["id"]).update_from_zip(fd)
