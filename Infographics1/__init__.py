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

# FUNCTIONS 
def creating_session(subsession):
    ## SETUP FOR PARTICIPANT
    for player in subsession.get_players():
        p, session = player.participant, subsession.session
        iTreatment = session.config['iTreatment'] # Snap nog even niet of het nou 4 of 5 treatments kunnen zijn
        iColour = session.config['iColour']
        if (iTreatment!=C.iRandomTreatment):
            player.iTreatment = p.iTreatment = iTreatment 
        else:
            player.iTreatment = p.iTreatment = iTreatment = random.randint(1,C.iRandomTreatment)
        if (iTreatment!=C.iRandomColour):
            player.iColour = p.iColour = iColour 
        else:
            player.iColour =  p.iColour = iColour = random.randint(1,C.iColour)
        
        print('Treatment for participant: {}'.format(p.iTreatment))
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
    dRTbelief           = models.FloatField(blank=True)
    dRTinfographics     = models.FloatField(blank=True)
    iTreatment          = models.IntegerField()
    iColour             = models.IntegerField()
    sSlideSequence      = models.StringField(blank=True)
    sSlideTime          = models.StringField(blank=True)

    # Beliefs
    B01 = models.FloatField()
    B02 = models.FloatField()
    B03 = models.FloatField()
    B11 = models.FloatField()
    B12 = models.FloatField()
    B13 = models.FloatField()


# PAGES
class Infographics(Page):
    form_model = 'player'
    form_fields = [ 
        'sSlideSequence',
        'sSlideTime',
        'dRTinfographics',
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

page_sequence = [FirstCheck, Infographics]
