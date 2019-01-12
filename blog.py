from bocadillo import API, HTTPError, view
from tortoise import Tortoise
from tortoise.exceptions import DoesNotExist
from models import Post, Category

api = API()

# Database setup.


@api.on("startup")
async def db_init():
    await Tortoise.init(
        db_url="sqlite://db.sqlite", modules={"models": ["models"]}
    )
    await Tortoise.generate_schemas()


@api.on("shutdown")
async def db_cleanup():
    await Tortoise.close_connections()


# Routes.

@api.route("/")
async def home(req, res):
    posts = await Post.all().prefetch_related("category")
    res.html = await api.template("home.html", posts=posts)


@api.route("/new")
class PostCreate:

    async def get(self, req, res):
        # Simple GET request. Display the form page.
        categories = await Category.all()
        res.html = await api.template("post_create.html", categories=categories)

    async def post(self, req, res):
        # Form data was submitted.
        form: dict = await req.form()

        # Get the category object based on the given category name, or
        # create it if it does not exist.
        category = form.pop("category")
        try:
            form["category"] = await Category.get(name=category)
        except DoesNotExist:
            form["category"] = await Category.create(name=category)

        # Create a new post in the database.
        post = Post(**form)
        await post.save()

        # Redirect to the post's detail page.
        api.redirect(name="post_detail", pk=post.id)


@api.route("/{pk:d}")
class PostDetail:
    async def get_or_404(self, pk: int) -> Post:
        try:
            return await Post.get(id=pk).prefetch_related("category")
        except DoesNotExist:
            raise HTTPError(404)

    async def get(self, req, res, pk: int):
        post = await self.get_or_404(pk)
        res.html = await api.template("post_detail.html", post=post)

    async def delete(self, req, res, pk: int):
        post = await self.get_or_404(pk)
        await post.delete()
        res.status_code = 204


if __name__ == "__main__":
    api.run()
