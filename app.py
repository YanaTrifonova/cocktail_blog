import logging
import sys

from flask import Flask, jsonify, request

from orm.orm import get_articles, get_tags, write_article_with_tags, get_top_tags

app_name = "r2r"

app = Flask(__name__)

logger = logging.getLogger(app_name)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


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
        data = get_articles(size, offset, search, cocktails_only, with_tag)
        output = {
            "articles": []
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
                "tags": [tg[0] for tg in all_tags if not tg[1]],
                "ingredients": [tg[0] for tg in all_tags if tg[1]]
            })
    except Exception as e:
        msg = "Error while processing request " + str(e)
        logger.exception(msg)
        return jsonify({"error": msg}), 500
    return jsonify(output), 200


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
