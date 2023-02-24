from setuptools import setup, find_packages

# Open readme
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='lcapygui',
    packages=find_packages(include=[
        "lcapygui",
        "lcapygui.*"
    ]),
    version="0.4.1",
    description="A GUI for lcapy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Michael Hayes, Jordan Hay",
    license="MIT",
    url="https://github.com/mph-/lcapy-gui",
    project_urls={
        "Bug Tracker": "https://github.com/mph-/lcapy-gui",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "setuptools",
        "importlib",
        "importlib-metadata",
        "importlib-resources",
        "pathlib",
        "lcapy>=1.12",
        "numpy",
        "tk",
        "pillow>=9.4.0",
        "matplotlib",
        "svgpathtools",
        "svgpath2mpl",
        "tkhtmlview"
    ],
    entry_points={
        'console_scripts': [
            'lcapy-tk=lcapygui.scripts.lcapytk:main',
        ],
    },
    include_package_data=True,
    package_data={'': ['data/svg/*.svg']},
    python_requires=">=3.7"  # matched with lcapy
)
