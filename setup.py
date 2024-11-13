from setuptools import setup, find_packages

setup(
    name="redis_plus",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "mmap-ninja>=1.0.0",
        "typing-extensions>=4.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-benchmark>=4.0.0",
        ],
    },
)