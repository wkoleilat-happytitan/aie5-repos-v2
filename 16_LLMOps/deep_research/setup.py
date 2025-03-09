from setuptools import setup, find_packages

setup(
    name="open_deep_research",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "langchain>=0.1.0",
        "langgraph>=0.0.15",
        "openai>=1.0.0",
    ],
) 