from setuptools import setup, find_packages

setup(
	name="nyu-mytime-cli",
	varsion="0.1",
	packages=find_packages(),
	install_requires=[
		'click',
		'selenium'
	],
	entry_points='''
		[console_scripts]
		nyu-mytime=nyu_mytime_cli.nyu_mytime_cli:cli
	''',
)