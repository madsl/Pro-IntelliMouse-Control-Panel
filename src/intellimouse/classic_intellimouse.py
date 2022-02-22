"""
This module provides a class representing an Classic IntelliMouse device.

### Example Usage
```python
from intellimouse import ClassicIntelliMouse

with ClassicIntelliMouse.enumerate()[0] as mouse:
    mouse.get_dpi()
    mouse.set_dpi(1600)
```
"""
from .intellimouse import IntelliMouse


class ClassicIntelliMouse(IntelliMouse):
    """
    This class represents a Classic IntelliMouse device.
    """

    __DPI_WRITE_PROPERTY = 0x96
    __DPI_READ_PROPERTY = __DPI_WRITE_PROPERTY + 0x01

    @classmethod
    def _get_interface(cls) -> int:
        return 0x01

    @classmethod
    def _get_usage_page(cls) -> int:
        return 0x0C

    @classmethod
    def _get_usage(cls) -> int:
        return 0x01

    def __str__(self):
        return ("Microsoft Classic IntelliMouse \n" + "* dots per inch: {}").format(
            self.get_dpi()
        )

    def get_dpi(self) -> int:
        """Returns the dpi."""
        return int.from_bytes(
            super()._read_property(self.__DPI_READ_PROPERTY)[1:], byteorder="little"
        )

    def set_dpi(self, dpi: int):
        """
        Sets the dpi.
        ### Parameters:
        * `dpi: int`:
            * an `int` representing the dpi.
        """
        if dpi % 200 != 0 or not 400 <= dpi <= 3200:
            raise ValueError(
                "please make sure to pass a valid value (dpi % 200 == 0 and (400 <= dpi <= 3200))"
            )
        super()._write_property(
            self.__DPI_WRITE_PROPERTY,
            [0x00] + list(dpi.to_bytes(2, byteorder="little")),
        )

    @classmethod
    def _get_write_report_id(cls) -> int:
        return 0x24

    @classmethod
    def _get_write_report_length(cls) -> int:
        return 0x20

    @classmethod
    def _get_read_report_id(cls) -> int:
        return 0x27

    @classmethod
    def _get_read_report_length(cls) -> int:
        return 0x20

    @classmethod
    def _get_pid(cls) -> int:
        return 0x0823
