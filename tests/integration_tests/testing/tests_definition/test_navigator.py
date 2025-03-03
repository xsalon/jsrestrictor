#
#  JavaScript Restrictor is a browser extension which increases level
#  of security, anonymity and privacy of the user while browsing the
#  internet.
#
#  Copyright (C) 2020  Martin Bednar
#  Copyright (C) 2021  Matus Svancar
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import pytest

from values_getters import get_navigator


## Setup method - it is run before navigator tests execution starts.
#
#  This setup method initialize variable navigator that contains current data about navigator and
#  this variable is provided to navigator tests and values in device variable are compared with expected values.
@pytest.fixture(scope='module', autouse=True)
def navigator(browser):
    return get_navigator(browser.driver)


## Test user agent.
def test_user_agent(browser, navigator, expected):
    if expected.navigator.userAgent[browser.type] == 'REAL VALUE':
        assert navigator['userAgent'] == browser.real.navigator.userAgent
    else:
        assert navigator['userAgent'] == expected.navigator.userAgent[browser.type]


## Test app version.
def test_app_version(browser, navigator, expected):
    if expected.navigator.appVersion == 'REAL VALUE':
        assert navigator['appVersion'] == browser.real.navigator.appVersion
    else:
        assert navigator['appVersion'] == expected.navigator.appVersion


## Test platform.
def test_platform(browser, navigator, expected):
    if expected.navigator.platform == 'REAL VALUE':
        assert navigator['platform'] == browser.real.navigator.platform
    else:
        assert navigator['platform'] == expected.navigator.platform


## Test vendor.
def test_vendor(browser, navigator, expected):
    if expected.navigator.vendor[browser.type] == 'REAL VALUE':
        assert navigator['vendor'] == browser.real.navigator.vendor
    else:
        assert navigator['vendor'] == expected.navigator.vendor[browser.type]


## Test language.
def test_language(browser, navigator, expected):
    if expected.navigator.language == 'REAL VALUE':
        assert navigator['language'] == browser.real.navigator.language
    else:
        assert navigator['language'] == expected.navigator.language


## Test languages.
def test_languages(browser, navigator, expected):
    if expected.navigator.languages == 'REAL VALUE':
        assert navigator['languages'] == browser.real.navigator.languages
    else:
        assert navigator['languages'] == expected.navigator.languages


## Test cookie enabled.
def test_cookie_enabled(browser, navigator, expected):
    if expected.navigator.cookieEnabled == 'REAL VALUE':
        assert navigator['cookieEnabled'] == browser.real.navigator.cookieEnabled
    else:
        assert navigator['cookieEnabled'] == expected.navigator.cookieEnabled


## Test doNotTrack flag.
def test_do_not_track(browser, navigator, expected):
    if expected.navigator.doNotTrack == 'REAL VALUE':
        assert navigator['doNotTrack'] == browser.real.navigator.doNotTrack
    else:
        assert navigator['doNotTrack'] == expected.navigator.doNotTrack


## Test oscpu
def test_oscpu(browser, navigator, expected):
    if expected.navigator.oscpu == 'REAL VALUE':
        assert navigator['oscpu'] == browser.real.navigator.oscpu
    else:
        assert navigator['oscpu'] == expected.navigator.oscpu

## Test plugins
def test_plugins(browser, navigator, expected):
    if expected.navigator.plugins == 'SPOOF VALUE':
        assert navigator['plugins'] != browser.real.navigator.plugins
    else:
        assert navigator['plugins'] == browser.real.navigator.plugins

## Test mimeTypes
def test_mime_types(browser, navigator, expected):
    if expected.navigator.mimeTypes == 'SPOOF VALUE':
        if navigator['mimeTypes'] == browser.real.navigator.mimeTypes:
            assert navigator['mimeTypes'] == []
        else:
            assert True
    else:
        assert navigator['mimeTypes'] == browser.real.navigator.mimeTypes
