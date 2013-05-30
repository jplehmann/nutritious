#!/bin/bash

RUNNER_PATH="/static/test/e2e/runner.html"
unamestr=`uname`

if [[ "$unamestr" == 'Darwin' ]]; then
  open "$RUNNER_URL"
elif [[ "$unamestr" == 'Linux' ]]; then
  google-chrome "http://localhost:8000$RUNNER_PATH"
else
  echo "Unknown OS version."
fi
