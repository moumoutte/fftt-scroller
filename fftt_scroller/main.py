from fftt_scroller.player import PlayersPagesByClubId
import json

form = PlayersPagesByClubId('http://www.fftt.com/')
players_page = form.submit('12940975')
players = []
for player in players_page:
       print('loading', player.last_name, player.first_name)
       players.append(
            {
         'name': player.last_name + ' ' + player.first_name,
         'rank': player.ranking,
         'progression': player.mounthly_progression,
         'mensuel': player.mounthly_points,
       }
       ) 


final = sorted(players, key=lambda x: x['progression'])
with open('progression.txt', 'w') as fd:
        fd.write(json.dumps(final, indent=4))
