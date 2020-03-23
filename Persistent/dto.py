# Data Transfer Objects:
class match:
    def __init__(self,match_id,leauge,date,
        home_team_name,away_team_name,
        home_team_rank,away_team_rank,
        home_team_scored,away_team_scored,
        home_team_received,away_team_received,
        home_att,away_att,
        home_def,away_def,
        home_mid,away_mid,
        home_odds_n,draw_odds_n,away_odds_n,
        result=None):

        self.match_id=match_id
        self.league=leauge
        self.date=date
        self.home_team_name=home_team_name
        self.away_team_name=away_team_name
        self.home_team_rank=home_team_rank
        self.away_team_rank=away_team_rank
        self.home_team_scored=home_team_scored
        self.away_team_scored=away_team_scored
        self.home_team_received=home_team_received
        self.away_team_received=away_team_received
        self.home_att=home_att
        self.away_att=away_att
        self.home_def=home_def
        self.away_def=away_def
        self.home_mid=home_mid
        self.away_mid=away_mid
        self.home_odds_n=home_odds_n
        self.draw_odds_n=draw_odds_n
        self.away_odds_n=away_odds_n
        self.result=result

class match_odds:
    def __init__(self,match_id,home_odds,draw_odds,away_odds,home_odds_plus1,away_odds_plus1):
        self.match_id=match_id
        self.home_odds=home_odds
        self.draw_odds=draw_odds
        self.away_odds=away_odds
        self.home_odds_plus1=home_odds_plus1
        self.away_odds_plus1=away_odds_plus1