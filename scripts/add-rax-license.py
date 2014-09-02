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

import argparse
import os


LICENSE = """# Copyright 2014, Rackspace US, Inc.
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
"""


def arguments():
    """Setup argument Parsing."""

    parser = argparse.ArgumentParser(
        usage='%(prog)s',
        description='Rackspace Openstack, License add',
        epilog='Ensure license headers on all files found in a given path')

    parser.add_argument(
        '-p',
        '--path',
        help='Path to search',
        required=True,
        default=None
    )

    parser.add_argument(
        '-f',
        '--file-type',
        help='file type to search for default: [ %(default)s ]',
        required=False,
        default='yml'
    )

    return vars(parser.parse_args())


def file_getter(path, file_type):
    """Recursively get all files in a provided path.

    :param path: ``str`` path to directory to get files from.
    :return: ``list``
    """

    files = []
    full_path = os.path.abspath(os.path.expanduser(path))
    if not os.path.isdir(full_path):
        raise SystemExit(
            'Provided path [ %s ] is not a directory' % full_path
        )

    for root, _, file_names in os.walk(full_path):
        for file_name in file_names:
            if file_name.endswith(file_type):
                files.append(os.path.join(root, file_name))
    else:
        return files


def check_files(file_names):
    """Inspect files for a license header.

    :param file_names: ``list`` names of files to check for licenses.
    :return: ``list``
    """

    files_missing_licenses = []
    for file_name in file_names:
        with open(file_name, 'rb') as f:
            file_contents = f.read()

        if LICENSE not in file_contents:
            files_missing_licenses.append(file_name)
    else:
        return files_missing_licenses


def add_licenses(file_names):
    """Insert the license header into the files.

    :param file_names: ``list`` names of files to check for licenses.
    """

    for file_name in file_names:
        if not os.path.isfile(file_name):
            continue
        else:
            print('Adding license header to [ %s ]' % file_name)

        # Open original file and read the contents as lines
        with open(file_name, 'rb') as f:
            orig_file = f.readlines()

        index = 0
        # Used to detect a script
        if orig_file[index].startswith('!#'):
            index += 1

        # Used to detect yaml documents
        if orig_file[index].startswith('---'):
            index += 1

        # Prepend the license to the file
        for line in LICENSE.splitlines():
            if not line.endswith('\n'):
                line = '%s\n' % line

            orig_file.insert(index, line)
            index += 1
        else:
            orig_file.insert(index, '\n')

        # Write back the changes to the original file
        with open(file_name, 'wb') as f:
            f.writelines(orig_file)


def main():
    """Run the main application."""

    args = arguments()
    all_files = file_getter(path=args['path'], file_type=args['file_type'])
    files_missing_licenses = check_files(file_names=all_files)
    fml_count = len(files_missing_licenses)
    notice = (
        'Found [ %s ] files with extension [ %s ]' % (
            len(all_files), args['file_type']
        )
    )

    print(notice)
    print('Files missing licenses [ %s ]' % fml_count)

    add_licenses(file_names=files_missing_licenses)


if __name__ == '__main__':
    main()
