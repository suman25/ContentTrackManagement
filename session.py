import datetime
from slot import Slot


class Session(object):

    def __init__(self, session_name, session_start_time, session_duration):
        self.session_name = session_name
        self.session_start_time = datetime.time(session_start_time[0], session_start_time[1], session_start_time[2])
        self.next_slot_time = datetime.time(session_start_time[0], session_start_time[1], session_start_time[2])
        self.session_duration = session_duration
        self.session_filled = 0
        self.is_session_full = 0
        self.session_slots = []

    def has_room(self, slot_duration):
        if self.session_filled + slot_duration <self.session_duration:
            return True
        elif self.session_filled + slot_duration == self.session_duration:
            self.is_session_full = 1
            return True
        else:
            return False

    def add_slot(self,slot_name,slot_duration):
        self.session_slots.append(Slot(self.next_slot_time, slot_name, slot_duration))
        self.next_slot_time = datetime.datetime.combine(datetime.date(1,1,1),self.next_slot_time) + datetime.timedelta(minutes= slot_duration)
        self.session_filled = self.session_filled + slot_duration
        self.next_slot_time = self.next_slot_time.time()
