import setuptools

setuptools.setup(
    name="ha-statusdisplay",
    version="0.0.0",
    description="MQTT topic discovery tool for Home Automation status display.",
    author="mgritz",
    packages=setuptools.find_packages(),
    py_modules=["__main__"],
    install_requires=[
        "paho-mqtt>=1.6.1",
        "Pillow",
        "Rpi.GPIO; platform_machine=='armv7l' or platform_machine=='aarch64'",
        "spidev; platform_machine=='armv7l' or platform_machine=='aarch64'",
    ],
    entry_points={
        "console_scripts": [
            "ha-statusdisplay=__main__:main"
        ]
    },
    python_requires=">=3.7",
)
