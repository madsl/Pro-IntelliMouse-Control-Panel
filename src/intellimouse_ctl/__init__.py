"""
This module provides the implementation for the intellimouse-ctl CLI.
"""
from __future__ import annotations
import argparse
from collections import namedtuple
import json
import traceback
import sys

from intellimouse import IntelliMouse
from intellimouse import ProIntelliMouse
from intellimouse import ClassicIntelliMouse


def _connected_devices() -> list[IntelliMouse]:
    return ProIntelliMouse.enumerate() + ClassicIntelliMouse.enumerate()


def _list_devices(output_json: bool):
    DeviceInfo = namedtuple("DeviceInfo", ["name", "path"])
    devices = [
        DeviceInfo(type(device).__name__, device.path.decode("utf-8"))
        for device in _connected_devices()
    ]
    if output_json:
        print(json.dumps([device._asdict() for device in devices], indent=4))
    else:
        for index, device in enumerate(devices):
            print(f'{index}. {device.name} @ "{device.path}"')


_SETTINGS = ["dpi", "lift_off_distance", "color", "polling_rate"]


def _get_or_set_device_values(device: IntelliMouse, namespace: argparse.Namespace):
    changed_settings = {}
    for setting in [
        setting
        for setting in _SETTINGS
        if vars(namespace)[setting] is not None
        and hasattr(device, f"{namespace.command}_{setting}")
    ]:
        func = getattr(device, f"{namespace.command}_{setting}")
        if namespace.command == "get":
            value = func()
            changed_settings[setting] = value
        else:
            func(vars(namespace)[setting])

    if namespace.json:
        print(json.dumps(changed_settings, indent=4))
    else:
        for key, value in changed_settings.items():
            print(f"{_snake_2_friendly(key)}: {value}")


def _snake_2_kebab(string: str) -> str:
    return string.replace("_", "-")


def _snake_2_friendly(string: str) -> str:
    return string.replace("_", " ")


def main():
    """
    This function provides an entrypoint for the intellimouse-ctl CLI.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", help="output JSON", action="store_true")
    subparsers = parser.add_subparsers(dest="command")

    # verb
    get_subparsers = subparsers.add_parser("get", help="get the value of a setting")
    # required
    get_subparsers.add_argument(
        "index",
        help="index of the device to get values from",
        type=int,
        metavar="index",
    )
    # optional
    for setting in _SETTINGS:
        get_subparsers.add_argument(
            f"--{_snake_2_kebab(setting)}",
            help=f"gets the {_snake_2_friendly(setting)}",
            action="store_true",
            default=None,
        )

    # verb
    set_subparsers = subparsers.add_parser("set", help="set the value of a setting")
    # required
    set_subparsers.add_argument(
        "index",
        help="index of the device to get values from",
        type=int,
        metavar="index",
    )
    # optional
    for setting in _SETTINGS:
        set_subparsers.add_argument(
            f"--{_snake_2_kebab(setting)}",
            help=f"sets the {_snake_2_friendly(setting)}",
            type=int,
            default=None,
        )

    # verb
    subparsers.add_parser("list", help="lists the connected devices and their indices")

    namespace = parser.parse_args()
    # pylint: disable=broad-except
    try:
        if namespace.command == "list":
            _list_devices(namespace.json)
        elif namespace.command in ("get", "set"):
            with _connected_devices()[namespace.index] as device:
                _get_or_set_device_values(device, namespace)
        else:
            parser.print_help()
    except Exception as err:
        if namespace.json:
            print(
                json.dumps(
                    {
                        "error": type(err).__name__,
                        "message": str(err),
                        "traceback": traceback.format_exc(),
                    },
                    indent=4,
                )
            )
            sys.exit(1)
        else:
            raise
    # pylint: enable=broad-except
