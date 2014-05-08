#-*- coding: utf-8 -*-
from lxml import html 

from fftt_scroller.pages import format_get_data
from fftt_scroller.constants import MALE, FEMALE

class NoNextPageFound(Exception):
    pass



class PlayerPage:

  def __init__(self, url):
     self.root = html.parse(url)
     full_name = self.root.xpath('/html/body/div[1]//b')[0].text.rstrip().lstrip()
     names = full_name.split(' ')
     self.first_name = names[0]
     self.last_name = names[-1]


  @property
  def ranking(self):
      html_node = self.root.xpath('/html/body/dd/div[2]//tr[5]/td[2]')[0]
      return int(html_node.text)


  @property
  def official_points(self):
      html_node = self.root.xpath('/html/body/dd/div[2]//tr[5]/td[4]')[0]
      return int(html_node.text)


  @property
  def mounthly_points(self):
      html_node = self.root.xpath('(/html/body/div)[3]//td[2]')[0]
      return int(html_node.text)
         

  @property
  def mounthly_progression(self):
      html_node = self.root.xpath('(/html/body/div)[3]//td[4]')[0]
      return float(html_node.text)



   
class PlayersListPage:

    def __init__(self, url):
        self.url = url
        self.root = html.parse(url)


    def __iter__(self):
        pass


    def next(self):
        try:
            node = self.root.xpath('/html/body/center[3]//td[last()]/a')[0]
        except IndexError:
            raise NoNextPageFound()

        base, _ = self.url.rsplit('/', 1)
        next_url = '{}/{}'.format(base, node.attrib['href'])
        return PlayersListPage(next_url)
        
            



class FormPage:

    def __init__(self, url):
        self.url = url
        self.root = html.parse(url)


    def submit(self, **kwargs):
        form = self.get_form()
        final_url = form.action + format_get_data(cler=self.cler, **kwargs)
        return self.class_result(final_url)


        
    def get_form(self):
        return self.root.xpath('//form')[0]



    # ahah :)
    @property
    def cler(self):
        return self.root.xpath('//input[@name="cler"]')[0].value



class AskingPlayersPage(FormPage):


    _url_path = 'sportif/pclassement/php3/FFTTfo.php3'



    def __init__(self, base_uri):
        self.base_uri = '{0}/{1}'.format(base_uri, self.url_path)
        super(AskingPlayersPage, self).__init__(self.base_uri)


    @property
    def url_path(self):
        return '{}{}'.format(self._url_path, format_get_data(**self.data))
        


class PlayerPageByLicence(AskingPlayersPage):

    data = {'Menu': 'J2'}

    class_result = PlayerPage


    def submit(self, licence, sex=MALE):
        return super(PlayerPageByLicence, self).submit(precision=licence, reqid=sex)



class PlayersPagesByClubId(AskingPlayersPage):

    data = {'Menu': 'J3'}

    class_result = PlayersListPage

    sex_mapping = {
      'f': 311,
      'm': 211
    }

    def submit(self, club_id, sex='m'):
        reqid = self.sex_mapping[sex]
        return super(PlayersPagesByClubId, self).submit(precision=club_id, reqid=reqid)




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
