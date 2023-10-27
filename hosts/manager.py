from config import logger, DRESMON_EXCLUDE, DRESMON_TARGET_IP
from .block_validator import validate_hosts_block
from .tags import get_end_tag, get_start_tag

def sync_hosts_file(domains):
    """
    Update the /etc/hosts file with the provided domains.
    """
    with open('/etc/hosts', 'r+') as hosts_file:
        hosts_content = hosts_file.readlines()

        if not block_exists(hosts_content):
            append_new_block(hosts_file, domains)
        else:
            update_existing_block(hosts_content, domains)

def block_exists(hosts_content):
    start_tag_exists = any(get_start_tag() in line for line in hosts_content)
    end_tag_exists = any(get_end_tag() in line for line in hosts_content)

    if start_tag_exists and end_tag_exists:
        start_index = next(i for i, line in enumerate(hosts_content) if get_start_tag() in line)
        end_index = next(i for i, line in enumerate(hosts_content) if get_end_tag() in line)
        if start_index > end_index:
            raise ValueError("Invalid block: Start tag appears after end tag.")
        return True
    elif start_tag_exists or end_tag_exists:
        raise ValueError("Invalid block: Multiple or missing start/end tags.")
    return False

def append_new_block(hosts_file, domains):
    """
    Append a new Dresmon block at the end of the hosts file.
    """
    hosts_file.write("\n")
    hosts_file.write(get_start_tag() + "\n")
    for domain in domains:
        hosts_file.write(f"{DRESMON_TARGET_IP} {domain}\n")
    hosts_file.write(get_end_tag() + "\n")

def update_existing_block(hosts_content, domains):
    """
    Update the existing Dresmon block in the hosts file.
    """
    validate_hosts_block(hosts_content)
    # TODO: Implement the logic to update existing block
    logger.warning(f"Not implemented: Update /etc/hosts for domains: {', '.join(domains)}")
