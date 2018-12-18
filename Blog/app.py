import bocadillo
import aiosqlite


api = bocadillo.API()

async with aiosqlite.connect('database.db') as db:
    await db.execute('''
        create table posts if not exists''')
    await db.commit()


@api.route("/")
async def index(req, res):
    res.html = await api.template("index.html")


@api.route("/post")
async def post(req, res):
    res.html = await api.template("post.html")


# Custom error handlers!
@api.error_handler(HTTPError)
def handle_json(req, res, exc):
    res.media = {
        "error": exc.status_phrase,
        "status": exc.status_code,
        "message": "Sorry!",
    }
    res.status_code = exc.status_code


if __name__ == "__main__":
    api.run()