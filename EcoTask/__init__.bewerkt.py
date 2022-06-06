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
    lDiffH = [[2,3], [10,10], [5, 5], [7,10], [10,10], [5,3], [12,20]]
    lDiffM = [[2,2], [10,10], [6, 5], [8,8], [7,8], [6,8], [20,15]]
    lDiffL = [[2,2], [12,10], [5, 5], [9,7], [9,8], [7,7], [15,5]]

    lDiff1H, lDiff1M, lDiff1L, lDiff2H, lDiff2M, lDiff2L = ([] for i in range(6))
    for list in lDiffH:
        lDiff1H.append([x+1 for x in list])
        lDiff2H.append([x*2 for x in list])

    for list in lDiffM:
        lDiff1M.append([x+1 for x in list])
        lDiff2M.append([x*2 for x in list])

    for list in lDiffL:
        lDiff1L.append([x+1 for x in list])
        lDiff2L.append([x*2 for x in list])

    lDiffAllH = lDiffH + lDiff1H + lDiff2H
    lDiffAllM = lDiffM + lDiff1M + lDiff2M
    lDiffAllL = lDiffL + lDiff1L + lDiff2L
      
    ## Number of trials
    num_reps            = 1 # number of repetitions per permutation
    num_repsEq          = 2 # Number of cases with equal sustainability
    num_prounds         = 3 # Number of Practice Rounds  
    num_rounds          = 21 + num_prounds # Number of rounds
    players_per_group   = None
    sImagePath          = 'global/figures/'

    sPathB              = sImagePath+'Blue.png'
    sPathLB             = sImagePath+'LightBlue.png'
    sPathR              = sImagePath+'Red.png'
    sPathY              = sImagePath+'Yellow.png'
    iRandomTreatment    = 4 # 1 to 4
    iRandomColour       = 4 # 1 to 4
    
    # Nog veranderen
    lEqual = dict(        
        sValueHigh = '10',
        sValueMid = '10', 
        sValueLow = '10',
    )
    lUnequal = dict(        
        sValueHigh = '20',
        sValueMid = '10', 
        sValueLow = '5',
    )
    lAttrRYB = dict(        
        attr = 'Colour Values',
        title = 'Colour Values',
        colour1 = 'Blue',
        colour2 = 'Red',
        colour3 = 'Yellow',
        sColour1 = sPathB,
        sColour2 = sPathR,
        sColour3 = sPathY, 
    )
    lAttrHR = dict(
        attr = 'Colour Values',
        title = 'Colour Values',
        colour1 = 'Red',
        colour2 = 'Light Blue',
        colour3 = 'Blue',
        sColour1 = sPathR,
        sColour2 = sPathLB,
        sColour3 = sPathB,
    )
    lAttrMR = dict(
        attr = 'Colour Values',
        title = 'Colour Values',
        colour1 = 'Blue',
        colour2 = 'Red',
        colour3 = 'Light Blue',
        sColour1 = sPathB,
        sColour2 = sPathR,
        sColour3 = sPathLB,
    )
    lAttrLR = dict(
        attr = 'Colour Values',
        title = 'Colour Values',
        colour1 = 'Light Blue',
        colour2 = 'Blue',
        colour3 = 'Red',
        sColour1 = sPathLB,
        sColour2 = sPathB,
        sColour3 = sPathR,
    )

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
    Mid0                  = models.StringField(blank=True)
    Mid1                  = models.StringField(blank=True)
    High0                  = models.StringField(blank=True)
    High1                  = models.StringField(blank=True)
    Low0                  = models.StringField(blank=True)
    Low1                  = models.StringField(blank=True)
    ## Van info1 erbij
    sAttrOrder          = models.StringField()
    dRTbelief           = models.FloatField(blank=True)
    dRTinfographics     = models.FloatField(blank=True)
    iTreatment          = models.IntegerField()
    iColour             = models.IntegerField()
    sSlideSequence      = models.StringField(blank=True)
    sSlideTime          = models.StringField(blank=True)

# FUNCTIONS

def creating_session(subsession):
    ## SETUP FOR PARTICIPANT
    if subsession.round_number == 1:
        for player in subsession.get_players():
            p, session = player.participant, subsession.session
            lTreat, lRownames   = createTreatment()
            p.vRownames         = lRownames
            p.mTreat            = lTreat             
            p.SelectedTrial     = random.choice(range(Constants.num_prounds+1,Constants.num_rounds))
            print('Trial selected for participant {}: {}'.format(p.code,p.SelectedTrial))
            
            iTreatment = session.config['iTreatment'] # Snap nog even niet of het nou 4 of 5 treatments kunnen zijn
            iColour = session.config['iColour']
            if (iTreatment!=Constants.iRandomTreatment):
                player.iTreatment = p.iTreatment = iTreatment 
            else:
                player.iTreatment =  p.iTreatment = iTreatment = random.randint(1,Constants.iRandomTreatment)
            if (iTreatment!=Constants.iRandomColour):
                player.iColour = p.iColour = iColour 
            else:
                player.iColour =  p.iColour = iColour = random.randint(1,Constants.iColour)
            
            print('Treatment for participant: {}'.format(p.iTreatment))
            lAttrRYB = Constants.lAttrRYB.copy()
            lAttrHR = Constants.lAttrHR.copy()
            lAttrMR = Constants.lAttrMR.copy()
            lAttrLR = Constants.lAttrLR.copy()
            lEqual = Constants.lEqual.copy()
            lUnequal = Constants.lUnequal.copy()

            if (player.iTreatment <= 2):
                p.lValuesFirst = lEqual
            else:
                p.lValuesFirst = lUnequal
            
            if (player.iColour==1):
                p.vColours = lAttrRYB
            elif (player.iColour==2):
                p.vColours = lAttrHR
            elif (player.iColour==3):
                p.vColours = lAttrMR
            else:
                p.vColours = lAttrLR 
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
            lAttr = p.mTreat[x]
        elif (round<=total_rounds): ## These are the trials of the block
            player.iBlockTrial = int(round)
            x = int(round-1)
            lAttr = p.mTreat[x]

        ## Randomize if mouse starts on left or right
        player.bStartLeft = random.choice([True,False])
        # Check order of Attributes and save them as player variables
        # DEZE QUA NAAM (Mid0 ENZO) VERANDEREN
        player.Mid0   = str(lAttr[1][0]) # Mid, Q is High, S is Low
        player.Mid1   = str(lAttr[1][1])
        if p.vRownames[0]=='Low':
            player.High0 = str(lAttr[2][0])
            player.High1 = str(lAttr[2][1]) #3
            player.Low0 = str(lAttr[0][0]) #4
            player.Low1 = str(lAttr[0][1]) #5
        else:
            player.High0 = str(lAttr[0][0]) #4
            player.High1 = str(lAttr[0][1]) #5
            player.Low0 = str(lAttr[2][0])
            player.Low1 = str(lAttr[2][1]) #3

