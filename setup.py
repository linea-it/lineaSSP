from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="lineaSSP",
    version="0.1.1",
    description="A Python module to use or retrieve information from the LIneA Solar System Portal.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/linea-it/lineaSSP",
    author="LIneA Team",
    author_email="helpdesk@linea.org.br",
    license="MIT",
    install_requires=[
        "numpy", 
        "scipy", 
        "sora-astro", 
        "astropy", 
        "cartopy", 
        "tqdm"
    ],
    extras_require={
        "dev": [
            "pytest>=4.4.1", 
            "twine>=4.0,<5.0"
        ],
    },
    test_suite="tests",
    python_requires=">=3.8",
    packages=find_packages(),  # No need for `where` or `package_dir`
)
