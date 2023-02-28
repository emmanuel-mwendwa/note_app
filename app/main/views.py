from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from . import main
from .forms import AddNoteForm, EditNoteForm
from .. import db
from ..models import Note, User

@main.route('/home', methods=["GET", "POST"])
@main.route('/', methods=["GET", "POST"])
@login_required
def index():
    form = AddNoteForm()
    if form.validate_on_submit():
        new_note = Note(data=request.form.get('note'), user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()
        return redirect(url_for('main.index'))
    
    return render_template('index.html', form=form)


@main.route('/<int:note_id>/edit', methods=["GET", "POST"])
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)
    form = EditNoteForm()

    if form.validate_on_submit():
        note.data = form.note.data
        # Update Database
        db.session.add(note)
        db.session.commit()
        flash("Note has been updated", category='success')
        return redirect(url_for('main.index'))
    return render_template('edit_note.html', form=form, note=note)

@main.route('/<int:note_id>/delete', methods=["POST"])
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('main.index'))