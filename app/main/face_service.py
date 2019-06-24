import cognitive_face
from io import BytesIO
from PIL import Image
import requests


def find_faces_of_same_person(target_face_id, other_face_ids, min_confidence):
    """
    Calls the Azure Face API to find similar faces to a given target face and then filters them by a minimum confidence
    """

    similar_faces = cognitive_face.face.find_similars(face_id=target_face_id, face_ids=other_face_ids)

    filtered_faces = [face['faceId'] for face in similar_faces if face['confidence'] > min_confidence]

    # the target face itself is also part of the similar face set
    filtered_faces.append(target_face_id)

    return filtered_faces


def detect_faces(img_uri):
    """
    Calls the Azure Face API for a given url and enriches the returned face data with stats regarding the image itself
    """

    faces = cognitive_face.face.detect(img_uri, attributes='age,gender,emotion')

    if len(faces) == 0:
        return []

    img_area = _find_image_area(img_uri)

    return [FaceInImage(face, img_area, img_uri) for face in faces]


def _find_image_area(img_uri):
    """
    Downloads an image from a given url and determines its area in pixels
    """

    req = requests.get(img_uri)
    im = Image.open(BytesIO(req.content))
    width, height = im.size

    return width * height


class FaceInImage:
    """
    Each image could have several faces in it. This object enriches the face meta with the uri of its image of origin.
    It also calculates what percentage of the image is taken up by the given face.
    """

    def __init__(self, _face_metadata, _image_area, _image_uri):
        self.face_metadata = _face_metadata
        self.image_uri = _image_uri

        face_rect = _face_metadata['faceRectangle']
        face_area = face_rect['width'] * face_rect['height']
        self.percent_of_image = face_area / _image_area

    def face_id(self):
        return self.face_metadata['faceId']

    def prepare_meta(self, num_common_faces_found):
        prepared_meta = self.face_metadata
        prepared_meta['image_uri'] = self.image_uri
        prepared_meta['num_common_faces_found'] = num_common_faces_found

        return prepared_meta

