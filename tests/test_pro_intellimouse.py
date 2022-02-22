import unittest
from intellimouse import ProIntelliMouse


class TestProIntelliMouse(unittest.TestCase):
    def test_enumarate(self):
        self.assertTrue(ProIntelliMouse.enumerate())

    def test_dpi(self):
        dpi = 1600
        with ProIntelliMouse.enumerate()[0] as mouse:
            mouse.set_dpi(dpi)
            self.assertEqual(mouse.get_dpi(), dpi)

    def test_color(self):
        color = 0xFF00FF
        with ProIntelliMouse.enumerate()[0] as mouse:
            mouse.set_color(color)
            self.assertEqual(mouse.get_color(), color)

    def test_polling_rate(self):
        polling_rate = 500
        with ProIntelliMouse.enumerate()[0] as mouse:
            mouse.set_polling_rate(polling_rate)
            self.assertEqual(mouse.get_polling_rate(), polling_rate)

    def test_lift_off_distance(self):
        lift_off_distance = 3
        with ProIntelliMouse.enumerate()[0] as mouse:
            mouse.set_lift_off_distance(lift_off_distance)
            self.assertEqual(mouse.get_lift_off_distance(), lift_off_distance)


if __name__ == "__main__":
    unittest.main()
