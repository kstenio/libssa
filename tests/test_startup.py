"""
A basic test to see if the gui starts up properly
"""
from pathlib import Path

import libssa.libssa2 as libssa

def test_startup(qtbot):
    """
    Test if the gui starts up
    """
    root = Path(__file__).parent
    uif = root.joinpath("../", "libssa", "env", "gui", "libssagui.ui")
    lof = root.joinpath("../", "libssa", "pic", "libssa.svg")
    app = libssa.LIBSSA2(uif, lof)
    qtbot.addWidget(app)
