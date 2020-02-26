#! /usr/bin/env python3

import git
from git import Repo
import os
from getpass import getpass
from datetime import datetime
import time
import argparse
import sys
import subprocess

parser = argparse.ArgumentParser(description='WYL GIT Auto-Pusher')
parser.add_argument('-c', '--confirm', action='store_true')
parser.add_argument('-n', '--no-comment', action='store_true')
args = parser.parse_args()

disabled_commenting = True if args.no_comment is True else False

def generate_timestamp():
    return datetime.now()

def generate_dt_string(timestamp_=None):
    now = datetime.now() if timestamp_ is None else timestamp_
    # readable - date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    return now.strftime("%m/%d/%Y, %H:%M:%S") # "%Y%m%d_%H%M%S"

def git_push(dc_=False):
    try:
        repo = Repo(PATH_OF_GIT_REPO)
        repo.git.add(update=True)
        if dc_ is False:
            repo.index.commit(COMMIT_MESSAGE)
        origin = repo.remote(name='origin')
        origin.push()
    except:
        print('Some error occured while pushing the code')   

def get_current_executing_user():
    process = subprocess.Popen(['whoami'], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT)
    stdout,stderr = process.communicate()
    return stdout.decode('utf-8').replace("\n","")
    

commit_dt_string = generate_dt_string(generate_timestamp())
username = ''
password = ''

if len(password) > 0:
    GIT_PW_NOT_SET = (("GIT_PASSWORD" in os.environ.keys()) is False)
    if GIT_PW_NOT_SET is True:
        os.environ['GIT_PASSWORD'] = password
else:
        os.environ['GIT_PASSWORD'] = getpass()

project_dir = os.path.dirname(os.path.abspath(__file__))
os.environ['GIT_ASKPASS'] = os.path.join(project_dir, 'askpass.py')
os.environ['GIT_USERNAME'] = username

# Absolute Directory of git-Repo
PATH_OF_GIT_REPO = r'/home/example-git1/repo'

executing_user = get_current_executing_user()
COMMIT_MESSAGE = 'not-really-a-important-comment @ '+commit_dt_string+' ('+executing_user+')'
        
if args.confirm is True:
    git_push(disabled_commenting)
else:
    print("-c / --confirm to confirm push")
