from track import Track

class Conference(object):
    def __init__(self):
        self.tracks = []

    def get_current_track(self):
        return self.tracks[-1]

    def add_track(self):
        track_id = len(self.tracks)+1
        self.tracks.append(Track(track_id))





