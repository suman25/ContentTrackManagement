import sys

from conference_config import *
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
                    if any(chr.isdigit() for chr in line):
                        res = re.split('(\d+)', line)
                    else:
                        index = line.find('lightning')
                        res[0] = line[0:index - 1]
                        res[1] = 'lightning'
                    task = Task(res[0], res[1])
                    task_list.append(task)
                    task_list.sort(key=lambda task: task.task_minutes, reverse=True)

    def print_sessions(self, conference):
        for track in conference.tracks:
            print('Track' + str(track.track_id))
            for session in track.sessions:
                for slot in session.session_slots:
                    print(slot.slot_time.strftime("%I:%M %p"), slot.slot_name, str(slot.slot_duration) + 'min')

    def run(self):
        session_list = []
        self.read_file_and_create_tasks()
        if len(task_list) > 0:
            conference = Conference()
            while any(task.is_scheduled == 0 for task in task_list):
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
                networking_session = Session(SessionType.Networking,
                                             [networking_start_time.hour, networking_start_time.minute,
                                              networking_start_time.second], NETWORKING_SESSION_DURATION)
                networking_session.add_slot('Networking', NETWORKING_SLOT_DURATION)
                session_list.append(networking_session)
                self.create_track_and_fill_track(conference, session_list)
            self.print_sessions(conference)

    def create_track_and_fill_track(self, conference, session_list):
        conference.add_track()
        current_track = conference.get_current_track()
        for session in session_list:
            current_track.add_sessions(session)

    def fill_session(self, session):
        for index, task_element in enumerate(task_list):
            if not (task_element.is_scheduled) and session.has_room(task_element.task_minutes):
                session.add_slot(task_element.task_name, task_element.task_minutes)
                task_element.is_scheduled = 1
            if session.is_session_full:
                break


if __name__ == '__main__':
    file_name = sys.argv[1]
    app = ConferenceManager(file_name)
    app.run()
