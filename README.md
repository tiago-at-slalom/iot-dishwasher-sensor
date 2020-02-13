
# Dishwasher Buddy

## What is it?
It is an IoT application that will notify you in MS Teams whenever your dishwasher programme ends.

## Installing instructions

### **Hardware**

**Required hardware:**
- Dishwasher (or any other electric appliance you want to track)
- Raspberry Pi Zero or similar
- AC Current Signal Conversion Module
- Open Type AC Transformer Probe
(also to interact with the Raspberry Pi you will need a monitor and a keyboard)

![alt text](/images/ac_current_sensor_20a.jpg "AC Current Signal Conversion Module and Probe")

**Connections:**

The below diagram shows how to connect the different hardware parts of our experiment
1. the probe will clamp onlu one of the AC wires
2. the probe jack is connected to the converison module
3. there are 3 connections between the conversion module and the Raspberry Pi
    - The + cable going into one of the 3V3 or 5V pins
    - The - cable going into one of the GND (ground) pins
    - The A cable going into the numbered GPIO pin configured in our application (14 by default)

(please take in consideration that instead of an Arduino we are using a Raspberry Pi)
![alt text](/images/connection_diagram.png "Connections diagram")

### **Software**

Raspberry Pi requirements:
- Have the operating system setup
- Have internet connection
- Have Python installed

Instalation steps:
1. navigate to the folder where you want to install the application. We will reference this location as [app_path]
2. clone this repository
3. Install the required Python packages
    - pip3 install pymsteams
    - pip3 install gpiozero
    - pip3 install RPi.GPIO
    - pip3 install pytest
    - pip3 install pytest-watch

## Configuration

App configuration is done in the "config.py" file. To get start we can copy the config.py.template file renaming it accordingly. Then we will need to edit variables inside the file to reflect the webhook for the Teams notification, the interval of time you want to app to check for activity in the machine and the Raspberry Pi GPIO pin to wich you connected the sensor.

## Run

For a one time run of the application, run the following command:

``` sudo python3 main.py ```

For the real life operation you will want to setup a cron job to run the application regularly. To do so follow these steps:
1. run ``` crontab -e ```
2. select and editor from the list (if you don't know what to pick, nano will work)
3. Navigate to the bottom of the file and add this text to a new line

``` * 8-19 * * 1-5 sudo python3 [app_path]/main.py ```

(this will setup a task that will run our app every minute between 8am and 7pm only on week days)

Reference: https://www.raspberrypi.org/documentation/linux/usage/cron.md

## Test

**Run tests:**

$ pytest

**To watch tests:**

$ ptw