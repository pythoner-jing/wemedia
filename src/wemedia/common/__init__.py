# -*- coding: utf-8 -*-

from flask import Blueprint

Common = Blueprint('Common', __name__, static_folder='static')

import views
import models