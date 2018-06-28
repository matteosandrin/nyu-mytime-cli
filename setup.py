from setuptools import setup

setup(
	name="nyu-mytime-cli",
	varsion="0.1",
	py_modules=['nyu_mytime_cli','browser','helper'],
	install_requires=[
		'click',
		'selenium'
	],
	entry_points='''
		[console_scripts]
		nyu-mytime=nyu_mytime_cli:cli
	''',
)