from setuptools import setup

setup(
   name='mftpclient',
   version='0.0.2',
   author='Vany Valentin Ingenzi',
   author_email='ingenzivany@gmail.com',
   packages=['mftpclient', 'mftpclient.test'],
   scripts=[],
   url='http://pypi.python.org/pypi/mftpclient/',
   license='LICENSE',
   description='A Minimal Mutlipath TCP FTP client',
   long_description=open('README.md').read()
)