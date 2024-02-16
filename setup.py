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
    version="0.94",
    description="A GUI for lcapy",
    long_description=long_description,
    long_description_content_mattype="text/markdown",
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
        "lcapy>=1.17",
        "numpy",
        "tk",
        "pillow>=9.4.0",
        "matplotlib",
        "svgpathtools",
        "svgpath2mpl",
        "tkhtmlview",
        "pyshortcuts"
    ],
    extras_require={
          'doc': ['sphinx', 'ipython', 'sphinx-rtd-theme'],
          'release': ['pyinstaller'],
      },
    entry_points={
        'console_scripts': [
            'lcapy-tk=lcapygui.scripts.lcapytk:main',
            'sketchview=lcapygui.scripts.sketchview:main',
        ],
    },
    include_package_data=True,
    package_data={'': ['data/svg/*/*.svg', 'data/lib/*/*.sch', 'data/icon/*']},
    python_requires=">=3.7"  # matched with lcapy
)
