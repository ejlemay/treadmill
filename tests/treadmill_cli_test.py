"""Unit test Treadmill CLI.
"""

import unittest

# Disable W0611: Unused import
import tests.treadmill_test_deps  # pylint: disable=W0611

import click
import click.testing
import mock

from treadmill import context
from treadmill.cli import scheduler as scheduler_cli
from treadmill.cli import blackout as blackout_cli
from treadmill.cli import configure as configure_cli
from treadmill.cli import discovery as discovery_cli
from treadmill.cli import sproc as sproc_cli
from treadmill.cli.admin import show as admin_show_cli

from treadmill.sproc import zk2fs as zk2fs_sproc


def check_help(testcase, args):
    """Checks help invocation."""
    testcase.assertEquals(
        testcase.runner.invoke(testcase.cli, args + ['--help']).exit_code, 0)


class TreadmillShowTest(unittest.TestCase):
    """Mock test for 'treadmill show' CLI"""

    def setUp(self):
        context.GLOBAL.dns_domain = 'xxx.com'
        self.module = admin_show_cli
        self.runner = click.testing.CliRunner()
        self.cli = self.module.init()

    def test_help(self):
        """Test help with no arguments."""
        check_help(self, [])
        check_help(self, ['--cell', '-', 'pending'])

    @mock.patch('treadmill.context.ZkContext._resolve', mock.Mock())
    @mock.patch('kazoo.client.KazooClient.get_children', mock.Mock())
    def test_action(self):
        """Test show actions."""
        self.runner.invoke(
            self.cli, ['--cell', 'foo', 'running'])
        self.assertEquals(context.GLOBAL.cell, 'foo')


class TreadmillSchedulerTest(unittest.TestCase):
    """Mock test for 'treadmill scheduler' CLI"""

    def setUp(self):
        context.GLOBAL.dns_domain = 'xxx.com'
        self.module = scheduler_cli
        self.runner = click.testing.CliRunner()
        self.cli = self.module.init()

    def test_help(self):
        """Test help with no arguments."""
        check_help(self, [])
        check_help(self, ['--cell', '-', 'view'])
        check_help(self, ['--cell', '-', 'view', 'allocs'])
        check_help(self, ['--cell', '-', 'view', 'servers'])
        check_help(self, ['--cell', '-', 'view', 'apps'])
        check_help(self, ['--cell', '-', 'view', 'queue'])

    @mock.patch('treadmill.context.ZkContext._resolve', mock.Mock())
    @mock.patch('kazoo.client.KazooClient.get_children', mock.Mock())
    def test_action(self):
        """Test scheduler commands."""
        self.runner.invoke(
            self.cli, ['--cell', 'foo', 'view', 'servers'])
        self.assertEquals(context.GLOBAL.cell, 'foo')


class TreadmillBlackoutTest(unittest.TestCase):
    """Mock test for 'treadmill blackout' CLI"""

    def setUp(self):
        context.GLOBAL.dns_domain = 'xxx.com'
        self.module = blackout_cli
        self.runner = click.testing.CliRunner()
        self.cli = self.module.init()

    def test_help(self):
        """Test help with no arguments."""
        check_help(self, [])
        check_help(self, ['--cell', '-', 'app'])
        check_help(self, ['--cell', '-', 'server'])


class TreadmillConfigureTest(unittest.TestCase):
    """Mock test for 'treadmill configure' CLI"""

    def setUp(self):
        context.GLOBAL.dns_domain = 'xxx.com'
        self.module = configure_cli
        self.runner = click.testing.CliRunner()
        self.cli = self.module.init()

    def test_help(self):
        """Test help with no arguments."""
        check_help(self, [])


class TreadmillDiscoveryTest(unittest.TestCase):
    """Mock test for 'treadmill configure' CLI"""

    def setUp(self):
        context.GLOBAL.dns_domain = 'xxx.com'
        self.module = discovery_cli
        self.runner = click.testing.CliRunner()
        self.cli = self.module.init()

    def test_help(self):
        """Test help with no arguments."""
        check_help(self, [])


class TreadmillSprocTest(unittest.TestCase):
    """Mock test for 'treadmill configure' CLI"""

    def setUp(self):
        context.GLOBAL.dns_domain = 'xxx.com'
        self.module = sproc_cli
        self.runner = click.testing.CliRunner()
        self.cli = self.module.init()

    def test_help(self):
        """Test help with no arguments."""
        check_help(self, [])

    def test_args(self):
        """Test passing context arguments."""
        self.runner.invoke(
            self.cli, ['--cell', 'foo', 'init', '--help'])
        self.assertEquals(context.GLOBAL.cell, 'foo')
        self.runner.invoke(
            self.cli, ['--cell', 'xxx', '--zookeeper', 'bla',
                       'init', '--help'])
        self.assertEquals(context.GLOBAL.cell, 'xxx')
        self.assertEquals(context.GLOBAL.zk.url, 'bla')


class TreadmillZk2FsTest(unittest.TestCase):
    """Mock test for 'treadmill configure' CLI"""

    def setUp(self):
        context.GLOBAL.dns_domain = 'xxx.com'
        self.module = zk2fs_sproc
        self.runner = click.testing.CliRunner()
        self.cli = self.module.init()

    def test_help(self):
        """Test help with no arguments."""
        check_help(self, [''])


if __name__ == '__main__':
    unittest.main()
