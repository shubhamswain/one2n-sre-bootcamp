# One2N SRE Bootcamp

This repo serves as an attempt at the [One2N SRE Bootcamp](https://one2n.io/sre-bootcamp/sre-bootcamp-exercises) exercises. 


## Installation
1.) Clone the repo. 

2.) Add the below config files :

.env
```
SQLALCHEMY_DATABASE_URI='sqlite:///student2.db'
```

.flaskenv
```
FLASK_APP=app
FLASK_DEBUG=false
FLASK_ENV=prod
```

3.) Build and run the app using make

```bash
make all
```
