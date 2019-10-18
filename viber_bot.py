from flask import Flask, request, Response
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages.text_message import TextMessage
from viberbot.api.viber_requests import ViberConversationStartedRequest
from viberbot.api.viber_requests import ViberFailedRequest
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberSubscribedRequest
from viberbot.api.viber_requests import ViberUnsubscribedRequest
from viberbot.api.event_type import EventType

import time
import logging
import sched
import threading
import os

from finder_for_bot import chars_2_words

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

NAME = os.getenv("NAME", None)
AUTH = os.getenv("VIBERAUTH", None)
URL = os.getenv("URL", None)

if not NAME or not AUTH or not URL:
    print("Set env var for NAME, VIBERAUTH, URL")
    exit(1)

app = Flask(__name__)
viber = Api(BotConfiguration(
    name='Game of Words',
    avatar='https://static.vecteezy.com/system/resources/previews/000/431/275/original/english-alphabets-in-many-colors-vector.jpg',
    auth_token='4a77884d38e7d449-db89dea2aa96bcab-e1c563c6dc7207e0'
))


@app.route('/', methods=['GET'])
def HOME():
    # print("--------------------------------HOME--------------------------------")
    characters = request.args.get('c')
    length = request.args.get('l')

    if not characters or not length:
        return "<html><h1>Send us characters and length, we will provide valid words.</h1>" \
               "<p>Send word and length in get params.<br> " \
               "Example <a href='https://gameofwords.herokuapp.com?c=glreyc&l=6'>https://gameofwords.herokuapp.com<strong>?c=glreyc&l=6</strong></a>" \
               "</p></html>"
    else:
        try:
            length = int(length)
        except:
            return "<html><h3> Length must be integer value </h3></html>"

        valid_words = chars_2_words(characters, length)
        return "<html><h1>Valid Words</h1><h3>"+'<br>'.join(valid_words)+"</h3></html>"


@app.route('/', methods=['POST'])
def incoming():
    # logger.debug("received request. post data: {0}".format(request.get_data()))
    # print("--------------------------------{}--------------------------------".format(request.get_data()))

    try:
        # print("--------------------------------INSIDE TRY--------------------------------")
        viber_request = viber.parse_request(request.get_data())

        if isinstance(viber_request, ViberMessageRequest):
            # print("NEW REQUEST", viber_request.sender.id, viber_request.message.text)
            # viber.send_messages(viber_request.sender.id, [
            #     TextMessage(text="SOME OF MY MESSAGE "+viber_request.message.text)])
            # '''
            user_message = viber_request.message.text.lower().split(' ')
            if len(user_message) == 3 and user_message[0] == 'find':
                characters, length = user_message[1], user_message[2]
                valid_words = chars_2_words(characters, length)
                word_str = '\n'.join(valid_words)
                message = "Valid Words:\n" + word_str
                viber.send_messages(viber_request.sender.id, [
                    TextMessage(text=message)])
            else:
                message = 'Invalid Format.\nPlease send "find <characters> <length>".\n Example "find glreyc 6".'
                viber.send_messages(viber_request.sender.id, [
                    TextMessage(text=message)])

            message = 'Sender: ' + viber_request.sender.name + '\nMessage: ' + viber_request.message.text + \
                      '\nResponse:\n' + message
            viber.send_messages("xBErJXaqmOexp2rliAXWEQ==", [
                TextMessage(text=message)
            ])
            # '''
        elif isinstance(viber_request, ViberConversationStartedRequest) \
                or isinstance(viber_request, ViberSubscribedRequest) \
                or isinstance(viber_request, ViberUnsubscribedRequest):
            message = 'Welcome to word finder.\nPlease send "find <characters> <length>".\n Example "find glreyc 6".'
            viber.send_messages(viber_request.sender.id, [
                TextMessage(None, None, viber_request.get_event_type())
            ])
            viber.send_messages(viber_request.sender.id, [
                TextMessage(text=message)])
        elif isinstance(viber_request, ViberFailedRequest):
            logger.warning("client failed receiving message. failure: {0}".format(viber_request))

        # elif isinstance(viber_request, EventType.WEBHOOK):
            # logger.debug("WEBHOOKEVENTS: {0}".format(request.get_data()))
            # print("--------------------------------WEBHOOKEVENTS--------------------------------")
    except Exception as e:
        return "--------------------------------ERRRRRRRRRRRRRRRRRRRR--------------------------------" + str(e)

    return Response(status=200)


def set_webhook(viber):
    # print("--------------------------------SET WEBHOOK--------------------------------")
    # I used heroku as it is easier and serves over https
    viber.set_webhook('https://gameofwords.herokuapp.com', [EventType.WEBHOOK, EventType.CONVERSATION_STARTED, EventType.DELIVERED, EventType.MESSAGE, EventType.SUBSCRIBED, EventType.UNSUBSCRIBED, EventType.FAILED, EventType.SEEN])


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1>"


if __name__ == "__main__":
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(13, 1, set_webhook, (viber,))
    t = threading.Thread(target=scheduler.run)
    t.start()

    app.run(host='0.0.0.0', port=int(os.getenv("PORT", "8443")), debug=True)
