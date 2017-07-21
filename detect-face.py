
# This code detects whether an images sent over an http post request is a face or not


import cv,cv2
import os
import time as tm

from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

# Initialize the Flask application
app = Flask(__name__)

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])

# initialize final response
STATUS = False

# For a given file, return whether it's an allowed type or not


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# function to detect the face using harcascade


def detect(image):
    image_faces = []
    bitmap = cv.fromarray(image)
    cascade = cv.Load('haarcascade_frontalface_alt.xml')
    faces = cv.HaarDetectObjects(bitmap, cascade, cv.CreateMemStorage(0))
    if faces:
        for (x, y, w, h), n in faces:
            image_faces.append(image[y:(y + h), x:(x + w)])
    return image_faces

# Route that will process the file upload


@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = str(tm.time()) + "__" + secure_filename(file.filename)

        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # apply the face detection algorithm on it
        # -------------------------------------------------------------
        path = 'uploads/'
        imagepath = path + filename
        image = cv2.imread(imagepath)
        image_faces = []
        image_faces = detect(image)
        if(image_faces == []):
            # no face detected
            STATUS = False
        else:
            # face detected
            STATUS = True
        return jsonify({'status':STATUS})

if __name__ == '__main__':
    app.run(debug=True, port=8080)
