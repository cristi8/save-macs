#!/bin/bash

echo 'Copying current directory...'
ssh pi rm -rf _test
scp -q -r . pi:_test

echo 'Running test command...'
ssh -t pi _test/web_server/web_server.py
#ssh -t pi _test/run.py
#ssh -t pi "cd _test/web_server; cherryd -i web_server -c cherrypy.conf"
