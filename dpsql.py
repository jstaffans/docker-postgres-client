#!/usr/bin/env python
# -*- coding: utf-8 -*-
##############################################################################
# The MIT License (MIT)

# Copyright (c) 2015 Augustin Cisterne-Kaas

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
##############################################################################
from docker_postgres_client import Client
import os


class Psql(Client):
    def parser(self):
        parser = super(Psql, self).parser()
        parser.add_argument('-d', '--database', help="Database name")
        parser.add_argument('-f', '--file', help="File to import")
        return parser

    def docker_cmd(self):
        args = self.args
        res = super(Psql, self).docker_cmd()
        if args.file:
            # get the file directory name to mount it as /tmp
            pwd = os.path.dirname(os.path.realpath(args.file))
            res.append('--volume %s:/tmp' % pwd)
        return res

    def container_cmd(self):
        # mount a volume if a file is passed as argument
        args = self.args
        res = ['psql -h db -p %s -U %s' % (args.port, args.user)]
        if args.database:
            res.append('-d %s' % args.database)
        # import the file from the mounted volume
        if args.file:
            res.append('-f /tmp/%s' % os.path.basename(args.file))
        return res


def main():
    psql = Psql()
    psql.run()

if __name__ == '__main__':
    main()
