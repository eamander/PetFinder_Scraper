from time import sleep
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common import action_chains
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from requests.exceptions import ConnectionError
import requests
import os
import sys


# Categories are sorted like this. For each category, you have a list which converts to part of the URL:
# breed: [Abyssinian, Chinchilla, Degu, Ferret] -->  breed%5B0%5D=Abyssinian&breed%5B1%5DChinchilla&...
# Notice that the numbers index: ...%5B{}%5D... for each category
# Species and dist, and other single-selection categories are just tacked on to the end:
# &distance=Anywhere&Species=Chinchilla
# Setting Species to Any will remove the selection
# So adding in this functionality just requires a category injection into the URL of the search.
# I think I am going to set that task aside for later since I WANT THESE CATS!

# All this javascript is making it difficult to use requests + BeautifulSoup. I might have to go for
# selenium again, at least to get to the first link I want.


class PetFinderScraper(object):
    def __init__(self, search_term='cats'):
        self.search_term = search_term
        # I want something here to transform bad search terms into good ones
        self.search_url = 'https://www.petfinder.com/search/'+self.search_term+'-for-adoption'
        self.destination_folder = ''
        self.pf_request = None
        self.pf_results = None
        self.scraped_list = []
        self.driver = webdriver.Chrome()
        self.last_site = ''
        self.last_site_file = None

        self.driver.implicitly_wait(8)

    def get_search_results(self):
        """
        Displays search results
        Use this to look at filters
        :return:
        """
        self.driver.get(self.search_url)

    def set_search(self, search_term, filters={}):
        """
        Changes the parameters of the search. Currently this just tries to apply the search term.
        It does not use the filters. These have to be encoded properly into your search term. I have not done this yet
        :param search_term: str
        :param filters: dict

        :return:
        """

        self.search_term = search_term
        self.search_url = 'https://www.petfinder.com/search/'+self.search_term+'-for-adoption'
        if 'state' in filters:
            append = '/us/' + filters['state'] + '/?distance=100'
            self.search_url = self.search_url + append
        if 'page' in filters:
            # This largely doesn't work with selenium. If I could get it to get a url without appending a / on the end
            # it might work.
            append = '/&page=' + str(filters['page'])
            self.search_url = self.search_url + append
        # at this point you would add in the parameters from filters.

    def set_destination_folder(self, path):
        self.destination_folder = path
        self.scraped_list = os.listdir(self.destination_folder)

    def scrape_pictures(self, delay=3):
        """
        Set search terms using pfs.set_search()
        Set destination folder for the images using pfs.set_destination_folder()
        I wanted to save a spot and start over, but it isn't obvious. I only need 4 days of scraping to get
        every cat, so maybe it is NBD and I should not worry about it.
        :param delay: int
            The number of seconds to wait between each pet. This will depend on network usage wherever
            you are

        :return:
        """
        # first thing, open the search:
        # then check to see if anything is written in the last_site.txt
        # self.last_site_file = open(os.path.join(self.destination_folder, 'last_site.txt'), 'r+')
        # self.last_site = self.last_site_file.readline()
        # if self.last_site is not '':
        #     pass
        # else:
        #     # if we are not picking up from where we left off, get the first cat.
        #     # OK this is not going to work. We might just have to bite the bullet and start over every time.
        #     # At least hundreds of new cats are getting added each day?
        #     # We are going to have to click on a cat instead of grabbing a URL
        #     self.last_site =
        next_pet = self.driver.find_element_by_class_name('petCard-overlay-link')
        sleep(delay)
        # next_pet = self.driver.find_element_by_class_name('petCard-link')
        # next_pet.click()
        # sleep(delay)
        # next_pet = self.driver.find_element_by_class_name('petCard-footer-cta')
        next_pet.click()

        sleep(delay)
        # Great! We have begun the search. It is time to get images, loop, and repeat until we are done.
        while next_pet:
            pic_elem_list = self.driver.find_elements_by_class_name('petCarousel-body-slide')
            if len(pic_elem_list) != 0:
                pic_url_list = [pic_elem.get_attribute('src') for pic_elem in pic_elem_list]
                pic_name_list = [url.split('=')[-1] + '.jpg' for url in pic_url_list]
                for i in range(len(pic_name_list)):
                    if not self.check_if_scraped(pic_name_list[i]):
                        try:
                            pic = requests.get(pic_url_list[i]).content
                            f = open(os.path.join(self.destination_folder, pic_name_list[i]), 'wb')
                            f.write(pic)
                            f.close()
                            self.scraped_list.append(pic_name_list[i])
                        except ConnectionError:
                            pass  # Sometimes we just won't get a pic. But there are THOUSANDS of pics.
            # Now all of the pics on that page should be saved. Move on to the next pet!
            try:
                next_pet = self.driver.find_elements_by_class_name('pdpNav-inner-btn')[1]
                next_pet.click()
                sleep(delay)
            except IndexError:
                next_pet = False

    def check_if_scraped(self, img_name):
        if img_name in self.scraped_list:
            return True
        else:
            return False

    def scrape_by_state(self, delay=3):
        """
        This really doesn't work. I can't seem to get the element to be selectable.
        I don't know JavaScript well enough to know what I have to inject to get this to work.
        :param delay:
        :return:
        """
        state_list = ['alabama', 'alaska', 'arizona', 'arkansas', 'california',
                      'colorado', 'connecticut', 'delaware', 'florida', 'georgia',
                      'hawaii', 'idaho', 'illinois', 'indiana', 'iowa', 'kansas',
                      'kentucky', 'louisiana', 'maine', 'maryland', 'massachusetts',
                      'michigan', 'minnesota', 'mississippi', 'missouri', 'montana',
                      'nebraska', 'nevada', 'new-hampshire', 'new-jersey', 'new-mexico',
                      'new-york', 'north-carolina', 'north-dakota', 'ohio', 'oklahoma',
                      'oregon', 'pennsylvania', 'rhode-island', 'south-carolina', 'south-dakota',
                      'tennessee', 'texas', 'utah', 'vermont', 'virginia', 'washington',
                      'west-virginia', 'wisconsin', 'wyoming']
        for state in state_list:
            self.set_search(self.search_term, filters={'state': state})
            self.get_search_results()
            self.scrape_pictures(delay=delay)

    def scrape_many_pages(self, pages, spacing, delay=3):
        """
        Runs a new search starting on every spacing-numbered page. After a certain number of "next pet" clicks,
        PetFinder gives up on letting you see the next pet! This workaround just reinitiates the search at a different
        place.
        Let this run until it errs. You will still get all your pics.
        :param pages: int
            The number of pages to scrape
        :param spacing: int
            The distance in pages between each page
        :param delay: int, float
            the length of time in seconds to delay between various actions in the scrape
        :return:
        """
        for i in range(pages):
            # self.set_search(self.search_term, {'page': i*spacing})
            err2 = True
            while err2:
                try:
                    self.get_search_results()
                    sleep(1)
                    self.get_search_results()  # The site has begun to stop loading the first time I call this.
                    err2 = False
                except TimeoutException:
                    sleep(30)
            for _ in range(i*spacing):
                err = True
                while err:
                    try:
                        rt_btn = self.driver.find_element_by_class_name("m-fieldBtn_iconRt")
                        rt_btn.click()
                        sleep(1)
                        err = False
                        # It is almost always just that the website hasn't fully loaded yet.
                        # So just keep retrying.
                    except (WebDriverException, StaleElementReferenceException, TimeoutException):
                        sleep(delay)
                        self.driver.refresh()

            try:
                self.scrape_pictures(delay=delay)
            except (TimeoutException, WebDriverException, NoSuchElementException):
                # There are plenty of images and we are better off losing some but continuing to scrape
                pass
            # At some point PyCharm forgets where chrome is. I think it is easier to reboot my webdriver.
            self.driver.close()
            self.driver = webdriver.Chrome()
            self.driver.implicitly_wait(8)


def main():
    my_scraper = PetFinderScraper()
    if sys.argv[1]:
        my_scraper.set_destination_folder(sys.argv[1])
    else:
        desired_path = os.path.join(os.curdir, "petfinder_image_data")
        if not os.path.exists(desired_path):
            os.mkdir(desired_path)  # make an image data folder inside the active directory
        my_scraper.set_destination_folder(os.path.join(os.curdir, "petfinder_image_data"))

    # my_scraper.get_search_results()
    my_scraper.scrape_many_pages(2000, 2)


if __name__ == "__main__":
    main()
