Needs Rabbitmq and Celery and linux OS, Celery has problems with Windows OS

sudo systemctl enable rabbitmq-server

sudo rabbitmq-plugins enable rabbitmq_management ; can be found on localhost:15672 via browser ; login and pass "guest" "guest"

Instructions: on bash type celery -A "file name" worker -l INFO , then go to python shell and import the functions

This example attempts to demonstrate a Distributed Job Scheduler / Task Queue using Celery. Rabbitmq is used as the message broker and sqlite as the backend
to store data.

Celery along with rabbitmq allows multiple machines to work on a given task provided that the machines have:

1.) Have the ip add of machine 1 in the broker url:

app = Celery('tasks', backend='amqp',

broker='amqp://<user>:<password>@<ip>/<vhost>')
  
2.) Configure RabbitMQ for other machines to connect to it in the terminal

sudo rabbitmqctl add_user <user> <password>
  
sudo rabbitmqctl add_vhost <vhost_name>

sudo rabbitmqctl set_permissions -p <vhost_name> <user> ".*" ".*" ".*" 
  
sudo rabbitmqctl restart

3.) Copy this file on other machines then run a worker to consume the tasks
