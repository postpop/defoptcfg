from setuptools import setup


setup(
    name='defoptcfg',
    version='0.1',
    py_modules=['defoptcfg', 'defopt_base'],
    # test_suite='test_defopt',
    install_requires=[
        'docutils',
        'sphinxcontrib-napoleon>=0.5.1',
    ],
    extras_require={
        ':sys.platform=="win32"': ['colorama>=0.3.4'],
    },
    keywords='argument parser parsing optparse argparse getopt docopt sphinx configargparse',
)
