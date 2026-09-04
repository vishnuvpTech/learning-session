"""Shared helper for turning a Device row into Netmiko connection kwargs."""

from . import models


def netmiko_params(device: "models.Device") -> dict:
    return {
        "device_type": device.device_type,
        "host": device.ip,
        "username": device.username,
        "password": device.password,
        "timeout": 15,
        "banner_timeout": 15,
    }
