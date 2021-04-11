import sys
from task import Task
import re
from conference import Conference
from session import Session
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
                    res[0] = line[0:index-1]
                    res[1] = 'lightning'
                task = Task(res[0], res[1])
                task_list.append(task)
                task_list.sort(key=lambda task: task.task_minutes, reverse=True)

    def print_sessions(self, conference):
        for track in conference.tracks:
            print('Track'+ str(track.track_id))
            for session in track.sessions:
                for slot in session.session_slots:
                    print(slot.slot_time.strftime("%I:%M %p") , slot.slot_name , str(slot.slot_duration) + 'min')

    def run(self):
        self.read_file_and_create_tasks()
        if len(task_list) > 0:
            conference = Conference()
            while any(task.is_scheduled == 0 for task in task_list):
                morning_session = Session('Morning_Session', [9, 0, 0], 180)
                self.fill_session(morning_session)
                lunch_session = Session('Lunch Session', [12, 0, 0], 60)
                lunch_session.add_slot('Lunch', 60)
                noon_session = Session('Noon_Session', [13, 0, 0], 240)
                self.fill_session(noon_session)
                networking_session = Session('Networking Session',[noon_session.next_slot_time.hour , noon_session.next_slot_time.minute , noon_session.next_slot_time.second] , 60)
                networking_session.add_slot('Networking',60)
                conference.add_track()
                current_track = conference.get_current_track()
                current_track.add_sessions(morning_session)
                current_track.add_sessions(lunch_session)
                current_track.add_sessions(noon_session)
                current_track.add_sessions(networking_session)
            self.print_sessions(conference)


    def fill_session(self, session):
        for index,task_element in enumerate(task_list):
            if not(task_element.is_scheduled) and session.has_room(task_element.task_minutes):
                session.add_slot(task_element.task_name, task_element.task_minutes)
                task_element.is_scheduled = 1
            if session.is_session_full:
                break



if __name__ == '__main__':
    file_name = sys.argv[1]
    app = ConferenceManager(file_name)
    app.run()
