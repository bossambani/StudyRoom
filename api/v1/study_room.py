import os
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Resource, StudyRoom, User
from flask import current_app as app
from app.forms import ResourceForm
from app import db
from api.v1.auth import dashboard

study_room = Blueprint('study_room', __name__)


# List of allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Function to check if the uploaded file has a valid extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route to upload resource
@study_room.route('/study_room/<int:room_id>/upload', methods=['GET', 'POST'])
@login_required
def upload_resource(room_id):
    room = StudyRoom.query.get_or_404(room_id)
    form = ResourceForm()

    if form.validate_on_submit():
        file = form.file.data
        if file and allowed_file(file.filename):  # Check for valid file type
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(f"File is being saved to {filepath}")
            file.save(filepath)

            # Generate URL for the uploaded file
            file_url = url_for('static', filename='uploads/' + filename)

            resource = Resource(
                title=form.title.data,
                link=file_url,  # Store the generated file URL in the database
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
            print("Resource uploaded successfully")
            return redirect(url_for('study_room.view_room', room_id=room.id))

    return render_template('Resource.html', form=form, room=room, user=current_user)


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


def is_room_owner(room):
    return room.owner_id == current_user.id

# Route to view room and manage participants
@study_room.route('/rooms/<int:room_id>', methods=['GET', 'POST'])
@login_required
def view_room(room_id):
    room = StudyRoom.query.get_or_404(room_id)

    if request.method == 'POST':
        if not is_room_owner(room):
            flash('You are not authorized to perform this action!', 'danger')
            return redirect(url_for('study_room.view_room', room_id=room_id))
        
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
        return redirect(url_for('study_room.view_room', room_id=room.id))
    else:
       flash('You are already a member of this room!', 'warning')
    return redirect(url_for('study_room.view_room', room_id=room.id))

# Route to leave a room
@study_room.route('/leave-room/<int:room_id>', methods=['POST'])
@login_required
def leave_room(room_id):
    room = StudyRoom.query.get_or_404(room_id)
    if current_user in room.members:
        room.members.remove(current_user)
        db.session.commit()
        flash('You have left the room!', 'success')
    return redirect(url_for('auth.dashboard', room_id=room.id))

@study_room.route('/delete-room/<int:room_id>', methods=['POST'])
@login_required
def delete_room(room_id):
    room = StudyRoom.query.get_or_404(room_id)

    # Check if the user is the owner of the room
    if not is_room_owner(room):
        flash('You are not authorized to perform this action!', 'danger')
        return redirect(url_for('study_room.view_room', room_id=room_id))
    
    db.session.delete(room)
    db.session.commit()
    flash('Room deleted successfully', 'success')
    return redirect(url_for('auth.dashboard'))

@study_room.route('/resources/<int:room_id>')
@login_required
def view_resources(room_id):
    room = StudyRoom.query.get_or_404(room_id)
    resources = Resource.query.filter_by(room_id=room_id).all()
    return render_template('view_resources.html', resources=resources, room=room, user=current_user)

@study_room.route('/delete-resource/<int:resource_id>', methods=['POST'])
@login_required
def delete_resource(resource_id):
    resource = Resource.query.get_or_404(resource_id)
    room = StudyRoom.query.get_or_404(resource.room_id)

    if not is_room_owner(room):
        flash('You are not authorized to perform this action!', 'danger')
        return redirect(url_for('study_room.view_room', room_id=room.id))
    
    db.session.delete(resource)
    db.session.commit()
    flash('Resource deleted successfully', 'success')
    return redirect(url_for('study_room.view_room', room_id=resource.room_id))