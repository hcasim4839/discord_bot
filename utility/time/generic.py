from datetime import datetime

def has_elapsed_time_passed(start_time:datetime.datetime,timeout_duration:int) -> bool:
    '''
    Checks if x amount of minutes have passed given a start datetime datatype and timeout_duration of int type

    Returns:
        bool: Whether the sufficient time has passed
    '''
    time_passed = datetime.now() - start_time
    has_elapsed_time_passed = time_passed >= datetime.timedelta(minutes=timeout_duration)

    return has_elapsed_time_passed