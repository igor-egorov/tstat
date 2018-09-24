from difflib import SequenceMatcher
from functools import reduce
import os
import os.path


def common_path_prefix(items):
    """Defines common path prefix for provided list of file paths"""

    def lcs_of_two(a, b):
        sequence_matcher = SequenceMatcher(None, a, b)
        match = sequence_matcher.find_longest_match(0, len(a), 0, len(b))
        return a[match.a:match.a + match.size] if match.a == 0 else ''

    return reduce(lcs_of_two, items)


def directories_tree(items):
    prefix = common_path_prefix(items)
    prefix_len = len(prefix)
    items = [i[prefix_len:] for i in items]
    root = {
        'name': prefix,
        'children': []
    }

    def add_node(root, item):
        pieces = os.path.normpath(item).split(os.sep)
        ptr = root
        for piece in pieces:
            found = False
            for child in ptr['children']:
                if child['name'] == piece:
                    found = True
                    ptr = child
                    break
            if not found:
                new_node = {
                    'name': piece,
                    'children': []
                }
                ptr['children'].append(new_node)
                ptr = new_node

    for item in items:
        add_node(root, item)
    return root
