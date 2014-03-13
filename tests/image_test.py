import base64
import cardoon
import math
import operator
import os
import tempfile
import unittest
from PIL import Image
from StringIO import StringIO

def compareImages(im1, im2):
    h1 = im1.histogram()
    h2 = im2.histogram()

    return math.sqrt(reduce(operator.add,
        map(lambda a,b: (a-b)**2, h1, h2))/len(h1))

class TestImage(unittest.TestCase):

    def setUp(self):
        self.image = 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAAK/INwWK6QAAABl0RVh0U29mdHdhcmUAQWRvYmUgSW1hZ2VSZWFkeXHJZTwAAAKfSURBVDjLpZPrS1NhHMf9O3bOdmwDCWREIYKEUHsVJBI7mg3FvCxL09290jZj2EyLMnJexkgpLbPUanNOberU5taUMnHZUULMvelCtWF0sW/n7MVMEiN64AsPD8/n83uucQDi/id/DBT4Dolypw/qsz0pTMbj/WHpiDgsdSUyUmeiPt2+V7SrIM+bSss8ySGdR4abQQv6lrui6VxsRonrGCS9VEjSQ9E7CtiqdOZ4UuTqnBHO1X7YXl6Daa4yGq7vWO1D40wVDtj4kWQbn94myPGkCDPdSesczE2sCZShwl8CzcwZ6NiUs6n2nYX99T1cnKqA2EKui6+TwphA5k4yqMayopU5mANV3lNQTBdCMVUA9VQh3GuDMHiVcLCS3J4jSLhCGmKCjBEx0xlshjXYhApfMZRP5CyYD+UkG08+xt+4wLVQZA1tzxthm2tEfD3JxARH7QkbD1ZuozaggdZbxK5kAIsf5qGaKMTY2lAU/rH5HW3PLsEwUYy+YCcERmIjJpDcpzb6l7th9KtQ69fi09ePUej9l7cx2DJbD7UrG3r3afQHOyCo+V3QQzE35pvQvnAZukk5zL5qRL59jsKbPzdheXoBZc4saFhBS6AO7V4zqCpiawuptwQG+UAa7Ct3UT0hh9p9EnXT5Vh6t4C22QaUDh6HwnECOmcO7K+6kW49DKqS2DrEZCtfuI+9GrNHg4fMHVSO5kE7nAPVkAxKBxcOzsajpS4Yh4ohUPPWKTUh3PaQEptIOr6BiJjcZXCwktaAGfrRIpwblqOV3YKdhfXOIvBLeREWpnd8ynsaSJoyESFphwTtfjN6X1jRO2+FxWtCWksqBApeiFIR9K6fiTpPiigDoadqCEag5YUFKl6Yrciw0VOlhOivv/Ff8wtn0KzlebrUYwAAAABJRU5ErkJggg=='

        self.analysis = {
            "name": "Image pixels",
            "inputs": [
                {
                    "name": "a",
                    "type": "image",
                    "format": "pil"
                }
            ],
            "outputs": [
                {
                    "name": "pixels",
                    "type": "number",
                    "format": "number"
                }
            ],
            "script": "pixels = a.size[0] * a.size[1]\n",
            "mode": "python"
        }

    def test_base64(self):
        outputs = cardoon.run(self.analysis,
            inputs={
                "a": {"format": "png.base64", "data": self.image},
            })
        self.assertEqual(outputs["pixels"]["format"], "number")
        self.assertEqual(outputs["pixels"]["data"], 256)

    def test_convert(self):
        tmp = tempfile.mktemp();

        output = cardoon.convert("image",
            {"format": "png.base64", "data": self.image},
            {"format": "png", "uri": "file://" + tmp})

        value = open(tmp).read()
        os.remove(tmp)
        self.assertEqual(output["format"], "png")
        self.assertEqual(base64.b64encode(value), self.image)

        output = cardoon.convert("image",
            {"format": "png.base64", "data": self.image},
            {"format": "pil"})

        tmp = tempfile.mktemp();

        output = cardoon.convert("image",
            output,
            {"format": "png"})

        io1 = StringIO(base64.b64decode(self.image))
        im1 = Image.open(io1)
        io2 = StringIO(output["data"])
        im2 = Image.open(io2)
        self.assertEqual(compareImages(im1, im2), 0)


if __name__ == '__main__':
    unittest.main()
