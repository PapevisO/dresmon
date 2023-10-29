import re

from config import (DRESMON_PROVIDER,
                    DRESMON_TLD,
                    DRESMON_HOSTS_BLOCK_TAG,
                    BLOCK_TAG_WARNING)

TAG_PAYLOAD_SUFFIX = (f"{DRESMON_HOSTS_BLOCK_TAG} "
                      f"{DRESMON_PROVIDER} managed block for "
                      f"{' '.join(DRESMON_TLD)}")

START_TAG = (f"# start {TAG_PAYLOAD_SUFFIX} # {BLOCK_TAG_WARNING}")
END_TAG = (f"# end {TAG_PAYLOAD_SUFFIX} # {BLOCK_TAG_WARNING}")

START_TAG_REGEX = re.compile(rf".*?start {TAG_PAYLOAD_SUFFIX}.*?\n?")
END_TAG_REGEX = re.compile(rf".*?end {TAG_PAYLOAD_SUFFIX}.*?\n?")
