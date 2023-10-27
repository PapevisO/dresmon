from config import (DRESMON_PROVIDER,
                    DRESMON_TLD,
                    DRESMON_HOSTS_BLOCK_TAG,
                    BLOCK_TAG_WARNING,
                    DEMARCATING_SYMBOL)

def generate_tag(tag_type):
    """
    Generate a tag (start or end) for the Dresmon block.
    example
    # start dresmon traefik managed block local # This block is managed by Dresmon. Do not edit manually!
    """
    return (
        f"# {tag_type} {DRESMON_HOSTS_BLOCK_TAG}"
        f" {DRESMON_PROVIDER} managed block for {' '.join(DRESMON_TLD)}"
        f" {DEMARCATING_SYMBOL} {BLOCK_TAG_WARNING}"
    )

def get_start_tag():
    return generate_tag("start")

def get_end_tag():
    return generate_tag("end")
