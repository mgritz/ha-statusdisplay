import setuptools

setuptools.setup(
    name="ha-statusdisplay",
    version="0.0.0",
    description="MQTT topic discovery tool for Home Automation status display.",
    author="mgritz",
    packages=setuptools.find_packages(),
    py_modules=["__main__"],
    install_requires=[
        "paho-mqtt>=1.6.1"
    ],
    entry_points={
        "console_scripts": [
            "ha-statusdisplay=__main__:main"
        ]
    },
    python_requires=">=3.7",
)
