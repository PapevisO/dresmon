from config import logger, DRESMON_TLD, DRESMON_PROVIDER
from .tags import get_start_tag, get_end_tag

def validate_block_tags(hosts_content):
    if hosts_content.count(get_start_tag()) != 1 or hosts_content.count(get_end_tag()) != 1:
        logger.error("Invalid block: Either start or end tag is missing or duplicated.")
        exit(1)

def validate_block_order(hosts_content):
    start_index = hosts_content.index(get_start_tag())
    end_index = hosts_content.index(get_end_tag())
    
    if start_index > end_index:
        logger.error("Invalid block: Start tag appears after end tag.")
        exit(1)

def validate_no_nested_blocks(hosts_content):
    start_index = hosts_content.index(get_start_tag())
    end_index = hosts_content.index(get_end_tag())
    
    for line in hosts_content[start_index+1:end_index]:
        if line.startswith("# start dresmod"):
            logger.error("Invalid block: Nested start tag detected.")
            exit(1)

def validate_hosts_block(hosts_content):
    validate_block_tags(hosts_content)
    validate_block_order(hosts_content)
    validate_no_nested_blocks(hosts_content)
    
    logger.warning("Block validated successfully.")
