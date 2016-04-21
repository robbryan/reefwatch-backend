# reefwatch-backend

## Setup
You will need [Tornado](https://tornadoweb.org) light-weight, non-blocking webserver installed and some libraries

```
sudo apt-get install python-setuptools
sudo easy_install tornado
```

## Running

Most simply, you can just run the app with python and background it
```
python app.py &
```
You can then check that it is running by using curl or your favourite browser
```
curl http://localhost:9880
```

There are a multitude of command-line options you can pass too - Check documentation at http://tornadoweb.org for details
```
python app.py --port=8888 --logging=debug --debug=1 &
```
