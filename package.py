
name = "flask_log_board"

version = "0.0.1"

description = \
    """
    A flask/jinja-based Dashboard for receiving and viewing logging events.
    """

uuid = "flask-log-board"

build_command = ""

variants = [
    ["platform-linux", "arch-x86_64", "os-Ubuntu-20+"]
]
def commands():
    env.PATH.append("{root}/bin")
    env.PYTHONPATH.append("{root}/python")