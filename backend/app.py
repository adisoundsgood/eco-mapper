import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename
import numpy as np
from osgeo import gdal
from .processor import calculate_ndvi, calculate_slope_aspect, estimate_carbon_storage

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app) # enables CORS for all routes

UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
ALLOWED_EXTENSIONS = {'tif', 'tiff'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return render_template("index.html")

@app.route('/results/<path:filename>')
def serve_result(filename):
  return send_from_directory(app.config['RESULT_FOLDER'], filename)

@app.route('/api/process', methods=['POST'])
def process_file():
  if 'file' not in request.files:
      return jsonify({'error': 'No file part'}), 400
  file = request.files['file']
  process_type = request.form.get('process_type', 'ndvi')  # Default to NDVI if not specified
  
  if file.filename == '':
      return jsonify({'error': 'No selected file'}), 400
  if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
      output_filename = f"processed_{filename}"
      output_path = os.path.join(app.config['RESULT_FOLDER'], output_filename)
      
      file.save(input_path)
      
      try:
          if process_type == 'ndvi':
              process_result = calculate_ndvi(input_path, output_path)
          elif process_type == 'slope_aspect':
              slope_path = os.path.join(app.config['RESULT_FOLDER'], f"slope_{filename}")
              aspect_path = os.path.join(app.config['RESULT_FOLDER'], f"aspect_{filename}")
              process_result = calculate_slope_aspect(input_path, slope_path, aspect_path)
          elif process_type == 'carbon':
              process_result = estimate_carbon_storage(input_path, output_path)
          else:
              return jsonify({'error': 'Invalid process type'}), 400
      except Exception as e:
          return jsonify({'error': str(e)}), 500
      
      if isinstance(process_result, tuple):
          result_urls = [f"/results/{os.path.basename(path)}" for path in process_result]
          return jsonify({'result_urls': result_urls}), 200
      else:
          result_url = f"/results/{os.path.basename(process_result)}"
          return jsonify({'result_url': result_url}), 200
      return jsonify({'error': 'File type not allowed'}), 400
  pass


if __name__ == '__main__':
    app.run(use_reloader=True, port=5000, threaded=True)