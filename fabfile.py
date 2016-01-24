from fabric.api import cd, sudo, run, prefix
from fabric.contrib.files import exists
from fabric.state import env
from contextlib import contextmanager as _contextmanager



##############
### config ###
##############


git_repo = 'https://github.com/b-cube/restparql.git'
app_dir = '~/restparql'
virtualenv_dir = app_dir + '/env'
flask_dir = app_dir + '/app'
nginx_dir = '/etc/nginx/sites-enabled'

env.directory = virtualenv_dir
env.activate = 'source {0}/bin/activate'.format(virtualenv_dir)

@_contextmanager
def virtualenv():
    with cd(env.directory):
        with prefix(env.activate):
            yield


#############
### tasks ###
#############

def install_os_requirements_1():
    """ Install required packages. """
    sudo('apt-get update')
    sudo('apt-get install -y build-essential')
    sudo('apt-get install -y python-dev')
    sudo('apt-get install -y libxslt1-dev')
    sudo('apt-get install -y libxml2-dev')
    sudo('apt-get install -y python3.4-dev')
    sudo('apt-get install -y python-pip')
    sudo('apt-get install -y nginx')
    sudo('apt-get install -y supervisor')
    sudo('apt-get install -y git')
    sudo('sudo pip install virtualenv')


def checkout_project_2():
    """
    1. Create project directories
    2. checkout the latest code
    """
    if exists(app_dir) is False:
        run('mkdir ' + app_dir)
    if exists(flask_dir) is False:
        with cd(app_dir):
            run('git clone ' + git_repo + ' ' + flask_dir)
    else:
        with cd(flask_dir):
            run('git pull --rebase')


def install_virtualenv_packages_3():
    """
    1. Create a new virtualenv
    2. Install the requirements
    """
    if exists(virtualenv_dir) is False:
        run('virtualenv -p python3 ' + virtualenv_dir)
    with virtualenv():
        run('pip install --upgrade pip')
        run('pip install -r ' + flask_dir + '/requirements.txt')


def configure_nginx_4():
    """
    1. Remove default nginx config file
    2. Create new config file
    3. Setup new symbolic link
    4. Restart nginx
    """
    sudo('/etc/init.d/nginx start')
    if exists('/etc/nginx/sites-enabled/default'):
        sudo('rm /etc/nginx/sites-enabled/default')
    if exists('/etc/nginx/sites-enabled/nginx_flask') is False:
        sudo('touch /etc/nginx/sites-available/nginx_flask')
        sudo('ln -s /etc/nginx/sites-available/nginx_flask' +
             ' /etc/nginx/sites-enabled/nginx_flask')
    sudo('cp ' + flask_dir + '/config/nginx_flask ' + nginx_dir)
    sudo('/etc/init.d/nginx restart')


def run_app():
    """ Run the app! """
    with virtualenv():
        with cd(flask_dir):
            run('gunicorn app:app -b localhost:5000 -w4 --daemon', pty=False)


def stop_app():
    sudo('pkill gunicorn.*')


def status():
    """ Is our app live? """
    run('ps -aux | grep gunicorn')


def provision():
    install_os_requirements_1()
    checkout_project_2()
    install_virtualenv_packages_3()
    configure_nginx_4()


