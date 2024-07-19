from typing import Optional, Sequence

import logging
from argparse import ArgumentParser, Namespace
from sys import exit

from .server import server_parser
from .example.cli import example_cli
from .logconf import set_default_logging

from .lib import hello_world
from .testing.cli import testing_cli
from .conf import conf_cli


log = logging.getLogger("root")


def BATCLI(ARGS: Optional[Sequence[str]] = None):
    p = argparser()
    # Execute
    # get only the first command in args
    args: Namespace = p.parse_args(ARGS)
    Commands.setup_logging(args)
    log.debug(f"BATCLI: {args=}")
    try:
        log.debug(f"BATCLI: exec {args.func=}")
        args.func(args)
    except Exception as err:
        log.exception(err)
        p.print_help()
        exit(1)
    exit(0)


class NestedNameSpace(Namespace):
    def __setattr__(self, name, value):
        if "." in name:
            group, name = name.split(".", 1)
            ns = getattr(self, group, NestedNameSpace())
            setattr(ns, name, value)
            self.__dict__[group] = ns
        else:
            self.__dict__[name] = value


def argparser() -> ArgumentParser:
    p = ArgumentParser(
        description="Utility for executing various bat tasks",
        usage="bat [<args>] <command>",
    )
    p.set_defaults(func=get_help(p))

    p.add_argument(
        "-v",
        "--verbose",
        help="enable INFO output",
        action="store_const",
        dest="loglevel",
        const=logging.INFO,
    )
    p.add_argument(
        "--debug",
        help="enable DEBUG output",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
    )
    p.add_argument(
        "-c",
        "--conf",
        "--config_file",
        dest="config_file",
        default=None,
        help="specify a config file to get environment details from."
        " default=./config.yaml",
    )
    p.add_argument(
        "-e",
        "--env",
        "--config_environment",
        dest="config_env",
        default=None,
        help="specify the remote environment to use from the config file",
    )

    # Add a subparser to handle sub-commands
    commands = p.add_subparsers(
        dest="command",
        title="commands",
        description="for additonal details on each command use: "
        '"bat {command name} --help"',
    )
    # hello args
    hello = commands.add_parser(
        "hello",
        description="execute command hello",
        help="for details use hello --help",
    )
    hello.set_defaults(func=Commands.hello)

    commands.add_parser(
        "server",
        help="http server related commands",
        add_help=False,
        parents=[server_parser()],
    )
    # Add a subparser from a module
    commands.add_parser(
        "conf",
        help="configuration management cli",
        add_help=False,
        parents=[conf_cli()],
    )

    commands.add_parser(
        "test",
        help="run e2e tests for this service",
        add_help=False,
        parents=[testing_cli()],
    )

    return p


def get_help(parser):
    def help(_: Namespace):
        parser.print_help()

    return help


class Commands:

    @staticmethod
    def hello(_: Namespace):
        print(hello_world())

    @staticmethod
    def setup_logging(args: Namespace):
        if args.loglevel:
            set_default_logging(log_level=args.loglevel)
        else:
            set_default_logging(log_level="ERROR")

    @staticmethod
    def raise_exception(_: Namespace):
        raise RuntimeError("boom!")
