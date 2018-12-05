#!/usr/bin/env python3
import sys
import storage
import scanner
import render

TITLE = 'Test Cases Report Generator'

if __name__ == '__main__':
    print(TITLE)
    if len(sys.argv) >= 2:
        exclude_dirs = sys.argv[2:]
        root_dir = sys.argv[1]
        _storage = storage.Storage()
        _scanner = scanner.Scanner(_storage, root_dir, exclude_dirs)
        _render = render.Render(_storage, root_dir, exclude_dirs)
        result = _render.render()
        with open('report.html', 'w') as out:
            out.write(result)
            out.flush()

    else:
        print('Error: at least one parameter should be passed - a path to directory with tests to scan.'
              'All the following parameters are subpaths to be excluded.')
