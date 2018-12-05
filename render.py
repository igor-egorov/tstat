"""

BE CAREFUL!!!

SHIT CODE BELOW. Needs to be rewritten with Jinja2

░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░▓████████▓░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░▒█████████▓▒░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░▓██▓▓▓▓▓▓███░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░▓██▓▓▓▓▓▓▓██▓░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░▓█▓▓▓▓▓▓▓▓█▓░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░▓█▓▓▓▓▓▓▓▓█▓▒░░░░░░░░░░░░
░░░░░░░░░░░░░░░▓██▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░
░░░░░░░░░░░▒▓▓█████▓▓▓▓▓▓▓▓██▓░░░░░░░░░░░
░░░░░░░░░▓█████████▓▓▓▓▓▓▓▓███▓▒░░░░░░░░░
░░░░░░░░▓███▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓████▓░░░░░░░░
░░░░░░▒████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓███▓░░░░░░░
░░░░░░▓██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██▓░░░░░░
░░░░░░▓██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██▓░░░░░░
░░░░░░███▓▓▓█████▓▓▓▓▓▓▓█████▓▓▓██▓░░░░░░
░░░░░░████▓█▓░░▒▓▓▓▓█▓██▓░░▒▓█▓███▓░░░░░░
░░░░░▒█████▓░░░░▒▓█████▓░░░░▒▓█████▒░░░░░
░░░░▓████▓▒░░▒█░░░▓███▒░░▒▓░░░▓█████▓░░░░
░░▒▓███▓▓▓░░░██▒░░▒▓█▓░░░▓█▓░░░▓▓▓███▓▒░░
░▓████▓▓▓▓▓░░░░░░░▓▓▓▓▒░░░░░░░▓▓▓▓▓████░░
░███▓▓▓▓▓▓▓▓▒░░░▓▓▓▓▓▓▓▓▒░░░▓▓▓▓▓▓▓▓▓██▓░
░███▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██▓░
░███▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██▓░
░███▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██▓░
░███▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██▓░
░█████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓███▒░
░▒█████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓███▓█░░
░░░▓████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓████▒░░░
░░░░▒▓█████████████████████████████▓▒░░░░
░░░░░▒▓███████████████████████████▓░░░░░░


"""


import utils
import os
from datetime import datetime

"""THIS IS VERY PRIMITIVE IMPLEMENTATION. Needs to be rewritten using jinja or smth like that"""


