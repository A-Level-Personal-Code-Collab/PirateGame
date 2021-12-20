#---------------------------------------------------------------------#
# File: https://github.com/A-Level-Personal-Code-Collab/PirateGame/app/game_items.py
# Project: https://github.com/A-Level-Personal-Code-Collab/PirateGame
# Created Date: Saturday, November 6th 2021, 8:43:40 pm
# Description: Describes how different items behave in the pirate game
# Author: Will Hall
# Copyright (c) 2021 Lime Parallelogram
# -----
# Last Modified: Mon Dec 20 2021
# Modified By: Will Hall
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	---------------------------------------------------------
# 2021-12-19	WH	Added explation messages to all items.
# 2021-11-09	WH	Added log message for personal items (Bomb and banks)
# 2021-11-07	WH	Fixed mirror function so that, when killing someone you don't get their money
# 2021-11-06	WH	Moved action declarations from main model
#---------------------------------------------------------------------#
#=========================================================#
#^ Data classes to define the action's model ^#
class actionItem():
    '''The base class for any action object that is created'''
    ACTION_EMOJI = "❔"
    ACTION_IDENTIFIER = "itmUNDEF"
    MATHS_EXPRESSION= "vCash=vCash:vBank=vBank|pCash=pCash:pBank=pBank"
    LOG_MESSAGE = "{emoji} !<{perpetrator}> did undefined action on !<{victim}> {emoji}"
    FUTURE_TENSE_VERB_MSG = "{emoji} UNDEF {emoji}"
    INVALID_RETALIATIONS = []

    def get_log(self, victim, perpetrator):
        return self.LOG_MESSAGE.format(emoji=self.ACTION_EMOJI,perpetrator=perpetrator,victim=victim)

    def get_declareData(self):
        ftVerbData = self.FUTURE_TENSE_VERB_MSG.format(emoji=self.ACTION_EMOJI)
        invalidRetals = ",".join(self.INVALID_RETALIATIONS)
        return {"action": self.ACTION_IDENTIFIER, "ftVerb": ftVerbData, "explanation": self.EXPLANATION, "invalidRetals": invalidRetals}

    def identify(self,test):
        if test == self.ACTION_IDENTIFIER:
            return True
        else:
            return False

    def get_itemNotify(self):
        popupMessage = self.FUTURE_TENSE_VERB_MSG.format(emoji=self.ACTION_EMOJI)
        return "itm_available", {"type": self.ACTION_IDENTIFIER, "ftVerb": popupMessage, "explanation": self.EXPLANATION}

    def get_expressions(self):
        expression = self.MATHS_EXPRESSION.split("|")
        if len(expression) == 1:
            return expression[0], ""
        else:
            return expression[0], expression[1]

    def isRetalValid(self,retalType):
        if retalType in self.INVALID_RETALIATIONS:
            return False
        else: 
            return True

#---------------#
class retaliatoryAction:
    '''The base class for retaliatory actions like mirror'''
    ACTION_EMOJI = "❔"
    ACTION_IDENTIFIER = "itmUNDEF"
    LOG_MESSAGE = "{emoji} !<{perpetrator}> did undefined action on !<{victim}> {emoji}"

    def get_log(self, victim, perpetrator):
        return self.LOG_MESSAGE.format(emoji=self.ACTION_EMOJI,perpetrator=perpetrator,victim=victim)

    def identify(self,test):
        if test == self.ACTION_IDENTIFIER:
            return True
        else:
            return False

    def get_itemNotify(self):
        return "retal_available", {"type": self.ACTION_IDENTIFIER, "image": self.IMAGE_LOCATION}

    def get_pushback_dat(self):
        return {"type": self.ACTION_IDENTIFIER, "animation-image": self.IMAGE_LOCATION[:-4]+"-notrans.png", "animation-class": self.ACTION_IDENTIFIER+"-animation"}

#=========================================================#
#^ Action Data classes  - describes what each action does and how it behaves ^#
class itmKill(actionItem):
    '''Class for kill item (victim's money is set to 0)'''
    IMAGE_LOCATION = "../static/img/items/set1/kill.png"
    ACTION_EMOJI = "⚔"
    ACTION_IDENTIFIER = "itmKill"
    MATHS_EXPRESSION= "self.vCash=0:self.vBank={vBank}|self.pCash={pCash}:self.pBank={pBank}"
    LOG_MESSAGE = "{emoji} !<{perpetrator}> killed !<{victim}> {emoji}"
    FUTURE_TENSE_VERB_MSG = "{emoji} KILL {emoji}"
    INVALID_RETALIATIONS = []
    TARGETTED = True
    EXPLANATION = "Reset the target's cash balance to 0."

#---------------#
class itmSteal(actionItem):
    '''Class for steal item (victim's money is given to perpetrator)'''
    IMAGE_LOCATION = "../static/img/items/set1/steal.png"
    ACTION_EMOJI = "💰"
    ACTION_IDENTIFIER = "itmSteal"
    MATHS_EXPRESSION= "self.vCash=0:self.vBank={vBank}|self.pCash={pCash}+{vCash}:self.pBank={pBank}"
    LOG_MESSAGE = "{emoji} !<{perpetrator}> stole from !<{victim}> {emoji}"
    FUTURE_TENSE_VERB_MSG = "{emoji} STEAL FROM {emoji}"
    EXPLANATION="Transfer all of your target's cash balance to your own."
    INVALID_RETALIATIONS = []
    TARGETTED = True

