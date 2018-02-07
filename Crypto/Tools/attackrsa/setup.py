from setuptools import *

setup(
        name="attackrsa",
        version='1.0',
        install_requires=['gmpy'],
        packages=["attackrsa"],
        scripts=["/bin/attackrsa"]
)
