import re

# Using Regex to scrape
def parse_definition(regex_pattern, string):
    i = re.compile(regex_pattern, flags=re.MULTILINE|re.DOTALL)
    return i.search(string).group(1)