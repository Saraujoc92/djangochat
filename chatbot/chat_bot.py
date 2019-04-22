from channels import Group
import threading
import json
import csv
import os
import redis
import time
import signal

_isInstantiated = False

STOCK_QUOTE = 'APPL.US quote is $93.42 per share'
STOCK_COMMAND = 'stock'


def start_chatbot():
    global _isInstantiated
    if _isInstantiated:
        return
    _isInstantiated = True
    Chatbot()


'''
Chatbot Class. Meant to be a singleton. Receives commands through redis channel 'command'
and returns the output through the channel 'message'.
'''
class Chatbot():
    def __init__(self, *args, **kwargs):

        self.r = redis.Redis(host='localhost', port=6379)
        t = threading.Thread(target=self.listen_for_messages)
        t.daemon = True
        t.start()

    def listen_for_messages(self):

        p = self.r.pubsub()
        p.subscribe('command')

        while True:
            message = p.get_message()
            if message:
                self.process_message(message['data'])
            time.sleep(0.1)


    def process_message(self, message):
        try:
            answer = self.get_answer(message.decode("utf-8"))
            my_dict = {'user': 'Bot', 'message': answer}

            self.r.publish('message', json.dumps(my_dict))
        except:
            pass


    def get_answer(self, message):
        try:
            command, arg = self.process_command(message)
        except:
            return 'Sorry, couldn\'t understand the command <b>%s</b>' % message

        if command != STOCK_COMMAND:
            return 'Ooops, I can only understand the command <b>/%s</b>' % STOCK_COMMAND
        else:
            return self.get_value_for(arg)


    def process_command(self, message):

        assert message[0] == '/'
        message = message[1:]
        message = message.split('=', 1)

        command = message[0]
        arg = message[1]

        return command, arg


    def get_value_for(self, stock_id):

        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, './aapl.us.csv')
        with open(file_path, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                if row["Symbol"].lower() == stock_id.lower():
                    return STOCK_QUOTE
            return 'No data for company %s' % stock_id