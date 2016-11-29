#!/usr/bin/python
"""barter_network directory as a module to be imported elsewhere"""

from flask import Flask

# initiating Flask app
app = Flask(__name__)

# specifying system path for module import
import sys
sys.path.append('..')

import barter_network.views
import barter_network.seed
import barter_network.network
import barter_network.model

