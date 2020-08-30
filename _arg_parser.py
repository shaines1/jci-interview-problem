"""Parse command line arguments."""

import argparse


def parse():
    """Parse command line arguments.

    Returns:
        Namespace: Command line argument keys and values.
    """
    parser = argparse.ArgumentParser(
        description='perform message parsing and searching with provided search parameters')
    parser.add_argument('-v', '--verbose', action='store_true', help='increase verbosity of log messages')

    inputs_group = parser.add_argument_group('message sources')
    inputs_group.add_argument('--file', type=argparse.FileType('r'),
                              required=True, help='a file with messages separated by ||')

    optimizations_group = parser.add_argument_group('optimizations')
    optimizations_group.add_argument('--chunk_size', type=int, help='size of file to read in each chunk')

    search_group = parser.add_argument_group('search criteria')
    search_group.add_argument('--segment', type=str, help='an optional segment name to search for')
    search_group.add_argument('--field_name', type=str, help='an optional field name to search for')

    results_group = parser.add_argument_group('message results')
    results_group.add_argument('--limit', type=int, help='a limit on the number of messages to return')

    args = parser.parse_args()

    if args.limit is not None and args.limit <= 0:
        raise argparse.ArgumentTypeError('limit must be a possitive value ({} was provided)'.format(args.limit))
    if args.chunk_size is not None and args.chunk_size <= 0:
        raise argparse.ArgumentTypeError(
            'chunk_size must be a possitive value ({} was provided)'.format(args.chunk_size))

    return args
