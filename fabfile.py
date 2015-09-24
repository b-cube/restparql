from fabric.api import cd, sudo
from fabric.contrib.files import exists


##############
### config ###
##############

git_repo = 'https://github.com/b-cube/restparql.git'
app_dir = '/opt/restparql'
virtualenv_dir = app_dir + '/env'
flask_dir = app_dir + '/app'
nginx_dir = '/etc/nginx/sites-enabled'
supervisor_dir = '/etc/supervisor/conf.d'


#############
### tasks ###
#############

def install_os_requirements_1():
    """ Install required packages. """
    sudo('apt-get update')
    sudo('apt-get install -y build-essential')
    sudo('apt-get install -y python-dev')
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
        sudo('mkdir ' + app_dir)
    if exists(flask_dir) is False:
        with cd(app_dir):
            sudo('git clone ' + git_repo + ' ' + flask_dir)
    else:
        with cd(flask_dir):
            sudo('git pull --rebase')


def install_virtualenv_packages_3():
    """
    1. Create a new virtualenv
    2. Install the requirements
    """
    if exists(virtualenv_dir) is False:
        sudo('virtualenv -p python3 ' + virtualenv_dir)
    sudo('source ' + virtualenv_dir + '/bin/activate')
    sudo('pip install --upgrade pip')
    sudo('pip install -r ' + flask_dir + '/requirements.txt')


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


def configure_supervisor_5():
    """
    1. update supervisor config file
    2. update supervisor
    """
    sudo('cp ' + flask_dir + '/config/restparql.conf ' +
         '/etc/supervisor/conf.d/')
    sudo('supervisorctl reread')
    sudo('supervisorctl update')


def run_app():
    """ Run the app! """
    sudo('source ' + virtualenv_dir + '/bin/activate')
    with cd(flask_dir):
        sudo('supervisorctl start restparql')


def status():
    """ Is our app live? """
    sudo('supervisorctl status')


def provision():
    install_os_requirements_1()
    checkout_project_2()
    install_virtualenv_packages_3()
    configure_nginx_4()
    configure_supervisor_5()

