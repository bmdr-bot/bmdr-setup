"""Setup script for BMDR CLI."""

from setuptools import find_packages, setup

setup(
    name="bmdr-cli",
    version="0.1.0",
    description="BMDR CLI - Project scaffolding and management",
    author="BMDR",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "bmdr_cli": ["../templates/**/*"],
    },
    entry_points={
        "console_scripts": [
            "bmdr=bmdr_cli.commands:main",
        ],
    },
    python_requires=">=3.11",
    install_requires=[
        "fastapi>=0.109.0",
        "uvicorn[standard]>=0.27.0",
        "pydantic>=2.5.3",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.4",
            "pytest-asyncio>=0.23.3",
            "httpx>=0.26.0",
            "ruff>=0.1.9",
            "mypy>=1.8.0",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
    ],
)
