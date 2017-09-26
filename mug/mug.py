#!/usr/bin/env python
"""Utility to manage Github organization users via the github api.

Author: Ben Andre <andre@ucar.edu>

"""

from __future__ import print_function

import sys

if sys.hexversion < 0x02070000:
    print(70 * "*")
    print("ERROR: {0} requires python >= 2.7.x. ".format(sys.argv[0]))
    print("It appears that you are running python {0}".format(
        ".".join(str(x) for x in sys.version_info[0:3])))
    print(70 * "*")
    sys.exit(1)

#
# built-in modules
#
import argparse
import os
import traceback

if sys.version_info[0] == 2:
    from ConfigParser import SafeConfigParser as config_parser
else:
    from configparser import ConfigParser as config_parser

#
# installed dependencies
#
from github import Github

#
# other modules in this package
#


# -------------------------------------------------------------------------------
#
# User input
#
# -------------------------------------------------------------------------------
def commandline_options():
    """Process the command line arguments.

    """
    parser = argparse.ArgumentParser(
        description='manage users in a github organization')

    parser.add_argument('--backtrace', action='store_true',
                        help='show exception backtraces as extra debugging '
                        'output')

    parser.add_argument('--debug', action='store_true',
                        help='extra debugging output')

    parser.add_argument('--config', nargs=1, default=['../mug.cfg'],
                        help='path to config file')

    options = parser.parse_args()
    return options


def read_config_file(filename):
    """Read the configuration file and process

    """
    print("Reading configuration file : {0}".format(filename))

    cfg_file = os.path.abspath(filename)
    if not os.path.isfile(cfg_file):
        raise RuntimeError("Could not find config file: {0}".format(cfg_file))

    config = config_parser()
    config.read(cfg_file)

    return config


# -------------------------------------------------------------------------------
#
# work functions
#
# -------------------------------------------------------------------------------
def view_user(gh):
    """experiment with users
    """
    gh_user = gh.get_user()

    print("{0}".format(gh_user.login))
    for repo in gh_user.get_repos():
        print("  {0} - {1}".format(repo.name, repo.owner))


def view_org(gh, org_name):
    """experiment with organizations
    """
    org = gh.get_organization(org_name)
    for member in org.get_members():
        print("{0} : {1}".format(org.login, member.login))

    for repo in org.get_repos():
        print("  {0} - ".format(repo.name), end='')
        for collab in repo.get_collaborators():
            print("{0}, ".format(collab.login), end='')
        print()


# -------------------------------------------------------------------------------
#
# main
#
# -------------------------------------------------------------------------------

def main(options):
    config = read_config_file(options.config[0])
    _user = config.get("github", "user")
    _token = config.get("github", "token")
    _organization = config.get("github", "organization")
    gh = Github(_user, _token)

    if False:
        view_user(gh)

    view_org(gh, _organization)

    return 0


if __name__ == "__main__":
    options = commandline_options()
    try:
        status = main(options)
        sys.exit(status)
    except Exception as error:
        print(str(error))
        if options.backtrace:
            traceback.print_exc()
        sys.exit(1)