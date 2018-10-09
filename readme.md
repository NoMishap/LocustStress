# Locust Loading Test
Python3 application for testing the loading time for website and webservices in concurrency mode using [locust](https://locust.io).

It allows to simulate a number `c` of concurrently users and a number `r` of new users for second until `c`.


## Installation

```
git clone https://github.com/NoMishap/LocustStress.git

cd LocustStress

pip install locustio

```

## Run

This application can be run in two different mode:
    
- **standalone**: running in a single host
- **distribuited**: running on multiple hosts sharing the jobs between the hosts

In each mode you can run displaying the result in a web gui or simply in your console

Running without web gui means more parameters to be passed to the python script. These parameters are the same for each mode and they are:

- ``--no-web`` to disable the web gui
- ``-c=[number_of_users]`` `number_of_users` indicate the number of users to simulate (mandatory in no web gui mode)
- ``-r=[users_for_second]`` `users_for_second` indicate the number of new users each second (mandatory in no web gui mode)
- ``-t=[time]`` `time` indicate the time until the test will stop (eg. `-t=1h30m` execute for one hour and 30 minutes ) (optional)


#### Run: standalone
Run on your host
```
python locust_standalone.py -f=[locustfile.py] --host=[http://example.com]
```
Where:

- ``-f=[locustfile.py]`` indicate the locustfile to use, it must be inside the folder `src/locust_files`
- ``--host[http://example.com]`` indicate the host to be tested

Optionally you can add:

``-o=[output]`` `output` indicate the prefix to attach on output csv files the name will be `[output]_distribution.csv` and `[output]_requests.csv` (optional) (default: `test`)

#### Run: distributed
In distributed way you have to run on one main host the master and in the other hosts the slaves.

The master must be:

```
python locust_master.py -f=[locustfile.py] --host=[http://example.com] --master
```

The slaves must be:
```
python locust_slave.py -f=[locustfile.py] --host=[http://example.com] --master-host=[master_ip]
```

Note that both master and slaves must have the same locustfile