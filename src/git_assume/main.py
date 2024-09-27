import argparse
import configparser
import logging
import os
import sys
from logging import Logger, getLogger
from typing import Dict, List, Optional

from git_assume import utils

LOGGER_CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "logger_config.yml"))

DEFAULT_NETRC_SHORTTERM_PATH = f"{os.path.expanduser("~")}/.netrc"
DEFAULT_NETRC_LONGTERM_PATH = f"{os.path.expanduser("~")}/.netrc-longterm"

def main(argv: Optional[List]=None):
    utils.setup_logger(LOGGER_CONFIG_PATH)

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    
    parser_assume = subparsers.add_parser("assume", help="see `assume -h`")
    parser_assume.add_argument(
        "profile",
        nargs="?",
        default="default"
    )
    parser_assume.add_argument(
        "--netrc-longterm",
        required=False,
        default=DEFAULT_NETRC_LONGTERM_PATH
    )
    parser_assume.add_argument(
        "--netrc",
        required=False,
        default=DEFAULT_NETRC_SHORTTERM_PATH
    )
    parser_assume.add_argument(
        "--log-level",
        help="Set log level",
        choices=["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"],
        required=False,
        default="INFO",
    )
    parser_assume.add_argument(
        "-y", "--yes",
        required=False,
        action='store_true'
    )
    parser_assume.set_defaults(handler=gitassume_assume)

    parser_assume = subparsers.add_parser("list", help="see `list -h`")
    parser_assume.add_argument(
        "--netrc-longterm",
        required=False,
        default=DEFAULT_NETRC_LONGTERM_PATH
    )
    parser_assume.add_argument(
        "--log-level",
        help="Set log level",
        choices=["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"],
        required=False,
        default="INFO",
    )
    parser_assume.set_defaults(handler=gitassume_list)

    if argv is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(argv)
    
    if hasattr(args, 'handler'):
        args.handler(args)
    else:
        parser.print_help()

def gitassume_assume(args: argparse.ArgumentParser):
    logger = getLogger(__name__)
    logger.setLevel(getattr(logging, args.log_level))

    validate_assume_args(args, logger)

    netrc_longterm_config = read_netrc_longterm(args.netrc_longterm, logger)
    validate_netrc_longterm_config(netrc_longterm_config, profile=args.profile, logger=logger)

    curr_netrc = read_netrc(args.netrc, logger)
    logger.debug(f"Successfully read .netrc: {args.netrc}")
    logger.debug("current .netrc setting:")
    for key, value in curr_netrc.items():
        logger.debug(f"  {key} = {value}")
    
    while not args.yes:
        ans = utils.ask(f"Are you sure to overwrite {args.netrc} with profile `{args.profile}`??")
        if ans is None:
            continue
        if not ans:
            logger.info(f"No update on {args.netrc}")
            sys.exit(0)
        elif ans:
            break
    
    write_netrc(netrc_longterm_config[args.profile], args.netrc, logger)

def gitassume_list(args: argparse.ArgumentParser):
    logger = getLogger(__name__)
    logger.setLevel(getattr(logging, args.log_level))

    validate_list_args(args, logger)

    netrc_longterm_config = read_netrc_longterm(args.netrc_longterm, logger)
    validate_netrc_longterm_config(netrc_longterm_config, profile=None, logger=logger)
    print(f"Profiles that exist in .netrc-longterm: {args.netrc_longterm}")
    for section in netrc_longterm_config.sections():
        print(f"- {section}")


def validate_netrc_longterm_config(netrc_longterm_config: configparser.ConfigParser, logger: Logger, profile: Optional[str]=None):
    if profile is not None and profile not in netrc_longterm_config:
        raise KeyError(f"Expected profile `{profile}` does not exist.")

    required_attributes = ("machine", "login", "password")
    for section in netrc_longterm_config.sections():
        for attr in required_attributes:
            if attr not in netrc_longterm_config[section] or netrc_longterm_config[section][attr] == "":
                raise KeyError(f"Attribute `{attr}` does not exist in profile `{profile}`")

    logger.debug(
        "Config file validation finished. "
        "All required attributes exist."
    )


def read_netrc(filename: str, logger: Logger) -> Dict[str,str]:
    with open(filename, "r") as f:
        ret = {}
        for line in f:
            line = line.strip()
            # ignore blank lines and comments
            if line == "" or line.startswith("#"):
                continue
            elements = [ elem for elem in line.split(" ") if not elem.startswith("#")]

            if len(elements) != 2:
                raise Exception(f"File format invalid. Each line of {filename} must be 2.")
            
            ret[elements[0].strip()] = elements[1].strip()
    return ret

def write_netrc(netrc: Dict[str,str], filename: str, logger: Logger):
    with open(filename, "w") as f:
        for key, value in netrc.items():
            f.write(f"{key} {value}\n")
            logger.debug(f"Successfully write: {key} = {value}")
    logger.info(f"Successfully write to .netrc: {filename}")


def validate_assume_args(args: argparse.ArgumentParser, logger: Logger):
    # validate netrc file
    if not os.path.isfile(args.netrc):
        raise FileNotFoundError(f"{args.netrc} does not exist.")
    logger.debug(f"Found .netrc: {args.netrc}")

    # validate netrc-longterm file
    if not os.path.isfile(args.netrc_longterm):
        raise FileNotFoundError(f"{args.netrc_longterm} does not exist.")
    logger.debug(f"Found .netrc-longterm: {args.netrc_longterm}")

def validate_list_args(args: argparse.ArgumentParser, logger: Logger):
    # validate netrc-longterm file
    if not os.path.isfile(args.netrc_longterm):
        raise FileNotFoundError(f"{args.netrc_longterm} does not exist.")
    logger.debug(f"Found .netrc-longterm: {args.netrc_longterm}")

def read_netrc_longterm(filename: str, logger: Logger) -> configparser.ConfigParser:
    config = configparser.ConfigParser()    
    try:
        config.read(filename)
    except configparser.ParsingError:
        logger.error(f"Can't parse {filename}")
        sys.exit(1)

    logger.debug(f"Successfully parsed {filename}")
    return config


if __name__ == "__main__":
    main()
