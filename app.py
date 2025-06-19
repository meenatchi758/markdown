import os
from flask import Flask, render_template, request, send_file, redirect, url_for
import markdown
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['CONVERTED_FOLDER'] = 'converted'

# Ensure folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['CONVERTED_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    html_output = ""
    markdown_text = ""

    if request.method == 'POST':
        # Case 1: From textarea
        if 'markdown_text' in request.form:
            markdown_text = request.form['markdown_text']
            html_output = markdown.markdown(markdown_text)

        # Case 2: File upload
        elif 'file' in request.files:
            file = request.files['file']
            if file.filename.endswith('.md'):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                with open(filepath, 'r', encoding='utf-8') as f:
                    markdown_text = f.read()
                    html_output = markdown.markdown(markdown_text)
            else:
                html_output = "<p style='color:red;'>Only .md files are allowed!</p>"

    return render_template("index.html", markdown_text=markdown_text, html_output=html_output)

@app.route('/download', methods=['POST'])
def download():
    html_content = request.form['html_content']
    output_file = os.path.join(app.config['CONVERTED_FOLDER'], 'converted.html')

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    return send_file(output_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
