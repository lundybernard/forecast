from argparse import ArgumentParser, RawDescriptionHelpFormatter, Namespace
from textwrap import dedent
from logging import getLogger

from ..conf import get_config


log = getLogger(__name__)


def testing_cli() -> ArgumentParser:
    test = ArgumentParser(
        prog="test",
        formatter_class=RawDescriptionHelpFormatter,
        description=dedent(
            """\
                execute functional tests against target service"
            """
        ),
    )
    # Default behavior if no sub-command is given
    # example.set_defaults(func=get_help(example))
    test.set_defaults(func=Commands.test)

    test.add_argument(
        "-H",
        "--host",
        dest="host",
        default="0.0.0.0",
        help="host ip on which the service will be run",
    )
    test.add_argument(
        "-P",
        "--port",
        dest="port",
        default="5000",
        help="port on which the service service will be run",
    )

    commands = test.add_subparsers(
        dest="command",
        title="commands",
        description="for additonal details on each command use: "
        '"bat {command name} --help"',
    )

    service = commands.add_parser(
        "service",
        description="execute e2etests against target service",
        help="for details use test --help",
    )
    service.set_defaults(func=Commands.test)

    # run_functional_tests args
    run_functional_tests = commands.add_parser(
        "run_functional_tests",
        description="start the server locally and run functional tests",
        help="for details use run_functional_tests --help",
    )
    run_functional_tests.set_defaults(func=Commands.run_functional_tests)

    # run_functional_tests args
    run_container_tests = commands.add_parser(
        "run_container_tests",
        description="start docker-compose and run functional tests",
        help="for details use test --help",
    )
    run_container_tests.set_defaults(func=Commands.run_container_tests)
    return test


class Commands:
    @staticmethod
    def test(_: Namespace):
        print("++ run functional tests ++")
        import unittest

        loader = unittest.TestLoader()
        suite = loader.discover("tests", pattern="*_test.py")
        runner = unittest.TextTestRunner()
        runner.run(suite)

    @staticmethod
    def run_functional_tests(args: Namespace):
        import subprocess
        import os
        import signal
        from time import sleep

        a = subprocess.Popen(["bat", "server", "start"])
        sleep(0.5)
        Commands.test(args)
        os.kill(a.pid, signal.SIGTERM)

    @staticmethod
    def run_container_tests(conf):
        import subprocess
        import os
        import signal
        from time import sleep

        a = subprocess.Popen(["docker-compose", "up"])
        sleep(0.5)
        Commands.test(conf)

        os.kill(a.pid, signal.SIGTERM)
        sleep(0.5)
