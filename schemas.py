from marshmallow import Schema, fields

class TasksSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, load_only = True)
    is_completed = fields.Boolean(dump_only = True)
    email = fields.Str(required = True)

class SingleTaskSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    is_completed = fields.Boolean(dump_only = True)
    email = fields.Str(required = True)

class TaskUpdateSchema(Schema):
    title = fields.Str()
    is_completed = fields.Boolean()
    
class ErrorSchema(Schema):
    error = fields.String(required=True)

class AllTasksSchema(SingleTaskSchema):
    tasks = fields.List(fields.Nested(SingleTaskSchema()))

class UserSchema(Schema):
    id = fields.Int(dump_only=True) #dump-only = True means we only expect this on output not input
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True) #load_only = True means we don't show this on output
    quote = fields.Str(required = True)

class UserLoginSchema(Schema):
    username = fields.Str(required = True)
    password = fields.Str(required = True, load_only = True)