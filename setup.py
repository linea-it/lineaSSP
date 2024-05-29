from setuptools import find_packages, setup

with open("README.md") as fh:
    long_description = fh.read()

setup(
    name="lineaSSP",
    version="0.1.0",
    description="A Python module to use or retrieve information from the LIneA Solar System Portal.",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/linea-it/lineaSSP",
    author="LIneA Team",
    author_email="helpdesk@linea.org.br",
    license="MIT",
    setup_requires=["pytest-runner"],
    install_requires=["tqdm"],
    extras_require={
        "dev": ["pytest>=4.4.1", "twine>=4.0,<5.0"],
    },
    test_suite="tests",
    python_requires=">=3.8",
)
