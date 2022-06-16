from email.policy import default
from otree.api import *
import numpy as np
from numpy import random
from random import SystemRandom, sample
from random import choices
import copy
import pandas as pd
import csv

from sqlalchemy import true

doc = """
Should create the buckets with balls for the first code
"""

class Constants(BaseConstants):
    name_in_url         = 'Main-Task'
    ## Colour Sets (Quantities) To be changed according to mail
    lDiffH = [[5,6], [5,12], [8,10], [14, 20], [10,12], [3,5], [6,10]]
    lDiffM = [[5,2], [12,10], [20,3], [10, 3], [7,8], [5,8], [8,10]]
    lDiffL = [[4,2], [6,2], [2,10], [5, 10], [18,5], [11,7], [3,8]]
    lMostValue = [[1,0], [0,1], [1,0], [0,1], [1,0], [0,1], [0,1]]

    lDiff1H, lDiff1M, lDiff1L, lDiff2H, lDiff2M, lDiff2L = ([] for i in range(6))
    for list in lDiffH:
        lDiff1H.append([x*2 for x in list])
        lDiff2H.append([x*3 for x in list])

    for list in lDiffM:
        lDiff1M.append([x*2 for x in list])
        lDiff2M.append([x*3 for x in list])

    for list in lDiffL:
        lDiff1L.append([x*2 for x in list])
        lDiff2L.append([x*3 for x in list])

    lDiffAllH = lDiffH + lDiff1H + lDiff2H
    lDiffAllM = lDiffM + lDiff1M + lDiff2M
    lDiffAllL = lDiffL + lDiff1L + lDiff2L
    lMostValues21 = lMostValue + lMostValue + lMostValue
      
    ## Number of trials
    num_prounds         = 3 # Number of Practice Rounds  
    num_rounds          = 21 + num_prounds # Number of rounds
    players_per_group   = None
    sImagePath          = 'global/figures/'

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    ## Decision Variables
    iDec                = models.IntegerField(blank=True)
    dRT                 = models.FloatField(blank=True)
    ## Attention Variables
    sButtonClick        = models.LongStringField(blank=True)
    sTimeClick          = models.LongStringField(blank=True)
    ## Trial Variables
    iPracticeRound      = models.BooleanField(initial=0)
    iBlock              = models.IntegerField(initial=1)
    iBlockTrial         = models.IntegerField(blank=True)
    sAttrOrder          = models.StringField(blank=True)
    bStartLeft          = models.BooleanField(blank=True)
    dRTbetween          = models.FloatField(blank=True)
    dTime2First         = models.FloatField(blank=True)
    ## Focus Variables
    iFocusLost          = models.IntegerField(blank=True)
    dFocusLostT         = models.FloatField(blank=True)
    iFullscreenChange   = models.IntegerField(blank=True)
    ## Attributes
    Corr0B1                  = models.StringField(blank=True)
    Corr1B1                  = models.StringField(blank=True)               
    Mid0B1                  = models.StringField(blank=True)
    Mid1B1                  = models.StringField(blank=True)
    High0B1                  = models.StringField(blank=True)
    High1B1                  = models.StringField(blank=True)
    Low0B1                  = models.StringField(blank=True)
    Low1B1                  = models.StringField(blank=True)
    ## Bonus trial
    iSelectedTrialB1        = models.IntegerField(blank=True)
    sCorrB1                 = models.StringField(blank=True)

# FUNCTIONS

