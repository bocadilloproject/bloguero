from tortoise.models import Model
from tortoise import fields


class User(Model):
    # Something to register and authenticate users
    username = fields.CharField(max_length=80)
    email = fields.CharField(max_length=80)
    password = fields.CharField(max_length=80)
    # TODO make every registered user have a record of h/her articles
    post = fields.ForeignKeyField("models.Post", related_name="posts")

    def __str__(self):
        return (self.username, self.email)

class Post(Model):
    title = fields.CharField(max_length=80)
    content = fields.TextField()
    category = fields.ForeignKeyField("models.Category", related_name="posts")

    def __str__(self):
        return self.title


class Category(Model):
    name = fields.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name
