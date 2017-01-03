from __future__ import print_function
from __future__ import division
import re

# 

comment = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE)

def sql_to_readme(text):
    """

    Originally based on:
    http://stackoverflow.com/questions/241327/python-snippet-to-remove-c-and-c-comments
    """
    text = text.strip()

    # Extract the first comment section and use it as README text

    match = comment.match(text)

    md_text = match.group(0)
    md_text = md_text[2:-2] # remove start and stop of comment
    md_text = md_text.strip()

    # Block quote the rest of the query 

    quoted_text = text[match.span()[1]:]

    chunks = [md_text]
    for line in quoted_text.split('\n'):
        chunks.append('    ' + line)

    return '\n'.join(chunks)


if __name__ == '__main__':
    from utility import this_dir
    text = open(this_dir + '/sql/active-mmsis.sql').read()
    print(sql_to_readme(text))