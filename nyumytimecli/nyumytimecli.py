import nyumytimecli.browser as browser
import click
import configparser
import os.path
import base64

def check_config_file(config_path=None):
	config = configparser.ConfigParser()
	if config_path is None:
		config_path = os.path.dirname(os.path.abspath(__file__)) + "/config.ini"
	config.read(config_path)
		
	default = config["DEFAULT"]

	if ("USERNAME" not in default or len(default["USERNAME"]) == 0):
		set_config_parameter("USERNAME", config, path=config_path)

	if ("PASSWORD" not in default or len(default["PASSWORD"]) == 0):
		set_config_parameter("PASSWORD", config, safe=True, path=config_path)

	if ("MFA_METHOD" not in default or len(default["MFA_METHOD"]) == 0):
		set_config_parameter("MFA_METHOD", config, options=['push', 'call'], path=config_path)


def set_config_parameter(name, config, safe=False, options=None, path=None, value=None):

	options_text = ""
	if options is not None:
		options_text = " [ {} ]".format(" / ".join(options))

	value = click.prompt("Please set the {} parameter{}".format(name,options_text), type=str, hide_input=safe)
	
	if safe:
		value = base64.b64encode(value.encode('utf-8')).decode('utf-8')

	if options is not None:
		if value not in options:
			click.secho("[error] Invalid option: {}. Choose between {}".format(value, ", ".join(options)), fg='red')
			set_config_parameter(name, config, safe=safe, options=options, path=path, value=value)

	config["DEFAULT"][name] = value
	if path is None:
		path = os.path.dirname(os.path.abspath(__file__)) + "/config.ini"

	with open(path,"w") as configfile:
		config.write(configfile)

@click.group()
def cli():
	pass

@click.command(name="in", help="Punch into the MyTime portal.")
def punchin():
	check_config_file()
	click.secho("[info] Performing punch-in operation...")
	if browser.punch_in():
		click.secho("[ ok ] Punch-in operation successful.", fg='green')
	else:
		click.secho("[error] Punch-in operation failed.", fg='red')

@click.command(name="out", help="Punch out of the MyTime portal.")
def punchout():
	check_config_file()
	click.secho("[info] Performing punch-out operation...")
	if browser.punch_out():
		click.secho("[ ok ] Punch-out operation successful.", fg='green')
	else:
		click.secho("[error] Punch-out operation failed.", fg='red')

@click.command(name="config", help="Set config variables.")
@click.argument("var_name", nargs=1, default=None, required=False)
@click.option("--config-path", nargs=1, default=None)
def config(var_name, config_path):

	if var_name is None:
		check_config_file(config_path=config_path)
		click.secho("[ ok ] Config verified.", fg="green")
	else:
		config = configparser.ConfigParser()
		if config_path is None:
			config_path = os.path.dirname(os.path.abspath(__file__)) + '/config.ini'
	
		config.read(config_path)

		var_name = var_name.lower()
		if var_name in ["login_url", "username", "password", "mfa_method"]:
			if var_name == "password":
				set_config_parameter(var_name, config, safe=True, path=config_path)
			elif var_name == "mfa_method":
				set_config_parameter(var_name, config, options=['push', 'call'], path=config_path)
			else:
				set_config_parameter(var_name, config, path=config_path)
		else:
			click.secho("[error] Invalid variable name: "+var_name, fg='red')

cli.add_command(punchin)
cli.add_command(punchout)
cli.add_command(config)