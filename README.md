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

Install testing libraries
```
pip install mock nose
```

Running tests
```
python setup.py nosetests
```
