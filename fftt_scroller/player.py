#-*- coding: utf-8 -*-
from lxml import html 

from fftt_scroller.pages import format_get_data

class FormPage:

    def __init__(self, url):
        self.url = url
        self.root = html.parse(url)


    def submit(self, **kwargs):
        form = self.get_form()
        final_url = form.action + format_get_data(cler=self.cler, **kwargs)
        return html.parse(final_url)


        
    def get_form(self):
        return self.root.xpath('//form')[0]



    # ahah :)
    @property
    def cler(self):
        return self.root.xpath('//input[@name="cler"]')[0].value



class AskingPlayerPage(FormPage):

    _url_path = 'sportif/pclassement/php3/FFTTfo.php3'



    def __init__(self, base_uri):
        self.base_uri = '{0}/{1}'.format(base_uri, self.url_path)
        super(AskingPlayerPage, self).__init__(self.base_uri)


    @property
    def url_path(self):
        return '{}?{}'.format(self._url_path, format_get_data(**self.data))
        


class PlayerPageByLicence(AskingPlayerPage):

    data = {'Menu': 'J2'}


    def submit(self, licence, sex=MALE):
        return super(PlayerPageByLicence, self).submit(precision=licence, reqid=sex)






class Player:

    def __init__(self, name, licence, club, category, ranking, mounthly_points, mounthly_progression):

        self.name = name
        self.licence = licence
        self.club = club
        self.category = category
        self.ranking = ranking
        self.mounthly_points = mounthly_points
        self.mounthly_progression = mounthly_progression


    @classmethod
    def from_page(cls, url):
        pass
