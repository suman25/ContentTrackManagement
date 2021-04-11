
class Track(object):
    def __init__(self, track_id):
        self.track_id = track_id
        self.sessions = []

    def add_sessions(self, session):
        self.sessions.append(session)

