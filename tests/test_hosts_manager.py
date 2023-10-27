import pytest
from hosts.manager import block_exists

# Define the path to the fixtures
FIXTURE_PATH = "tests/fixtures/"

@pytest.mark.parametrize("fixture_file, expected_result", [
    (FIXTURE_PATH + "normal_case.txt", True),
    (FIXTURE_PATH + "no_block.txt", False),
    (FIXTURE_PATH + "only_start_tag.txt", False),
    (FIXTURE_PATH + "only_end_tag.txt", False),
    (FIXTURE_PATH + "multiple_blocks.txt", True),
    (FIXTURE_PATH + "wrong_order.txt", False)
])

def test_block_exists(fixture_file, expected_result):
    with open(fixture_file, 'r') as f:
        content = f.readlines()
    try:
        result = block_exists(content)
        assert result == expected_result
    except ValueError as e:
        if expected_result:
            pytest.fail(f"Unexpected error: {e}")
