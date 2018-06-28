from setuptools import setup, find_packages

setup(
	name="nyumytimecli",
	varsion="0.1",
	packages=find_packages(),
	install_requires=[
		'click',
		'selenium'
	],
	entry_points='''
		[console_scripts]
		nyu-mytime=nyumytimecli.nyumytimecli:cli
	''',
)