from time import sleep
import schedule
from kumo import kumo_config_main

# Change the show start and end times here. Use military time, so 1:00 pm = 13:00
city_hall_in = '18:29:50'
gc360_start = '15:59:50'
gc360_end = '16:30:00'

# IP Address for the AJA KUMO Video Router
kumo_addr = '192.168.1.2'

# SOURCES
tricaster = 7
scala = 13
city_hall = 14
terrell = 15
centennial = 16

# DESTINATIONS
terrell_return = 1
monitor_rack = 8
bmd_record = 11
master_out = 16

intervals = (
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),    # 60 * 60 * 24
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
    )


def display_time(seconds, granularity=4):
    result = []
    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])


def switch_to_city_hall():
    kumo_config_main(address=kumo_addr, source=city_hall, destination=monitor_rack)
    kumo_config_main(address=kumo_addr, source=city_hall, destination=master_out)
    print('\nbSwitching to City Hall Feed.')


def switch_to_gc360():
    kumo_config_main(address=kumo_addr, source=terrell, destination=master_out)
    kumo_config_main(address=kumo_addr, source=terrell, destination=monitor_rack)
    kumo_config_main(address=kumo_addr, source=terrell, destination=terrell_return)
    print('\nSTARTING GC360')


def default():
    kumo_config_main(address=kumo_addr, source=scala, destination=monitor_rack)
    kumo_config_main(address=kumo_addr, source=scala, destination=master_out)
    kumo_config_main(address=kumo_addr, source=scala, destination=terrell_return)
    print('\nRouter returned to default.')


# Examples of switching commands:
# schedule.every().tuesday.at(city_hall_in).do(switch_to_city_hall)
schedule.every().thursday.at(gc360_start).do(switch_to_gc360)
schedule.every().thursday.at(gc360_end).do(default)

if __name__ == '__main__':
    print('=======================\n  Program initialized.\n=======================\n')
    while True:
        try:
            t = schedule.idle_seconds()
            print('Time until next switch command:', display_time(t))
        except TypeError:
            print('\nNo switch scheduled. Exiting.')
            break
        schedule.run_pending()
        sleep(1)
