#!/bin/bash

# source bash for path
. $HOME/.bashrc
#export /Users/john/prog/ChartDirector/lib:/Users/john/git/IbPy:/Users/john/git/old-svn-repo/jplpy/src:/Users/john/git/old-svn-repo/trading/src:/Users/john/git/textbites:/Users/john/git/pybible
export PYTHONPATH=$HOME/git/old-svn-repo/jplpy/src:$HOME/git/old-svn-repo/trading/src:$HOME/git/textbites:$HOME/git/pybible


cd $HOME/git/nutritious

#source $HOME/.venv/tagz/bin/activate
source $HOME/.venv/nutritious/bin/activate

./manage.py runserver 8001
