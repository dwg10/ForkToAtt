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
    name_in_url         = 'Main-Task2'
    ## Colour Sets (Quantities) To be changed according to mail
    lDiffACH = [[5,6], [5,12], [8,10], [14, 20], [10,12], [3,5], [6,10]]
    lDiffACM = [[5,2], [12,10], [20,3], [10, 3], [7,8], [5,8], [8,10]]
    lDiffACL = [[4,2], [6,2], [2,10], [5, 10], [18,5], [11,7], [3,8]]
    lMostValue = [[1,0], [0,1], [1,0], [0,1], [1,0], [0,1], [0,1]]
    
    # NL, L, NL, L, NL, L, L
    # L, R, L, R, L, R, R

    lDiff1ACH, lDiff1ACM, lDiff1ACL, lDiff2ACH, lDiff2ACM, lDiff2ACL = ([] for i in range(6))
    for list in lDiffACH:
        lDiff1ACH.append([x*2 for x in list])
        lDiff2ACH.append([x*3 for x in list])

    for list in lDiffACM:
        lDiff1ACM.append([x*2 for x in list])
        lDiff2ACM.append([x*3 for x in list])

    for list in lDiffACL:
        lDiff1ACL.append([x*2 for x in list])
        lDiff2ACL.append([x*3 for x in list])

    lDiffAllACH = lDiffACH + lDiff1ACH + lDiff2ACH
    lDiffAllACM = lDiffACM + lDiff1ACM + lDiff2ACM
    lDiffAllACL = lDiffACL + lDiff1ACL + lDiff2ACL
    lMostValues21 = lMostValue + lMostValue + lMostValue
      
    ## Number of trials
    # num_reps            = 1 # number of repetitions per permutation
    # num_repsEq          = 2 # Number of cases with equal sustainability
    num_prounds         = 0 # Number of Practice Rounds  
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
    # iTest2              = models.IntegerField(blank=True)
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
    Corr0B2                  = models.StringField(blank=True)
    Corr1B2                  = models.StringField(blank=True)   
    Mid0B2                  = models.StringField(blank=True)
    Mid1B2                  = models.StringField(blank=True)
    High0B2                 = models.StringField(blank=True)
    High1B2                 = models.StringField(blank=True)
    Low0B2                  = models.StringField(blank=True)
    Low1B2                  = models.StringField(blank=True)
    ## Bonus trial
    iSelectedTrialB2        = models.IntegerField(blank=True)
    sCorrB2                 = models.StringField(blank=True)

# FUNCTIONS

def creating_session(subsession):
    ## SETUP FOR PARTICIPANT
    if subsession.round_number == 1:
        for player in subsession.get_players():
            p, session = player.participant, subsession.session
            iTreatment = p.iTreatment
            vRownames = p.vRownames
            lTreat, lCorrB2 = createTreatment(iTreatment, vRownames)
            # p.vRownames         = lRownames
            p.mTreat              = lTreat      
            p.lCorrB2             = lCorrB2             
            p.iSelectedTrialB2     = random.choice(range(Constants.num_prounds+1,Constants.num_rounds))
            print('Random trial selected for participant from block 2 {}: {}'.format(p.code,p.iSelectedTrialB2))

            # Select either trial from Block 1 or 2 randomly

    ## SETUP FOR PLAYER ROUNDS
    for player in subsession.get_players():
        ## Load participant and save participant variables in player
        p = player.participant
        player.sAttrOrder = p.sAttrOrder = p.vRownames[0] # Used to be 1 # Order of presentation of attributes. 1st attribute always price, then Q or S
        ## Round Variables
        total_rounds = Constants.num_rounds-Constants.num_prounds
        round = player.round_number-Constants.num_prounds

        if round<1: ## These are practice rounds, random trial selected
            player.iPracticeRound   = 1
            player.iBlockTrial      = random.randint(total_rounds)
            x = int( player.iBlockTrial-1)
        elif (round<=total_rounds): ## These are the trials of the block
            player.iBlockTrial = int(round)
            x = int(round-1)
        
        lAttr = p.mTreat[x]
        lCorr = p.lCorrB2[x]

        ## Randomize if mouse starts on left or right
        player.bStartLeft = random.choice([True,False])
        # Check order of Attributes and save them as player variables
        # DEZE QUA NAAM (Mid0 ENZO) VERANDEREN
        player.Mid0B2   = str(lAttr[1][0]) # Mid, Q is High, S is Low
        player.Mid1B2   = str(lAttr[1][1])
        player.Corr0B2 = str(lCorr[0])
        player.Corr1B2 = str(lCorr[1])
        if p.vRownames[0]=='Low':
            player.High0B2 = str(lAttr[2][0])
            player.High1B2 = str(lAttr[2][1]) #3
            player.Low0B2 = str(lAttr[0][0]) #4
            player.Low1B2 = str(lAttr[0][1]) #5
        else:
            player.High0B2 = str(lAttr[0][0]) #4
            player.High1B2 = str(lAttr[0][1]) #5
            player.Low0B2 = str(lAttr[2][0])
            player.Low1B2 = str(lAttr[2][1]) #3

