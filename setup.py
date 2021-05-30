from setuptools import setup


def read_requirements():
    """Parse requirements from requirements.txt."""
    with open('requirements.txt', 'r') as f:
        requirements = [line.rstrip() for line in f]
    return requirements


setup(install_requires=read_requirements())
