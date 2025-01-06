#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: constants
Created: 1/3/24

Description:

    shared constants

Usage:

    >>> from nfl.constants import *

"""
import os

NFL_ROOT = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(NFL_ROOT)

COLORS = {
    'ARI': ["#97233F", "#000000", "#FFB612"],
    'ATL': ["#A71930", "#000000", "#A5ACAF"],
    'BAL': ["#241773", "#000000"],
    'BUF': ["#00338D", "#C60C30"],
    'CAR': ["#0085CA", "#101820", "#BFC0BF"],
    'CHI': ["#0B162A", "#C83803"],
    'CIN': ["#FB4F14", "#000000"],
    'CLE': ["#311D00", "#FF3C00"],
    'DAL': ["#003594", "#041E42", "#869397"],
    'DEN': ["#FB4F14", "#002244"],
    'DET': ["#0076B6", "#B0B7BC", "#000000"],
    'GB': ["#203731", "#FFB612"],
    'HOU': ["#03202F", "#A71930"],
    'IND': ["#002C5F", "#A2AAAD"],
    'JAX': ["#101820", "#D7A22A", "#9F792C"],
    'KC': ["#E31837", "#FFB81C"],
    'LA': ["#003594", "#FFA300", "#FF8200"],
    'LAC': ["#0080C6", "#FFC20E", "#FFFFFF"],
    'LV': ["#000000", "#A5ACAF"],
    'MIA': ["#008E97", "#FC4C02", "#005778"],
    'MIN': ["#4F2683", "#FFC62F"],
    'NE': ["#002244", "#C60C30", "#B0B7BC"],
    'NO': ["#101820", "#D3BC8D"],
    'NYG': ["#0B2265", "#A71930", "#A5ACAF"],
    'NYJ': ["#125740", "#000000", "#FFFFFF"],
    'PHI': ["#004C54", "#A5ACAF", "#ACC0C6"],
    'PIT': ["#FFB612", "#101820"],
    'SEA': ["#002244", "#69BE28", "#A5ACAF"],
    'SF': ["#AA0000", "#B3995D"],
    'TB': ["#D50A0A", "#FF7900", "#0A0A08"],
    'TEN': ["#0C2340", "#4B92DB", "#C8102E"],
    'WAS': ["#5A1414", "#FFB612"],
    'football': ["#CBB67C", "#663831"]
}
