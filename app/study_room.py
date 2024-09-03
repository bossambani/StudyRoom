import os
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Resource, StudyRoom
from app.forms import ResourceForm
from app import db

study_room = Blueprint('study_room', __name__)

@study_room.route('/study_room/<int:room_id>/upload', methods=['GET', 'POST'])
@login_required
def upload_resource(room_id):
    room = StudyRoom.query.get_or_404(room_id)
    form = ResourceForm()
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        form.file.data.save(os.path.join('uploads', filename))
        resource = Resource(title=form.title.data, link=form.link.data, description=form.description.data, type=form.type.data, user_id=current_user.id, room_id=room.id)
        db.session.add(resource)
        db.session.commit()
        flash('Resource uploaded successfully', 'success')
        return redirect(url_for('study_room.room', room_id=room.id))
    
    return render_template('Resource.html', form=form, room=room)
