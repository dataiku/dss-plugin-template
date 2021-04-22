# Plugin Template

This repository is a template for developers to create Dataiku DSS plugins from GitHub.

Use it and adapt it as you wish, and have fun with Dataiku!


# How to test your plugin

We recommend supporting your development cycle with unit and integration tests.
To operate integration tests, you will need the help of the `dataiku-plugin-tests-utils` package to automate their executions while targeting dedicated DSS instances.

`dataiku-plugin-tests-utils` will be installed as a `pytest plugin`. Install that package inside an environment dedicated to integration tests; otherwise, `pytest` will complain about unused fixtures inside your unit tests.

# How to install in your plugin

To install the `dataiku-plugin-tests-utils` package for your plugins, use the following line depending on your preferred way to managed packages.

## Using requirements.txt

### Development

```
git+git://github.com/dataiku/dataiku-plugin-tests-utils.git@<BRANCH>#egg=dataiku-plugin-tests-utils
```

Replace `<BRANCH>` with the most accurate value

### Stable release

```
git+git://github.com/dataiku/dataiku-plugin-tests-utils.git@releases/tag/<RELEASE_VERSION>#egg=dataiku-plugin-tests-utils
```

Replace `<RELEASE_VERSION>` with the most accurate value

## Using pipfile

Put the following line under `[dev-packages]` section

### Development cycle

```
dku-plugin-test-utils = {git = "git://github.com/dataiku/dataiku-plugin-tests-utils.git", ref = "<BRANCH>"}
```

### Stable release
TBD

## Dev env

### Config

First, ensure that you have personal API Keys for the DSS you want to target.
Secondly, define a config file that will give the DSS you will target.
```
{
	"DSSX":
	{
		"url": ".......",
		"users": {
			"usrA": "api_key",
			"usrB": "api_key",
			"default": "usrA"
		},
        "python_interpreter": ["PYTHON27", "PYTHON36"]

	},
	"DSSY":
	{
		"url": "......",
		"users": {
			"usrA": "api_key",
			"usrB": "api_key",
			"default": "usrB"
		},
        "python_interpreter": ["PYTHON36", "PYTHON39"]
	}
}

```

**BEWARE**: User names must be identical in the configuration file between the different DSS instances.
Then, set the environment variable `PLUGIN_INTEGRATION_TEST_INSTANCE` to point to the config file.

# How to use the package

## General information

To use the package in your test files:
```python
import dku_plugin_test_utils
import dku_plugin_test_utils.subpakcage.subsymbol
```
Look at the next section for more information about potential `subpackage` and `subsymbol`.

The python integration test files are indirections towards the "real" tests written as DSS scenarios on DSS instances.
The python test function triggers the targeted DSS scenario and waits either for its successful or failed completion.
Thence your test function should look like the following snippet :
```python
# Mandatory imports
from dku_plugin_test_utils import dss_scenario

def test_run_some_dss_scenario(user_dss_clients):
     dss_scenario.run(user_clients, 'PROJECT_KEY', 'scenario_id', user="user1")

# [... other tests ...]
```
With:
- `user_dss_clients`: representing the DSS client corresponding to the desired user.
- `PROJECT_KEY`: The project that holds the test scenarios
- `scenario_id`: The test scenario to run
- `user`: Specify the user to run the scenario with. It is an optional argument. By default, it is "default".

## How to generate a graphical report with Allure for integration tests

For each plugin, a folder named `allure_report` should exist inside the `test` folder; reports will be generated inside that folder.
To generate the graphical report, you must have Allure installed on your system as described [on their installation guide](https://docs.qameta.io/allure/#_manual_installation). Once the installation is done, run the following :
```shell
allure serve path/to/the/allure_report/dir/inside/you/plugin/test/folder/
```

# Package hierarchy

As it is a tooling package for integration tests, it will aggregate different packages with different goals. 
The following hierarchy exposes the different sub-package contained in `dku_plugin_test_utils` with their aim 
and the list of public symbols:

- `run_config`:
  - `ScenarioConfiguration`: Class exposing the parsed run configuration as a python dictionary.
  - `PluginInfo`: Parse the plugin.json and the code-env desc.json files to extract plugin metadata as a python dictionary.
- `dss_scenario`: 
  - `run`: Run the target DSS scenario and wait for its completion (either success or failure).
