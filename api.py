from flask import Flask, render_template, request
from pathlib import Path
import json


# Resolve the JSON file relative to this script, regardless of the working directory.
BASE_DIR = Path(__file__).resolve().parent
FILE_PATH = BASE_DIR / "results.json"

app = Flask(__name__)

def read_file(file_path=FILE_PATH):
    """Read and return the stored JSON collection."""
    with open(file_path, "r") as file:
        content = file.read()

    return json.loads(content)

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/api/v1/results", methods=["GET", "POST"])
def results():
    """Retrieve security findings or add new findings to the collection."""
    if request.method == "GET":
        data = read_file()
        return data

    else:
        data = read_file()
        new_result = request.get_json()
        required_fields = {"name", "type", "description", "date"}

        if type(new_result) == dict:
            if new_result in data["results"]:
                return {"error": "Entry already exists."}, 409

            if required_fields <= new_result.keys():
                data["results"].append(new_result)

            else:
                return {"error": "Not all required fields are present."}, 400

        elif type(new_result) == list:
            for each_result in new_result:
                if each_result in data["results"]:
                    return {"error": "One entry already exists, or you may have duplicates."}, 409

                if required_fields <= each_result.keys():
                    data["results"].append(each_result)

                else:
                    return {"error": "Not all required fields are present."}, 400

        else:
            return {"error": "Expected a JSON object or a list of JSON objects."}, 400

        # Write only after validation succeeds for the entire request.
        with open(FILE_PATH, "w") as file:
            file.write(json.dumps(data))

        return {
            "message": "Received successfully",
            "result": new_result
        }, 201


if __name__ == "__main__":
    app.run(debug=True, port=5000)