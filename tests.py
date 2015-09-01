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
import unittest
from mock import patch
from docker_postgres_client import Client
from dcreatedb import CreateDB
from ddropdb import DropDB
from dpsql import Psql
from dpg_dump import PgDump
import os


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.get_image_patcher = patch('docker_postgres_client.check_output')
        self.mock_shellout = self.get_image_patcher.start()
        self.mock_shellout.return_value = "'postgres:latest'"


class ClientTests(BaseTest):
    def setUp(self):
        super(ClientTests, self).setUp()
        self.client = Client([])
        self.parser = self.client.parser()

    def test_get_image_latest(self):
        output = self.client.get_image('containers_postgres_1')
        self.assertTrue(self.mock_shellout.called)
        self.assertEqual('postgres:latest', output)

    def test_get_image_specific_version(self):
        self.mock_shellout.return_value = "'postgres:9.4'"
        output = self.client.get_image('containers_postgres_1')
        self.assertTrue(self.mock_shellout.called)
        self.assertEqual('postgres:9.4', output)

    def test_parser_with_empty_args(self):
        args = self.parser.parse_args([])
        self.assertEqual('postgres', args.user)
        self.assertEqual('containers_postgres_1', args.container)
        self.assertEqual(5432, args.port)

    def test_parser_with_args(self):
        args = self.parser.parse_args(
            ['-U', 'bob', '-c', 'postgres', '-p', '5438'])
        self.assertEqual('bob', args.user)
        self.assertEqual('postgres', args.container)
        self.assertEqual(5438, int(args.port))

    def test_cmd(self):
        with self.assertRaises(NotImplementedError):
            self.client.cmd()

    def test_docker_cmd(self):
        self.assertEqual([], self.client.docker_cmd())

    def test_container_cmd(self):
        with self.assertRaises(NotImplementedError):
            self.client.container_cmd()


class CreateDBTests(BaseTest):
    def setUp(self):
        super(CreateDBTests, self).setUp()
        self.createdb = CreateDB(['blog'])

    def test_parser(self):
        parser = self.createdb.parser()
        args = parser.parse_args(['blog'])
        self.assertEqual('blog', args.database)

    def test_container_cmd(self):
        self.assertEqual(['createdb -h db -p 5432 -U postgres blog'],
                         self.createdb.container_cmd())


class DropDBTests(BaseTest):
    def setUp(self):
        super(DropDBTests, self).setUp()
        self.dropdb = DropDB(['blog'])

    def test_parser(self):
        parser = self.dropdb.parser()
        args = parser.parse_args(['blog'])
        self.assertEqual('blog', args.database)

    def test_container_cmd(self):
        self.assertEqual(['dropdb -h db -p 5432 -U postgres blog'],
                         self.dropdb.container_cmd())


class PsqlTests(BaseTest):
    def setUp(self):
        super(PsqlTests, self).setUp()
        self.psql = Psql([])

    def test_parser(self):
        parser = self.psql.parser()
        args = parser.parse_args(['-d', 'blog', '-f', 'blog.sql'])
        self.assertEqual('blog', args.database)
        self.assertEqual('blog.sql', args.file)

    def test_container_cmd(self):
        self.assertEqual(['psql -h db -p 5432 -U postgres'],
                         self.psql.container_cmd())

    def test_container_cmd_with_database(self):
        psql = Psql(['-d', 'blog'])
        self.assertIn('-d blog', psql.container_cmd())

    def test_container_cmd_with_file(self):
        psql = Psql(['-f', 'blog.sql'])
        self.assertIn('-f /tmp/blog.sql', psql.container_cmd())

    def test_docker_cmd(self):
        self.assertEqual([], self.psql.docker_cmd())

    def test_docker_cmd_with_file(self):
        psql = Psql(['-f', 'blog.sql'])
        pwd = os.getcwd()
        self.assertIn('--volume %s:/tmp' % pwd, psql.docker_cmd())


class PgDumpTests(BaseTest):
    def setUp(self):
        super(PgDumpTests, self).setUp()
        self.pgdump = PgDump(['blog'])
        self.parser = self.pgdump.parser()

    def test_parser(self):
        args = self.parser.parse_args(['blog'])
        self.assertEqual('blog', args.database)

    def test_parser_with_file(self):
        args = self.parser.parse_args(['blog', '-f', 'blog.sql'])
        self.assertEqual('blog.sql', args.file)

    def test_container_cmd(self):
        self.assertEqual(
            ['pg_dump -h db -p 5432 -U postgres -d blog', '> /tmp/blog.out'],
            self.pgdump.container_cmd())

    def test_container_cmd_with_file(self):
        # mount a volume if a file is passed as argument
        pgdump = PgDump(['blog', '-f', 'blog.sql'])
        self.assertEqual(
            ['pg_dump -h db -p 5432 -U postgres -d blog', '> /tmp/blog.sql'],
            pgdump.container_cmd())

    def test_docker_cmd(self):
        # mount a volume if a file is passed as argument
        pwd = os.getcwd()
        self.assertEqual(['--volume %s:/tmp' % pwd], self.pgdump.docker_cmd())

if __name__ == '__main__':
    unittest.main()
