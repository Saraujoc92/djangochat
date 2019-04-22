from django.test import SimpleTestCase
from .chat_bot import Chatbot, STOCK_QUOTE, STOCK_COMMAND


class ChatbotTests(SimpleTestCase):
    def setUp(self):
        self.chatbot = Chatbot()

    def test_known_stock_code(self):
        known_code = 'aapl.us'
        quote = self.chatbot.get_value_for(known_code)
        self.assertEquals(quote, STOCK_QUOTE)

    def test_unknown_stock_code(self):
        unknown_id = 'unknown'
        quote = self.chatbot.get_value_for(unknown_id)
        self.assertEquals(quote, 'No data for company %s' % unknown_id)

    def test_parse_invalid_command(self):
        invalid_command = '/stock;stock_code'
        with self.assertRaises(IndexError):
            self.chatbot.process_command(invalid_command)

    def test_parse_non_command(self):
        invalid_command = 'stock=stock_code'
        with self.assertRaises(AssertionError):
            self.chatbot.process_command(invalid_command)

    def test_parse_valid_command(self):
        invalid_command = '/stokk=stock_code'
        answer = self.chatbot.process_command(invalid_command)
        self.assertEquals(answer, ('stock', 'stock_code'))

    def test_answer_unknown_command(self):
        invalid_command = '/stokk=stock_code'
        answer = self.chatbot.get_answer(invalid_command)
        self.assertEquals(
            answer, 'Ooops, I can only understand the command <b>/%s</b>' %
            STOCK_COMMAND)

    def test_parse_unknowk_id(self):
        stock_id = 'stock_code'
        unknown_id_command = '/stock=%s' % stock_id
        answer = self.chatbot.get_answer(unknown_id_command)
        self.assertEquals(answer, 'No data for company %s' % stock_id)

    def test_parse_valid_command(self):
        known_id = 'aapl.us'
        valid_command = '/stock=%s' % known_id
        answer = self.chatbot.get_answer(valid_command)
        self.assertEquals(answer, STOCK_QUOTE)
