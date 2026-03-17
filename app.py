from flask import Flask, render_template, request, redirect, url_for
from flask import flash
from s3_utils import delete_folder, folder_has_files
from s3_utils import (
    list_buckets,
    create_bucket,
    list_objects,
    upload_file,
    delete_object,
    create_folder,
    copy_object,
    move_object,
    delete_bucket_with_contents,
    is_bucket_empty
)
app = Flask(__name__)
app.secret_key = "my_secret_key_123"

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
    folder = request.form.get("folder", "").strip()

    if file and bucket:
        try:
            filename = file.filename

            # If folder selected → prepend folder
            if folder:
                key = f"{folder}{filename}"
            else:
                key = filename

            upload_file(bucket, file, key)
            flash("File uploaded successfully", "success")

        except Exception as e:
            flash(f"Upload failed: {str(e)}", "error")

    else:
        flash("No file selected", "error")

    return redirect(url_for("view_bucket", bucket_name=bucket))

@app.route("/delete-file", methods=["POST"])
def delete_file():
    bucket = request.form.get("bucket")
    key = request.form.get("key")

    try:
        delete_object(bucket, key)
        flash("File deleted successfully", "success")

    except Exception as e:
        flash(f"Error deleting file: {str(e)}", "error")

    return redirect(url_for("view_bucket", bucket_name=bucket))

@app.route("/create-folder", methods=["POST"])
def create_folder_route():
    bucket = request.form.get("bucket")
    folder = request.form.get("folder")

    try:
        create_folder(bucket, folder)
        flash("Folder created successfully", "success")

    except Exception as e:
        flash(f"Error creating folder: {str(e)}", "error")

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
            flash("File copied successfully", "success")

        elif action == "move":
            move_object(src_bucket, src_key, dest_bucket, dest_key)
            flash("File moved successfully", "success")

    except ValueError as e:
        flash(str(e), "error")
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


@app.route("/delete-bucket/<bucket_name>")
def delete_bucket_confirm(bucket_name):
    empty = is_bucket_empty(bucket_name)

    return render_template(
        "delete_bucket.html",
        bucket=bucket_name,
        is_empty=empty
    )


@app.route("/delete-bucket", methods=["POST"])
def delete_bucket_route():
    bucket = request.form.get("bucket")

    try:
        delete_bucket_with_contents(bucket)
        flash(f"Bucket '{bucket}' deleted successfully", "success")

    except Exception as e:
        flash(f"Error deleting bucket: {str(e)}", "error")

    return redirect(url_for("index"))

@app.route("/delete-folder/<bucket>/<path:folder>")
def delete_folder_confirm(bucket, folder):
    has_files = folder_has_files(bucket, folder)

    return render_template(
        "delete_folder.html",
        bucket=bucket,
        folder=folder,
        has_files=has_files
    )

@app.route("/delete-folder", methods=["POST"])
def delete_folder_route():
    bucket = request.form.get("bucket")
    folder = request.form.get("folder")

    try:
        delete_folder(bucket, folder)
        flash("Folder deleted successfully", "success")

    except Exception as e:
        flash(f"Error deleting folder: {str(e)}", "error")

    return redirect(url_for("view_bucket", bucket_name=bucket))

if __name__=="__main__":
 app.run(debug=True)
