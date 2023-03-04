from sanic import Blueprint
from .telnyx import bp as telnyx_bp

bp = Blueprint.group(telnyx_bp)
