from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="appwrite-utils",
    version="0.1.0",
    author="Dung Vu",
    author_email="hoangdung00275@gmail.com",
    description="A collection of utilities and extensions for Appwrite",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dung00275/appwrite-utils-python",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
            "pre-commit>=2.20.0",
        ],
    },
    keywords="appwrite, utilities, extensions, python",
    project_urls={
        "Bug Reports": "https://github.com/dung00275/appwrite-utils-python/issues",
        "Source": "https://github.com/dung00275/appwrite-utils-python",
        "Documentation": "https://github.com/dung00275/appwrite-utils-python#readme",
    },
) 