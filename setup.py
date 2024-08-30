from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="prompt_execution_sdk",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "pydantic",
        "requests",
        "supabase",
        "typing-extensions",
        "PyYAML",
        "Jinja2"
    ],
    author="David Hague",
    author_email="david.hague@gmail.com",
    description="Retrieve and execute prompts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/davehague/prompt_execution_sdk",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
)
