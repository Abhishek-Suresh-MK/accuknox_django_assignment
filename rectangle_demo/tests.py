from django.test import SimpleTestCase

from .rectangle import Rectangle


class RectangleTests(SimpleTestCase):
    def test_iteration_returns_length_then_width(self):
        rectangle = Rectangle(10, 5)

        self.assertEqual(
            list(rectangle),
            [{"length": 10}, {"width": 5}],
        )

    def test_can_iterate_with_for_loop(self):
        rectangle = Rectangle(3, 2)
        result = []
        for item in rectangle:
            result.append(item)

        self.assertEqual(result, [{"length": 3}, {"width": 2}])
