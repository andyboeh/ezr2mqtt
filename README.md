# ezr2mqtt - a Möhlenhoff Alpha2 MQTT gateway

This utility is a simple python script to attach the Möhlenhoff Alpha2 HVAC
to HomeAssistant or other MQTT capable hosts.

## Limitations

Currently, only the following settings/values are supported:

  * Current temperature (get)
  * Target temperature (get, set)
  * Auto/Off state (get) - powering on is not supported via the XML API
  * Auto/Day/Night mode (get, set)

## Usage

Configure your devices in the file config.yaml - have a look at the provided config.yaml
for the syntax. If you have MQTT autodiscovery enabled in your HomeAssistant platform,
then the devices will appear automagically. 

The `prefix` in the ezr settings needs to be unique, as this identifies the devices/entitites.

## Notes

Please be aware that it takes up to a few minutes until a change from Home Assistant
is visible in the Alpha 2 web interface and the room control units: The settings are
synced by the script during polling, the Alpha 2 transmits the values only every now
and then to the room control units.
