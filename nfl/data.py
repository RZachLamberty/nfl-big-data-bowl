#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: data
Created: 1/3/24

Description:

    data loading utilities

Usage:

    >>> import nfl.data

"""
import os
from functools import wraps

import pandas as pd

from nfl.constants import REPO_ROOT

YEAR = 2025
DATA_DIR = os.path.join(REPO_ROOT, 'data', str(YEAR))


def _make_categoricals(df: pd.DataFrame, cat_cols: list[str]) -> None:
    for col in cat_cols:
        df[col] = df[col].astype('category')


def load_games() -> pd.DataFrame:
    games = pd.read_csv(os.path.join(DATA_DIR, 'games.csv'),
                        parse_dates=['gameDate'])

    _make_categoricals(df=games, cat_cols=['homeTeamAbbr', 'visitorTeamAbbr'])

    return games


def load_players() -> pd.DataFrame:
    players = pd.read_csv(os.path.join(DATA_DIR, 'players.csv'))

    def height_str_to_inches(s: str) -> int:
        ft, inches = s.split('-')
        return 12 * int(ft) + int(inches)

    players.loc[:, 'height_in'] = players.height.apply(height_str_to_inches)

    _make_categoricals(df=players, cat_cols=['collegeName', 'position'])

    return players


def pq_cache(f_pq):
    def pq_decorator(func):
        @wraps(func)
        def wrapped_func(*args, **kwargs):
            f_pq_full = os.path.join(DATA_DIR, f_pq.format(**kwargs))
            try:
                return pd.read_parquet(f_pq_full)
            except FileNotFoundError:
                df = func(*args, **kwargs)
                df.to_parquet(f_pq_full, index=False)
                return df
        return wrapped_func
    return pq_decorator


@pq_cache('plays.pq')
def load_plays() -> pd.DataFrame:
    plays = pd.read_csv(os.path.join(DATA_DIR, 'plays.csv'))
    plays['playNullifiedByPenalty'] = plays['playNullifiedByPenalty'] == 'Y'
    _make_categoricals(df=plays, cat_cols=['possessionTeam', 'defensiveTeam', 'passResult',
                                           'offenseFormation'])
    return plays


def get_ballcarrier() -> pd.DataFrame:
    plays = load_plays()
    return plays[['gameId', 'playId', 'ballCarrierId']]


@pq_cache('tackles.pq')
def load_tackles() -> pd.DataFrame:
    tackles = pd.read_csv(os.path.join(DATA_DIR, 'tackles.csv'))
    return tackles


@pq_cache('tracking_week_{week_num}.pq')
def load_tracking_week(week_num: int) -> pd.DataFrame:
    f_name = os.path.join(DATA_DIR, f'tracking_week_{week_num}.csv')
    tw = pd.read_csv(f_name)
    _make_categoricals(df=tw, cat_cols=['club', 'playDirection', 'event'])
    return tw

@pq_cache('tracking_week_{week_num_start}_{week_num_end}.pq')
def load_all_tracking(week_num_start: int, week_num_end: int) -> pd.DataFrame:
    t = None
    for week_num in range(week_num_start, week_num_end + 1):
        tw = load_tracking_week(week_num=week_num)
        if t is None:
            t = tw
        else:
            t = pd.concat([t, tw])
    return t
