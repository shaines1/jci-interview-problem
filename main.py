import logging

import _arg_parser
from jci_interview_problem import message_parser

LOGGING_FILENAME = '.jci_interview_problem.log'
LOGGING_FORMAT = '[%(asctime)-15s] %(levelname)-8s - %(name)s.%(funcName)s: %(message)s'


def main():
    """Command line interface to parse messages."""
    args = _arg_parser.parse()

    logging.basicConfig(filename=LOGGING_FILENAME, format=LOGGING_FORMAT)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG if args.verbose else logging.INFO)

    messages = message_parser.parse(args.message_file, args.segment, args.field_name, args.limit)

    print('Parsed and found {} messages:\n'.format(len(messages)))
    print('\n'.join(messages))


if __name__ == '__main__':
    main()
