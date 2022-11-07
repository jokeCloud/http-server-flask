from event import Event


class EventOnline(Event):
    def __init__(self, name, _=''):
        local = f'https://greatevents.com/events?id={EventOnline.id}'
        super().__init__(name, local)

    def print_information(self):
        print(f'Event id: {self.id}')
        print(f'Event name: {self.name}')
        print(f'Link to go event: {self.local}')
        print('__________________')
