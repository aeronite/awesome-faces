import unittest
from app.main import common_face_finder


class TestFaceFinder(unittest.TestCase):

    def test_remove_used_faces(self):
        face_id_set = {'3', '5', '7', '8', '9'}
        ids_to_remove = ['5', '7']

        common_face_finder._remove_used_faces(face_id_set, ids_to_remove)
        self.assertEqual({'3', '8', '9'}, face_id_set)

    def test_other_ids(self):
        face_id_set = {'3', '5', '7', '8', '9'}

        other_ids = common_face_finder._other_face_ids('5', face_id_set)
        self.assertEqual(['3', '7', '8', '9'], other_ids)


if __name__ == '__main__':
    unittest.main()