def creating_session(subsession):
    ## SETUP FOR PARTICIPANT
    if subsession.round_number == 1:
        for player in subsession.get_players():
            p, session = player.participant, subsession.session
            lTreat, lRownames, lCorrB1   = createTreatment()
            p.vRownames         = lRownames
            p.mTreat            = lTreat
            p.lCorrB1           = lCorrB1             
            p.iSelectedTrialB1    = random.choice(range(1,Constants.num_rounds))
            print('Random trial selected for participant from block 1 {}: {}'.format(p.code,p.iSelectedTrialB1))
    ## SETUP FOR PLAYER ROUNDS
    for player in subsession.get_players():
        ## Load participant and save participant variables in player
        p = player.participant
        player.sAttrOrder = p.sAttrOrder = p.vRownames[0] # Order of presentation of attributes, either High or Low
        ## Round Variables
        total_rounds = Constants.num_rounds-Constants.num_prounds
        round = player.round_number-Constants.num_prounds

        if round<1: ## These are practice rounds, random trial selected
            player.iPracticeRound   = 1
            player.iBlockTrial      = random.randint(total_rounds)
            x = int(player.iBlockTrial-1)
        elif (round<=total_rounds): ## These are the trials of the block
            player.iBlockTrial = int(round)
            x = int(round-1)
        
        lAttr = p.mTreat[x]
        lCorr = p.lCorrB1[x]

        ## Randomize if mouse starts on left or right
        player.bStartLeft = random.choice([True,False])
        # Check order of Attributes and save them as player variables
        player.Mid0B1   = str(lAttr[1][0]) # Mid 
        player.Mid1B1   = str(lAttr[1][1])
        player.Corr0B1 = str(lCorr[0])
        player.Corr1B1 = str(lCorr[1])
        if p.vRownames[0]=='Low':
            player.High0B1 = str(lAttr[2][0])
            player.High1B1 = str(lAttr[2][1]) #3
            player.Low0B1 = str(lAttr[0][0]) #4
            player.Low1B1 = str(lAttr[0][1]) #5
        else:
            player.High0B1 = str(lAttr[0][0]) #4
            player.High1B1 = str(lAttr[0][1]) #5
            player.Low0B1 = str(lAttr[2][0])
            player.Low1B1 = str(lAttr[2][1]) #3

# # Functions
# def join2String(list, delimiter= ','):
#         return delimiter.join(map(str,list))

def createTreatment():

    ## Sets
    iSize = int((Constants.num_rounds-Constants.num_prounds))
    
    ## AllDiff
    lDiffAllH = Constants.lDiffAllH
    lDiffAllM = Constants.lDiffAllM
    lDiffAllL = Constants.lDiffAllL
    lMostValues21 = Constants.lMostValues21

    lTreatments = ["" for x in range(iSize)]
    lCorrB1 = ["" for x in range(iSize)]
    lAttr = [] 
    lCorr = []

    # Establish order of qualities
    order = sample(['High','Low'],2)
    leftRightOrder = random.choice([True,False])
    counter = 0
    randomOrder = sample(range(len(lDiffAllH)), len(lDiffAllH))
    for i in randomOrder:
        # Invert order if in this trial outcomes are flipped
        if (leftRightOrder == True):
            high        = copy.copy((lDiffAllH[i]))[::-1]
            low         = copy.copy((lDiffAllL[i]))[::-1]
            mid         = copy.copy((lDiffAllM[i]))[::-1]
            lCorr        = copy.copy((lMostValues21[i]))[::-1]
        else:
            high        = copy.copy((lDiffAllH[i]))
            low         = copy.copy((lDiffAllL[i]))
            mid         = copy.copy((lDiffAllM[i]))
            lCorr        = copy.copy((lMostValues21[i]))

        # Add attributes depending order
        if order[0] == 'High':
            lAttr.append(high)
            lAttr.append(mid)
            lAttr.append(low)
        else: 
            lAttr.append(low)
            lAttr.append(mid)
            lAttr.append(high)
        lTreatments[counter] = lAttr
        lCorrB1[counter] = lCorr
        
        lAttr = []
        lCorr = []
        counter +=1
    
    lAttList = [order[0], 'Mid', order[1]]
    return lTreatments, lAttList, lCorrB1

