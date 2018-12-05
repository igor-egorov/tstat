import os
from os.path import join
import re


class TestCase(object):

    def __init__(self, file_name, line, signature, docstring):
        """
        Pareses test case description
        :param signature: heading line of a case like TEST_F(blah, blah) {
        :param docstring: list of lines with docstring between /** and */
        """
        self.fixture = False
        self.file_name = file_name
        self.line = line
        self.fixture_name = \
            self.test_name = \
            self.caption = \
            self.given = \
            self.when = \
            self.then = None
        self._parse_signature(signature)
        if docstring:
            self._parse_docstring(docstring)
        if not self.caption:
            self.caption = None
        if not self.given:
            self.given = None
        if not self.when:
            self.when = None
        if not self.then:
            self.then = None

    def _parse_signature(self, signature):
        pattern = r'(TYPED_)?TEST(_CASE)?(_[FP])?[ ]*\(([A-Za-z0-9_ ]+),([A-Za-z0-9_ ]+)\)'
        match = re.search(pattern, signature)
        assert match is not None, 'Unsupported test case signature format: {}\n{}:{}'.format(signature, self.file_name,
                                                                                             self.line)
        assert len(match.groups()) == 5, 'Unsupported test case signature format: {}'.format(signature)
        self.fixture = True if match.group(3) or match.group(1) else False
        self.fixture_name = match.group(4).strip()
        self.test_name = match.group(5).strip()

    def _parse_docstring(self, docstring):
        lines = [x.strip() for x in docstring]
        assert len(lines), 'The length of test case docstring must be at least one line long: {}'.format(docstring)
        lines[0] = lines[0].replace('/**', '', 1).strip()
        lines[-1] = ''.join(lines[-1].rsplit('*/', 1)).strip()
        for index, line in enumerate(lines):
            if index == 0 or index == len(lines):
                continue
            lines[index] = line.replace('*', '', 1).strip()
        begin_index = 0
        for index, line in enumerate(lines):
            if line.startswith('@given'):
                self.caption = ' '.join(lines[begin_index: index]).strip()
                begin_index = index
            if line.startswith('@when'):
                self.given = ' '.join(lines[begin_index: index]).strip()
                begin_index = index
            if line.startswith('@then'):
                self.when = ' '.join(lines[begin_index: index]).strip()
                begin_index = index
        if self.caption is None and self.given is None and self.when is None:
            self.caption = ''.join(lines).strip()
        else:
            self.then = ''.join(lines[begin_index:]).strip()
        if self.given is not None:
            self.given = self.given.replace('@given', '', 1).strip()
        if self.when is not None:
            self.when = self.when.replace('@when', '', 1).strip()
        if self.then is not None:
            self.then = self.then.replace('@then', '', 1).strip()


class Scanner(object):
    """Recursively walks over a directory tree scanning C++ sources for Google Test cases"""
    TARGET_EXTS = ('.cpp', '.cxx', '.cc', '.c', '.hpp', '.h')

    def __init__(self, storage, dir):
        """Scan all recursively under the root_dir"""
        self._storage = storage
        self._sources = []
        self.scan_dir(dir)
        for file in self._sources:
            self.scan_file(file)

    def scan_dir(self, dir):
        for root, _, files in os.walk(dir):
            for file in files:
                if file.endswith(self.TARGET_EXTS):
                    self._sources.append(join(root, file))

    def scan_file(self, file_path):
        lines = []
        with open(file_path, 'r') as file:
            lines = file.readlines()
        contents = [re.sub(' +', ' ', line).strip() for line in lines]

        comment = None
        comment_begin = -1
        test_begin = -1
        for index, line in enumerate(contents):
            if '/**' in line:
                comment_begin = index
            if '*/' in line and comment_begin > -1:
                if len(contents) > index + 1 and (
                        contents[index + 1].startswith('TEST') or contents[index + 1].startswith('TYPED_TEST_CASE')):
                    comment = contents[comment_begin:index + 1]
                else:
                    comment = None
                comment_begin = -1
            if line.startswith('TEST') or line.startswith('TYPED_TEST_CASE'):
                test_begin = index
            if test_begin > -1 and ')' in line:
                test_signature = ''.join(contents[test_begin:index + 1])
                test_case = TestCase(file_path, test_begin + 1, test_signature, comment)
                self._storage.add_test(test_case)
                test_begin = -1
                comment = None