# # Functions
# def join2String(list, delimiter= ','):
#         return delimiter.join(map(str,list))

def createTreatment():
    n = Constants.num_reps
    n_eq = Constants.num_repsEq

    ## Sets
    iSize = int((Constants.num_rounds-Constants.num_prounds))
    
    ## AllDiff
    lDiffAllH = Constants.lDiffAllH
    lDiffAllM = Constants.lDiffAllM
    lDiffAllL = Constants.lDiffAllL

    lTreatments = ["" for x in range(iSize)] # Initialiseren variabelen
    lAttr = [] # DIT ZELF TOEGEVOEGD

    # Establish order of qualities
    order = sample(['High','Low'],2)
    counter = 0
    randomOrder = sample(range(len(lDiffAllH)), len(lDiffAllH))
    for i in randomOrder:
        # Invert order if in this trial outcomes are flipped
        # Even uitgezet
        if random.choice([True,False]):
            high        = copy.copy((lDiffAllH[i]))[::-1]
            low         = copy.copy((lDiffAllL[i]))[::-1]
            mid         = copy.copy((lDiffAllM[i]))[::-1]
        else:
            high        = copy.copy((lDiffAllH[i]))
            low         = copy.copy((lDiffAllL[i]))
            mid         = copy.copy((lDiffAllM[i]))

        # high        = copy.copy((lDiffAllH[i]))
        # low         = copy.copy((lDiffAllL[i]))
        # mid         = copy.copy((lDiffAllM[i]))

        # Add attributes depending order
        if order[0] == 'High':
            lAttr.append(high)
            lAttr.append(mid) # Toegevoegd
            lAttr.append(low)
        else: 
            lAttr.append(low)
            lAttr.append(mid) # Toegevoegd
            lAttr.append(high)
        lTreatments[counter] = lAttr
        lAttr = []
        counter +=1
    
    lAttList = [order[0], 'Mid', order[1]]
    # random.shuffle(lTreatments)
    # Nu bepaald door order
    return lTreatments, lAttList

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
        colour1 = vColours.colour1
        colour2 = vColours.colour2
        colour3 = vColours.colour3

        if vRownames[0]=='Low': # Quality
            A10 = player.Low0
            A11 = player.Low1
            A20 = player.High0
            A21 = player.High1
        else:
            A10 = player.High0
            A11 = player.High1
            A20 = player.Low0
            A21 = player.Low1
        
        return dict(
            Attr0 = vRownames[0],
            Attr1 = vRownames[1],
            Attr2 = vRownames[2],
            ColourHigh = colour1,
            ColourMid = colour2,
            ColourLow = colour3,
            Mid0 = player.Mid0,
            Mid1 = player.Mid1,
            A10 = A10,
            A11 = A11,
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
        # Add Focus variables to total if it's not practice trial
        if (player.round_number > Constants.num_prounds):
            participant.iOutFocus = int(participant.iOutFocus) + player.iFocusLost
            participant.iFullscreenChanges = int(participant.iFullscreenChanges) + player.iFullscreenChange
            participant.dTimeOutFocus = float(participant.dTimeOutFocus) + player.dFocusLostT
        # If this is selected trial, save relevant variables
        if (participant.SelectedTrial==player.round_number):
            if (player.iDec==0):
                participant.Price = player.Mid0
                participant.Q = player.High0
                participant.S = player.Low0
            else:
                participant.Price = player.Mid1
                participant.Q = player.High1
                participant.S = player.Low1
       

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

class Infographics(Page):
    form_model = 'player'
    form_fields = [ 
        # 'sSlideSequence',
        # 'sSlideTime',
        # 'dRTinfographics',
        ]

    @staticmethod
    def js_vars(player: Player):
        lSolutions = ['3','1']
        if player.iTreatment ==1:
            lSolutions.extend(['15','15'])
        elif player.iTreatment ==2:
            lSolutions.extend(['15','2.5'])
        elif player.iTreatment ==3:
            lSolutions.extend(['27.5','15'])


        return dict(
            lSolutions = lSolutions
        )
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            # lAttr = player.participant.lAttr,
            lValuesFirst = player.participant.lValuesFirst,
            vColours = player.participant.vColours
        )

class FirstCheck(Page):
    pass

page_sequence = [FirstCheck, Infographics, Ready, Between, Task]
# page_sequence = [Task]
