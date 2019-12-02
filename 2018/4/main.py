import sys
from typing import NamedTuple
from datetime import datetime, timedelta
from collections import defaultdict


class Interval(NamedTuple):
    start: datetime
    end: datetime

    def size(self):
        return (self.end - self.start).seconds // 60

    def minutes_asleep(self):
        i = self.start
        result = []
        while i != self.end:
            result.append(i.minute)
            i += timedelta(minutes=1)
        return result


def get_datetime_from_line(line):
    return datetime.strptime(
        line[1:].split(']')[0],
        '%Y-%m-%d %H:%M',
    )

def get_guard_id_from_line(line):
    assert '#' in line
    return int(line.split('#')[1].split(' ')[0])

def parse_sleep_times(lines):
    sleep_times = defaultdict(list)
    current_guard = None
    sleep_start = None
    for line in lines:
        if '#' in line:
            current_guard = get_guard_id_from_line(line)

        if 'falls asleep' in line:
            assert current_guard is not None
            sleep_start = get_datetime_from_line(line)

        if 'wakes up' in line:
            assert current_guard is not None
            sleep_times[current_guard].append(Interval(
                start=sleep_start,
                end=get_datetime_from_line(line),
            ))
    return sleep_times


def get_guard_with_most_sleep(sleep_times):
    return max((sum(time.size() for time in times), id) for id, times in sleep_times.items())[1]


def get_most_slept_minutes(sleep_times, guard_id):
    slept_on_minute = defaultdict(int)
    for interval in sleep_times[guard_id]:
        for minute in interval.minutes_asleep():
            slept_on_minute[minute] += 1
    return max((v, k) for k, v in slept_on_minute.items())[1]

def get_guard_with_most_frequently_asleep(sleep_times):
    slept_on_minute = defaultdict(lambda: defaultdict(int))
    for guard_id, intervals in sleep_times.items():
        for interval in intervals:
            for minute in interval.minutes_asleep():
                slept_on_minute[guard_id][minute] += 1

    guard_to_time_slept = {guard_id: max((time, minute) for minute, time in sleep_minutes.items()) for guard_id, sleep_minutes in slept_on_minute.items()}
    return max((time, guard_id, minute) for guard_id, (time, minute) in guard_to_time_slept.items())[1:]

    

def get_all_sorted_input():
    lines = [line.strip() for line in sys.stdin]
    return sorted(lines, key=get_datetime_from_line)

def main():
    sleep_times = parse_sleep_times(get_all_sorted_input())
    guard_with_most_sleep = get_guard_with_most_sleep(sleep_times)
    most_slept = get_most_slept_minutes(sleep_times, guard_with_most_sleep)
    print(guard_with_most_sleep * most_slept)
    guard_id, minute = get_guard_with_most_frequently_asleep(sleep_times)
    print(guard_id * minute)


if __name__ == '__main__':
    main()
