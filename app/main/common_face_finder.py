from . import face_service


def find_most_common(face_urls, confidence):
    """
    Detects face metadata from a list of images and then attempts to find the most common face
    """

    faces_by_image = [face_service.detect_faces(face) for face in face_urls]

    # flatten face lists for each image into one larger list
    faces = [face for faces_for_single_image in faces_by_image for face in faces_for_single_image]

    # map these into a dict of faces keyed by their face_ids
    faces_by_id = {faces[i].face_id: faces[i] for i in range(0, len(faces))}

    most_face_ids_of_same_person = []

    for face in faces:
        other_face_ids = _other_face_ids(face.face_id(), faces_by_id)
        face_ids_of_same_person = _find_faces_of_same_person(face.face_id(), other_face_ids, confidence)
        if len(face_ids_of_same_person) > len(most_face_ids_of_same_person):
            most_face_ids_of_same_person = face_ids_of_same_person

    return _find_best_common_face(most_face_ids_of_same_person, faces_by_id)


def _find_faces_of_same_person(face_id, other_face_ids, confidence):
    return face_service.find_faces_of_same_person(face_id, other_face_ids, confidence)


def _other_face_ids(face_id, faces_by_id):
    face_ids = set(faces_by_id.keys())
    face_ids.remove(face_id)
    return face_ids


def _find_best_common_face(common_face_ids, faces_by_id):
    """
    Find the face which takes up the largest percent of its image from all the common faces
    """

    best_face = None
    for face_id in common_face_ids:
        face = faces_by_id[face_id]
        if best_face is None or face.percent_of_image > best_face.percent_of_image:
            best_face = face

    return best_face
