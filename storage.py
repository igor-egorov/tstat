import sqlite3
from sys import exit


class Storage(object):
    """In-memory SQLite-based storage for processing temp results of scanning"""

    MIN_SQLITE_VERSION = '3.24.0'  # in 3.24.0 "upsert" was introduced

    TESTS_TABLE = """
        CREATE TABLE cases (
          file text NOT NULL,
          line integer NOT NULL,
          fixture_name text NOT NULL,
          test_name text NOT NULL,
          fixture integer,
          caption text,
          cgiven text,
          cwhen text,
          cthen text,
          CONSTRAINT unique_test UNIQUE (file, fixture_name, test_name) 
        );
    """

    def __init__(self):
        try:
            self._connect = sqlite3.connect(':memory:')
            self._check_sqlite_version()
        except Exception as e:
            print('SQLite initialization error: {}'.format(e))
            exit(1)
        self._create_tables()

    def __del__(self):
        if hasattr(self, '_connect'):
            self._connect.close()

    def _check_sqlite_version(self):
        from distutils.version import StrictVersion
        min_version = StrictVersion(self.MIN_SQLITE_VERSION)
        cursor = self._connect.cursor()
        cursor.execute('SELECT sqlite_version();')
        result = cursor.fetchone()
        actual_version = StrictVersion(result[0])
        assert actual_version >= min_version, \
            'Minimum required version of SQLite is {}'.format(self.MIN_SQLITE_VERSION)

    def _create_tables(self):
        try:
            cursor = self._connect.cursor()
            cursor.execute(self.TESTS_TABLE)
            self._connect.commit()
        except Exception as e:
            print('Error during SQLite tables creation: {}'.format(e))

    def add_test(self, test_case):
        """
        Save test case info
        :param test_case: object defined as TestCase in scanner.py
        :return:
        """
        sql = '''INSERT INTO cases(file, line, fixture_name, test_name, fixture, caption, cgiven, cwhen, cthen) ''' \
              '''VALUES(?,?,?,?,?,?,?,?,?)'''
        cursor = self._connect.cursor()
        d = test_case
        cursor.execute(sql, (
            d.file_name, d.line, d.fixture_name, d.test_name, d.fixture, d.caption, d.given, d.when, d.then))
        self._connect.commit()

    def get_sources(self):
        """Retrieves a list of all source files"""
        cursor = self._connect.cursor()
        cursor.execute('SELECT DISTINCT file FROM cases ORDER BY file')
        rows = cursor.fetchall()
        return [x[0] for x in rows]

    def get_test_cases(self, path):
        """Get all test cases from specified file"""
        cursor = self._connect.cursor()
        cursor.execute(
            'SELECT line, fixture_name, test_name, fixture, caption, cgiven, cwhen, cthen FROM cases WHERE file=?',
            (path,))
        rows = cursor.fetchall()
        return rows

    def count_files_with_tests(self):
        """Count files with Gtest cases detected"""
        cursor = self._connect.cursor()
        sql = '''SELECT COUNT(*) FROM (SELECT DISTINCT file FROM CASES)'''
        cursor.execute(sql)
        row = cursor.fetchone()
        return row[0]

    def count_test_cases(self):
        """Get the number of test cases"""
        cursor = self._connect.cursor()
        sql = '''SELECT COUNT(*) FROM cases'''
        cursor.execute(sql)
        row = cursor.fetchone()
        return row[0]

    def count_disabled_test_cases(self):
        """Get the number of disabled test cases"""
        cursor = self._connect.cursor()
        sql = '''SELECT COUNT(*) FROM cases WHERE test_name LIKE 'DISABLED_%' '''
        cursor.execute(sql)
        row = cursor.fetchone()
        return row[0]

    def count_test_cases_without_description(self):
        """Get the number of test cases without description"""
        cursor = self._connect.cursor()
        sql = '''SELECT COUNT(*) FROM cases WHERE caption IS NULL AND ''' + \
              '''cgiven IS NULL AND cwhen is NULL AND cthen IS NULL '''
        cursor.execute(sql)
        row = cursor.fetchone()
        return row[0]
