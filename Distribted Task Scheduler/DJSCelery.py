#Needs Rabbitmq and Celery and linux OS, Celery has problems with Windows OS
#sudo systemctl enable rabbitmq-server
#sudo rabbitmq-plugins enable rabbitmq_management ; can be found on localhost:15672 via browser ; login and pass "guest" "guest"
#Instructions: on bash type celery -A "file name" worker -l INFO , then go to python shell and import the functions
"""
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
"""

from __future__ import absolute_import
from celery import Celery
import sqlite3
import csv
import requests
app= Celery()
app.config_from_object('config')

#This function reads a csv file containing 1000 words, reading it line by line and stores the words in an sqlite database
@app.task #decorator for Celery to recognize this function
def insertMultipleRecords(filename):
    try:
        #opens sqlite3 connection
        sqliteConnection = sqlite3.connect('cdataBase.db')
        cursor = sqliteConnection.cursor()
        #confirms connection to the database
        print("Connected to SQLite")
        #fileContent is the list that contains the 1000 words
        fileContent=csv.reader(open(filename))
        # query to insert the words into the table
        sqlite_insert_query = """INSERT INTO myTable
                          (name) 
                          VALUES (?);"""
        #execute many is used to individually insert each line of text into the database
        cursor.executemany(sqlite_insert_query, fileContent)
        sqliteConnection.commit()
        #confirms if the query has been completed, otherwise, returns an error message
        print("Total", cursor.rowcount, "Records inserted successfully into myTable")
        #python does not autocommit every time it modifies a table so the commit() function is used everytime a change to the db is made
        sqliteConnection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert multiple records into sqlite table", error)
    finally:
        #Closes the connection to the database
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")

    """
    Run this script in pythonshell in the same directory after spawning Celery Worker
    from DJSCelery import insertMultipleRecords
    insertMultipleRecords.delay("wordlist.csv") # celery uses the .delay() function to execute tasks
    """













