import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

install_requires = ["Click"]

setuptools.setup(
    name="cricpy",
    version="0.0.1",
    author="Sanchit Sreekanth",
    author_email="sanchitsreekanth@gmail.com",
    description="THe complete python package for cricket stats and analysis with historic data",
    url="https://github.com/sanchitsreekanth/cricpy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=install_requires,
    packages=setuptools.find_packages(exclude=["tests"]),
    include_package_data=True,
    package_data={
        "": ["data/*"]
    },
    entry_points={
        "console_scripts": [
            "cricpy=cricpy.scripts.main_script:cricpy_main"
        ]
    },
    python_requires=">=3.6"
)
