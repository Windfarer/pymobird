from setuptools import setup, find_packages
from pymobird import __version__
setup(
    name = "pymobird",
    version = __version__,
    packages = find_packages(),
    install_requires = ['requests', 'Pillow'],
    author = "windfarer",
    author_email = "windfarer@gmail.com",
    description = "Memobird printer python client",
    license = "MIT",
    keywords = "memobird",
    url = "https://github.com/Windfarer/pymobird", 
)
