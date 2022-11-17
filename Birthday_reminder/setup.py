from importlib.metadata import entry_points
from setuptools import setup, find_namespace_packages

setup(name='birthday_reminder',
      version='1.0.1',
      description='Basic function to display user birthdays per week',
      url='https://github.com/DenysTantsiura/Denys-hw-8.git',
      author='Denys Tantsiura',
      author_email='tdv@tesis.kiev.ua',
      license='MIT',
      packages=find_namespace_packages(),
      entry_points={'console_scripts': ['bday = birthday_reminder.birthday_reminder:main']})

"""
The package is installed in the system by the command:
 pip install -e . 
 (or :
python setup.py install
, administrator rights are required!)
"""
