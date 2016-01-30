[![Build Status](https://travis-ci.org/ftl-toolbox/ansible-swagger-generator.svg?branch=master)](https://travis-ci.org/ftl-toolbox/ansible-swagger-generator)  
[![Coverage Status](https://coveralls.io/repos/github/ftl-toolbox/ansible-swagger-generator/badge.svg?branch=master)](https://coveralls.io/github/ftl-toolbox/ansible-swagger-generator?branch=master)  
[![Quantified Code](https://www.quantifiedcode.com/api/v1/project/8654f1411a88489cba96254b537d2180/badge.svg)](https://www.quantifiedcode.com/app/project/8654f1411a88489cba96254b537d2180)  
[![Code Climate](https://codeclimate.com/github/ftl-toolbox/ansible-swagger-generator/badges/issue_count.svg)](https://codeclimate.com/github/ftl-toolbox/ansible-swagger-generator)  
[![Stories in Ready](https://badge.waffle.io/ftl-toolbox/ansible-swagger-generator.svg?label=ready&title=Ready)](http://waffle.io/ftl-toolbox/ansible-swagger-generator)  


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

