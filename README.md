[![Build Status](https://travis-ci.org/ansible-swagger-generator/ansible-swagger-generator.svg?branch=master)](https://travis-ci.org/ansible-swagger-generator/ansible-swagger-generator)

# Running from source
Creating the virtual environment:
```
virtualenv asg
source ./asg/bin/activate
virtualenv --relocatable ./asg
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
pip install mock nose
```

Running tests
```
python setup.py nosetests
```

