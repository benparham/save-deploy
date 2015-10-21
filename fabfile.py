import os, errno

from fabric.api import env, task

# ------ ENVIRONMENT SETTINGS --------

# Read in configurable settings.
environment_settings = {
    'aws_access_key_id': None,
    'aws_secret_access_key': None,
    'aws_default_region': None,
    'aws_ssh_key_name': None,
    'aws_ssh_port': None,
    'aws_ec2_instance_type': None,
    'aws_ec2_ami_id': None,
    'aws_ec2_security_group_name': None,
    'aws_rds_allocated_storage': None,
    'aws_rds_instance_class': None,
    'aws_rds_master_username': None,
    'aws_rds_master_password': None,
    'aws_rds_database_name': None,
    'aws_rds_security_group_name': None,
}
for name, value in environment_settings.items():
    env_value = os.getenv(name.upper())
    env[name] = env_value
    if not env_value:
        raise Exception('Missing environment setting: {}'.format(name.upper()))

# Define non-configurable settings
env.root_directory = os.path.dirname(os.path.realpath(__file__))
env.deploy_directory = os.path.join(env.root_directory, 'deploy')
env.app_settings_directory = os.path.join(env.deploy_directory, 'settings')
env.app_settings_base = os.path.join(env.app_settings_directory, 'base.json')
env.app_settings_deploy_key = os.path.join(env.app_settings_directory, 'deploy_key')
env.hosts_directory = os.path.join(env.deploy_directory, 'hosts')
env.ssh_directory = os.path.join(env.deploy_directory, 'ssh')
env.aws_key_path = os.path.join(env.ssh_directory, env.aws_ssh_key_name + '.pem')


# ------ PREP DIRECTORIES ------

def prep_directory(dir, perm):
    try:
        os.makedirs(dir)
    except OSError as e:
        if e.errno != errno.EEXIST or not os.path.isdir(dir):
            raise Exception('Error prepping \'{}\' directory'.format(dir))
    if perm: os.chmod(dir, perm)

prep_directory(env.deploy_directory, 0700)
prep_directory(env.ssh_directory, 0700)
prep_directory(env.hosts_directory, None)
prep_directory(env.app_settings_directory, None)


# ------ FABRIC TASKS -------

@task
def test():
    print env.aws_key_path
