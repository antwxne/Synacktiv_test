from flask import Blueprint, render_template, request, url_for, jsonify
import subprocess
from vulnapp.core import config

gallery = Blueprint('gallery', __name__)


@gallery.route('/gallery')
def gallery_page():
    images = {'1': 'launching.jpg', '2': 'launching2.jpg', '3': 'launching3.jpg'}
    return render_template('gallery.html', images=images)


@gallery.route('/gallery/download')
def download():
    filepath = request.args.get('file', '')
    b64_encode = request.args.get('base64', '')
    file_content = ''
    complete_filepath = config.STATIC_FOLDER + 'static/img/' + filepath
    if not b64_encode:
        with open(complete_filepath, 'rb') as download_file:
            file_content = download_file.read()
    else:
        file_content = subprocess.check_output(
            f"cat {complete_filepath} | base64", shell=True,)
    return jsonify({'filecontent': file_content.decode('utf-8')})
