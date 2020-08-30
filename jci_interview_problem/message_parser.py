"""Parses messages with a provided data source and search criteria."""

import concurrent.futures
import logging

FIELD_DELIMETER = '|'
MESSAGE_DELIMETER = '||'

DEFAULT_CHUNK_SIZE = 1024 * 1024


def _worker(raw_messages, search_segment='', search_field_name=''):
    """A worker node which parses a subset of raw messages and returns the matching messages.

    Args:
        raw_messages (str): A string subset of raw (delimeted) messages.
        search_segment (Optional(str)): A segment to search for. If empty, results are not filtered by segment.
        search_field_name (Optional(str)): A field name to search for. If empty, results are not filtered by field name.

    Returns:
        List[str]: The matching messages.
    """
    logging.debug('starting worker node')

    messages = raw_messages.split(MESSAGE_DELIMETER)
    if not search_segment and not search_field_name:
        logging.debug('no search criteria')
        return messages

    returned_messages = []
    for message in messages:
        split = message.split(FIELD_DELIMETER)
        if (message and (not search_segment or split[0] == search_segment) and
                (not search_field_name or any(field for field in split[1:] if field[:3] == search_field_name))):
            returned_messages.append(message)

    return returned_messages


def parse(message_file, chunk_size=None, search_segment='', search_field_name='', limit=None):
    """Parses an open file handle for messages matching the provided search criteria.

    Args:
        message_file (File): A file object containint 0 or more messages.
        chunk_size (Optional(int)): The size of file chunk to read at a time.
        search_segment (Optional(str)): A segment to search for. If empty, results are not filtered by segment.
        search_field_name (Optional(str)): A field name to search for. If empty, results are not filtered by field name.
        limit (Optional(int)): The number of messages to return.

    Returns:
        List[str]: The matching messages.
    """
    logging.info('starting message parsing')
    returned_messages, running_futures, chunk_size = [], set(), chunk_size or DEFAULT_CHUNK_SIZE

    raw_messages, spillover_text = '', ''
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # assume the file is too large to fit into 2x RAM. Need to read more manually
        while True:
            # read a block of messages
            raw_messages = message_file.read(chunk_size)
            raw_messages_len = len(raw_messages)

            # append any spillover text
            if spillover_text:
                logging.debug('appending spillover text: %s', spillover_text)
                raw_messages = spillover_text + raw_messages

            if not raw_messages_len and not spillover_text:
                # nothing left to read
                break

            if raw_messages_len == chunk_size or raw_messages[-2:] == MESSAGE_DELIMETER:
                # parse out the last (presumably) incomplete message or a trailing delimeter
                raw_messages, match, spillover_text = raw_messages.rpartition(MESSAGE_DELIMETER)

                if not match:
                    # we haven't read enough data yet - keep reading
                    continue
            else:
                logging.debug('reached end of file')
                spillover_text = ''

            running_futures.add(executor.submit(_worker, raw_messages, search_segment, search_field_name))

            # wait to check if any processing has finished to check against the limit and potentially return early
            finished_futures, running_futures = concurrent.futures.wait(
                running_futures, 1, concurrent.futures.FIRST_COMPLETED)

            for future in finished_futures:
                returned_messages.extend(future.result())

            if (limit and len(returned_messages) >= limit) or raw_messages_len < chunk_size:
                break

        # wait for any remaining futures to finish
        finished_futures, _ = concurrent.futures.wait(running_futures, 1, concurrent.futures.FIRST_COMPLETED)
        for future in finished_futures:
            returned_messages.extend(future.result())

        return returned_messages[:limit]
