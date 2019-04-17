from setuptools import setup

setup(
    name='idrop-api',
    packages=['api'],
    include_package_data=True,
    license='GPLv3',
    install_requires=[
        'flask',
    ],
    tests_require=[
        'pytest',
    ],
)
