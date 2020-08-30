"""Test jci_interview_problem.message_parser"""

import io
import unittest

from jci_interview_problem import message_parser


class TestMessageParser(unittest.TestCase):
    def test_empty_file(self):
        """Tests providing an empty file of messages."""
        messages = message_parser.parse(io.StringIO(''))

        self.assertEqual(messages, [])

    def test_single_message_no_search(self):
        """Tests a file with a single message and no search criteria."""
        sample_message = 'NAM|FNAFred|LNABlogs'
        input_file = io.StringIO(sample_message + '||')

        messages = message_parser.parse(input_file)

        self.assertEqual(messages, [sample_message])

    def test_single_message_no_eof_delimeter(self):
        """Tests a file with a single message and no end of file || delimeter."""
        sample_message = 'NAM|FNAFred|LNABlogs'
        input_file = io.StringIO(sample_message)

        messages = message_parser.parse(input_file)

        self.assertEqual(messages, [sample_message])

    def test_search_segment(self):
        """Tests searching with a segment search criteria."""
        input_messages = ['NAM|FNAFred|LNABlogs', 'BIO|DOB02/03/1974']
        input_file = io.StringIO('||'.join(input_messages))

        messages = message_parser.parse(input_file, segment='NAM')

        self.assertEqual(messages, [input_messages[0]])

    def test_search_field_name(self):
        """Tests searching with a field name search criteria."""
        input_messages = ['NAM|FNAFred|LNABlogs', 'BIO|DOB02/03/1974']
        input_file = io.StringIO('||'.join(input_messages))

        messages = message_parser.parse(input_file, field_name='DOB')

        self.assertEqual(messages, [input_messages[1]])

    def test_search_segment_and_field_name(self):
        """Tests searching with segment and field name search criteria."""
        input_messages = ['NAM|FNAFred|LNABlogs', 'BIO|DOB02/03/1974']
        input_file = io.StringIO('||'.join(input_messages))

        messages = message_parser.parse(input_file, segment='BIO', field_name='DOB')

        self.assertEqual(messages, [input_messages[1]])

    def test_return_limit(self):
        """Tests returning only a subset of found messages."""
        input_messages = ['NAM|FNAFred|LNABlogs', 'BIO|DOB02/03/1974']
        input_file = io.StringIO('||'.join(input_messages))

        messages = message_parser.parse(input_file, limit=1)

        self.assertEqual(messages, [input_messages[0]])
