from setuptools import setup

setup(
    name='idrop-api',
    version='0.2',
    packages=['api'],
    include_package_data=True,
    license='GPLv3',
    install_requires=[
        'flask',
        'flask-cors',
    ],
    tests_require=[
        'pytest',
    ],
)
