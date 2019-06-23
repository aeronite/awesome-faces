from flask_restplus import Api, Resource, fields
from werkzeug.exceptions import BadRequest
from . import common_face_finder

api = Api(version='1.0')
ns_faces = api.namespace('faces', description='Awesome face tools')

analysis_input = ns_faces.model("Requested images to analyze", {
    "image_ids": fields.List(fields.String(description="id of a given image", required=True), required=True)
})


@ns_faces.route("/most_common")
class FaceAnalyzerResource(Resource):
    @ns_faces.expect(analysis_input)
    def post(self):
        req = CommonFaceRequest(api.payload)

        most_common_face = common_face_finder.find_most_common(req.image_ids, req.confidence)
        if most_common_face is None:
            return {"status": "no faces found"}

        return most_common_face


class CommonFaceRequest:
    """
    Validates the json inut and extracts the 'image_ids' and 'confidence' params
    """

    def __init__(self, json_input):

        if 'image_ids' not in json_input:
            raise BadRequest('image_ids param required')

        image_ids = json_input['image_ids']
        if not isinstance(image_ids, list):
            raise BadRequest('image_ids param should be a list of urls')

        if len(image_ids) == 0:
            raise BadRequest('image_ids param cannot be empty')

        self.image_ids = image_ids

        if 'confidence' in json_input:
            self.confidence = json_input['confidence']
        else:
            self.confidence = 0.8
