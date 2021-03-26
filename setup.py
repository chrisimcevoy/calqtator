import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name='calqtator',
    version='0.1.0',
    packages=['calqtator'],
    description='A simple calculator built with Qt bindings for Python',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/chrisimcevoy/calqtator',
    license='MIT',
    author='Chris McEvoy',
    author_email='chrisimcevoy@gmail.com',
    install_requires=["PySide6"],
    entry_points={
        'console_scripts': ['calqtator=calqtator.__main__:main'],
    },
)
