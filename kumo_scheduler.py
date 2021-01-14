import time
import schedule
import sys
from kumo import kumo_config_main

show_start = '12:07'
show_end = '12:08'


def get_time():
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    return current_time


def start_show():
    print('\nSTARTING SHOW')
    kumo_config_main(address='168.16.203.243', source=7, destination=12)


def end_show():
    kumo_config_main(address='168.16.203.243', source=14, destination=12)
    sys.exit('Show complete. Exiting program.')


schedule.every().day.at(show_start).do(start_show)
schedule.every().day.at(show_end).do(end_show)

if __name__ == '__main__':
    print('Show begins at:', show_start)
    while True:
        schedule.run_pending()
        time.sleep(1)
        print('Current time:', get_time())
