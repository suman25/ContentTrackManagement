from conference_config import NETWORKING_SESSION_MAXIMUM, NETWORKING_SESSION_MINIMUM


def create_track_and_fill_track(conference, session_list):
    conference.add_track()
    current_track = conference.get_current_track()
    for session in session_list:
        current_track.add_sessions(session)


def validate_network_start_time(networking_start_time):
    if networking_start_time.hour > NETWORKING_SESSION_MAXIMUM or \
            networking_start_time.hour < NETWORKING_SESSION_MINIMUM:
        raise Exception('Not enough sessions, please provide enough slots for the day')


def print_sessions(conference):
    for track in conference.tracks:
        print('Track' + str(track.track_id))
        for session in track.sessions:
            for slot in session.session_slots:
                print(slot.slot_time.strftime("%I:%M %p"), slot.slot_name, str(slot.slot_duration) + 'min')
