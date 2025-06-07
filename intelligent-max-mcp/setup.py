"""
Setup configuration for Intelligent Max MCP Server
"""
from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

setup(
    name="intelligent-max-mcp",
    version="0.1.0",
    description="Intelligent Max/MSP MCP Server with living knowledge base",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Corrado (Coco) & Claude",
    author_email="",
    url="https://github.com/cocosberlucens/interleaved-max-minutiae",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Sound/Audio",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "anthropic-mcp-sdk>=0.1.0",
        "mcp>=0.1.0",
        "requests>=2.28.0",
        "jsonschema>=4.0.0",
        "pydantic>=2.0.0",
        "numpy>=1.21.0",
        "beautifulsoup4>=4.11.0",
        "lxml>=4.9.0",
        "gitpython>=3.1.0",
        "aiohttp>=3.8.0",
        "aiofiles>=22.0.0",
        "pyyaml>=6.0.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.20.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.10.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "mypy>=1.0.0",
            "flake8>=6.0.0",
            "pylint>=2.16.0",
            "pre-commit>=3.0.0",
            "sphinx>=6.0.0",
            "sphinx-rtd-theme>=1.2.0",
            "jupyter>=1.0.0",
            "notebook>=6.5.0",
            "ipykernel>=6.20.0",
        ],
        "jupyter": [
            "jupyter>=1.0.0",
            "notebook>=6.5.0",
            "ipykernel>=6.20.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "intelligent-max-mcp=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.yaml", "*.yml", "*.json", "*.md"],
    },
)