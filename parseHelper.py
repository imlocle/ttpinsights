import re
from bs4 import BeautifulSoup
import requests

"""
This function is to parse out content using a regular expression pattern from a string.
<param>regex_pattern</param>
<param>string</param>
"""
def parse_definition(regex_pattern, string):
    result = re.compile(regex_pattern, flags=re.MULTILINE|re.DOTALL)
    # Checking if the patten works for the string
    if not result.search(string):
        return "None"
    else:
        return result.search(string).group(1)