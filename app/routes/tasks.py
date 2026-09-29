from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import Task

tasks_bp = Blueprint("task", __name__)

@tasks_bp.route("/")
def view_task() :
    if "user" not in session:
        return redirect(url_for("auth.login"))

    tasks = Task.query.all()
    return render_template("task.html", tasks=tasks)

@tasks_bp.route("/add", methods=["POST"])
def add_task() :
    if "user" not in session :
        return redirect(url_for("auth.login"))

    title = request.form.get("title")
    if title :
        new_task = Task(title=title, status = "pending")
        db.session.add(new_task)
        db.session.commit()
        flash("Task added successfully", "success")
    return redirect(url_for("task.view_task"))

@tasks_bp.route("/toggle/<int:task_id>", methods=["POST"])
def toggle_status(task_id):
    if "user" not in session:
        return redirect(url_for("auth.login"))
    task = Task.query.get_or_404(task_id)
    if task :
        if task.status == "pending" :
            task.status = "working"
        elif task.status == "working" :
            task.status = "Done"
        else :
            task.status = "pending"
        db.session.commit()
        flash("Task status updated!", "success")
    return redirect(url_for("task.view_task"))

@tasks_bp.route("/clear", methods=["POST"])
def clear_task():
    Task.query.delete()
    db.session.commit()
    flash("all tasks cleared!", "info")
    return redirect(url_for("task.view_task"))