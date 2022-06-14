from otree.api import *
from numpy import random

# from Infographics1 import FirstCheck, Infographics

doc = """
Treatments will be:
1 - Unequal Start (20-10-5) - Higher Mid Value (20-20-5)
2 - Unequal Start (20-10-5) - Lower Mid Value (20-5-5)
3 - Equal Start (10-10-10) - Higher Mid Value (10-20-10)
4 - Equal Start (10-10-10) - Lower Mid Value (10-5-10)

This Game functions mostly to explain the base concept of the balls and their values
"""

class C(BaseConstants):
    NAME_IN_URL = 'Infographics1'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    sImagePath          = 'global/figures/'
    sPathB              = sImagePath+'Blue.png'
    sPathLB             = sImagePath+'LightBlue.png'
    sPathR              = sImagePath+'Red.png'
    sPathY              = sImagePath+'Yellow.png'
    iRandomTreatment    = 5 # 1 to 4, 1 more?
    iRandomColour       = 5 # 1 to 4, 1 more?
    
    # Nog veranderen
    lEqual = dict(        
        sValueHigh = '10',
        sValueMid = '10', 
        sValueLow = '10',
        sValueHighThreeTimes = '30',
        sValueLowFourTimes = '40',
    )
    lUnequal = dict(        
        sValueHigh = '20',
        sValueMid = '10', 
        sValueLow = '5',
        sValueHighThreeTimes = '60',
        sValueLowFourTimes = '20',
    )
    lAttrRYB = dict(        
        title = 'Colour Values',
        titleB2 = 'Value Change',
        colour1 = 'Blue',
        colour2 = 'Red',
        colour3 = 'Yellow',
        sColour1 = sPathB,
        sColour2 = sPathR,
        sColour3 = sPathY, 
    )
    lAttrHR = dict(
        title = 'Colour Values',
        titleB2 = 'Value Change',
        colour1 = 'Red',
        colour2 = 'Light Blue',
        colour3 = 'Blue',
        sColour1 = sPathR,
        sColour2 = sPathLB,
        sColour3 = sPathB,
    )
    lAttrMR = dict(
        title = 'Colour Values',
        titleB2 = 'Value Change',
        colour1 = 'Blue',
        colour2 = 'Red',
        colour3 = 'Light Blue',
        sColour1 = sPathB,
        sColour2 = sPathR,
        sColour3 = sPathLB,
    )
    lAttrLR = dict(
        title = 'Colour Values',
        titleB2 = 'Value Change',
        colour1 = 'Light Blue',
        colour2 = 'Blue',
        colour3 = 'Red',
        sColour1 = sPathLB,
        sColour2 = sPathB,
        sColour3 = sPathR,
    )

# FUNCTIONS 
def creating_session(subsession):
    ## SETUP FOR PARTICIPANT
    for player in subsession.get_players():
        p, session = player.participant, subsession.session
        iTreatment = session.config['iTreatment'] # 5 treatments
        iColour = session.config['iColour']
        if (iTreatment!=C.iRandomTreatment):
            player.iTreatment = p.iTreatment = iTreatment 
        else:
            player.iTreatment = p.iTreatment = iTreatment = random.randint(1,C.iRandomTreatment)
        if (iColour!=C.iRandomColour):
            player.iColour = p.iColour = iColour 
        else:
            player.iColour =  p.iColour = iColour = random.randint(1,C.iRandomColour)
        
        print('Treatment for participant: {}'.format(p.iTreatment))
        print('Colour Scheme for participant: {}'.format(p.iColour))
        lAttrRYB = C.lAttrRYB.copy()
        lAttrHR = C.lAttrHR.copy()
        lAttrMR = C.lAttrMR.copy()
        lAttrLR = C.lAttrLR.copy()
        lEqual = C.lEqual.copy()
        lUnequal = C.lUnequal.copy()

        if (player.iTreatment <= 2):
            p.lValuesFirst = lUnequal
        else:
            p.lValuesFirst = lEqual
        
        if (player.iColour==1):
            p.vColours = lAttrRYB
        elif (player.iColour==2):
            p.vColours = lAttrHR
        elif (player.iColour==3):
            p.vColours = lAttrMR
        else:
            p.vColours = lAttrLR 

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass

class Player(BasePlayer):
    # Check hoeveel hier nog nodig van is
    sAttrOrder          = models.StringField()
    dRTinfographics     = models.FloatField(blank=True)
    iTreatment          = models.IntegerField()
    iColour             = models.IntegerField()
    sSlideSequence      = models.StringField(blank=True)
    sSlideTime          = models.StringField(blank=True)

# PAGES
class Infographics1(Page):
    form_model = 'player'
    form_fields = [ 
        'sSlideSequence',
        'sSlideTime',
        'dRTinfographics',
        # 'iTreatment',
        # 'iColour',
        ]

    @staticmethod
    def js_vars(player: Player):
        lSolutions = ['3','1']

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

class FirstCheck1(Page):
    pass

page_sequence = [FirstCheck1, Infographics1]
