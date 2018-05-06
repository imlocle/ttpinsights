import re
from bs4 import BeautifulSoup
import requests

"""
This function is to parse out content using a regular expression pattern from a string.
<param>regex_pattern</param>
<param>string</param>
"""
def parse_definition(regex_pattern, string):
    i = re.compile(regex_pattern, flags=re.MULTILINE|re.DOTALL)
    return i.search(string).group(1)