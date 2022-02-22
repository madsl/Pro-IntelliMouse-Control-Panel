"""
This module provides a class representing an Pro IntelliMouse device.

### Example Usage
```python
from intellimouse import ProIntelliMouse

with ProIntelliMouse.enumerate()[0] as mouse:
    mouse.get_dpi()
    mouse.set_dpi(1600)
```
"""
from .intellimouse import IntelliMouse


class ProIntelliMouse(IntelliMouse):
    """
    This class represents a Pro IntelliMouse device.
    """

    __DISTANCE_WRITE_PROPERTY = 0xB8
    __DISTANCE_READ_PROPERTY = __DISTANCE_WRITE_PROPERTY - 0x02
    __POLLING_WRITE_PROPERTY = 0x83
    __POLLING_READ_PROPERTY = __POLLING_WRITE_PROPERTY + 0x01
    __COLOR_WRITE_PROPERTY = 0xB2
    __COLOR_READ_PROPERTY = __COLOR_WRITE_PROPERTY + 0x01
    __DPI_WRITE_PROPERTY = 0x96
    __DPI_READ_PROPERTY = __DPI_WRITE_PROPERTY + 0x01

    __POLLING_MAPPING = {0x02: 125, 0x01: 500, 0x00: 1000}
    __POLLING_MAPPING_INVERSE = dict(
        zip(__POLLING_MAPPING.values(), __POLLING_MAPPING.keys())
    )

    __DISTANCE_MAPPING = {0x00: 2, 0x01: 3}
    __DISTANCE_MAPPING_INVERSE = dict(
        zip(__DISTANCE_MAPPING.values(), __DISTANCE_MAPPING.keys())
    )

    @classmethod
    def _get_write_report_id(cls) -> int:
        return 0x24

    @classmethod
    def _get_write_report_length(cls) -> int:
        return 0x49

    @classmethod
    def _get_read_report_id(cls) -> int:
        return 0x27

    @classmethod
    def _get_read_report_length(cls) -> int:
        return 0x29

    @classmethod
    def _get_pid(cls) -> int:
        return 0x082A

    @classmethod
    def _get_interface(cls) -> int:
        return 0x01

    @classmethod
    def _get_usage_page(cls) -> int:
        return 0xFF07

    @classmethod
    def _get_usage(cls) -> int:
        return 0x212

    def __str__(self):
        return (
            "Microsoft Pro IntelliMouse \n"
            + "* color: {}\n"
            + "* dots per inch: {}\n"
            + "* polling rate: {}\n"
            + "* lift off distance: {}"
        ).format(
            hex(self.get_color()).upper(),
            self.get_dpi(),
            self.get_polling_rate(),
            self.get_lift_off_distance(),
        )

    def get_color(self) -> int:
        """Returns the color of the tail-light."""
        return int.from_bytes(
            super()._read_property(self.__COLOR_READ_PROPERTY), byteorder="big"
        )

    def set_color(self, color: int):
        """
        Sets the color of the tail-light.
        ### Parameters:
        * `color: int`:
            * an `int` representing the color of the tail-light.
        """
        color = 0xFFFFFF & color
        super()._write_property(
            self.__COLOR_WRITE_PROPERTY, list(color.to_bytes(3, byteorder="big"))
        )

    def get_dpi(self) -> int:
        """Returns the dpi."""
        return int.from_bytes(
            super()._read_property(self.__DPI_READ_PROPERTY), byteorder="little"
        )

    def set_dpi(self, dpi: int):
        """
        Sets the dpi.
        ### Parameters:
        * `dpi: int`:
            * an `int` representing the dpi.
        """
        if dpi % 50 != 0 or not 200 <= dpi <= 16000:
            raise ValueError(
                "please make sure to pass a valid value (dpi % 50 == 0 and (200 <= dpi <= 16000))"
            )
        super()._write_property(
            self.__DPI_WRITE_PROPERTY, list(dpi.to_bytes(2, byteorder="little"))
        )

    def get_polling_rate(self) -> int:
        """Returns the polling rate."""
        return self.__POLLING_MAPPING[
            super()._read_property(self.__POLLING_READ_PROPERTY)[0]
        ]

    def set_polling_rate(self, rate: int):
        """
        Sets the polling rate.
        ### Parameters:
        * `rate: int`:
            * an `int` representing the polling rate in MHz.
        """
        if rate not in (125, 500, 1000):
            raise ValueError(
                "please make sure to pass a valid value (rate == 125 or rate == 500 or rate == 1000)"
            )
        super()._write_property(
            self.__POLLING_WRITE_PROPERTY, [self.__POLLING_MAPPING_INVERSE[rate]]
        )

    def get_lift_off_distance(self) -> int:
        """Returns the lift off distance."""
        return self.__DISTANCE_MAPPING[
            super()._read_property(self.__DISTANCE_READ_PROPERTY)[0]
        ]

    def set_lift_off_distance(self, distance: int):
        """
        Sets the lift off distance (in mm).

        ### Parameters:
        * `distance: int`:
            * an `int` representing the lift off distance in mm.
        """
        if distance not in (2, 3):
            raise ValueError(
                "please make sure to pass a valid lift off distance (distance == 2 or distance == 3)"
            )
        super()._write_property(
            self.__DISTANCE_WRITE_PROPERTY, [self.__DISTANCE_MAPPING_INVERSE[distance]]
        )
