import telebot
import json
from threading import Thread, Event

bot = telebot.AsyncTeleBot()
stop_event = Event()
commands_sent = []
google_assistant_reply = []
chat_id = 511021111
variables = {'Targets_Commands': 'pc laptop wakeup'}

def send_given_reqest(target, command):
    """Function send request to next point in chain. Return True if it needs to be waiting for respond."""
    request = {"target": target, "command": command}
    message = json.dumps(request)
    commands_sent.append({key: request[key] for key in ("target", "command")})

    message_sended = bot.send_message(chat_id, message).wait()
    bot.delete_message(message_sended.chat.id, message_sended.message_id)
#    print("Command send: ", message)


def wait_for_request():
    """Function returns answer of request."""
    while commands_sent:
        updates = bot.get_updates(offset=(bot.last_update_id + 1), timeout=1)
        bot.process_new_updates(updates)
        if stop_event.is_set():
            break


@bot.message_handler(content_types=['text'])
def get_reply(message):
    if message.chat.id == chat_id:
        reply = json.loads(message.text)
        commands_sent.remove({key: reply[key] for key in ("target", "command")})
#        print("Command replyed: ",  reply)
    # getting program reply for google assistant to say
        if reply["result"]:
            google_assistant_reply.append(reply["result"])

    else:
        bot.send_message(message.chat.id, 'Sorry, it`s private bot.')


def main():
    """Function gets google assistant request, handle it and returns answer."""
    _ = set(variables['Targets_Commands'].split(' '))
    targets, commands = _ & {'pc', 'laptop'}, _ - {'pc', 'laptop'}
    for target in targets:
        for command in commands:
            send_given_reqest(target, command)
    action_thread = Thread(target=wait_for_request)
    action_thread.start()
    action_thread.join(timeout=20)
    stop_event.set()
    if not google_assistant_reply:
        google_assistant_reply.append("Sorry, server is unreachable.")
    print(google_assistant_reply)
    variables[ "Google_assistant_answers" ] = google_assistant_reply


if __name__ == '__main__':
    main()
