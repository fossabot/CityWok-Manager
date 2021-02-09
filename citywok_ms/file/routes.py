from datetime import datetime

from flask.helpers import send_file

from citywok_ms import db
from citywok_ms.file.forms import FileUpdateForm
from citywok_ms.models import File
from flask import (Blueprint, current_app, flash, redirect, render_template,
                   request, send_from_directory, url_for)

file = Blueprint('file', __name__, url_prefix="/file")


@file.route('/<file_id>/download', strict_slashes=False)
@file.route('/<file_id>/download/<file_name>', strict_slashes=False)
def download(file_id, file_name=None):
    '''
    View to download the file
    '''
    f: File = db.session.query(File).get_or_404(file_id)
    if f.full_name != file_name:
        return redirect(url_for('file.download', file_id=file_id, file_name=f.full_name))
    return send_file(f.file_path,
                     cache_timeout=0)


@file.route('/<file_id>/delete', methods=['POST'])
def delete(file_id):
    '''
    View to delete(move to trash bin and removed later) a file
    '''
    f: File = db.session.query(File).get_or_404(file_id)
    if f.delete_date:
        flash('File has already been deleted', 'info')
    else:
        f.delete()
        flash('File has been move to trash bin', 'success')
    return redirect(f.owner_url)


@file.route('/<file_id>/restore', methods=['POST'])
def restore(file_id):
    '''
    View to restore the file form trash bin
    '''
    f: File = db.session.query(File).get_or_404(file_id)
    if not f.delete_date:
        flash("File hasn't been deleted", 'info')
    else:
        f.restore()
        flash('File has been restore', 'success')
    return redirect(f.owner_url)


@file.route('/<file_id>/update', methods=["GET", "POST"])
def update(file_id):
    '''
    View to update the file's information
    '''
    f: File = db.session.query(File).get_or_404(file_id)
    form = FileUpdateForm()
    if form.validate_on_submit():
        f.update(form)
        flash("File has been update", "success")
        return redirect(f.owner_url)
    form.file_name.data = f.file_name
    form.remark.data = f.remark
    return render_template('file/update.html',
                           title="Update File",
                           form=form,
                           file=f)