class Render(object):

    def __init__(self, storage, root_dir, excluded):
        self._storage = storage
        self._root_dir = root_dir
        self._excluded = excluded

    def render(self):
        return ''.join([
            self._render_header(),
            self._render_summary(),
            self._render_statistics(),
            self._render_directories_tree(),
            self._render_semi_a(),
            self._render_test_cases(),
            self._render_semi_b()
        ])

    def _render_header(self):
        return '''<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Test Cases Report - ''' + self._root_dir + '''</title>
    <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.3.3/semantic.min.css">
    <style>
        h2 {
            margin-top:1.5em !important;
        }
        .dont-break-out {

  /* These are technically the same, but use both */
  overflow-wrap: break-word;
  word-wrap: break-word;

  -ms-word-break: break-all;
  /* This is the dangerous one in WebKit, as it breaks things wherever */
  word-break: break-all;
  /* Instead use this non-standard one: */
  word-break: break-word;

  /* Adds a hyphen where the word breaks, if supported (No Blink) */
  -ms-hyphens: auto;
  -moz-hyphens: auto;
  -webkit-hyphens: auto;
  hyphens: auto;
min-width:110px !important;
}
    </style>
</head>
<body>
<div class="ui container" style="padding-top:20px">
    <h1 class="ui dividing header">Test Cases Report</h1>

    <div class="ui vertical segment">
        <h2 class="ui header">Summary</h2>
            <p>The report contains statistics about test cases written using Google Test framework</p>



        <table class="ui striped very basic celled collapsing table">
            <tbody>
        '''

    def _render_summary(self):
        return '''
        <tr>
                <td>Project Root Dir</td>
                <td><code>{}</code></td>
            </tr>
            <tr>
                <td>Excluded Paths</td>
                <td><small><code>{}</code></small></td>
            </tr>
            <tr>
                <td>Report Generation Date</td>
                <td>{}</td>
            </tr>
            <tr>
                <td>Target File Extensions</td>
                <td><code>.cpp .cxx .cc .c .hpp .h</code></td>
            </tr>
            <tr>
                <td>Target Cases Types</td>
                <td><code>TEST, TEST_F, TEST_P, TYPED_TEST_CASE</code></td>
            </tr>
            </tbody>
        </table>


        <div class="ui small statistics">
        '''.format(self._root_dir, '<br>'.join(self._excluded), datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def _render_statistics(self):
        return '''
        <div class="statistic">
                <div class="value">
                    {}
                </div>
                <div class="label">
                    files with tests
                </div>
            </div>
            <div class="statistic">
                <div class="value">
                    {}
                </div>
                <div class="label">
                    test cases
                </div>
            </div>
            <div class="orange statistic">
                <div class="value">
                    {}
                </div>
                <div class="label">
                    lacks in description
                </div>
            </div>
            <div class="statistic">
                <div class="value">
                    {}
                </div>
                <div class="label">
                    disabled cases
                </div>
            </div>
        </div>
    </div>


    <div class="ui vertical segment" id="tree">
        <h2 class="ui header">Directories Tree</h2>

        <div class="ui list">
        '''.format(
            self._storage.count_files_with_tests(),
            self._storage.count_test_cases(),
            self._storage.count_test_cases_without_description(),
            self._storage.count_disabled_test_cases()
        )

    def _render_directories_tree(self):
        files = self._storage.get_sources()
        tree = utils.directories_tree(files)

        def render_node(node, prefix):
            result = []
            dir = len(node['children'])
            icon = 'folder outline' if dir else 'file'
            result.append('<div class="item">')
            result.append('<i class="{} icon"></i>'.format(icon))
            result.append('<div class="content">')
            new_prefix = '' if os.sep in node['name'] else prefix + node['name']
            if dir:
                result.append('<div class="header">{}</div>'.format(node['name']))
            else:
                result.append('<div class="header"><a href="#{}">{}</a></div>'.format(
                    new_prefix, node['name']
                ))
            if dir:
                result.append('<div class="list">')
                for child in node['children']:
                    result.append(render_node(child, new_prefix))
                result.append('</div>')
            result.append('</div></div>')
            return ''.join(result)

        return render_node(tree, '')

    def _render_semi_a(self):
        return '''
        </div>

    </div>

    <h2 class="ui header">Test Cases</h2>
        '''

    def _render_test_cases(self):
        sources = self._storage.get_sources()
        prefix = utils.common_path_prefix(sources)

        def render_test_case(path, prefix):
            result = []
            result.append('''<div class="ui top attached block header" id="{}">
        <div style="display:inline-block">{}</div>
        <div style="float: right;">
            <a href="#tree"><i class="small angle up icon"></i>back to tree</a>
        </div>
    </div>'''.format(path[len(prefix):].replace(os.sep, ''),
                path[len(prefix):]))
            result.append('''<div class="ui bottom attached segment"><table class="ui selectable very basic celled attached table">
            <thead>
            <tr>
                <th>Line #</th>
                <th class="collapsing">Fixture (
                    <div class="ui mini empty circular purple label"></div>
                    ) / Test Name
                </th>
                <th>Test Case Name</th>
                <th>Caption</th>
                <th>Given</th>
                <th>When</th>
                <th>Then</th>
            </tr>
            </thead>
            <tbody>''')
            for row in self._storage.get_test_cases(path):
                line = row[0]
                fixture_name = row[1]
                test_name = row[2]
                has_fixture = int(row[3])
                caption = row[4] if row[4] else ''
                given = row[5] if row[5] else ''
                when = row[6] if row[6] else ''
                then = row[7] if row[7] else ''
                disabled = '<div class="ui grey horizontal label">DISABLED</div>' if test_name.startswith(
                    'DISABLED_') else ''
                test = test_name[len('DISABLED_'):] if disabled else test_name
                warning = (not caption and not given and not when and not then)
                result.append('''<tr class="{}"><td>{}</td><td>{}{}</td><td class="dont-break-out">{}{}</td>'''.format(
                    'warning' if warning else '',
                    line,
                    fixture_name,
                    '&nbsp;<div class="ui mini empty circular purple label"></div>' if has_fixture else '',
                    disabled,
                    test
                ))
                result.append('''<td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'''.format(
                    caption, given, when, then
                ))
            result.append('''
            </tbody>
        </table>

    </div>
            ''')
            return ''.join(result)

        res = []
        for source in sources:
            res.append(render_test_case(source, prefix))
        return ''.join(res)

    def _render_semi_b(self):
        return '''
        <div class="ui basic segment">&nbsp;</div>

</div>
</body>
</html>
        '''
