from bs4 import BeautifulSoup as bs
import requests

class WebScraper:
    """A simple class for web scraping tasks using BeautifulSoup."""
    def __init__(self, url):
        """
        Initialize the WebScraper object with the provided URL.

        Args:
            url (str): The URL of the web page to scrape.
        """

        self.url = url
        self.content = self.get_page_content()

    def get_content(self):
        """
        Fetch the content of the web page using the provided URL.

        Returns:
            bytes or None: The content of the web page as bytes, or None if there was an error.
        """
        response = requests.get(self.url)
        if response.status_code == 200:
            return response.content
        else:
            print("Error: Unable to retrieve page content.")
            return None

    def get_soup(self):
        """
        Parse the fetched page content using BeautifulSoup and return a BeautifulSoup object.

        Returns:
            BeautifulSoup or None: The BeautifulSoup object representing the parsed HTML, or None if there was an error.
        """

        if self.content:
            return BeautifulSoup(self.content, 'lxml')
        else:
            print("Error: Unable to create BeautifulSoup object. Page content is missing.")
            return None

    def find_elements(self, tag, class_=None):
        # soup = self.get_soup()
        # if soup:
        #     if class_:
        #         return soup.find_all(tag, class_=class_)
        #     else:
        #         return soup.find_all(tag)
        # else:
        #     return None
        pass

    def find_element(self, tag, class_=None):
        # soup = self.get_soup()
        # if soup:
        #     if class_:
        #         return soup.find(tag, class_=class_)
        #     else:
        #         return soup.find(tag)
        # else:
        #     return None
        pass

