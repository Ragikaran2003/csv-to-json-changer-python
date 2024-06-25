from flask import Flask, render_template, request, redirect, url_for, send_file
import csv
import json
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    # Check if a file was submitted
    if 'file' not in request.files:
        return redirect(url_for('index'))

    file = request.files['file']

    # If no file selected
    if file.filename == '':
        return redirect(url_for('index'))

    # Save the file to the uploads folder
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Convert CSV to JSON
    json_file_path = os.path.splitext(file_path)[0] + '.json'
    convert_csv_to_json(file_path, json_file_path)

    # Provide download link to the user
    return render_template('result.html', csv_filename=file.filename, json_filename=os.path.basename(json_file_path))

def convert_csv_to_json(csv_file, json_file):
    data = []

    # Read CSV file and convert rows to dictionaries
    with open(csv_file, 'r', newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            data.append(row)

    # Write data to JSON file
    with open(json_file, 'w') as jsonfile:
        json.dump(data, jsonfile, indent=4)

@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
