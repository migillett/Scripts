# AJA-Kumo-Automation

## Introduction
This code allows you to alter inputs and outputs on an AJA KUMO video router. You can either run it from a terminal (see below) or schedule tasks to happen at a specific time.
This repository is forked off of the work from [szumlins/Scripts](https://github.com/szumlins/Scripts).

## From the Command Line
To run the script from the command line, all you have to do is navigate to the folder where the `kumo.py` file exists. Then use this command:
`python3 ./kumo.py -a [your router address here] -s [source] -d [destination]`

`-a` refers to your video routers IP address. For instance; `192.168.1.2`. If the script cannot find 

`-s` refers to the video source you wish to pull from. If you select an input outside the range of the router, you'll get an error. This flag is optional.

`-d` refers to the video destination you want to map the input to. Same as above, if you select a destination outside the range, you'll get an error.

### Examples
`python3 ./kumo.py -a 192.168.1.2 -d 15` - will return what input is currently mapped to destination 15.

`python3 ./kumo.py -a 192.168.1.2 -s 5 -d 15` - will remap source 5 to destination 15.

## Using the Automation Script
This program also features another script that allows you to schedule tasks. For example, if you wanted to have an input start at 12:00  and switch back to default at 12:30.
What you have to do is instead of running the `kumo.py` script, run the `kumo_automation.py` script. All you'll have to do is edit a few lines of code that I've marked. It pulls from the `kumo.py` script, so make sure they're in the same directory.
