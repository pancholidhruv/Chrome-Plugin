from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask import request, jsonify
from models.ImageMatch import ImageMatch
import json
from collections import OrderedDict

app = Flask(__name__)
Bootstrap(app)

def create_app(config_filename):

    app.config.from_object(config_filename)

    # from app import api_bp
    # app.register_blueprint(api_bp, url_prefix='/api')

    return app

@app.route('/')
def index():
    return render_template('index_test.html')


@app.route('/get_single_score', methods=['POST'])
def get_single_score():
    #path = request.form.to_dict(flat=False)
    data = request.data.decode("utf-8").split(",")
    images = OrderedDict()
    for img in data:
        images[img.split(":")[0]] = img.split(":")[1]

    print(images)
    result = {}
    for i in range(1, len(data)):
        diff = verify("fraud_detection/test/"+ data[i-1].split(":")[1], "fraud_detection/test/"+data[i].split(":")[1], FRmodel)
        result[i] = str(diff)

    return(jsonify(json.dumps(result)))
    #return verify("fraud_detection/test/tshirt2.jpeg","mobile6",database, FRmodel)
    #return render_template('index2.html', result=jsonify(get_score(path["files"][0]).serialize()))


@app.route('/get_scores', methods=['POST'])
def get_scores():
    raw_data = request.form.to_dict(flat=False)
    file1 = raw_data.get("file1", None)
    file2 = raw_data.get("file2", None)
    file3 = raw_data.get("file3", None)
    file4 = raw_data.get("file4", None)
    result = []
    diff = verify("static/test_imgs/"+file1[0],"static/test_imgs/"+file2[0], FRmodel)
    result.append(ImageMatch(file1[0], str(diff), "", "").serialize())
    diff = verify("static/test_imgs/"+file2[0],"static/test_imgs/"+file3[0], FRmodel)
    result.append(ImageMatch(file1[0], str(diff), "", "").serialize())
    diff = verify("static/test_imgs/"+file3[0],"static/test_imgs/"+file4[0], FRmodel)
    result.append(ImageMatch(file1[0], str(diff), "", "").serialize())
    # if dir:
    #     for path in get_full_path(files):
    #         result.append(get_score(path).serialize())
    # else:
    #     return {"Error": "dir not found"}
    return render_template('index2.html', result=jsonify(result))


if __name__ == "__main__":
    app = create_app("config")

    context = ('cert.pem', 'key.pem')
    app.run(debug=True, use_reloader=True, host="0.0.0.0",  ssl_context=context)
