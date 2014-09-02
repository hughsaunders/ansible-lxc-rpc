#!/usr/bin/env python
# Copyright 2014, Rackspace US, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# (c) 2014, Kevin Carter <kevin.carter@rackspace.com>

import os
import subprocess
import sys


FAIL_Q = []


def get_file_names():
    """Return a list of all files in the vars/repo_packages directory."""
    paths = os.walk(os.path.abspath('vars/repo_packages'))
    files = []
    for fpath, cpath, afiles in paths:
        files.extend(afiles)
    else:
        return files


def build_job(user_vars, pvt):
    # Iterate through the found file names and use it as the variable name

    try:
        base_command = [
            'ansible-playbook',
            '-e',
            '@%s' % user_vars,
            'playbooks/utils/py-source-archive.yml',
            '-e',
            'repo_package_var="%s"' % pvt
        ]
        subprocess.check_call(' '.join(base_command), shell=True)
    except subprocess.CalledProcessError as exp:
        FAIL_Q.append({'repo_package_var': pvt, 'error': exp})


def main():
    cwd = os.getcwd()
    if os.path.basename(cwd) != 'rpc_deployment':
        raise SystemExit(
            'you are in the directory [ %s ] please move to rpc_deployment'
            ' to execute this script' % cwd
        )

    if len(sys.argv) < 2:
        raise SystemExit(
            'You are required to pass a user_variables.yml file. This file'
            ' should be in $HOME/rpc_deploy/user_variables.yml or '
            ' /etc/rpc_deploy/user_variables.yml.'
        )
    else:
        user_vars = sys.argv[1]
        if user_vars == '-e':
            print Warning('There is no need to use "-e" in this script')
            user_vars = sys.argv[2]

        if '@' in user_vars:
            print Warning('There is no need to use an "@" in this script')
            user_vars = user_vars.split('@')[-1]

        for file_name in get_file_names():
            build_job(user_vars, file_name)

        if FAIL_Q:
            for fail in FAIL_Q:
                print('FAILURES')
                print(fail)
        else:
            print('100% Success...')



if __name__ == "__main__":
    main()
