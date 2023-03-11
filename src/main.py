import os

from sanic import Sanic
from sanic.log import logger
from sanic.response import text

from views import bp


app = Sanic(__name__)

app.blueprint(bp)


@app.get("/")
async def homepage(request):
    logger.debug("Debug is turned on.")
    return text("OK")


if __name__ == "__main__":
    debug = os.getenv("DEBUG", "").lower() in ("true", "t", "yes", "y", "on")
    app.run(host="0.0.0.0", debug=debug, auto_reload=debug, fast=not debug)
