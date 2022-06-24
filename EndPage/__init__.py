from otree.api import *
from numpy import random
import numpy as np
import time

doc = """
This app creates the questionnaire and shows end page. 
"""

class Constants(BaseConstants):
    name_in_url = 'EndPage'
    players_per_group = None
    num_rounds = 1

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    # Selected Trial
    partID              = models.StringField()
    iSelectedTrial       = models.IntegerField()
    sSelectedTrialBlock = models.StringField()
    bCorrectBonus        = models.StringField()
    ProlificID          = models.StringField()
    validQ              = models.IntegerField()
    TotalTime           = models.FloatField()
    dTimeOutFocus       = models.FloatField()
    iOutFocus           = models.IntegerField()
    iFSChanges          = models.IntegerField()

# FUNCTIONS

def creating_session(subsession):
    for player in subsession.get_players():
        p = player.participant

# PAGES

class EndPage(Page):

    @staticmethod
    def vars_for_template(player):
        p = player.participant
        iSelectedTrialB1 = p.iSelectedTrialB1
        iSelectedTrialB2 = p.iSelectedTrialB2
        randomTrial = random.choice([True,False])
        if (randomTrial == True):
            p.iSelectedTrial = iSelectedTrialB1
            p.sSelectedTrialBlock = 'Block 1'
            p.bCorrectBonus = p.sCorrB1
        else:
            p.iSelectedTrial = iSelectedTrialB2
            p.sSelectedTrialBlock = 'Block 2'
            p.bCorrectBonus = p.sCorrB2
        
        return {
            'iSelectedTrial' : p.iSelectedTrial,
            'sSelectedTrialBlock' : p.sSelectedTrialBlock,
            'bCorrectBonus' : p.bCorrectBonus,
            'iBonusPayment' : int(10),
            'iBlockTrials' : int(21),
            'iTotalTrials' : int(42),
        }

    @staticmethod
    def before_next_page(player, timeout_happened):
        # Define Participant and other Vars
        part    = player.participant
        start   = part.startTime
        end     = time.time()
        # Save relevant variables

        # Checken of onderstaande nog nodig is
        player.partID           = part.code
        player.ProlificID       = part.label
        player.TotalTime        = end - start
        player.iSelectedTrial    = int(part.iSelectedTrial)
        player.sSelectedTrialBlock    = part.sSelectedTrialBlock
        player.bCorrectBonus    = part.bCorrectBonus
        player.validQ           = part.validQuestionnaire
        player.iFSChanges       = part.iFullscreenChanges
        player.iOutFocus        = part.iOutFocus
        player.dTimeOutFocus    = part.dTimeOutFocus

class FinalPage(Page):
    pass

page_sequence = [EndPage, FinalPage]



