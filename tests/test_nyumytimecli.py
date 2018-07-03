from nyumytimecli import nyumytimecli
from click.testing import CliRunner
import configparser
import pytest

@pytest.fixture()
def isolated_cli_runner():
	
	runner = CliRunner()
	with runner.isolated_filesystem():
		with open("config-test.ini", "w") as config_file:
			config_file.write("""
				[DEFAULT]
				login_url = https://test.url
				chromedriver_path = /usr/local/bin/chromedriver
				username = testUser
				password = testPassword
				mfa_method = testMethod
			""")
		yield runner

def test_setting_variable_in_config_command(isolated_cli_runner):
	
	isolated_cli_runner.invoke(nyumytimecli.config, ["USERNAME", "--config-path", "config-test.ini"], input="testPassed")
	config = configparser.ConfigParser()
	config.read("config-test.ini")
	assert "DEFAULT" in config
	assert "USERNAME" in config["DEFAULT"]
	assert config["DEFAULT"]["USERNAME"] == "testPassed"

def test_validating_configuration(isolated_cli_runner):

	result = isolated_cli_runner.invoke(nyumytimecli.config,["--config-path", "config-test.ini"])
	assert result.output == "[ ok ] Config verified.\n"