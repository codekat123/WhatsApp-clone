import time

MESSAGE_LIMIT = 5
TIME_WINDOW = 3


def allowed_to_send(msg_timestamps):
    now = time.time()
    msg_timestamps = [t for t in msg_timestamps if now - t < TIME_WINDOW]

    if len(msg_timestamps) >= MESSAGE_LIMIT:
        return False, msg_timestamps

    msg_timestamps.append(now)
    return True, msg_timestamps
