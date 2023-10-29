import pytest
from hosts.manager import block_exists

# Define the path to the fixtures
FIXTURE_PATH = "tests/fixtures"

@pytest.mark.parametrize("fixture_file, expected_result", [
    ("normal_case.txt", True),
    ("no_block.txt", False),
    ("only_start_tag.txt", False),
    ("only_end_tag.txt", False),
    ("multiple_blocks.txt", True),
    ("wrong_order.txt", False)
])

def test_block_exists(fixture_file, expected_result):
    with open(f"{FIXTURE_PATH}/{fixture_file}", 'r') as f:
        content = f.read()
    try:
        result = block_exists(content)
        assert result == expected_result
    except ValueError as e:
        if expected_result:
            pytest.fail(f"Unexpected error: {e}")
