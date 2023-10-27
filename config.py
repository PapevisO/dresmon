import os
import logging

LOG_LEVEL = os.environ.get("LOG_LEVEL", "info").upper()
# Set up logging
logging.basicConfig(level=getattr(logging, LOG_LEVEL))

logger = logging.getLogger(__name__)

# Configuration variables
DRESMON_PROVIDER = os.environ.get('DRESMON_PROVIDER', 'traefik')
DRESMON_TLD = os.environ.get('DRESMON_TLD', 'local').split(',')
logger.warning(f"Not implemented: DRESMON_TLD")
DRESMON_EXCLUDE = os.environ.get('DRESMON_EXCLUDE', '').split(',')
logger.warning(f"Not implemented: DRESMON_EXCLUDE")
DRESMON_TARGET_IP = os.environ.get('DRESMON_TARGET_IP', '127.0.0.1')
logger.warning(f"Not implemented: DRESMON_TARGET_IP")
DRESMON_HOSTS_BLOCK_TAG = os.environ.get('DRESMON_HOSTS_BLOCK_TAG', 'dresmon')
logger.warning(f"Not implemented: DRESMON_HOSTS_BLOCK_TAG")

BLOCK_TAG_WARNING = "This block is managed by Dresmon. Do not edit manually!"
DEMARCATING_SYMBOL = "#"
