#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from flask import Flask, render_template
from flask_socketio import SocketIO
from pprint import pprint

import logging

from log2sql import DB, entities

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask("log-board")
app.config.update(
    {
        "DEBUG": True,
        "SECRET_KEY": "magnetic-lab"
    })
socketio = SocketIO(app)
DB.log_level = logging.DEBUG
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#
@app.route('/')
def index():
    db = DB()
    db.connect()
    template = render_template(
        'pages/home.html',
        # TODO: need filter here to only grab certain amount
        log_events = db.query(entities.LoggingEvent).all()
    )
    db.disconnect()
    return template

@socketio.on("logging_event")
def handle_logging_event(data):
    db = DB()
    db.connect()
    log_record, username = data.values()
    db.submit_new_logging_event(log_record, username)
    db.disconnect()

# Error handlers.
@socketio.on_error()        # Handles the default namespace
def error_handler(e):
    pprint("ERROR HANDLER RAN")
    pprint(e)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    socketio.run(app, debug=True)

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
