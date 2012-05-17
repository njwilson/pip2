"""
Formats data returned from the various commands to be displayed on command
line.

"""

import sys
import textwrap

import pip2.commands.install
import pip2.commands.uninstall
import pip2.commands.freeze
import pip2.commands.search
import pip2.util


# TODO: Add options to match pip feature set


def install(args):
    result = pip2.commands.install.install(args.package_list)

    if result['installed'] != []:
        successful = ', '.join(map(str, result['installed']))
        print('Successfully installed {0}.'.format(successful))
    if result['failed'] != []:
        failed = ', '.join(map(str, result['failed']))
        print('Failed to install {0}.'.format(failed))

    return


def uninstall(args):
    result = pip2.commands.uninstall.uninstall(args.package_list)

    if result['uninstalled'] != []:
        successful = ', '.join(map(str, result['uninstalled']))
        print('Successfully uninstalled {0}.'.format(successful))
    if result['failed'] != []:
        failed = ', '.join(map(str, result['failed']))
        print('Failed to uninstall {0}.'.format(failed))

    return


def freeze(args):
    distributions = pip2.commands.freeze.freeze()
    dist_names = list(distributions.keys())
    dist_names.sort()
    for dist_name in dist_names:
        print(dist_name + '==' + distributions[dist_name]['version'])
    return


def search(args):
    results = pip2.commands.search.search(args.package)
    if results == {}:
        print('Search returned no results...')
        return
    # when cli_wrapper gets split into multiple files, one for each command
    # these will be global
    # separator to use for name and summary
    sep = ' - '
    name_len = 26
    min_term_width = 40
    term_width = pip2.util.getTerminalSize()[0]
    if term_width < min_term_width:
        term_width = min_term_width
    # the '- 1' is so we don't get a newline
    # when summary is exactly one full line
    sum_len = term_width - name_len - len(sep) - 1
    sum_fmt = textwrap.TextWrapper(sum_len)

    for res in results.keys():
        summary = sum_fmt.wrap(results[res]['summary'])
        try:
            line = '{0:<{1}}{2}{3}'.format(res, name_len, sep, summary.pop(0))
            line = line[: (term_width - 1)]
        # international packages have encoding issues, we just skip and move on
        except SystemError:
            print('SKIPPING RESULT: CANNOT DISPLAY UNKNOWN CHARACTERS')
            continue
        success = _search_safe_print(line, res)
        if not success:
            continue
        for line in summary:
            next_line = ' ' * (name_len + len(sep)) + line
            success = _search_safe_print(next_line)
            if not success:
                break
        if ('installed_version' in results[res] and
            'latest_version' in results[res] and success):
            print('\tINSTALLED: {0}\n\tLATEST   : {1}'.format(
                  results[res]['installed_version'],
                  results[res]['latest_version']))
    return


def _search_safe_print(string, name=None):
    # temp assignment, will be removed when search cli is in its own file
    sep = ' - '
    name_len = 26
    try:
        print(string)
    except UnicodeError:
        if name:
            # try and print just the package name incase the summary is causing
            # the exception
            try:
                print('{0:<{1}}{2}'.format(name, name_len, sep) +
                      'CANNOT DISPLAY SUMMARY WITH ' +
                      '({0}) ENCODING'.format(sys.getdefaultencoding()))
            except UnicodeError:
                print('SKIPPING RESULT: CANNOT DISPLAY WITH ' +
                      '({0}) ENCODING'.format(sys.getdefaultencoding()))
                return False
            else:
                return True
        else:
            return True
    else:
        return True
