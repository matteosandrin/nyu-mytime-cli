from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
	name="nyumytimecli",
	version="0.0.4",
	author="Matteo Sandrin",
	long_description=long_description,
    long_description_content_type="text/markdown",
	description="A command-line interface for NYU's employee time-tracking website",
	url="https://github.com/matteosandrin/nyu-mytime-cli",
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
    include_package_data=True,
)