from os import environ

SESSION_CONFIGS = [
    dict(
    name='session_config',
    display_name='Ecolabels Config',
    num_demo_participants=6,
    # app_sequence=['Instructions', 'EcoTask', 'Infographics2','EcoTask2','EndBelief','Questionnaire' ,'EndPage'],
    app_sequence=['Instructions', 'Infographics1', 'EcoTask', 'Infographics3', 'EcoTask2', 'Questionnaire', 'EndPage'],
    # app_sequence=['Infographics1', 'EcoTask', 'Infographics3', 'EcoTask2', 'EndPage'],
    # app_sequence=['Instructions', 'Infographics1', 'Infographics3', 'EcoTask2'], #, 'EndBelief','Questionnaire','EndPage'],
    iTreatment = 5, # 1 meer dan het aantal treatments
    iColour = 5, # 1 meer dan het aantal treatments
    iTimeOut=0,
    bRequireFS=True,
    bCheckFocus=True,
    doc="""
    Edit the following variables with these options:
    iTreatment: int, Between-subject treatment.  [1: Linear, 2: Concave, 3: Convex]
    sActivation: str, type of VT activation. ['mouseover','click']
    iTimeOut: int, seconds before trial time-out. (0 means no timeout)
    bRequireFS: bool, require fullscreen.
    bCheckFocus: bool, require checking if page is active.
    vTrigger: str, buttons that get activated. ['val','row','col']
    Attr_order: str, to shuffle attributes.
    """
    ),
    dict(
        name='Questionnaire',
        num_demo_participants= 1,
        app_sequence=['Questionnaire']
    ),
        dict(
        name='Endpage',
        num_demo_participants= 1,
        app_sequence=['EndPage'],
        bRequireFS=True,
        bCheckFocus=True,
        # dPixelRatio=True,
        iTimeOut=0
        # 'StartLeft'         : player.bStartLeft,
        # dPixelRatio'       : p.dPixelRatio,
    ),
    dict(
        name='Part1',
        num_demo_participants= 1,
        app_sequence=['Instructions', 'EcoTask'],
        bRequireFS=True,
        bCheckFocus=True,
        # dPixelRatio=True,
        iTimeOut=0
        # 'StartLeft'         : player.bStartLeft,
        # dPixelRatio'       : p.dPixelRatio,
    ),
    dict(
        name='Intro',
        num_demo_participants= 1,
        app_sequence=['Instructions']
    ),
    dict(
        name='Infographics2',
        num_demo_participants= 10,
        app_sequence=['Infographics2'],
        iTreatment = 4,
        iTimeOut=0,
        bRequireFS=True,
        bCheckFocus=True,
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

PARTICIPANT_FIELDS = [
    'treatment',
    'colour',
    'iTest',
    'iCounterCorrect',
    'PresOrder',
    'mTreat',
    'vRownames',
    'iSelectedTrial',
    'iSelectedTrialB1',
    'iSelectedTrialB2',
    'sSelectedTrialBlock',
    'bCorrectBonus',
    'sCorr',
    'sCorrB1',
    'sCorrB2',
    'CorrSelB1',
    'CorrSelB2',
    'ProlificID',
    'Bonus',
    'TreeAmount',
    'validQuestionnaire',
    'dTimeOutFocus',
    'iOutFocus',
    'sAttrOrder',
    'iFullscreenChanges',
    'iCorrectBeliefs',
    'iTreatment',
    'iColour',
    'startTime',
    'sTreesLocation',
    'dPixelRatio',
    'lAttr',
    'vColours',
    'lValuesFirst',
    'lValuesSecond',
    ]

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

#OTREE_PRODUCTION = 1


# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = [
    dict(
        name='econ101',
        display_name='Econ 101 class',
        participant_label_file='_rooms/econ101.txt',
    ),
    dict(name='prolific', display_name='Prolific Room (no participant labels)'),
]


ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""
SECRET_KEY = '4165392775761'

INSTALLED_APPS = ['otree']

