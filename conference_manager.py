import sys

from conference_config import *
from conference_utils import create_track_and_fill_track, print_sessions, validate_network_start_time
from task import Task
import re
from conference import Conference
from session import Session, SessionType

task_list = []


class ConferenceManager(object):
    def __init__(self, input_file):
        self.input_file = input_file

    def read_file_and_create_tasks(self):
        with open(self.input_file) as file:
            for line in file:
                if any(input_char.isdigit() for input_char in line):
                    res = re.split('(\d+)', line)
                else:
                    index = line.find(FIVE_MINUTES_STRING)
                    if index > 0:
                        res[0] = line[0:index - 1]
                        res[1] = FIVE_MINUTES_STRING
                    else:
                        raise Exception('Incorrect Data. Please provide a proper input')
                task = Task(res[0], res[1])
                task_list.append(task)
                task_list.sort(key=lambda input_task: input_task.task_minutes, reverse=True)

    def create_and_fill_sessions(self):
        session_list = []
        morning_session = Session(SessionType.Morning, MORNING_START_TIME, MORNING_SESSION_DURATION)
        self.fill_session(morning_session)
        session_list.append(morning_session)
        lunch_session = Session(SessionType.Lunch, LUNCH_START_TIME, LUNCH_SESSION_DURATION)
        lunch_session.add_slot('Lunch', LUNCH_SLOT_DURATION)
        session_list.append(lunch_session)
        noon_session = Session(SessionType.Noon, NOON_START_TIME, NOON_SESSION_DURATION)
        self.fill_session(noon_session)
        session_list.append(noon_session)
        networking_start_time = noon_session.next_slot_time
        validate_network_start_time(networking_start_time)
        networking_session = Session(SessionType.Networking,
                                     [networking_start_time.hour, networking_start_time.minute,
                                      networking_start_time.second], NETWORKING_SESSION_DURATION)
        networking_session.add_slot('Networking', NETWORKING_SLOT_DURATION)
        session_list.append(networking_session)
        return session_list

    @staticmethod
    def fill_session(session):
        for index, task_element in enumerate(task_list):
            if not task_element.is_scheduled and session.has_room(task_element.task_minutes):
                session.add_slot(task_element.task_name, task_element.task_minutes)
                task_element.is_scheduled = 1
            if session.is_session_full:
                break


def run():
    try:
        file_name = sys.argv[1]
        app = ConferenceManager(file_name)

        app.read_file_and_create_tasks()
        if len(task_list) > 0:
            conference = Conference()
            while any(task.is_scheduled == 0 for task in task_list):
                session_list = app.create_and_fill_sessions()
                create_track_and_fill_track(conference, session_list)
            print_sessions(conference)
        else:
            print('No tasks given to be scheduled')
    except IndexError:
        print('Please give the input file with command')
    except BaseException as e:
        print('some error occurred' + str(e))


if __name__ == '__main__':
    run()
