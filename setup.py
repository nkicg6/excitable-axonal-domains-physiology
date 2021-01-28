from setuptools import setup


try:
    with open("README.md", "r") as f:
        readme = f.read()
except Exception as e:
    readme = "Couldn't find README. See: https://github.com/nkicg6/excitable-axonal-domains-physiology for README."

setup(
    name="thesis_ephys",
    version="0.6-submission",
    author="Nicholas George",
    description="Analysis routines for patch clamp and extracellular physiology.",
    long_description=readme,
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
