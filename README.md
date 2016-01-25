[![Build Status](https://travis-ci.org/ansible-swagger-generator/ansible-swagger-generator.svg?branch=master)](https://travis-ci.org/ansible-swagger-generator/ansible-swagger-generator)
[![Coverage
Status](https://coveralls.io/repos/github/ansible-swagger-generator/ansible-swagger-generator/badge.svg?branch=master)](https://coveralls.io/github/ansible-swagger-generator/ansible-swagger-generator?branch=master)

# Running from source
Creating the virtual environment:
```
virtualenv asg
source ./asg/bin/activate
python setup.py develop
```

Running the cli tool:
```
asg/bin/ansible-swagger-generator -s <path to swagger spec>
```

Exiting the virtualenv:
```
deactivate
```

# Running Tests
Install testing libraries
```
pip install -r test-requirements.txt
```

Running tests
```
python setup.py nosetests
python setup.py flake8
```

