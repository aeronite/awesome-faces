from . import face_service


def find_most_common(face_urls, confidence):
    """
    Detects face metadata from a list of images and then attempts to find the most common face

    The algorithm heuristic eagerly groups faces into dis-joined sets.

    For example, consider an analysis of faces a,b & c with min confidence of 0.9:
    a - b has confidence 0.92
    a - c has confidence 0.85
    b - c has confidence 0.91

    The first set found is [a,b] after this only 'c' is left so it forms its own set [c]. This is even
    though theoretically 'b' could have formed the set [b,a,c] if it ran first.
    """

    faces_by_image = [face_service.detect_faces(face) for face in face_urls]

    # flatten face lists for each image into one larger list
    faces = [face for faces_for_single_image in faces_by_image for face in faces_for_single_image]

    # map these into a dict of faces keyed by their face_ids
    faces_by_id = {faces[i].face_id(): faces[i] for i in range(0, len(faces))}
    face_id_set = set(faces_by_id)

    most_face_ids_of_same_person = []

    for face in faces:
        # first make sure we haven't already grouped this face in previous iterations
        if face.face_id() in face_id_set:
            other_face_ids = _other_face_ids(face.face_id(), face_id_set)

            if len(other_face_ids) > 0:
                same_person_ids = face_service.find_faces_of_same_person(face.face_id(), other_face_ids, confidence)

                if len(same_person_ids) > len(most_face_ids_of_same_person):
                    most_face_ids_of_same_person = same_person_ids

                _remove_used_faces(face_id_set, same_person_ids)

    return _find_best_common_face(most_face_ids_of_same_person, faces_by_id)


def _remove_used_faces(face_id_set, face_ids_to_remove):
    for id in face_ids_to_remove:
        face_id_set.discard(id)


def _other_face_ids(target_face_id, face_id_set):
    face_id_set.discard(target_face_id)
    return list(face_id_set)


def _find_best_common_face(common_face_ids, faces_by_id):
    """
    Find the face which takes up the largest percent of its image from all the common faces
    """

    best_face = None
    for face_id in common_face_ids:
        face = faces_by_id[face_id]
        if best_face is None or face.percent_of_image > best_face.percent_of_image:
            best_face = face

    return best_face.prepare_meta(len(common_face_ids))
