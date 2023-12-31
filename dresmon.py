from no_windows import terminate_if_windows_assumed
terminate_if_windows_assumed()

import docker
import importlib
import pkgutil
from providers import BaseProvider
from config import logger, DRESMON_PROVIDER
from hosts.manager import sync_hosts_file

client = docker.from_env()

###
# Container events data provider
###

# Dynamically load all providers from the providers directory
package_name = 'providers'
package = importlib.import_module(package_name)
for _, module_name, _ in pkgutil.iter_modules(package.__path__):
    importlib.import_module(f'{package_name}.{module_name}')

provider_class = BaseProvider.PROVIDER_MAPPING.get(DRESMON_PROVIDER)
if not provider_class:
    logger.error(f"Unknown provider: {DRESMON_PROVIDER}")
    raise ValueError(f"Unknown provider: {DRESMON_PROVIDER}")

provider_instance = provider_class()

###
# Define algorythm 
###

def process_container(container):
    domains = provider_instance.get_domains(container)
    if domains:
        logger.debug(f"Domains for container {container.name}: {', '.join(domains)}")
        sync_hosts_file(domains)

    logger.debug("No domains to update /etc/hosts")

def process_existing_containers():
    logger.info("Processing existing containers...")
    for container in client.containers.list():
        process_container(container)

def monitor_docker_events():
    logger.info("Starting to monitor Docker events...")
    # Continuously listen to Docker events
    for event in client.events(decode=True):
        if event['Type'] == 'container' and event['Action'] == 'start':
            container = client.containers.get(event['id'])
            logger.debug(f"New container started: {container.name}")
            process_container(container)

###
# Start and listen for container events
###

if __name__ == "__main__":
    process_existing_containers()
    monitor_docker_events()
