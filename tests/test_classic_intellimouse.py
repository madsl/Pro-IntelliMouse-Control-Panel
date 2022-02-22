import unittest
from intellimouse import ClassicIntelliMouse


class TestClassicIntelliMouse(unittest.TestCase):
    def test_enumarate(self):
        self.assertTrue(ClassicIntelliMouse.enumerate())

    def test_dpi(self):
        value = 600
        with ClassicIntelliMouse.enumerate()[0] as mouse:
            mouse.set_dpi(value)
            self.assertEqual(mouse.get_dpi(), value)


if __name__ == "__main__":
    unittest.main()
