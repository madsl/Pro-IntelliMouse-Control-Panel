"""
This module provides an abstract base class representing an abstract IntelliMouse device.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
import time

import hid


class IntelliMouse(ABC):
    """
    This class is an abstract base class for IntelliMouse devices from which concrete implementations such as;
    * `intellimouse.pro_intellimouse.ProIntelliMouse`
    * `intellimouse.classic_intellimouse.ClassicIntelliMouse`

    inherit.
    """

    def __init__(self, path: str):
        self._device = hid.device()
        self._path = path

    def open(self):
        """Opens the device."""
        self._device.open_path(self._path)

    def close(self):
        """Closes the device."""
        self._device.close()

    def __enter__(self):
        self._device.open_path(self._path)
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        self._device.close()

    def __del__(self):
        self.close()

    @property
    def path(self):
        """Returns the path to this device."""
        return self._path

    @classmethod
    @abstractmethod
    def _get_write_report_id(cls) -> int:
        pass

    @classmethod
    @abstractmethod
    def _get_write_report_length(cls) -> int:
        pass

    @classmethod
    @abstractmethod
    def _get_read_report_id(cls) -> int:
        pass

    @classmethod
    @abstractmethod
    def _get_read_report_length(cls) -> int:
        pass

    @classmethod
    @abstractmethod
    def _get_pid(cls) -> int:
        pass

    @classmethod
    def _get_vid(cls) -> int:
        return 0x045E

    @classmethod
    @abstractmethod
    def _get_interface(cls) -> int:
        pass

    @classmethod
    @abstractmethod
    def _get_usage_page(cls) -> int:
        pass

    @classmethod
    @abstractmethod
    def _get_usage(cls) -> int:
        pass

    @abstractmethod
    def __str__(self):
        pass

    @classmethod
    def enumerate(cls):
        """
        This class method is to be called on an concrete subclass of `IntelliMouse`.
        It enumerates all the found IntelliMouse devices.
        ### Example Usage:
        ```python
            from intellimouse import ClassicIntelliMouse
            from intellimouse import ProIntelliMouse

            ClassicIntelliMouse.enumerate()
            ProIntelliMouse.enumerate()
        ```

        ### Returns:
        * `devices: list[IntelliMouse]`:
            * a `list` of all the found concrete IntelliMouse devices.
        """
        devices = [
            device
            for device in hid.enumerate()
            if device["interface_number"] == cls._get_interface()
            and device["product_id"] == cls._get_pid()
            and device["vendor_id"] == cls._get_vid()
        ]
        if not all(
            device["usage_page"] == 0 and device["usage"] == 0 for device in devices
        ):
            devices = [
                device
                for device in devices
                if device["usage_page"] == cls._get_usage_page()
                and device["usage"] == cls._get_usage()
            ]

        return [cls(device["path"]) for device in devices]

    def _write_property(self, write_property: int, data: list[int]):
        report = IntelliMouse.__pad_right(
            [self._get_write_report_id(), write_property, len(data)] + data,
            self._get_write_report_length(),
        )
        bytes_written: int = self._device.send_feature_report(report)
        IntelliMouse.__sleep()
        if bytes_written != self._get_write_report_length():
            raise IOError(
                "couldn't properly write to device, it may be disconnected, or this program may be lacking permissions."
            )

    def _read_property(self, read_property: int):
        report = IntelliMouse.__pad_right(
            [self._get_write_report_id(), read_property, 0x01],
            self._get_write_report_length(),
        )
        self._device.send_feature_report(report)
        IntelliMouse.__sleep()
        result: list[int] = self._device.get_input_report(
            self._get_read_report_id(), self._get_read_report_length()
        )
        IntelliMouse.__sleep()
        return result[4 : 4 + result[3]]

    @staticmethod
    def __sleep():
        # sleep ~50 ms, the classic intellimouse seems to need extra time to process commands.
        time.sleep(0.05)

    @staticmethod
    def __pad_right(data: list[int], until: int) -> list[int]:
        return data + ((until - len(data)) * [0x00])
