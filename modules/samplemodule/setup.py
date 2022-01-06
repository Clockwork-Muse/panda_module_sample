import sys

from skbuild import setup

setup(
    name="samplemodule",
    version="0.0.1",
    description="Sample module",
    author='Stephen A. Imhoff',
    license="MIT",
    packages=['samplemodule'],
    install_requires=['panda3d'],
)
