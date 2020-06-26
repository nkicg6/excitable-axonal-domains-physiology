from setuptools import setup

setup(
    name="thesis_ephys",
    version="0.1-dev",
    description="Analysis routines for patch clamp and extracellular electrophysiology.",
    packages=["lfp", "patch"],
    entry_points={"console_scripts": ["lfp = lfp.__main__:main"]},
)
