import fnmatch, fcntl
from config import logger, DRESMON_TLD, DRESMON_EXCLUDE, DRESMON_TARGET_IP
from .block_validator import validate_hosts_block
from .tags import START_TAG_REGEX, START_TAG, END_TAG_REGEX, END_TAG

def sync_hosts_file(domains):
    """
    Update the /etc/hosts file with the provided domains.
    """
    with open('/etc/hosts', 'r+') as hosts_file:
        # lock file to prevent concurrency
        fcntl.flock(hosts_file, fcntl.LOCK_EX)

        hosts_content = hosts_file.read()

        if not block_exists(hosts_content):
            hosts_content = append_empty_block(hosts_content)

        hosts_content = update_existing_block(hosts_content, domains)

        logger.info("Updating /etc/hosts")
        hosts_file.seek(0)
        hosts_file.write(hosts_content)
        hosts_file.truncate()
        fcntl.flock(hosts_file, fcntl.LOCK_UN)

def block_exists(hosts_content_str):
    start_matches = list(START_TAG_REGEX.finditer(hosts_content_str))
    end_matches = list(END_TAG_REGEX.finditer(hosts_content_str))

    if len(start_matches) != len(end_matches):
        raise ValueError("Invalid block: Mismatched number of start and end tags.")

    for start_match, end_match in zip(start_matches, end_matches):
        if start_match.start() > end_match.start():
            raise ValueError("Invalid block: Start tag appears after end tag.")

    return len(start_matches) > 0

def append_empty_block(hosts_content):
    """
    Append a new Dresmon block at the end of the hosts file.
    """
    return "\n".join([
        hosts_content,
        START_TAG,
        END_TAG,
        ""
    ])

def update_existing_block(hosts_content, domains):
    """
    Update the existing Dresmon block in the hosts file.
    Expected application to crash if block validation fails
    """
    validate_hosts_block(hosts_content)
    before_block, inside_block, after_block = split_hosts_content(hosts_content)
    
    logger.debug(f"Inside block previous: \n{inside_block}")

    missing_domains = filter_valid_existing_domains(domains, inside_block)
    filtered_domains = filter_excluded_domains(missing_domains)

    for domain in filtered_domains:
        inside_block += f"{DRESMON_TARGET_IP} {domain}\n"

    logger.debug(f"Inside block next: \n{inside_block}")

    # Combine blocks to form the updated hosts_content
    return (before_block + inside_block + after_block)

def split_hosts_content(hosts_content):
    """
    Split the hosts_content into three parts: before, inside, and after the Dresmon block.
    """
    start_match = START_TAG_REGEX.search(hosts_content)
    end_match = END_TAG_REGEX.search(hosts_content)

    start_inside_block = hosts_content.find('\n', start_match.end()) + 1

    before_block = hosts_content[0:start_inside_block]
    inside_block = hosts_content[start_inside_block:end_match.start()]
    after_block = hosts_content[end_match.start():]

    return before_block, inside_block, after_block

def filter_excluded_domains(domains):
    """
    Filter out domains that match any pattern in DRESMON_EXCLUDE.
    """
    filtered_domains = []
    for domain in domains:
        excluded = True

        for tld in DRESMON_TLD:
            if fnmatch.fnmatch(domain, f"*.{tld}"):
                logger.info(f"Domain {domain} is managed {tld}")
                excluded = False
            else:
                logger.debug(f"Domain {domain} does not match tld: {tld}")

        for pattern in DRESMON_EXCLUDE:
            if fnmatch.fnmatch(domain, pattern):
                logger.debug(f"Domain {domain} is excluded due to pattern {pattern}")
                excluded = True
                break

        if not excluded:
            filtered_domains.append(domain)
    return filtered_domains

def filter_valid_existing_domains(domains, inside_block):
    """
    Filter out domains that match existing records with matching target ip.
    """
    
    # Extract domain names from inside_block
    existing_entries = {line.split()[-1]: line.split()[0] for line in inside_block.split('\n') if line}

    # Find domains that are not in inside_block
    missing_domains = []
    for domain in domains:
        if domain not in existing_entries:
            missing_domains.append(domain)
        elif existing_entries[domain] != DRESMON_TARGET_IP:
            missing_domains.append(domain)

    return missing_domains
