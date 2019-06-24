import unittest
from app.main import face_service


class TestFaceInImage(unittest.TestCase):

    def test_percent_of_image(self):
        face_meta = {"faceRectangle": {"width": 5, "height": 2}}

        face = face_service.FaceInImage(face_meta, 40, "hello")
        self.assertEqual(0.25, face.percent_of_image)


if __name__ == '__main__':
    unittest.main()