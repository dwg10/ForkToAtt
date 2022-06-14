from statistics import mode
from otree.api import *
import time

doc = """
Initialize Introduction app.
Includes introduction page and instructions
"""

class Constants(BaseConstants):
    name_in_url = 'Instructions'
    players_per_group = None
    num_rounds = 1
    ## Symbols directory
    UvA_logo = 'global/figures/UvA_logo.png'
    revealed_task = 'global/figures/revealed_task_balls_img.png'
    revealed_task_question = 'global/figures/revealed_task_balls_question_img.png'
    circled_task = 'global/figures/circled_task_balls_img.png'
    star_symbol = 'global/figures/one_star.png'
    ## Variables that are not fully defined yet
    BonusPayment = int(10)
    FixedPayment = int(20)
    MaxPayment = int(30)
    NumTrials = int(42)
    AvgDuration = "10-12"

    ## Slides for introduction
    SlidePath = 'Instructions/slide'
    SlidesIntro = [
        dict(
            Title = 'Introduction',
            path='Introduction/slide0.html',
            ),
        dict(
            Title = 'Informed Consent',
            path='Introduction/slide1.html',
            ),        
    ]
    Slides = [
        dict(
            Title = 'The Experiment',
            path=SlidePath+'0.html',
            ),
        dict(
            Title = 'The Setup (1): Baskets and Balls',
            path=SlidePath+'1.html',
            ),
        dict(
            Title = 'The Setup (2): Value Information',
            path=SlidePath+'2.html',
            ),
        dict(
            Title = 'The Setup (3): Computing Values',
            path=SlidePath+'22.html',
            ),
        dict(
            Title = 'The Setup (4): Retrieving Information',
            path=SlidePath+'3.html',
            ),
        dict(
            Title = 'The Setup (5): Decision Process and Possible Payments',
            path=SlidePath+'4.html',
            ),
        dict(
            Title = 'All clear? Please answer these questions correctly to proceed:',
            path=SlidePath+'5.html',
            ),
    ]

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    bClickedLocation    = models.BooleanField()
    dPixelRatio         = models.FloatField()
    sSlideSequence      = models.StringField(blank=True)
    sSlideTime          = models.StringField(blank=True)
    sProlific_ID        = models.StringField()

# PAGES
class Introduction(Page):

    @staticmethod
    def vars_for_template(player):

        return dict(
            UvA_logo = Constants.UvA_logo,
            Slides = Constants.SlidesIntro,
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        part = player.participant
        # Initialize Focus variables#        
        part.startTime          = time.time()
        part.iOutFocus          = 0
        part.iFullscreenChanges = 0
        part.dTimeOutFocus      = 0
        player.sProlific_ID     = part.label

class Calibration(Page):
    form_model = 'player'
    form_fields = [ 'dPixelRatio' ]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        part = player.participant
        part.dPixelRatio = player.dPixelRatio

class Instructions(Page):
    form_model = 'player'
    form_fields = [ 
        'sSlideSequence',
        'sSlideTime',
        ]
    
    @staticmethod
    def vars_for_template(player):
        return dict(
            Slides = Constants.Slides,
    )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        part = player.participant

    @staticmethod
    def js_vars(player: Player):
        session = player.session
        p = player.participant
        return {
            'bRequireFS'        : session.config['bRequireFS'],
            'bCheckFocus'       : session.config['bCheckFocus'],
            'dPixelRatio'       : p.dPixelRatio,
        }

page_sequence = [Introduction, Calibration, Instructions]


