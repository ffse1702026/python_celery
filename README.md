#
Just me and Open sources
TechWorld with Hana
linuxacademy.com
vargrant --> VirtualBox --> create K8s
minikube



#TEST
import * as settle from 'axios/lib/core/settle';
// import * as settle from 'axios/lib/core/settle';
const adapter = async (config) => {
    var res = {sang: 123};
    console.log('config', config);

    return new Promise((resolse, reject) => {
        var response = {
            data: res, status: 200, config: config
        }
        settle(resolse, reject, response)
    })
}

export default adapter;

axios.defaults.adapter = adapter;
        axios.get('https://test/test', {
            params: {
              ID: 12345
            }
          }).then((res) => {
              console.log('resss', res)
          })


# REqurement
celery 5.0.5 
eventlet
set redis: 127.0.0.1


# command
celery -A app.client worker --loglevel=info -P eventlet
pip3 install flask-cors
run and test

celery -A test worker -l info -Ofair
flower -A app.client --port=5555
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object("config")
CORS(app)



[![HitCount](http://hits.dwyl.io/ro6ley/flask-celery-demo.svg)](http://hits.dwyl.io/ro6ley/flask-celery-demo)

# Ping! 

This repository contains the code for this [blogpost](https://stackabuse.com/asynchronous-tasks-using-flask-redis-and-celery/) on [StackAbuse](https://stackabuse.com/).

## Getting Started

### Prerequisites

Kindly ensure you have the following installed on your machine:

- [ ] [Python 3](https://realpython.com/installing-python/)
- [ ] [Pipenv](https://pipenv.readthedocs.io/en/latest/#install-pipenv-today)
- [ ] [Redis](http://redis.io/)
- [ ] Git
- [ ] An IDE or Editor of your choice

### Running the Application

1. Clone the repository
```
$ git clone https://github.com/ro6ley/flask-celery-demo.git
```

2. Check into the cloned repository
```
$ cd flask-celery-demo
```

3. If you are using Pipenv, setup the virtual environment and start it as follows:
```
$ pipenv install && pipenv shell
```

4. Install the requirements
```
$ pip install -r requirements.txt
```

4. Start the Flask app
```
$ python app.py
```

5. Start the Celery Cluster in a separate terminal window
```
$ celery worker -A app.client --loglevel=info
```

6. Start Flower in another separate terminal window
```
$ flower -A app.client --port=5555
```

7. Navigate to http://localhost:5000 and schedule an email with a message

8. Navigate to http://localhost:5555 to view the workers and scheduled messages under `Tasks` section

9. Check the receipient email inbox for the scheduled message after the time has ellapsed


## Contribution

Please feel free to raise issues using this [template](./.github/ISSUE_TEMPLATE.md) and I'll get back to you.

You can also fork the repository, make changes and submit a Pull Request using this [template](./.github/PULL_REQUEST_TEMPLATE.md).


import React from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import {updateTest} from '../actions/index'
import * as lodash from 'lodash'

class Test extends React.Component {
    constructor(props) {
      super(props);
      this.state = {data: 'ABC'}
    }
    static getDerivedStateFromProps(props, state) {
        let computed = {}
        computed.name = props.test.name
        computed.dataName = state.data
        return computed
    }
    getSnapshotBeforeUpdate(prevProps, prevState) {
        console.log('getSnapshotBeforeUpdate');
        return null;
    }

    updateTest = () => {
        this.props.updateTest({name: 'HA'})
    }
    componentDidMount= () => {
        console.log('componentDidmount');
    }

    shouldComponentUpdate(nextProps, nextState) {
        return true;
        
    }

    componentDidUpdate(preProps, preState) {
        console.log('componentDidUpdate');
    }
  
    render() {
        console.log('render', this.state);
      return (
          <div>
        <div onClick={this.updateTest}>{this.state.name}</div>
            <div onClick={() => this.setState({data: 'abc'})}>{this.state.dataName}</div>
        </div>
      );
    }
}

const mapStateToProps = (state)  => {
    console.log('state', state);
    return {
        test : state.cart.test
    }

}

export default connect(mapStateToProps, {updateTest})(Test)


# test
import os
from flask import Flask, flash, render_template, request, redirect, send_file, url_for, send_from_directory
from celery import Celery
from celery.result import AsyncResult
from flask_cors import CORS

app = Flask(__name__,static_url_path='')
app.config.from_object("config")
CORS(app)


# set up celery client
client = Celery(app.name, broker='redis://127.0.0.1:6379/0', backend='redis://127.0.0.1:6379/0')
# client.conf.update(app.config)

@client.task
def caculator():
    return 5


@app.route('/create', methods=['GET', 'POST'])
def index():
    task = caculator.delay()
    return render_template('build/index.html')

@app.route('/get', methods=['GET', 'POST'])
def getData():
    id = request.args.get('id')
    print("========ID",id)
    task = client.AsyncResult(id )
    print('done', task.result)
    return "1"

@app.route('/static/js/<path:path>')
def send_js(path):
    print('gothis', path)
    return send_from_directory('templates/build/static/js', path)




if __name__ == '__main__':
    app.run(debug=True)

