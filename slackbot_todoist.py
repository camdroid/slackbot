import todoist
from secrets import TODOIST_API_KEY
from config import todoist_inbox_id



class Todoist(object):
    #TODO Figure out how to get this dynamically

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
        return self.project['items']

    def parse_commands(self, commands):
        if commands[0] == 'list':
            return self.list()
