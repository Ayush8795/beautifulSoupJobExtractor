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
    if not urls or not topics or not page_limits:
        return jsonify(
            {
                "status": "error",
                "message": "Please provide all required fields.",
                "statusCode": 400
            }
        ), 400

    experiences = request.form.getlist('experience[]')
    limits = [int(x) for x in page_limits]

    ret = jexx.runner(urls, topics, limits, experiences)

    if ret:
        return jsonify(
            {
                "status": "success",
                "message": "Job extraction completed successfully.",
                "data": ret,
                "statusCode": 200
            }
        ), 200
    return jsonify({
        "status": "error",
        "message": "Job extraction failed.",
        "statusCode": 500
    }), 500

if __name__ == '__main__':
    app.run(debug=True)