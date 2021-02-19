# ezr2mqtt - a Möhlenhoff Alpha2 MQTT gateway

This utility is a simple Python-based Home Assistant addon/script to attach the
Möhlenhoff Alpha2 floor heating controller to HomeAssistant or other MQTT capable hosts.

## Installation

If you run Home Assistant OS (HassOS), you can run it as an addon. Simply create
a new folder "ezr2mqtt" in your local "addons" folder and copy the contents
of the repository there. Then, copy the file `ezr2mqtt.yaml` to the "config" directory
and adapt it to your needs. All Alpha 2 controllers to connect to are defined here,
see "Usage" below for details.

## Limitations

Currently, only the following settings/values are supported:

  * Current temperature (get)
  * Target temperature (get, set)
  * Auto/Off state (get) - powering on is not supported via the XML API
  * Auto/Day/Night mode (get, set)

## Usage

Configure your devices in the file ezr2mqtt.yaml - have a look at the provided ezr2mqtt.yaml
for the syntax. If you have MQTT autodiscovery enabled in your HomeAssistant platform,
then the devices will appear automagically. 

The `prefix` in the ezr settings needs to be unique, as this identifies the devices/entitites.

If you do not need MQTT authentication, leave the options 'username' and 'password' blank.

## Notes

Please be aware that it takes up to a few minutes until a change from Home Assistant
is visible in the Alpha 2 web interface and the room control units: The settings are
synced by the script during polling, the Alpha 2 transmits the values only every now
and then to the room control units.
