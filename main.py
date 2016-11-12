import os
from slackclient import SlackClient
from secrets import SLACKBOT_TOKEN
from secrets import TODOIST_API_KEY
import time
from slackbot_todoist import Todoist


BOT_NAME = 'test_bot'
BOT_ID = 'U2Z5U89FT'
slack_client = SlackClient(SLACKBOT_TOKEN)
AT_BOT = '<@' + BOT_ID +'>'
BOT_CHANNEL = 'D2ZRPJTMY'


def print_user_ids():
    api_call = slack_client.api_call('users.list')
    if api_call.get('ok'):
        users = api_call.get('members')
        for user in users:
            print('User ID for {} is {}'.format(user['name'], user.get('id')))
    else:
        print('Couldn\'t find users')


def parse_slack_output(slack_rtm_output):
    if slack_rtm_output:
        print('Slack output: {}'.format(slack_rtm_output))
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                text = output['text'].split(AT_BOT)[1].strip().lower()
                print('\nText: {}\nChannel: {}'.format(text, output['channel']))
                return text, output['channel']
    return None, None


def handle_command(command, channel):
    print('Received: \n{}\n in {}'.format(command, channel))
    commands = [c.lower() for c in command.split(' ')]
    if commands[0] == 'todo':
        todo = Todoist()
        results = todo.parse_commands(commands[1:])
        message = todo.format_list(results)
    slack_client.api_call('chat.postMessage', channel=channel,
                          text=message, as_user=True)


def main():
    READ_WEBSOCKET_DELAY = 1
    if slack_client.rtm_connect():
        print('{} is up and running!'.format(BOT_NAME))
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print('Connection failed.')


if __name__ == '__main__':
   main() 
