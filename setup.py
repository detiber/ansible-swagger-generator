from setuptools import setup

setup(
    name="ansible-swagger-generator",
    version="0.0.1",
    author="Jason DeTiberus",
    author_email="jdetiber@redhat.com",
    description=("Generate Ansible Modules form a Swagger spec"),
    license="Apache License, Version 2.0",
    keywords="Ansible Swagger",
    url="https://github.com/ansible-swagger-generator/ansible-swagger-generator",
    packages=['swagger'],
    install_requires=['click', 'requests', 'six', 'pyRFC3339', 'pytz'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "Environment :: Console",
        'Programming Language :: Python :: 2.7',
        "License :: OSI Approved :: Apache Software License",
    ],
    # use_2to3=True,
    tests_require=['nose', 'coverage', 'flake8'],
    test_suite='nose.collector',
    entry_points={
        'console_scripts': [
            'ansible-swagger-generator=cli.cli:cli'
        ]
    }
)
