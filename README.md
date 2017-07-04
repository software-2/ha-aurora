# ha-aurora
Nanoleaf Aurora component for Home Assistant

### Alpha Release ###

Please be aware that this component is still in development. It would be of immense help to me if you could provice feedback, submit bugs, etc. If you work for Nanoleaf, you should send me some more lights to develop with.

During this time, interfaces and features are subject to change without concern for backwards compatibility. (Meaning I might break your scripts.)

### Prerequisites ###

I believe Home Assistant should automatically grab the Nanoleaf library. Please let me know if it doesn't. If you do need to manually get it, instructions are on [the GitHub Project](https://github.com/software-2/nanoleaf).

If you don't have an API token, you'll need to generate one using the above library's setup tools.

## Install ##

Copy `aurora.py` into `.homeassistant\custom_components\light`

## Setup ##

Add the following to your `configuration.yaml` file. If you have multiple auroras, add one for each light controller.

```yaml
light:
  - platform: aurora
    host: 192.168.1.113
    api_key: 5GPFfAketAKeYq7hC6IsFaKeGTJ6YlUaI7d
    name: myAurora
```

I strongly suggest assigning a static IP to your Auroras. Improvements to the Nanoleaf library are planned to find devices with changing IPs, but for now make sure you use a static IP.

### Supported Features ###

* Effects saved to the device
* Color
* Brightness
* Color Temperature

### Planned Improvements ###

* Extra effects built into the library that don't need to be saved to the device's limited storage
* Better device discovery (No IP needed)