#---------------#
class itmGift(actionItem):
    '''Class for gift item (victim receives 1000M from nowhere)'''
    IMAGE_LOCATION = "../static/img/items/set1/gift.png"
    ACTION_EMOJI = "🎁"
    ACTION_IDENTIFIER = "itmGift"
    MATHS_EXPRESSION= "self.vCash={vCash}+1000:self.vBank={vBank}|self.pCash={pCash}:self.pBank={pBank}"
    LOG_MESSAGE = "{emoji} !<{perpetrator}> gifted !<{victim}> {emoji}"
    FUTURE_TENSE_VERB_MSG = "{emoji} GIFT {emoji}"
    EXPLANATION="Give £1000 to your target. This money does not come from your balance."
    INVALID_RETALIATIONS = []
    TARGETTED = True


#---------------#
class itmSwap(actionItem):
    '''Class for swap item (perpetrator and victim swap cash)'''
    IMAGE_LOCATION = "../static/img/items/set1/swap.png"
    ACTION_EMOJI = "🤝"
    ACTION_IDENTIFIER = "itmSwap"
    MATHS_EXPRESSION= "self.vCash={pCash}:self.vBank={vBank}|self.pCash={vCash}:self.pBank={pBank}"
    LOG_MESSAGE = "{emoji} !<{perpetrator}> swapped with !<{victim}> {emoji}"
    FUTURE_TENSE_VERB_MSG = "{emoji} SWAP WITH {emoji}"
    EXPLANATION="Switch your cash with your target's cash."
    INVALID_RETALIATIONS = ["itmMirror"]
    TARGETTED = True

#---------------#
class itmBomb(actionItem):
    '''Class for bomb item'''
    IMAGE_LOCATION = "../static/img/items/set1/bomb.png"
    ACTION_EMOJI = "💣"
    ACTION_IDENTIFIER = "itmBomb"
    MATHS_EXPRESSION= "self.vCash=0:self.vBank={vBank}"
    LOG_MESSAGE = "{emoji} !<{victim}> blew up {emoji}"
    EXPLANATION="Your cash is reset to 0."
    INVALID_RETALIATIONS = ["itmShield","itmMirror"]
    TARGETTED = False

#---------------#
class itmBank(actionItem):
    '''Class for bank item'''
    IMAGE_LOCATION = "../static/img/items/set1/bank.png"
    ACTION_EMOJI = "🏦"
    ACTION_IDENTIFIER = "itmBank"
    MATHS_EXPRESSION= "self.vCash=0:self.vBank={vBank}+{vCash}"
    LOG_MESSAGE = "{emoji} !<{victim}> put your money safely away {emoji}"
    EXPLANATION="Your money is stored safely away."
    INVALID_RETALIATIONS = ["itmShield","itmMirror"]
    TARGETTED = False

#=========================================================#
#^ Defines how retaliation actions behave ^#
class itmMirror(retaliatoryAction):
    '''Class for mirror modifier item'''
    IMAGE_LOCATION = "../static/img/items/set1/mirror.png"
    ACTION_EMOJI = "🪞"
    ACTION_IDENTIFIER = "itmMirror"
    LOG_MESSAGE = "{emoji} !<{victim}> mirrored that {emoji}"
    EXPLANATION="Force your opponent to receive the action instead of you."

    def expression_manipulate(self, expression):
        self.new_expression = expression.replace("self.vCash","___V.CASH___")
        self.new_expression = self.new_expression.replace("self.pCash","___P.CASH___")
        self.new_expression = self.new_expression.replace("{vCash}","__V.CASH__")
        self.new_expression = self.new_expression.replace("{pCash}","__P.CASH__")
        self.new_expression = self.new_expression.replace("___P.CASH___","self.vCash")
        self.new_expression = self.new_expression.replace("___V.CASH___","self.pCash")
        self.new_expression = self.new_expression.replace("__P.CASH__","{vCash}")
        self.new_expression = self.new_expression.replace("__V.CASH__","{pCash}")
        return self.new_expression

#---------------#
class itmShield(retaliatoryAction):
    '''Class for shield modifier item'''
    IMAGE_LOCATION = "../static/img/items/set1/shield.png"
    ACTION_EMOJI = "🛡"
    ACTION_IDENTIFIER = "itmShield"
    LOG_MESSAGE = "{emoji} !<{victim}> blocked that {emoji}"
    EXPLANATION="Action is dropped and nothing happens."

    def expression_manipulate(self, expression):
        return "self.vCash={vCash}:self.vBank={vBank}:self.pCash={pCash}:self.pBank={pBank}"

#=========================================================#
#^ Money Data Class ^#
class money:
    '''Class that defines the behavior of money items'''
    IMAGE_LOCATION = "../static/img/items/set1/M{denom}.png"
    IDENTIFIER = "M{denom}"
    DENOMINATION = 200

    def __init__(self, denomination):
        self.DENOMINATION = denomination
        self.IDENTIFIER = self.IDENTIFIER.format(denom=str(denomination))
        self.IMAGE_LOCATION = self.IMAGE_LOCATION.format(denom=str(denomination))

    def identify(self,value):
        if value[0] == "M":
            return True
        else:
            return False

    def cash_update(self,old_cash):
        return old_cash + self.DENOMINATION