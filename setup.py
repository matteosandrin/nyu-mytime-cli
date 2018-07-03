from setuptools import setup, find_packages

setup(
	name="nyumytimecli",
	varsion="1.0",
	packages=find_packages(),
	install_requires=[
		'click',
		'selenium'
	],
	entry_points='''
		[console_scripts]
		nyu-mytime=nyumytimecli.nyumytimecli:cli
	''',
	setup_requires=["pytest-runner"],
    tests_require=["pytest"],
)