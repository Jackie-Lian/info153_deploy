from flask import request, url_for
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models import TasksModel
from schemas import TasksSchema, SingleTaskSchema, AllTasksSchema, TaskUpdateSchema, ErrorSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

import os
import requests
from flask import current_app
from tasks import send_simple_message


# def send_simple_message():
# 	return requests.post(
# 		"https://api.mailgun.net/v3/YOUR_DOMAIN_NAME/messages",
# 		auth=("api", "YOUR_API_KEY"),
# 		data={"from": "Excited User <mailgun@YOUR_DOMAIN_NAME>",
# 			"to": ["bar@example.com", "YOU@YOUR_DOMAIN_NAME"],
# 			"subject": "Hello",
# 			"text": "Testing some Mailgun awesomeness!"})

blp = Blueprint("tasks", __name__, description="Task APIs")

@blp.route("/v1/task")
class Task(MethodView):
    @blp.arguments(TasksSchema)
    @blp.response(200, SingleTaskSchema)
    def post(self, tasks_data):
        task = TasksModel(**tasks_data) 

        try:
            db.session.add(task)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Error occured while inserting a new task")

        return task, 201


@blp.route("/v1/tasks")
class Tasks(MethodView):
    @blp.response(200, AllTasksSchema)
    def get(self):
        output = TasksModel.query.all()
        return {"tasks": output}
    
    # @blp.arguemnts(200, AllTasksSchema)
    def post(self):
        tasks_list = request.get_json()["tasks"]
        output = []
        try:
            for task_data in tasks_list:
                task = TasksModel(**task_data) 
                db.session.add(task)
                db.session.commit()
                output.append({"id": task.id, "is_completed": task.is_completed})
            return {"tasks": output}, 201
        except Exception:
            abort(400, message="Error occurred when bulk adding.")
    
    def delete(self):
        tasks_list = request.get_json()["tasks"]
        try: 
            for task_dic in tasks_list:
                task_id = task_dic["id"]
                task = TasksModel.query.get(task_id)
                db.session.delete(task)
                db.session.commit()
        except Exception:
            return '', 204
        return '', 204

@blp.route("/v1/tasks/<string:task_id>")
class Tasks(MethodView):
    @blp.response(200, SingleTaskSchema)
    def get(self, task_id):
        # task = TasksModel.query.get_or_404(task_id)
        # try:
        task = TasksModel.query.get(task_id)
        if not task:
            # abort with 404 and custom error message
            # return {
            #     "error": "There is no task at that id"
            # }
            abort(404, message="There is no task at that id")
        else:
            return task
    
    def delete(self, task_id):
        task = TasksModel.query.get(task_id)
        try: 
            db.session.delete(task)
            db.session.commit()
        except Exception:
            return '', 204
        return '', 204
    
    @blp.arguments(TaskUpdateSchema)
    def put(self, task_data, task_id):
        task = TasksModel.query.get(task_id)
        if task:
            if "title" in task_data:
                task.title = task_data["title"]
            if "is_completed" in task_data:
                task.is_completed = task_data["is_completed"]
                if task.is_completed:
                    current_app.queue.enqueue(send_simple_message, task.email, task.title)

        else:
            return {"error": "There is no task at that id"}, 404
        try:
            db.session.add(task)
            db.session.commit()
            return '', 204
        except SQLAlchemyError:
            abort(500, message="Error occured while updating item")
            

        

# class TasksList(MethodView):
    

                # # Create an instance of the Task class
                # task_instance = Task()
                # # Call the post method directly
                # schema = TasksSchema()
                # validated_data = schema.load(task_data)
                # response, status_code = task_instance.post(validated_data)
                # print(response)
                # output.append(response)