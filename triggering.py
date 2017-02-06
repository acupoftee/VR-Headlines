#==============================================================================
# NOTE/CAUTION/WARNING:
#
# This file is used to store offensive terms so that triggering or offensive
# headlines are not satirized by VR Headlines and other bots. Accordingly, it
# contains a lot of terms that are triggering, be they sexual, violent or
# otherwise.
#==============================================================================

import re

triggering = re.compile(
    r"\b(deaths?|dead(ly)?|die(s|d)?|hurts?|(sex(ual(ly)?)?|child)[ -]?(abused?|trafficking|"
    r"assault(ed|s)?)|injur(e|i?es|ed|y)|kill(ing|ed|er|s)?s?|wound(ing|ed|s)?|fatal(ly|ity)?|"
    r"shoo?t(s|ing|er)?s?|crash(es|ed|ing)?|attack(s|ers?|ing|ed)?|murder(s|er|ed|ing)?s?|"
    r"hostages?|(gang)?rap(e|es|ed|ist|ists|ing)|assault(s|ed)?|pile-?ups?|massacre(s|d)?|"
    r"assassinate(d|s)?|sla(y|in|yed|ys|ying|yings)|victims?|tortur(e|ed|ing|es)|"
    r"execut(e|ion|ed|ioner)s?|gun(man|men|ned)|suicid(e|al|es)|bomb(s|ed|ing|ings|er|ers)?|"
    r"mass[- ]?graves?|bloodshed|state[- ]?of[- ]?emergency|al[- ]?Qaeda|blasts?|violen(t|ce)|"
    r"lethal|cancer(ous)?|stab(bed|bing|ber)?s?|casualt(y|ies)|sla(y|ying|yer|in)|"
    r"drown(s|ing|ed|ings)?|bod(y|ies)|kidnap(s|ped|per|pers|ping|pings)?|rampage|beat(ings?|en)|"
    r"terminal(ly)?|abduct(s|ed|ion)?s?|missing|behead(s|ed|ings?)?|homicid(e|es|al)|"
    r"burn(s|ed|ing)? alive|decapitated?s?|jihadi?s?t?|hang(ed|ing|s)?|funerals?|traged(y|ies)|"
    r"autops(y|ies)|child sex|sob(s|bing|bed)?|pa?edophil(e|es|ia)|9(/|-)11|Sept(ember|\.)? 11|"
    r"genocide)\W?\b",
    flags=re.IGNORECASE)

def tact(headline):
    """Avoid producing tactless tweets"""
    if re.search(triggering, headline) is None:
        return True
    else:
        return False