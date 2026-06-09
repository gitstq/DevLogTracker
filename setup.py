from setuptools import setup, find_packages

setup(
    name="devlog-tracker",
    version="1.0.0",
    description="🚀 Intelligent Developer Log Tracker - Auto-capture, analyze and visualize your development workflow",
    author="Lobster Team",
    author_email="dev@lobster.team",
    url="https://github.com/gitstq/DevLogTracker",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click>=8.0.0",
        "rich>=13.0.0",
        "watchdog>=3.0.0",
        "pyyaml>=6.0",
        "jinja2>=3.1.0",
    ],
    entry_points={
        "console_scripts": [
            "devlog=devlog_tracker.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
)
