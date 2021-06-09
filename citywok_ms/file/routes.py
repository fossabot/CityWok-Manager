from citywok_ms.file.forms import FileUpdateForm
from flask import Blueprint, flash, redirect, render_template, url_for
from flask.helpers import send_file
import citywok_ms.file.service as fileservice

file = Blueprint("file", __name__, url_prefix="/file")


@file.route("/<file_id>/download", strict_slashes=False)
@file.route("/<file_id>/download/<file_name>", strict_slashes=False)
def download(file_id, file_name=None):
    f = fileservice.get_file(file_id)
    if f.full_name != file_name:
        return redirect(
            url_for("file.download", file_id=file_id, file_name=f.full_name)
        )
    return send_file(f.path, cache_timeout=0)


@file.route("/<file_id>/delete", methods=["POST"])
def delete(file_id):
    f = fileservice.get_file(file_id)
    if f.delete_date:
        flash("File has already been deleted", "info")
    else:
        fileservice.delete_file(f)
        flash("File has been move to trash bin", "success")
    return redirect(f.owner_url)


@file.route("/<file_id>/restore", methods=["POST"])
def restore(file_id):
    f = fileservice.get_file(file_id)
    if not f.delete_date:
        flash("File hasn't been deleted", "info")
    else:
        fileservice.restore_file(f)
        flash("File has been restore", "success")
    return redirect(f.owner_url)


@file.route("/<file_id>/update", methods=["GET", "POST"])
def update(file_id):
    f = fileservice.get_file(file_id)
    form = FileUpdateForm()
    if form.validate_on_submit():
        fileservice.update_file(f, form)
        flash("File has been update", "success")
        return redirect(f.owner_url)
    form.file_name.data = f.base_name
    form.remark.data = f.remark
    return render_template("file/update.html", title="Update File", form=form, file=f)
