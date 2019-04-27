from flask import Flask, render_template, request, url_for
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import TextAreaField
from textblob import TextBlob, Word
# from flask_uploads import UploadSet, configure_uploads, All, DATA
from werkzeug.utils import secure_filename
import random
import os

# configuration
app = Flask(__name__)
secret_key = os.urandom(24)
app.config['SECRET_KEY'] = secret_key
# files = UploadSet('files', All)
# app.config['UPLOADED_FILES_DEST'] = 'static/data'
# configure_uploads(app, files)


class textinput(FlaskForm):
    text = TextAreaField()


class uploadfile(FlaskForm):
    txtfiles = FileField(validators=[
        FileAllowed(['txt'], 'must be txt file!')])


@app.route('/')
def index():
    form = textinput()
    upload = uploadfile()
    return render_template('index.html', form=form, upload=upload)


@app.route('/analyze', methods=['POST', 'GET'])
def analyze():
    form = textinput()
    upload = uploadfile()
    if form.validate_on_submit():
        text = form.text.data

        # nlp processing
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        numofwords = len(list(blob.words))

    return render_template('index.html', form=form, upload=upload, blob=blob, polarity=polarity, subjectivity=subjectivity, numofwords=numofwords)


@app.route('/dataupload', methods=['GET', 'POST'])
def dataupload():
    form = textinput()
    upload = uploadfile()
    if upload.validate_on_submit():
        txt = upload.txtfiles.data
        content = txt.read()
        content = content.decode("utf-8")

        # nlp processing
        blob = TextBlob(content)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        numofwords = len(list(blob.words))

    return render_template('index.html', form=form, upload=upload, content=content, blob=blob, polarity=polarity, subjectivity=subjectivity, numofwords=numofwords)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
