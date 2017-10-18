from nanoleaf import Aurora
import logging
import voluptuous as vol

# For instructions or bug reports, please visit
# https://github.com/software-2/ha-aurora

from homeassistant.components.light import (
    ATTR_BRIGHTNESS, SUPPORT_BRIGHTNESS, ATTR_COLOR_TEMP, SUPPORT_COLOR_TEMP, ATTR_RGB_COLOR, SUPPORT_RGB_COLOR, Light, PLATFORM_SCHEMA, ATTR_EFFECT, ATTR_EFFECT_LIST, SUPPORT_EFFECT )
from homeassistant.const import CONF_HOST, CONF_API_KEY, CONF_NAME
import homeassistant.helpers.config_validation as cv

REQUIREMENTS = ['nanoleaf==0.4.0']

SUPPORT_AURORA = ( SUPPORT_BRIGHTNESS | SUPPORT_COLOR_TEMP )


_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_API_KEY): cv.string,
    vol.Optional(CONF_NAME, default='Aurora'): cv.string,
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    host = config.get(CONF_HOST)
    apikey = config.get(CONF_API_KEY)
    name = config.get(CONF_NAME)

    my_aurora = Aurora(host, apikey)
    my_aurora.hass_name = name

    if my_aurora.on is None:
        _LOGGER.error("Could not connect to Nanoleaf Aurora: " + name)

    add_devices([AuroraLight(my_aurora)])


# TODO: https://github.com/home-assistant/home-assistant/pull/7596
# Remove ATTR_BRIGHTNESS and replace with ATTR_BRIGHTNESS_PCT
# And switch to kelvin
def brightness_scale_nanoleaf_to_hass(range_value):
    # Hass uses 0-255, Aurora uses 0-100
    if range_value is None:
        _LOGGER.error("Nanoleaf: brightness_scale_nanoleaf_to_hass() got 'None'...using default value 0")
        return 0
    return range_value * 2.55

def brightness_scale_hass_to_nanoleaf(range_value):
    if range_value is None:
        _LOGGER.error("Nanoleaf: brightness_scale_hass_to_nanoleaf() got 'None'...using default value 0")
        return 0
    return int(range_value / 2.55)

def color_temp_scale_nanoleaf_to_hass(range_value):
    # Hass uses 154-500, Aurora uses 1200-6500
    if range_value is None:
        _LOGGER.error("color_temp_scale_nanoleaf_to_hass() got 'None'...using default value 154")
        return 154
    return ((range_value - 1200) / 5300) * 346 + 154

def color_temp_scale_hass_to_nanoleaf(range_value):
    if range_value is None:
        _LOGGER.error("Nanoleaf: color_temp_scale_hass_to_nanoleaf() got 'None'...using default value 1200")
        return 1200
    return int(((range_value - 154) / 346) * 5300 + 1200)

class AuroraLight(Light):
    """Representation of a Nanoleaf Aurora inside Home Assistant."""

    def __init__(self, light):
        """Initialize an Aurora."""
        self._light = light
        self._name = light.hass_name
        self._state = light.on
        self._brightness = brightness_scale_nanoleaf_to_hass(light.brightness)
        self._effect = light.effect
        self._effects_list = light.effects_list
        self._color_temp = color_temp_scale_nanoleaf_to_hass(light.color_temperature)
        self._rgb_color = light.rgb

    @property
    def name(self):
        """Return the display name of this light."""
        return self._name

    @property
    def brightness(self):
        """Return the brightness of the light."""
        return self._brightness

    @property
    def effect_list(self):
        """Return the list of supported effects."""
        return self._effects_list

    @property
    def effect(self):
        """Return the current effect."""
        return self._effect

    @property
    def is_on(self):
        """Return true if light is on."""
        return self._state

    @property
    def color_temp(self):
        """Return the current color temperature"""
        return self._color_temp

    @property
    def rgb_color(self):
        """Return the color in RGB"""
        return self._rgb_color

    @property
    def supported_features(self):
        """Flag supported features."""
        return SUPPORT_AURORA

    def turn_on(self, **kwargs):
        """Instruct the light to turn on."""
        self._light.on = True

        if ATTR_BRIGHTNESS in kwargs:
            new_brightness = brightness_scale_hass_to_nanoleaf(kwargs.get(ATTR_BRIGHTNESS, 255))
            print("BRIGHTNESS: " + str(new_brightness))
            self._light.brightness = new_brightness

        if ATTR_EFFECT in kwargs:
            new_effect = kwargs[ATTR_EFFECT]
            print("EFFECT: " + str(new_effect))
            self._light.effect = new_effect

        if ATTR_COLOR_TEMP in kwargs:
            new_color_temp = color_temp_scale_hass_to_nanoleaf(kwargs.get(ATTR_COLOR_TEMP, 100))
            print("COLOR TEMP: " + str(new_color_temp))
            self._light.color_temperature = new_color_temp

        if ATTR_RGB_COLOR in kwargs:
            new_rgb_color = kwargs[ATTR_RGB_COLOR]
            print("COLOR RGB: " + str(new_rgb_color))
            self._light.rgb = new_rgb_color

    def turn_off(self, **kwargs):
        """Instruct the light to turn off."""
        self._light.on = False

    def update(self):
        """Fetch new state data for this light.

        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = self._light.on
        self._brightness = brightness_scale_nanoleaf_to_hass(self._light.brightness)
        self._effect = self._light.effect
        self._effects_list = self._light.effects_list
        self._color_temp = color_temp_scale_nanoleaf_to_hass(self._light.color_temperature)
        self._rgb_color = self._rgb_color


