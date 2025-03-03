#
#  JavaScript Restrictor is a browser extension which increases level
#  of security, anonymity and privacy of the user while browsing the
#  internet.
#
#  Copyright (C) 2020  Martin Bednar
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

from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select

from web_browser_type import BrowserType
import values_real
from configuration import get_config


## Browser object represents one browser in which tests run. E.g.: chrome, firefox
#
#  Class Browser contains method definition for creating browser, installing JSR to browser and changing JSR level.
#  Browser object has information about itself - browser type, current jsr level, real tested values of browser etc.
#  Methods are sometimes divided based on browser type - same operations are made differently in different browser.
#  Created browser object offers uniform way how to work with every browser.
class Browser:

    ## manually create testing level for Brave like fingerprinting protection in JSR options
    def define_test_level(self):
        sleep(1)
        self.driver.get(self._jsr_options_page)
        self.driver.find_element_by_id('new_level').click()
        sleep(1)
        self.driver.find_element_by_id('level_text').send_keys("4")
        self.driver.find_element_by_id('level_id').send_keys("4")
        self.driver.find_element_by_id('level_description').send_keys("Brave like protection")
        self.driver.find_element_by_id('time_precision').click()
        select_tpm = Select(self.driver.find_element_by_id("time_precision_precision"))
        select_tpm.select_by_index(1)
        self.driver.find_element_by_id('htmlcanvaselement').click()
        self.driver.find_element_by_id('audiobuffer').click()
        self.driver.find_element_by_id('webgl').click()
        self.driver.find_element_by_id('plugins').click()
        self.driver.find_element_by_id('enumerateDevices').click()
        select_em = Select(self.driver.find_element_by_id("enumerateDevices_method"))
        select_em.select_by_index(1)
        self.driver.find_element_by_id('hardware').click()
        select_hw = Select(self.driver.find_element_by_id("hardware_method"))
        select_hw.select_by_index(1)
        self.driver.find_element_by_id('webworker').click()
        self.driver.find_element_by_id('geolocation').click()
        select_gl = Select(self.driver.find_element_by_id("geolocation_locationObfuscationType"))
        select_gl.select_by_index(3)
        self.driver.find_element_by_id('save').click()

    ## Find URL of JSR option page after JSR was installed to browser.
    def find_options_jsr_page_url(self):
        sleep(1)
        # KNOWN ISSUE: Tab in browser is sometimes not switched by this command.
        # And it leads to error and stopping execution of script. It is driver's issue.
        # Workaround for this issue is wait a while before and after tabs switching.
        self.driver.switch_to.window(self.driver.window_handles[-1])
        sleep(1)
        if self.type == BrowserType.FIREFOX:
            self.driver.get('about:memory')
            self.driver.find_element_by_id('measureButton').click()
            WebDriverWait(self.driver, 10).until(
                ec.presence_of_element_located((By.ID, 'end0'))
            )
            for elem in self.driver.find_elements_by_css_selector(
                    'div#mainDiv div.outputContainer div.sections div.section:first-child > pre.entries > span.kids > '
                    'span.mrName'):
                if 'id=jsr@javascriptrestrictor' in elem.text:
                    self._jsr_options_page = elem.text.split(',')[2].split('=')[1][:-1] + "options.html"
        if self.type == BrowserType.CHROME:
            self.driver.get('chrome://system/')
            WebDriverWait(self.driver, 10).until(
                ec.presence_of_element_located((By.ID, 'extensions-value-btn'))
            )
            for elem in self.driver.find_element_by_id('extensions-value').text.splitlines():
                if 'JavaScript Restrictor' in elem:
                    self._jsr_options_page = "chrome-extension://" + elem.split(':')[0][:-1] + "/options.html"

    ## Create new browser of given type (Chrome, Firefox).
    def __init__(self, type):
        self.type = type
        self.__jsr_level = 2
        self._jsr_options_page = ""
        if type == BrowserType.FIREFOX:
            self.driver = webdriver.Firefox(firefox_profile=webdriver.FirefoxProfile(get_config("firefox_profile")),
                                            executable_path=get_config("firefox_driver"))
            self.real = values_real.init(self.driver)
            self.driver.install_addon(get_config("firefox_jsr_extension"), temporary=True)
            self.find_options_jsr_page_url()
            self.define_test_level()
        elif type == BrowserType.CHROME:
            driver_tmp = webdriver.Chrome(executable_path=get_config("chrome_driver"))
            self.real = values_real.init(driver_tmp)
            sleep(1)
            driver_tmp.quit()
            options = Options()
            options.add_extension(get_config("chrome_jsr_extension"))
            self.driver = webdriver.Chrome(executable_path=get_config("chrome_driver"), options=options)
            self.find_options_jsr_page_url()
            self.define_test_level()

    ## Get current level of JSR in browser.
    @property
    def jsr_level(self):
        return self.__jsr_level

    ## Set current level of JSR in browser.
    #
    # To set JSR level is needed to go to JSR option page and select given default level.
    @jsr_level.setter
    def jsr_level(self, level):
        self.driver.get(self._jsr_options_page)
        self.driver.find_element_by_id('level-' + str(level)).click()
        self.__jsr_level = level
        self.driver.get(get_config("testing_page"))

    ## Quit browser driver, close browser window and delete itself.
    def quit(self):
        self.driver.quit()
        del self
