import json


class Event:
    id = 1

    def __init__(self, name, local=''):
        self.name = name
        self.local = local
        self.id = Event.id
        Event.id += 1

    def print_information(self):
        print(f'Event id: {self.id}')
        print(f'Event name: {self.name}')
        print(f'Event local: {self.local}')
        print('-------------')

    def to_json(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def calculate_limit_persons_area(area):
        if 5 <= area < 10:
            return 5
        elif 10 <= area < 20:
            return 15
        elif area >= 20:
            return 30
        else:
            return 0
