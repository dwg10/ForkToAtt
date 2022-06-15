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
    # # Quality and Sustainability ranges
    # Q1      = 60
    # Q_step  = 10
    # S1      = 0
    # S2_2    = 15
    # S2_3    = 5
    # S3      = 10
    # S_step  = 10
    # Others
    # dBeliefBonus = 0.1
    ProlificLink = "https://app.prolific.co/submissions/complete?cc=1EA38881" ## Nog te veranderen!
    # Slides = [
    #     dict(
    #         Title = 'Results',
    #         path='EndPage/slide0.html',
    #         ),
    #     dict(
    #         Title = 'Results',
    #         path='EndPage/slide1.html',
    #         ),        
    # ]

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    # Selected Trial
    partID              = models.StringField()
    iCorrectB1          = models.IntegerField()
    iCorrectB2          = models.IntegerField()
    iCorrectTotal          = models.IntegerField()
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
        # p.qRandom = 5*(random.randint(0,3))
        # p.sRandom = 5*(random.randint(0,3))

# PAGES

class EndPage(Page):

    @staticmethod
    def vars_for_template(player):
        p = player.participant
        p.iCorrectB1 = p.iTest1
        p.iCorrectB2 = p.iTest2
        p.iCorrectTotal = int(p.iCorrectB1) + int(p.iCorrectB2)
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
        # ## Determining Value of Sustainability rating
        # S = int(participant.S)
        # T = int(participant.iTreatment)
        # Q = int(participant.Q)
        # print("Treatment {} Sustainability {}".format(T,S))
        # if (T==1):
        #     print('Treatment 1')
        #     Smin = Constants.S1 + S*Constants.S_step 
        # elif (S==1 & T==2):
        #     print('Treatment 2')
        #     Smin = Constants.S2_2 
        #     print(Smin)
        # elif (S==1 & T==3):
        #     print('Treatment 3')
        #     Smin = Constants.S2_3
        # else: 
        #     print('Treatment 4')
        #     Smin = Constants.S1 + S*Constants.S_step 

        # Svalue = (Smin + participant.sRandom)/10
        # ## Determining value of Quality rating
        # Qvalue =  (Constants.Q1 + Q*Constants.Q_step + participant.qRandom)/20
        # dBeliefBonus = np.round(participant.iCorrectBeliefs*Constants.dBeliefBonus,1)
        # participant.Bonus = Qvalue - float(participant.Price) + dBeliefBonus
        # participant.TreeAmount = Svalue
        # S_rounded  = int(np.ceil(Svalue))
        
        return {
            'iCorrectB1' : p.iCorrectB1,
            'iCorrectB2' : p.iCorrectB2,
            'iCorrectTotal' : p.iCorrectTotal,
            'iSelectedTrial' : p.iSelectedTrial,
            'sSelectedTrialBlock' : p.sSelectedTrialBlock,
            'bCorrectBonus' : p.sCorr,
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
        player.iCorrectB1    = int(part.iCorrectB1)
        player.iCorrectB2    = int(part.iCorrectB2)
        player.iCorrectTotal    = int(part.iCorrectTotal)
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



