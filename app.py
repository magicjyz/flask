from flask import Flask, render_template, request, send_from_directory, redirect, url_for, flash
from werkzeug.utils import secure_filename
from modules import module1
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESULT_FOLDER'] = 'results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html', active_module='module1')

@app.route('/upload/module1', methods=['POST'])
def upload_module1():
    file = request.files.get('file')
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        sequences = module1.read_uploaded_sequences(file_path)
        return render_template('index.html',
                               active_module='module1',
                               sequences=sequences,
                               uploaded_filename=filename)
    else:
        flash("请上传一个有效的FASTA文件")
        return redirect(url_for('index'))

@app.route('/generate/module1', methods=['POST'])
def generate_module1():
    filename = request.form['file_path']
    mutation_mode = request.form['mutation_mode']
    positions_str = request.form.get('positions', '')
    positions = [int(p.strip()) for p in positions_str.split(',') if p.strip().isdigit()] if positions_str else []

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    peptides = module1.generate_mutated_sequences(file_path, mutation_mode, positions)
    summary, download_link = module1.save_and_summarize(peptides)

    return render_template('index.html',
                           active_module='module1',
                           result=summary,
                           download_link=download_link)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(RESULT_FOLDER, filename, as_attachment=True)

@app.route('/download/example')
def download_example():
    return send_from_directory('static/files', 'example.fasta', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
