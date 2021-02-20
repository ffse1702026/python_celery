import os
from flask import Flask, flash, render_template, request, redirect, send_file, url_for
from celery import Celery
from celery.result import AsyncResult

app = Flask(__name__)
app.config.from_object("config")

# set up celery client
client = Celery(app.name, broker='redis://127.0.0.1:6379/0', backend='redis://127.0.0.1:6379/0')
# client.conf.update(app.config)

@client.task
def caculator():
    return 5


@app.route('/create', methods=['GET', 'POST'])
def index():
    task = caculator.delay()
    return task.id

@app.route('/get', methods=['GET', 'POST'])
def getData():
    id = request.args.get('id')
    print("========ID",id)
    task = client.AsyncResult(id )
    print('done', task.result)
    return "1"




if __name__ == '__main__':
    app.run(debug=True)
