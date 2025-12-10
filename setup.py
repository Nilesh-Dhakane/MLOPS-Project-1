from setuptools import setup, find_packages


with open("requirements.txt") as file:
    requirements = file.read().splitlines()


setup(
    name="MLOPS-1",
    version="0.1",
    author="Nilesh Dhakane",
    description="Hotel Reservation Prediction",
    packages=find_packages(),
    install_requires = requirements
)