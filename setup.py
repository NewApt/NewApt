# Always prefer setuptools over distutils
from setuptools import setup
from pathlib import Path
import newapt
# Define the directory that setup.py is in
here = Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.rst').read_text(encoding='utf-8')

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
	name='newapt',  # Required
	version=newapt.__version__,  # Required
	description='a wrapper for the apt package manager.',  # Optional
	long_description=long_description,  # Optional
	long_description_content_type='text/reStructuredText',  # Optional (see note above)
	author='Anubhav Vardhan, Bhaskar',  # Optional
	author_email='vardhananubhav@gmail.com',  # Optional

	keywords='newapt, package management, apt',  # Optional
	packages=['newapt'],  # Required
	python_requires='>=3.6, <4',
	entry_points={  # Optional
		'console_scripts': [
			'newapt=newapt.__main__:main',
		],
	},

)