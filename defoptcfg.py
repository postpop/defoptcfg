"""Love child of defopt and configargparse."""
import defopt
import sys
import logging
from typing import Callable, Iterable, Union, Dict


def run(func: Callable,
        config_argname: str = 'cfg',
        default_config_files: Union[str, Iterable[str]] = [],
        continue_on_missing_args: bool = False):
    """Process config files and command line arguments and run the given functions.

    Args:
        func
        config_argname: name of the command line argument for supplying the config file (default 'cfg'),
        default_config_files: list of strings for config files that are always loaded (default [])
        continue_on_missing_args:  (default False)

    Returns:
        return value of func

    TODO:
        test with more complex args

    """
    if isinstance(func, list):
        logging.warning(" Does not support lists of funcs - currently only works with single function calls.")

    # create parser that will run even when required args are missing from command line
    parser = defopt._create_parser(func, ignore_required=True, config_argname=config_argname)
    logging.debug(f" Processing command line args.")
    args = parser.parse_args(sys.argv[1:])
    logging.debug(f"   found required args {parser._required_args}.")

    # parse and merge all supplied config files into a single dict
    config_files = default_config_files
    if hasattr(args, config_argname):
        config_files = [*default_config_files, getattr(args, config_argname)]
    logging.debug(f" Reading config files")
    config = read_config_files(config_files)

    # get required args not supplied in command line
    missing_args = []
    for arg in parser._required_args:
        if args.__contains__(arg) and getattr(args, arg) is None:
            missing_args.append(arg)
        elif not args.__contains__(arg):
            missing_args.append(arg)
    logging.debug(f" Required args not supplied via command line: {missing_args}")

    # add config args - supply missing required args or override defaults
    supplied_args = []
    if config:
        logging.debug(f" Adding args from config files:")
        logging.debug(f"   {config}")
        # now add overwrite missing or default values with config
        for key, value in config.items():
            if hasattr(args, key):
                # if required args are None (we set this as a default for require values) set vals from from cfg
                if key in parser._required_args and getattr(args, key) is None:
                    setattr(args, key, value)
                    supplied_args.append(key)
                    logging.debug(f"   adding missing arg from cfg {key}:{value}")
                # if args still have default values override them from cfg
                elif getattr(args, key) == parser._arg_info[key]['default']:
                    setattr(args, key, value)  # only do if defaults
                    logging.debug(f"   overriding defaults from cfg {key}:{value}")

        logging.debug(f"   missing signals supplied from config: {supplied_args}")

    for missing_arg in missing_args:
        if missing_arg in supplied_args:
            missing_args.remove(missing_arg)
    logging.debug(f" Still missing: {missing_args}")
    if continue_on_missing_args:
        logging.debug(f"   You requested to ignore these - set to None and continue.")

    if missing_args and not continue_on_missing_args:
        raise NameError(f"{missing_args} not supplied by command line and missing in config file")

    logging.debug(f" Calling {func} with args namespace")
    logging.debug(f"   {args}.")
    defopt._call_function(parser, args._func, args)


def read_config_files(config_files: Iterable[str] = []) -> Dict:
    """Parse and merge config files."""
    if config_files:
        try:
            import yaml
        except ImportError:
            raise ImportError("Could not import yaml. It can be installed by running 'pip install PyYAML'")

    config = dict()
    for config_file in config_files:
        logging.debug(f"   Parsing config from {config_file}.")
        with open(config_file, 'r') as stream:
            try:
                this_config = yaml.load(stream)
            except yaml.YAMLError as exc:
                logging.error(exc)
        logging.debug(f"     found the following args:")
        logging.debug(f"     {this_config}")
        config = {**config, **this_config}
    logging.debug(f"   merges resulted in new config:")
    logging.debug(f"   {config}")
    return config
