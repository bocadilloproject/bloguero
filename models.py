from tortoise.models import Model
from tortoise import fields

class User(Model):
	email = fields.charField(max_length=80)
	password = fields.charField(max_length=80)

	def __init__(self, email: str, password: str):
		self.email = email
		self.password = password

	def __str__(self):
		return f'''User is {self.email} {self.password}'''



class Post(Model):
    title = fields.CharField(max_length=80)
    content = fields.TextField()
    category = fields.ForeignKeyField("models.Category", related_name="posts")
    userid = fields.ForeignKeyField("models.User", related_name="posts")

    def __str__(self):
        return self.title


class Category(Model):
    name = fields.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name
