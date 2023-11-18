from flask import render_template, flash, redirect, url_for
from flask_login import login_required

from app import db
from app.feedback import feedback
from app.feedback.forms import FeedbackForm
from app.feedback.models import Feedback

@feedback.route('/feedback_list')
@login_required
def feedback_list():
    feedback_list = db.session.query(Feedback).all()
    feedback_form = FeedbackForm()
    return render_template("feedbacks.html", feedback_list=feedback_list, active="ToDo", title="ToDo", feedback_form=feedback_form)

@feedback.route("/add_feedback", methods=["POST"])
def add_feedback():
    feedback_form = FeedbackForm()
    if feedback_form.validate_on_submit():
        username = feedback_form.username.data
        feedback_body = feedback_form.feedback.data

        existing_user = Feedback.query.filter_by(username=username).first()
        if existing_user:
            flash("Username with its own feedback already exists.", category='flash-error')
            return redirect(url_for("feedback.feedback_list"))

        new_feedback = Feedback(username=username, feedback=feedback_body)
        db.session.add(new_feedback)
        db.session.commit()
        flash("Feedback has been successfully added", category='flash-success')
        return redirect(url_for("feedback.feedback_list"))
    flash("Error adding feedback", category='flash-error')
    return redirect(url_for("feedback.feedback_list"))

@feedback.route("/delete_feedback/<int:todo_id>")
@login_required
def delete_feedback(todo_id):
    todo = Feedback.query.get(todo_id)
    db.session.delete(todo)
    db.session.commit()
    flash("Feedback has been successfully deleted", category='flash-success')
    return redirect(url_for("feedback.feedback_list"))
