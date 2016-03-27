#!/bin/bash

echo 'Copying current directory...'
ssh pi rm -rf _test
scp -q -r . pi:_test

echo 'Running test command...'
ssh -t pi _test/run.py

