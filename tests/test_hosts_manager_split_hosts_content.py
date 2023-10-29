import re
import pytest
from hosts.manager import split_hosts_content

# Define the path to the fixtures
FIXTURE_PATH = "tests/fixtures"

@pytest.mark.parametrize(
    ("fixture_file, expected_before, "
                   "expected_inside, "
                   "expected_after, "
                   "expected_exception"), [
    ("normal_case.txt", "# start dresmon .*\n",
                        "(127.0.0.1 .*\n)+",
                        "# end dresmon .*\n",
                        None),
    ("normal_case_multiple_entries.txt", "# start dresmon .*\n",
                                         "(127.0.0.1 .*\n)+",
                                         "# end dresmon .*\n",
                                         None),
    ("no_block.txt", None, None, None,
                     AttributeError),
    ("only_start_tag.txt", None, None, None,
                           AttributeError),
    ("only_end_tag.txt", None, None, None,
                         AttributeError),
    # Not expected to process content of any matching blocks but the first
    ("multiple_blocks.txt", "# start dresmon .*\n",
                            "127.0.0.1 .*\n",
                            "# end dresmon .*\n",
                            None),
    # Not expected to validate wrong tags order,
    # expects validation to be done before passing content to function
    ("wrong_order.txt", "(.*\n)*# start dresmon .*\n",
                        "",
                        "",
                        None),
])

def test_split_hosts_content(fixture_file, expected_before,
                                           expected_inside,
                                           expected_after,
                                           expected_exception):
    with open(f"{FIXTURE_PATH}/{fixture_file}", "r") as f:
        content = f.read()


    if expected_exception:
        with pytest.raises(expected_exception):
            before, inside, after = split_hosts_content(content)
    else:
        try:
            before, inside, after = split_hosts_content(content)
        
            assert re.match(expected_before, before)
            assert re.match(expected_inside, inside)
            assert re.match(expected_after, after)
        except ValueError as e:
            pytest.fail(f"Unexpected error: {e}")
