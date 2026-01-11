"""
Setup configuration for Formula Student Telemetry System
"""

from setuptools import setup, find_packages

with open("README_APP.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="fs-telemetry",
    version="1.0.0",
    author="Formula Student Community",
    author_email="contact@formulastudent.com",
    description="Real-time telemetry acquisition and analysis system for Formula Student vehicles",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marcle-bert26-ui/fs-telemetry",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "gui": ["PyQt5>=5.15.0"],
        "dev": [
            "pytest>=7.4.3",
            "pytest-cov>=4.1.0",
            "autopep8>=2.0.0",
            "pylint>=2.16.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "fs-telemetry=gui.main_window:main",
            "fs-telemetry-cli=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.csv", "*.txt"],
    },
)
