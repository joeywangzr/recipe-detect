"""
Routes for processing an image.
"""

from flask import Blueprint, request, Response

from image_process.process import crop_flyer

processing_routes = Blueprint('processing', __name__, url_prefix='/process')

@processing_routes.route('/', methods=["POST"])
def process_image():
    data = request.get_json()
    print(data)
    file_path = data.get("path")
    pantry = data.get("pantry")
    crop_flyer(file_path)

    return {}