# # Functions
# def join2String(list, delimiter= ','):
#         return delimiter.join(map(str,list))

def createTreatment(trNumber, vRow):
    ## Sets
    iSize = int((Constants.num_rounds-Constants.num_prounds))

    ## AllDiff
    lDiffAllACH = Constants.lDiffAllACH
    lDiffAllACM = Constants.lDiffAllACM
    lDiffAllACL = Constants.lDiffAllACL
    lMostValues21 = Constants.lMostValues21

    lTreatments = ["" for x in range(iSize)] # Initialiseren variabelen
    lCorrB2 = ["" for x in range(iSize)]
    lAttr = [] # DIT ZELF TOEGEVOEGD
    lCorr = []

    # Establish order of qualities
    # order = sample(['High','Low'],2) # Neem order van block 1
    leftRightOrder = random.choice([True,False])
    counter = 0
    randomOrder = sample(range(len(lDiffAllACH)), len(lDiffAllACH))
    for i in randomOrder:
        # Invert order (Left - Right) if in this trial outcomes are flipped
        if ((leftRightOrder == True) & (trNumber == 1)):
            high        = copy.copy((lDiffAllACH[i]))[::-1]
            low         = copy.copy((lDiffAllACL[i]))[::-1]
            mid         = copy.copy((lDiffAllACM[i]))[::-1]
            lCorr        = copy.copy((lMostValues21[i]))[::-1]
        elif ((leftRightOrder == True) & (trNumber == 2)):
            high        = copy.copy((lDiffAllACH[i]))[::-1]
            low         = copy.copy((lDiffAllACL[i]))[::-1]
            mid         = copy.copy((lDiffAllACM[i]))[::-1]
            lCorr        = copy.copy((lMostValues21[i]))[::-1]
        elif ((leftRightOrder == True) & (trNumber == 3)):
            high        = copy.copy((lDiffAllACM[i]))[::-1]
            low         = copy.copy((lDiffAllACL[i]))[::-1]
            mid         = copy.copy((lDiffAllACH[i]))[::-1]
            lCorr        = copy.copy((lMostValues21[i]))[::-1]
        elif ((leftRightOrder == True) & (trNumber == 4)):
            high        = copy.copy((lDiffAllACH[i]))[::-1]
            low         = copy.copy((lDiffAllACM[i]))[::-1]
            mid         = copy.copy((lDiffAllACL[i]))[::-1]
            lCorr        = copy.copy((lMostValues21[i]))[::-1]
        elif ((leftRightOrder == False) & (trNumber == 1)):
            high        = copy.copy((lDiffAllACH[i]))
            low         = copy.copy((lDiffAllACL[i]))
            mid         = copy.copy((lDiffAllACM[i]))
            lCorr        = copy.copy((lMostValues21[i]))
        elif ((leftRightOrder == False) & (trNumber == 2)):
            high        = copy.copy((lDiffAllACH[i]))
            low         = copy.copy((lDiffAllACL[i]))
            mid         = copy.copy((lDiffAllACM[i]))
            lCorr        = copy.copy((lMostValues21[i]))
        elif ((leftRightOrder == False) & (trNumber == 3)):
            high        = copy.copy((lDiffAllACM[i]))
            low         = copy.copy((lDiffAllACL[i]))
            mid         = copy.copy((lDiffAllACH[i]))
            lCorr        = copy.copy((lMostValues21[i]))
        elif ((leftRightOrder == False) & (trNumber == 4)):
            high        = copy.copy((lDiffAllACH[i]))
            low         = copy.copy((lDiffAllACM[i]))
            mid         = copy.copy((lDiffAllACL[i]))
            lCorr        = copy.copy((lMostValues21[i]))

        # Invert order (Up - Down) randomly
        if vRow[0] == 'High':
            lAttr.append(high)
            lAttr.append(mid) # Toegevoegd
            lAttr.append(low)
        else: 
            lAttr.append(low)
            lAttr.append(mid) # Toegevoegd
            lAttr.append(high)
        lTreatments[counter] = lAttr
        lCorrB2[counter] = lCorr

        lCorr = []
        lAttr = []
        counter +=1
    
    # lAttList = [order[0], 'Mid', order[1]]
    # Nu bepaald door order
    return lTreatments, lCorrB2

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
            A00 = player.Low0B2
            A01 = player.Low1B2
            A20 = player.High0B2
            A21 = player.High1B2
            sColourFirst = vColours['sColour3']
            sColourSecond = vColours['sColour2']
            sColourThird = vColours['sColour1']
        else:
            A00 = player.High0B2
            A01 = player.High1B2
            A20 = player.Low0B2
            A21 = player.Low1B2
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
            A10 = player.Mid0B2,
            A11 = player.Mid1B2,
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
        Corr0B2 = player.Corr0B2
        Corr1B2 = player.Corr1B2
        # iTestUTN2 = player.iTest2
        # Add Focus variables to total if it's not practice trial
        if (player.round_number > Constants.num_prounds):
            participant.iOutFocus = int(participant.iOutFocus) + player.iFocusLost
            participant.iFullscreenChanges = int(participant.iFullscreenChanges) + player.iFullscreenChange
            participant.dTimeOutFocus = float(participant.dTimeOutFocus) + player.dFocusLostT
            # if (player.iDec == 0):
            #     player.iTest2 = int(iTestUTN2) + int(Corr0B2)
            # else:
            #     player.iTest2 = int(iTestUTN2) + int(Corr1B2)                 
        # If this is selected trial, save relevant variables
        if (participant.iSelectedTrialB2==player.round_number):
            if (player.iDec==0):
                if (int(player.Corr1B2) + int(player.iDec) == 1):
                    participant.sCorrB2 = "did"
                elif (int(player.Corr1B2) + int(player.iDec) == 0):
                    participant.sCorrB2 = "did not"
            else:
                if (int(player.Corr1B2) * int(player.iDec) == 1):
                    participant.sCorrB2 = "did"
                elif (int(player.Corr1B2) + int(player.iDec) == 1):
                    participant.sCorrB2 = "did not"
            
            randomTrial = random.choice([True,False])
            if (randomTrial == True):
                player.participant.iSelectedTrial = player.participant.iSelectedTrialB1
                player.participant.sSelectedTrialBlock = 'Block 1'
                player.participant.sCorr = player.participant.sCorrB1
            else:
                player.participant.iSelectedTrial = player.participant.iSelectedTrialB2
                player.participant.sSelectedTrialBlock = 'Block 2'
                player.participant.sCorr = player.participant.sCorrB2
       
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
        # Return selected text
        return dict(
            text = 'We will now continue with the experiment.'
        )

    @staticmethod
    def is_displayed(player):
        # Displayed on: First round of each block or first round after the trials
        return (
            (player.round_number==1) or (player.round_number==Constants.num_prounds+1)
        )
        

page_sequence = [Ready, Between, Task]
# page_sequence = [Task]
