from sanic import Sanic
from sanic.config import Config

from routes import bp


config = Config()


app = Sanic(__name__)
app.blueprint(bp)

app.ctx.white_list = config.get('WHITE_LIST', '').split(',')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, auto_reload=True)
