import todoist
from secrets import TODOIST_API_KEY
from secrets import todoist_inbox_id



class Todoist(object):
    def __init__(self):
        self.api = todoist.TodoistAPI(TODOIST_API_KEY)

    def sync(self):
        return self.api.sync()

    def get_project(self, project_name='Inbox'):
        if project_name == 'Inbox':
            self.project = self.api.projects.get_data(todoist_inbox_id)
            return self.project

    def list(self):
        self.project = self.get_project()
        items = self.project['items']
        return items[:20]

    def parse_commands(self, commands):
        if not commands:
            print('Command not found')
            return
        if commands[0] == 'list':
            items = self.list()
            msgs = [item['content'] for item in items]
            return msgs

    def format_list(self, list):
        messages = ['{}) {}'.format(i, l) for i, l in enumerate(list)]
        msg = '\n'.join(messages)
        return msg
