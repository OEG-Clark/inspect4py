import os
import flask
import copy
from flask import request, url_for, render_template, redirect, flash, send_from_directory, current_app, session, jsonify
from flask_bootstrap import Bootstrap

from source.chowlk.transformations import transform_ontology
from source.chowlk.utils import read_drawio_xml
import xml.etree.ElementTree as ET
from config import config


config_name = os.environ.get("APP_MODE") or "development"

app = flask.Flask(__name__)
app.config.from_object(config[config_name])
bootstrap = Bootstrap(app)

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")

@app.route("/demoeswc2021", methods=["GET", "POST"])
def poster():
    return render_template("chowlk_poster.html")


@app.route("/download/<path:format>", methods=["GET", "POST"])
def download(format):
    ontology_directory = os.path.join(current_app.root_path, app.config["TEMPORAL_FOLDER"])
    if format == "ttl":
        return send_from_directory(ontology_directory, session.get("ttl_filename"), as_attachment=True)
    elif format == "xml":
        return send_from_directory(ontology_directory, session.get("xml_filename"), as_attachment=True)


@app.route("/diagram_upload", methods=["GET", "POST"])
def diagram_upload():

    if request.method == "POST" and "diagram_data" in request.files:
        file = request.files["diagram_data"]
        
        filename = file.filename

        if filename == "":
            error = "No file choosen. Please choose a diagram."
            flash(error)
            return redirect(url_for("home"))

        root = read_drawio_xml(file)
        ttl_filename = filename[:-3] + "ttl"
        xml_filename = filename[:-3] + "owl"

        if not os.path.exists(app.config["TEMPORAL_FOLDER"]):
            os.makedirs(app.config["TEMPORAL_FOLDER"])
        
        ttl_filepath = os.path.join(app.config["TEMPORAL_FOLDER"], ttl_filename)
        xml_filepath = os.path.join(app.config["TEMPORAL_FOLDER"], xml_filename)
        turtle_file_string, xml_file_string, new_namespaces, errors = transform_ontology(root)

        # Eliminating keys that do not contain errors
        new_errors = copy.copy(errors)
        for key, error in errors.items():
            if len(error) == 0:
                del new_errors[key]

        with open(ttl_filepath, "w") as file:
            file.write(turtle_file_string)

        with open(xml_filepath, "w") as file:
            file.write(xml_file_string)

        session["ttl_filename"] = ttl_filename
        session["xml_filename"] = xml_filename


        with open(ttl_filepath, "r", encoding='utf-8') as f:
            ttl_data = f.read()
            ttl_data = ttl_data.split('\n')

        with open(xml_filepath, "r", encoding='utf-8') as f:
            xml_data = f.read()
            xml_data = xml_data.split('\n')

        return render_template("output.html", ttl_data=ttl_data, xml_data=xml_data, namespaces=new_namespaces, errors=new_errors)


@app.route("/api", methods=["GET", "POST"])
def api():

    if request.method == "POST":
        file = request.files["data"]
        filename = file.filename

        if filename == "":
            error = "No file choosen. Please choose a diagram."
            flash(error)
            return redirect(url_for("home"))

        root = read_drawio_xml(file)
        ttl_filename = filename[:-3] + "ttl"
        xml_filename = filename[:-3] + "owl"

        ttl_filepath = os.path.join(app.config["TEMPORAL_FOLDER"], ttl_filename)
        transform_ontology(root)

        session["ttl_filename"] = ttl_filename

        with open(ttl_filepath, "r") as f:
            ttl_data = f.read()

        return ttl_data

@app.route("/errors", methods=["GET", "POST"])
def errors():

    if request.method == "POST":
        file = request.files["data"]
        filename = file.filename

        if filename == "":
            error = "No file choosen. Please choose a diagram."
            flash(error)
            return redirect(url_for("home"))

        root = read_drawio_xml(file)
        ttl_filename = filename[:-3] + "ttl"

        ttl_filepath = os.path.join(app.config["TEMPORAL_FOLDER"], ttl_filename)
        turtle_file_string, xml_file_string, namespaces, errors = transform_ontology(root)

        return jsonify(errors)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=app.config["DEBUG"])