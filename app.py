from flask import Flask, render_template, request, redirect, url_for
from s3_utils import (
    list_buckets,
    create_bucket,
    list_objects,
    upload_file,
    delete_object,
    create_folder,
    copy_object,
    move_object
)
app = Flask(__name__)

@app.route("/")
def index():
    buckets = list_buckets()
    return render_template("index.html", buckets=buckets)
    
@app.route("/create-bucket", methods=["POST"])
def create_bucket_route():
    bucket_name = request.form.get("bucket_name")
    if bucket_name:
        create_bucket(bucket_name)
    return redirect(url_for("index"))


@app.route("/bucket/<bucket_name>")
def view_bucket(bucket_name):
    objects = list_objects(bucket_name)
    buckets = list_buckets()

    files = []
    folders = []

    for obj in objects:
        key = obj["Key"]
        if key.endswith("/"):
            folders.append(key)
        else:
            files.append(key)

    return render_template(
        "bucket.html",
        bucket=bucket_name,
        objects=objects,
        files=files,
        folders=folders,
        buckets=buckets
    )



@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")
    bucket = request.form.get("bucket")

    if file and bucket:
        upload_file(bucket, file, file.filename)

    return redirect(url_for("view_bucket", bucket_name=bucket))

@app.route("/delete-file", methods=["POST"])
def delete_file():
    bucket = request.form.get("bucket")
    key = request.form.get("key")

    if bucket and key:
        delete_object(bucket, key)

    return redirect(url_for("view_bucket", bucket_name=bucket))

@app.route("/create-folder", methods=["POST"])
def create_folder_route():
    bucket = request.form.get("bucket")
    folder = request.form.get("folder")

    if bucket and folder:
        create_folder(bucket, folder)

    return redirect(url_for("view_bucket", bucket_name=bucket))

    
@app.route("/copy-move", methods=["POST"])
def copy_move():
    src_bucket = request.form.get("src_bucket").strip()
    src_key = request.form.get("src_key").strip()
    dest_bucket = request.form.get("dest_bucket").strip()
    dest_key = request.form.get("dest_key").strip()
    action = request.form.get("action")

    try:
        if action == "copy":
            copy_object(src_bucket, src_key, dest_bucket, dest_key)
        elif action == "move":
            move_object(src_bucket, src_key, dest_bucket, dest_key)

    except ValueError as e:
        objects = list_objects(src_bucket)
        return render_template(
            "bucket.html",
            bucket=src_bucket,
            objects=objects,
            files=[o["Key"] for o in objects if not o["Key"].endswith("/")],
            folders=[o["Key"] for o in objects if o["Key"].endswith("/")],
            buckets=list_buckets(),
            error=str(e)
        )

    return redirect(url_for("view_bucket", bucket_name=src_bucket))




if __name__=="__main__":
 app.run(debug=True)
