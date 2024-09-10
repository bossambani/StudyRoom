import os
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Resource, StudyRoom, User
from flask import current_app as app
from app.forms import ResourceForm
from app import db

study_room = Blueprint('study_room', __name__)

# Route to upload resource
@study_room.route('/study_room/<int:room_id>/upload', methods=['GET', 'POST'])
@login_required
def upload_resource(room_id):
    room = StudyRoom.query.get_or_404(room_id)
    form = ResourceForm()

    if form.validate_on_submit():
        file = form.file.data
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            resource = Resource(
                title=form.title.data,
                link=form.link.data,
                description=form.description.data,
                type=form.type.data,
                user_id=current_user.id,
                room_id=room.id,
                filename=filename,
                filepath=filepath
            )
            db.session.add(resource)
            db.session.commit()
            flash('Resource uploaded successfully', 'success')
            return redirect(url_for('study_room.view_room', room_id=room.id))

    return render_template('Resource.html', form=form, room=room)

# Route to create a study room
@study_room.route('/create-room', methods=['GET', 'POST'])
@login_required
def create_room():
    if request.method == 'POST':
        room_name = request.form['name']
        description = request.form.get('description')
        new_room = StudyRoom(name=room_name, description=description, owner_id=current_user.id)
        db.session.add(new_room)
        db.session.commit()
        flash('Study room created successfully!', 'success')
        return redirect(url_for('study_room.view_room', room_id=new_room.id))
    return render_template('create_room.html', user=current_user)

# Route to view room and manage participants
@study_room.route('/rooms/<int:room_id>', methods=['GET', 'POST'])
@login_required
def view_room(room_id):
    room = StudyRoom.query.get_or_404(room_id)

    if request.method == 'POST':
        action = request.form.get('action')
        user_id = request.form.get('user_id')

        # Add participant
        if action == 'add' and user_id:
            user = User.query.get(user_id)
            if user not in room.participants:
                room.participants.append(user)
                db.session.commit()
                flash(f'{user.username} added to the room!', 'success')
            else:
                flash(f'{user.username} is already a participant!', 'warning')

        # Remove participant
        elif action == 'remove' and user_id:
            user = User.query.get(user_id)
            if user in room.participants:
                room.participants.remove(user)
                db.session.commit()
                flash(f'{user.username} removed from the room!', 'success')
            else:
                flash(f'{user.username} is not a participant!', 'warning')

    return render_template('view_room.html', room=room, user=current_user)

# Route to join a room
@study_room.route('/join-room/<int:room_id>', methods=['POST'])
@login_required
def join_room(room_id):
    room = StudyRoom.query.get_or_404(room_id)
    if current_user not in room.members:
        room.members.append(current_user)
        db.session.commit()
        flash('You have joined the room!', 'success')
    else:
        flash('You are already a member of this room!', 'warning')
    return redirect(url_for('auth.dashboard'))

# Route to leave a room
@study_room.route('/leave-room/<int:room_id>', methods=['POST'])
@login_required
def leave_room(room_id):
    room = StudyRoom.query.get_or_404(room_id)
    if current_user in room.members:
        room.members.remove(current_user)
        db.session.commit()
        flash('You have left the room!', 'success')
    return redirect(url_for('study_room.view_room', room_id=room.id))