# PAGES
class Task(Page):
    template_name = 'ecotask/Task.html'

    form_model = 'player'
    form_fields = [
        'iDec', 
        'sButtonClick', 
        'sTimeClick',
        'dRT',
        'sAttrOrder',
        'iFocusLost',
        'dFocusLostT',
        'iFullscreenChange',
        'dTime2First',
    ]

    @staticmethod
    def vars_for_template(player):
        participant = player.participant
        print('Part: {}, trial: {}'.format(participant.label, player.round_number))
        vRownames = participant.vRownames   ## Variable order
        vColours = participant.vColours

        if vRownames[0]=='Low': # Quality
            A00 = player.Low0B1
            A01 = player.Low1B1
            A20 = player.High0B1
            A21 = player.High1B1
            sColourFirst = vColours['sColour3']
            sColourSecond = vColours['sColour2']
            sColourThird = vColours['sColour1']
        else:
            A00 = player.High0B1
            A01 = player.High1B1
            A20 = player.Low0B1
            A21 = player.Low1B1
            sColourFirst = vColours['sColour1']
            sColourSecond = vColours['sColour2']
            sColourThird = vColours['sColour3']
        
        return dict(
            Attr0 = vRownames[0],
            Attr1 = vRownames[1],
            Attr2 = vRownames[2],
            sColour1 = sColourFirst,
            sColour2 = sColourSecond,
            sColour3 = sColourThird,
            A10 = player.Mid0B1,
            A11 = player.Mid1B1,
            A00 = A00,
            A01 = A01,
            A20 = A20,
            A21 = A21,
        ) 

    @staticmethod
    def js_vars(player: Player):
        session = player.session
        p = player.participant
        return {
            'bRequireFS'        : session.config['bRequireFS'],
            'bCheckFocus'       : session.config['bCheckFocus'],
            'iTimeOut'          : session.config['iTimeOut'],
            'dPixelRatio'       : p.dPixelRatio,
        }

    # DEZE NOG AANPASSEN
    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        Corr0B1 = player.Corr0B1
        Corr1B1 = player.Corr1B1
        # Add Focus variables to total if it's not practice trial
        if (player.round_number > Constants.num_prounds):
            participant.iOutFocus = int(participant.iOutFocus) + player.iFocusLost
            participant.iFullscreenChanges = int(participant.iFullscreenChanges) + player.iFullscreenChange
            participant.dTimeOutFocus = float(participant.dTimeOutFocus) + player.dFocusLostT 
        # If this is selected trial, save relevant variables
        if (participant.iSelectedTrialB1==player.round_number):
            if (player.iDec==0):
                if (int(player.Corr1B1) + int(player.iDec) == 1):
                    participant.sCorrB1 = "did"
                elif (int(player.Corr1B1) + int(player.iDec) == 0):
                    participant.sCorrB1 = "did not"
            else:
                if (int(player.Corr1B1) * int(player.iDec) == 1):
                    participant.sCorrB1 = "did"
                elif (int(player.Corr1B1) + int(player.iDec) == 1):
                    participant.sCorrB1 = "did not"
       

class Between(Page):
    template_name = 'ecotask/Between.html'
    form_model = 'player'
    form_fields = [
        'dRTbetween',
    ]
    
    @staticmethod
    def js_vars(player: Player):
        session = player.subsession.session
        p = player.participant
        return {
            'StartLeft'         : player.bStartLeft,
            'bRequireFS'        : session.config['bRequireFS'],
            'bCheckFocus'       : session.config['bCheckFocus'],
            'dPixelRatio'       : p.dPixelRatio,
        }


class Ready(Page):
    template_name = 'ecotask/Ready.html'

    @staticmethod
    def vars_for_template(player: Player):
        # Choose text depending round
        if (player.round_number==1):
            sText = 'Now, you will have '+str(Constants.num_prounds)+' practice rounds. </br> These rounds will not be considered for your final payment.'
        else:
            sText = 'The practice rounds are over. Now, we will continue with the experiment.'
        # Return selected text
        return dict(
            text = sText
        )

    @staticmethod
    def is_displayed(player):
        # Displayed on: First round of each block or first round after the trials
        return (
            (player.round_number==1) or (player.round_number==Constants.num_prounds+1)
        )
        
page_sequence = [Ready, Between, Task]
# page_sequence = [Task]
