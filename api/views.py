from io import open 
import json
import os
import utils
import csv
import settings
import middleware
from middleware import model_predict
from werkzeug.utils import secure_filename

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    jsonify,
)

router = Blueprint("app_router", __name__, template_folder="templates")


@router.route("/", methods=["GET"])
def index():
    """
    Index endpoint, renders our HTML code.
    """
    return render_template("index.html")


@router.route("/", methods=["POST"])
def upload_image():
    """
    Function used in our frontend so we can upload and show an image.
    When it receives an image from the UI, it also calls our ML model to
    get and display the predictions.
    """
    # No file received, show basic UI
    if "file" not in request.files:
        flash("No file part")
        return redirect(request.url)

    # File received but no filename is provided, show basic UI
    file = request.files["file"]
    if file.filename == "":
        flash("No image selected for uploading")
        return redirect(request.url)

    # File received and it's an image, we must show it and get predictions
    if file and utils.allowed_file(file.filename):
        # In order to correctly display the image in the UI and get model
        # predictions you should implement the following:

        #   1. Get an unique file name using utils.get_file_hash() function
        file_hash = utils.get_file_hash(file)
        file.filename = file_hash
        sec_filename = secure_filename(file.filename)

        #   2. Store the image to disk using the new name
        if not os.path.exists(settings.UPLOAD_FOLDER+sec_filename):
    
            file.save(os.path.join(settings.UPLOAD_FOLDER, sec_filename))

        #   3. Send the file to be processed by the `model` service
        #      Hint: Use middleware.model_predict() for sending jobs to model
        #            service using Redis.
        predict, score = middleware.model_predict(file_hash)

        #   4. Update `context` dict with the corresponding values
        # TODO
        context = {
            "prediction": predict,
            "score": score,
            "filename": file_hash,
        }
 
        # Update `render_template()` parameters as needed
        # TODO
        return render_template(
            "index.html", filename=file_hash, context=context
        )
    # File received and but it isn't an image
    else:
        flash("Allowed image types are -> png, jpg, jpeg, gif")
        return redirect(request.url)


@router.route("/display/<filename>")
def display_image(filename):
    """
    Display uploaded image in our UI.
    """
    return redirect(
        url_for("static", filename="uploads/" + filename), code=301
    )


@router.route("/predict", methods=["POST"])
def predict():
    """
    Endpoint used to get predictions without need to access the UI.

    Parameters
    ----------
    file : str
        Input image we want to get predictions from.

    Returns
    -------
    flask.Response
        JSON response from our API having the following format:
            {
                "success": bool,
                "prediction": str,
                "score": float,
            }

        - "success" will be True if the input file is valid and we get a
          prediction from our ML model.
        - "prediction" model predicted class as string.
        - "score" model confidence score for the predicted class as float.
    """
    # To correctly implement this endpoint you should:
    #   1. Check a file was sent and that file is an image
    rpse = {"success": False, "prediction": None, "score": None}
    
    # file_not_null = ("file" in request.files) and (request.files["file"] is not None)
    # file_is_allowed = (file and utils.allowed_file(file.filename))
    if "file" not in request.files:
        return jsonify(rpse), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify(rpse), 400

    if file and utils.allowed_file(file.filename):

    #   2. Store the image to disk 
        file_hash = utils.get_file_hash(file)
        file.filename = file_hash
        sec_filename = secure_filename(file.filename)
        if not os.path.exists(settings.UPLOAD_FOLDER+sec_filename):
           file.save(os.path.join(settings.UPLOAD_FOLDER, sec_filename))
    #   3. Send the file to be processed by the `model` service
    #      Hint: Use middleware.model_predict() for sending jobs to model
    #            service using Redis.
        predict, score = model_predict(sec_filename)
    #   4. Update and return `rpse` dict with the corresponding values
        rpse = {"success": True, "prediction": str(predict), "score": float(score)}
        return jsonify(rpse), 200
    # If user sends an invalid request (e.g. no file provided) this endpoint
    # should return `rpse` dict with default values HTTP 400 Bad Request code
    # TODO
    else:
        return jsonify(rpse), 400


@router.route("/feedback", methods=["GET", "POST"])
def feedback():
    """
    Store feedback from users about wrong predictions on a text file.

    Parameters
    ----------
    report : request.form
        Feedback given by the user with the following JSON format:
            {
                "filename": str,
                "prediction": str,
                "score": float
            }

        - "filename" corresponds to the image used stored in the uploads
          folder.
        - "prediction" is the model predicted class as string reported as
          incorrect.
        - "score" model confidence score for the predicted class as float.
    """
    # Get reported predictions from `report` key
    report = request.form.get("report")

    # Store the reported data to a file on the corresponding path
    # already provided in settings.py module
    # report.save(settings.FEEDBACK_FILEPATH)

    # TODO
    # import csv
    # import json

    # report = {
    #             "filename": str,
    #             "prediction": str,
    #             "score": float
    #         }
    # info = json.loads(report)['Results']
            


    # print(info[0].keys())
      

    with open('feedback/feedback', 'a') as f:

        # write the data
        f.write(str(report))
        f.write("\n")
        f.close()
 
    return render_template("index.html")
