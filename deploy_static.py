from fabric.api import *
from fabric.contrib import project

env.hosts = ['127.0.0.1']

env.project_root = r'd:\github\dianyings'

def deploy_static():
    with cd(env.project_root):
        run('./manage.py collectstatic -v0 --noinput')

if __name__ == "__main__":
    deploy_static()
