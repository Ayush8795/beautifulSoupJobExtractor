from flask import Flask, request, jsonify, render_template
import jobExtractor as jexx

app = Flask(__name__)

@app.route("/", methods = ['GET'])
def welcome():
    return render_template("home.html")

@app.route('/execute/', methods=['POST'])
def execute():
    urls = request.form.getlist('url[]')
    topics = request.form.getlist('topic[]')
    page_limits = request.form.getlist('limit[]')

    limits = [int(x) for x in page_limits]

    ret = jexx.runner(urls, topics, limits)

    if ret:
        return 'success'
    return 'error',500

if __name__ == '__main__':
    app.run(debug=True)