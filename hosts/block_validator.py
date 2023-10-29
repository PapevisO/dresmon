from config import logger
from .tags import START_TAG_REGEX, END_TAG_REGEX

def validate_block_tags(hosts_content_str):
    if len(START_TAG_REGEX.findall(hosts_content_str)) != 1 or len(END_TAG_REGEX.findall(hosts_content_str)) != 1:
        logger.error("Invalid block: Either start or end tag is missing or duplicated.")
        exit(1)

def validate_block_order(hosts_content_str):
    start_match = START_TAG_REGEX.search(hosts_content_str)
    end_match = END_TAG_REGEX.search(hosts_content_str)
    
    if not start_match or not end_match:
        logger.error("Tags not found.")
        exit(1)

    if start_match.start() > end_match.start():
        logger.error("Invalid block: Start tag appears after end tag.")
        exit(1)

def validate_no_nested_blocks(hosts_content_str):
    start_match = START_TAG_REGEX.search(hosts_content_str)
    end_match = END_TAG_REGEX.search(hosts_content_str)
    
    nested_start_matches = START_TAG_REGEX.findall(hosts_content_str[start_match.end():end_match.start()])
    if nested_start_matches:
        logger.error("Invalid block: Nested start tag detected.")
        exit(1)

def validate_hosts_block(hosts_content):
    hosts_content_str = "".join(hosts_content)
    validate_block_tags(hosts_content_str)
    validate_block_order(hosts_content_str)
    validate_no_nested_blocks(hosts_content_str)
    
    logger.warning("Block validated successfully.")
