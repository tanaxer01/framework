from setuptools import setup, find_packages

setup(
    name="framework",
    version="1.0.0",
    description="A module focused in creating random trafic and packaging into a quizz",
    packages=find_packages("."),
    install_requires=['scapy','pyyaml'],
    entry_points={'console_scripts':['framework-cli = framework.run:main']}
)
