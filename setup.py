from setuptools import setup

setup(
    name="thesis_ephys",
    version="0.5-presubmission",
    description="Analysis routines for patch clamp and extracellular physiology.",
    install_requires=[
        "numpy==1.19.2",
        "pyabf==2.2.8",
        "pytest==6.0.2",
        "matplotlib==3.3.2",
        "scipy==1.5.2",
    ],
    packages=["lfp", "patch_clamp"],
    entry_points={"console_scripts": ["lfp = lfp.__main__:main"]},
)
