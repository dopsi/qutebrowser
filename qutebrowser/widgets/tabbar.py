# Copyright 2014 Florian Bruhin (The Compiler) <mail@qutebrowser.org>
#
# This file is part of qutebrowser.
#
# qutebrowser is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# qutebrowser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with qutebrowser.  If not, see <http://www.gnu.org/licenses/>.

"""The tab widget used for TabbedBrowser from browser.py."""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTabWidget, QTabBar, QSizePolicy

import qutebrowser.utils.config as config
from qutebrowser.utils.style import Style


class TabWidget(QTabWidget):

    """The tabwidget used for TabbedBrowser."""

    # FIXME there is still some ugly 1px white stripe from somewhere if we do
    # background-color: grey for QTabBar...

    _stylesheet = """
        QTabWidget::pane {{
            position: absolute;
            top: 0px;
        }}

        QTabBar {{
            {font[tabbar]}
        }}

        QTabBar::tab {{
            {color[tab.bg]}
            {color[tab.fg]}
            padding-left: 5px;
            padding-right: 5px;
            padding-top: 0px;
            padding-bottom: 0px;
        }}

        QTabBar::tab:first, QTabBar::tab:middle {{
            border-right: 1px solid {color[tab.seperator]};
        }}

        QTabBar::tab:selected {{
            {color[tab.bg.selected]}
        }}
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setStyle(Style(self.style()))
        self.setStyleSheet(config.get_stylesheet(self._stylesheet))
        self.setDocumentMode(True)
        self.setElideMode(Qt.ElideRight)
        self._init_config()

    def _init_config(self):
        """Initialize attributes based on the config."""
        position_conv = {
            'north': QTabWidget.North,
            'south': QTabWidget.South,
            'west': QTabWidget.West,
            'east': QTabWidget.East,
        }
        select_conv = {
            'left': QTabBar.SelectLeftTab,
            'right': QTabBar.SelectRightTab,
            'previous': QTabBar.SelectPreviousTab,
        }
        # pylint: disable=maybe-no-member
        self.setMovable(config.config.getboolean('tabbar', 'movable'))
        self.setTabsClosable(config.config.getboolean('tabbar',
                                                      'closebuttons'))
        self.setUsesScrollButtons(config.config.getboolean('tabbar',
                                                           'scrollbuttons'))
        posstr = config.config.get('tabbar', 'position').lower()
        selstr = config.config.get('tabbar', 'select_on_remove').lower()
        try:
            self.setTabPosition(position_conv[posstr])
            self.tabBar().setSelectionBehaviorOnRemove(select_conv[selstr])
        except KeyError:
            pass
