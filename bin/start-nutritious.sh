#!/bin/bash

# source bash for path
. $HOME/.bashrc
#export /Users/john/prog/ChartDirector/lib:/Users/john/git/IbPy:/Users/john/git/old-svn-repo/jplpy/src:/Users/john/git/old-svn-repo/trading/src:/Users/john/git/textbites:/Users/john/git/pybible

cd $HOME/git/nutritious

./manage.py runserver
