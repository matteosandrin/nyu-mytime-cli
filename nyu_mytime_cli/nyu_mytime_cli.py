import nyu_mytime_cli.browser
import click
import configparser
import os.path
import base64

def check_config_file():
	config = configparser.ConfigParser()
	config.read(os.path.dirname(os.path.abspath(__file__)) + '/config.ini')
	default = config["DEFAULT"]

	if ("USERNAME" not in default or len(default["USERNAME"]) == 0):
		set_config_parameter("USERNAME", config)

	if ("PASSWORD" not in default or len(default["PASSWORD"]) == 0):
		set_config_parameter("PASSWORD", config, safe=True)

	if ("MFA_METHOD" not in default or len(default["MFA_METHOD"]) == 0):
		set_config_parameter("MFA_METHOD", config, options=['push', 'call'])


def set_config_parameter(name, config, safe=False, options=None):

	options_text = ""
	if options is not None:
		options_text = " [ {} ]".format(" / ".join(options))

	value = click.prompt("Please set the {} parameter{}".format(name,options_text), type=str, hide_input=safe)
	
	if safe:
		value = base64.b64encode(value.encode('utf-8')).decode('utf-8')

	if options is not None:
		if value not in options:
			click.echo("Invalid option: {}. Choose between {}".format(value, ", ".join(options)))
			set_config_parameter(name, config, safe=safe, options=options)

	config["DEFAULT"][name] = value

	with open("config.ini","w") as configfile:
		config.write(configfile)

@click.group()
def cli():
	pass

@click.command(name="in", help="Punch into the MyTime portal.")
def punchin():
	check_config_file()
	click.echo("Performing punch-in operation...")
	browser.punch_in()
	click.echo("Punch-in operation performed.")

@click.command(name="out", help="Punch out of the MyTime portal.")
def punchout():
	check_config_file()
	click.echo("Performing punch-out operation...")
	browser.punch_out()
	click.echo("Punch-out operation performed.")

@click.command(name="config", help="Set config variables.")
@click.argument("var_name", nargs=1, default=None, required=False)
def config(var_name):
	if var_name is None:
		check_config_file()
		click.echo("Config verified.")
	else:
		config = configparser.ConfigParser()
		config.read(os.path.dirname(os.path.abspath(__file__)) + '/config.ini')
		var_name = var_name.lower()
		if var_name in ["login_url", "username", "password", "mfa_method"]:
			if var_name == "password":
				set_config_parameter(var_name, config, safe=True)
			elif var_name == "mfa_method":
				set_config_parameter(var_name, config, options=['push', 'call'])
			else:
				set_config_parameter(var_name, config)
		else:
			click.echo("Invalid variable name:",var_name)


cli.add_command(punchin)
cli.add_command(punchout)
cli.add_command(config)
