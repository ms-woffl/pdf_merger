from flask import Flask, request, redirect, url_for, send_file, render_template
import os
from PyPDF2 import PdfMerger
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MERGED_FOLDER'] = 'merged'

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['MERGED_FOLDER'], exist_ok=True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/merge', methods=['POST'])
def merge_pdfs():
    if 'files[]' not in request.files:
        return "No files uploaded", 400

    files = request.files.getlist('files[]')
    if not files or len(files) < 2:
        return "Please upload at least two PDF files.", 400

    # Save uploaded files
    file_paths = []
    for file in files:
        if file.filename == '':
            return "Empty filename detected.", 400

        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        file_paths.append(file_path)

    # Merge PDFs
    merged_file_path = os.path.join(app.config['MERGED_FOLDER'], 'merged_output.pdf')
    pdf_merger = PdfMerger()

    try:
        for path in file_paths:
            pdf_merger.append(path)

        pdf_merger.write(merged_file_path)
        pdf_merger.close()
    except Exception as e:
        return f"Error merging PDFs: {e}", 500

    # Return the merged PDF file
    return send_file(merged_file_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
