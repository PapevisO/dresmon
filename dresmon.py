import os
import docker
import importlib
import pkgutil
from providers import BaseProvider

# Initialize environment variables
DRESMON_PROVIDER = os.environ.get('DRESMON_PROVIDER', 'traefik')
DRESMON_TLD = os.environ.get('DRESMON_TLD', 'local').split(',')
DRESMON_EXCLUDE = os.environ.get('DRESMON_EXCLUDE', '').split(',')
DRESMON_TARGET_IP = os.environ.get('DRESMON_TARGET_IP', '127.0.0.1')
DRESMON_HOSTS_BLOCK_TAG = os.environ.get('DRESMON_HOSTS_BLOCK_TAG', 'dresmon').split(',')

client = docker.from_env()

# Dynamically load all providers from the providers directory
package_name = 'providers'
package = importlib.import_module(package_name)
for _, module_name, _ in pkgutil.iter_modules(package.__path__):
    importlib.import_module(f'{package_name}.{module_name}')

provider_class = BaseProvider.PROVIDER_MAPPING.get(DRESMON_PROVIDER)
if not provider_class:
    raise ValueError(f"Unknown provider: {DRESMON_PROVIDER}")

provider_instance = provider_class()

def update_hosts(container):
    domains = provider_instance.get_domains(container)
    # TODO: Update /etc/hosts with the domains

def process_existing_containers():
    for container in client.containers.list():
        update_hosts(container)

def monitor_docker_events():
    # Continuously listen to Docker events
    for event in client.events(decode=True):
        if event['Type'] == 'container' and event['Action'] == 'start':
            container = client.containers.get(event['id'])
            update_hosts(container)

if __name__ == "__main__":
    process_existing_containers()
    monitor_docker_events()
