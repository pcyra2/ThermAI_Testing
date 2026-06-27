from setuptools import setup
# set up using "pip install -e ."
setup(
    name='AmoryQuantum',
    version='1.0',
    py_modules=['AmoryQuantum'],
    entry_points={
        'console_scripts': [
             "sp = AmoryQuantum.SinglePoint:main"
        ],
    },
    install_requires=["pyscf", "pyscf-dispersion", "numpy"]
)
