import logging
import sys

from flask import Flask, jsonify, request, render_template

from orm.orm import get_articles, get_tags, write_article_with_tags, get_top_tags, get_cocktails, get_article_db

app_name = "r2r"

app = Flask(__name__)

logger = logging.getLogger(app_name)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route('/')
def static_page():
    return render_template('index.html')


@app.route('/posts/<guid>')
def static_single_post(guid):
    return render_template('index.html')

@app.route('/post')
def post_page():
    return render_template('post.html')


@app.route('/ingredients')
def ingredients_page():
    return render_template('Ingredients.html')


@app.route('/list')
def list_page():
    return render_template('list.html')


@app.route('/contactUs')
def contact_us_page():
    return render_template('contactUs.html')


@app.route('/about')
def about_page():
    return render_template('about.html')


@app.route('/articles', methods=['PUT'])
def save_articles():
    body = request.get_json()
    try:
        write_article_with_tags(body)
    except Exception as e:
        msg = "Error while processing request " + str(e)
        logger.exception(msg)
        return jsonify({"error": msg}), 500
    return jsonify({"status": "data are saved"}), 200


@app.route("/tags", methods=["GET"])
def get_req_tags():
    try:
        is_ingr = request.args.get("ingredient")
        if is_ingr is not None:
            is_ingr = True if is_ingr == "true" else False
    except Exception as e:
        msg = "Incorrect input request " + str(e)
        logger.exception(msg)
        return jsonify({"error": msg}), 400
    try:
        data = get_tags(is_ingr, None)
        output = {"tags": []}
        for dt in data:
            output["tags"].append({"name": dt[0]})
    except Exception as e:
        msg = "Error while processing request " + str(e)
        logger.exception(msg)
        return jsonify({"error": msg}), 500
    return jsonify(output), 200


@app.route("/tags/top", methods=["GET"])
def get_top_req_tags():
    try:
        top_number = request.args.get("top_number", 10)
    except Exception as e:
        msg = "Incorrect input request " + str(e)
        logger.exception(msg)
        return jsonify({"error": msg}), 400
    try:
        data = get_top_tags(top_number)
        output = {"tags": []}
        for dt in data:
            output["tags"].append({"name": dt[0]})
    except Exception as e:
        msg = "Error while processing request " + str(e)
        logger.exception(msg)
        return jsonify({"error": msg}), 500
    return jsonify(output), 200


@app.route('/articles/<guid>', methods=['GET'])
def get_article(guid):
    try:
        data = get_article_db(guid)
        output = create_output(data, False, False)
    except Exception as e:
        msg = "Error while processing request " + str(e)
        logger.exception(msg)
        return jsonify({"error": msg}), 500
    return jsonify(output), 200


@app.route('/articles', methods=['GET'])
def get_all_articles():
    try:
        size = request.args.get('size', 5)
        offset = request.args.get('offset', 0)
        search = request.args.get("search")
        with_tag = request.args.get("tag")
        cocktails_only = request.args.get("cocktail")
        if cocktails_only is not None:
            cocktails_only = True if cocktails_only == "true" else False
    except Exception as e:
        msg = "Incorrect input request " + str(e)
        logger.exception(msg)
        return jsonify({"error": msg}), 400
    try:
        data, has_prev, has_next = get_articles(size, offset, search, cocktails_only, with_tag)
        output = create_output(data, has_prev, has_next)
    except Exception as e:
        msg = "Error while processing request " + str(e)
        logger.exception(msg)
        return jsonify({"error": msg}), 500
    return jsonify(output), 200

@app.route('/cocktails', methods=['GET'])
def get_all_cocktails():
    try:
        cocktails = get_cocktails()
        output = {"cocktails": {}}
        for id, nm, ingr in cocktails:
            output["cocktails"].setdefault(ingr, []).append({"name": nm, "id": id})
    except Exception as e:
        msg = "Error while processing request " + str(e)
        logger.exception(msg)
        return jsonify({"error": msg}), 500
    return jsonify(output), 200


def create_output(data, has_prev, has_next):
    output = {
        "articles": [],
        "has_previous": has_prev,
        "has_next": has_next
    }
    for dt in data:
        all_tags = get_tags(None, [dt[0]])

        output["articles"].append({
            "id": dt[0],
            "title": dt[1],
            "body": dt[2],
            "is_cocktail": dt[3],
            "creation_time": dt[4],
            "user_id": dt[5],
            "cocktail_name": dt[6],
            "tags": [tg[0] for tg in all_tags if not tg[1]],
            "ingredients": [tg[0] for tg in all_tags if tg[1]]
        })
    return output


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
