import time
import schedule
import sys
from kumo import kumo_config_main

# Change the show start and end times here. Use military time, so 1:00 pm = 13:00
show_start = '12:00'
show_end = '12:30'

# Put the IP address of your KUMO router here
kumo_addr = '192.168.1.2'


def start_show():
    print('\nSTARTING SHOW')
    
    # Edit the sources and destinations as you see fit here. This is the start of the show.
    # Add as many lines as you like if you have multiple switches at the same time.
    kumo_config_main(address=kumo_addr, source=7, destination=12)


def end_show():
    # Edit the sources and destinations here. This is at the end of the show.
    # Add as many lines as you like if you have multiple switches at the same time.
    kumo_config_main(address=kumo_addr, source=14, destination=12)
    
    sys.exit('Show complete. Exiting program.')


schedule.every().day.at(show_start).do(start_show)
schedule.every().day.at(show_end).do(end_show)

if __name__ == '__main__':
    print('Show begins at:', show_start)
    while True:
        schedule.run_pending()
        time.sleep(1)
