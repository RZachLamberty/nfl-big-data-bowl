#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: vis
Created: 12/1/24

Description:

    visualization utilities

    all play animation code is copied from
    [here](https://www.kaggle.com/code/nickwan/animate-plays-with-plotly-real-no-lies-here) with
    some slight modifications

Usage:

    >>> from nfl.vis import animate_play

"""
import numpy as np
import plotly.graph_objects as go
from matplotlib.colors import to_rgb

from nfl.constants import COLORS


def hex_to_rgb_array(hex_color):
    """
    take in hex val and return rgb np array
    helper for 'color distance' issues
    """
    return np.array([to_rgb(hex_color)])


def get_color_distance(hex1, hex2):
    """
    d = {} distance between two colors(3)
    helper for 'color distance' issues
    """
    if hex1 == hex2:
        return 0
    rgb1 = np.array(to_rgb(hex1))
    rgb2 = np.array(to_rgb(hex2))

    rm = 0.5 * (rgb1[0] + rgb2[0])
    d = abs(sum((2 + rm, 4, 3 - rm) * (rgb1 - rgb2) ** 2)) ** 0.5
    return d


def get_color_pairs(team1, team2):
    """
    Pairs colors given two teams
    If colors are 'too close' in hue, switch to alt color
    """
    color_array_1 = COLORS[team1]
    color_array_2 = COLORS[team2]
    # If color distance is small enough then flip color order
    if get_color_distance(color_array_1[0], color_array_2[0]) < 500:
        return {
            team1: [color_array_1[0], color_array_1[1]],
            team2: [color_array_2[1], color_array_2[0]],
            'football': COLORS['football']
        }
    else:
        return {
            team1: [color_array_1[0], color_array_1[1]],
            team2: [color_array_2[0], color_array_2[1]],
            'football': COLORS['football']
        }


def animate_play(games, tracking_df, play_df, gameId, playId):
    """
    Generates an animated play using the tracking data.
    """
    selected_game_df = games.loc[games['gameId'] == gameId].copy()
    selected_play_df = (play_df
                        .loc[(play_df['playId'] == playId) & (play_df['gameId'] == gameId)]
                        .copy())

    tracking_players_df = tracking_df.copy()
    selected_tracking_df = (tracking_players_df
                            .loc[(tracking_players_df['playId'] == playId)
                                 & (tracking_players_df['gameId'] == gameId)]
                            .copy())

    sorted_frame_list = selected_tracking_df.frameId.unique()
    sorted_frame_list.sort()

    # get good color combos
    team_combos = list(set(selected_tracking_df['club'].unique()) - set(['football']))
    color_orders = get_color_pairs(team_combos[0], team_combos[1])

    # get play General information
    line_of_scrimmage = selected_play_df['absoluteYardlineNumber'].values[0]

    # Fixing first down marker issue from last year
    ytg = selected_play_df['yardsToGo'].values[0]
    if selected_tracking_df['playDirection'].values[0] == 'right':
        first_down_marker = line_of_scrimmage + ytg
    else:
        first_down_marker = line_of_scrimmage - ytg
    down = selected_play_df['down'].values[0]
    quarter = selected_play_df['quarter'].values[0]
    game_clock = selected_play_df['gameClock'].values[0]
    play_description = selected_play_df['playDescription'].values[0]

    # Handle case where we have a really long Play Description and want to split it into two lines
    if len(play_description.split(" ")) > 15 and len(play_description) > 115:
        play_description = (" ".join(play_description.split(" ")[0:16])
                            + "<br>"
                            + " ".join(play_description.split(" ")[16:]))

    # initialize plotly start and stop buttons for animation
    updatemenus_dict = [{"buttons": [{"args": [None, {"frame": {"duration": 100, "redraw": False},
                                                      "fromcurrent": True,
                                                      "transition": {"duration": 0}}],
                                      "label": "Play",
                                      "method": "animate"},
                                     {"args": [[None], {"frame": {"duration": 0, "redraw": False},
                                                        "mode": "immediate",
                                                        "transition": {"duration": 0}}],
                                      "label": "Pause",
                                      "method": "animate"}],
                         "direction": "left",
                         "pad": {"r": 10, "t": 87},
                         "showactive": False,
                         "type": "buttons",
                         "x": 0.1,
                         "xanchor": "right",
                         "y": 0,
                         "yanchor": "top"}]
    # initialize plotly slider to show frame position in animation
    sliders_dict = {"active": 0,
                    "yanchor": "top",
                    "xanchor": "left",
                    "currentvalue": {"font": {"size": 20},
                                     "prefix": "Frame:",
                                     "visible": True,
                                     "xanchor": "right"},
                    "transition": {"duration": 300, "easing": "cubic-in-out"},
                    "pad": {"b": 10, "t": 50},
                    "len": 0.9,
                    "x": 0.1,
                    "y": 0,
                    "steps": []}

    frames = []
    for frameId in sorted_frame_list:
        data = []
        # Add Numbers to Field
        data.append(
            go.Scatter(
                x=np.arange(20, 110, 10),
                y=[5] * len(np.arange(20, 110, 10)),
                mode='text',
                text=list(map(str, list(np.arange(20, 61, 10) - 10) + list(np.arange(40, 9, -10)))),
                textfont_size=30,
                textfont_family="Courier New, monospace",
                textfont_color="#ffffff",
                showlegend=False,
                hoverinfo='none'
            )
        )
        data.append(
            go.Scatter(
                x=np.arange(20, 110, 10),
                y=[53.5 - 5] * len(np.arange(20, 110, 10)),
                mode='text',
                text=list(map(str, list(np.arange(20, 61, 10) - 10) + list(np.arange(40, 9, -10)))),
                textfont_size=30,
                textfont_family="Courier New, monospace",
                textfont_color="#ffffff",
                showlegend=False,
                hoverinfo='none'
            )
        )
        # Add line of scrimage
        data.append(
            go.Scatter(
                x=[line_of_scrimmage, line_of_scrimmage],
                y=[0, 53.5],
                line_dash='dash',
                line_color='blue',
                showlegend=False,
                hoverinfo='none'
            )
        )
        # Add First down line
        data.append(
            go.Scatter(
                x=[first_down_marker, first_down_marker],
                y=[0, 53.5],
                line_dash='dash',
                line_color='yellow',
                showlegend=False,
                hoverinfo='none'
            )
        )
        # Add Endzone Colors
        endzoneColors = {0: color_orders[selected_game_df['homeTeamAbbr'].values[0]][0],
                         110: color_orders[selected_game_df['visitorTeamAbbr'].values[0]][0]}
        for x_min in [0, 110]:
            data.append(
                go.Scatter(
                    x=[x_min, x_min, x_min + 10, x_min + 10, x_min],
                    y=[0, 53.5, 53.5, 0, 0],
                    fill="toself",
                    fillcolor=endzoneColors[x_min],
                    mode="lines",
                    line=dict(
                        color="white",
                        width=3
                    ),
                    opacity=1,
                    showlegend=False,
                    hoverinfo="skip"
                )
            )
        # Plot Players
        for team in selected_tracking_df['club'].unique():
            plot_df = selected_tracking_df.loc[(selected_tracking_df['club'] == team) & (
                    selected_tracking_df['frameId'] == frameId)].copy()

            if team != 'football':
                hover_text_array = []

                for nflId in plot_df['nflId'].unique():
                    selected_player_df = plot_df.loc[plot_df['nflId'] == nflId]
                    nflId = int(selected_player_df['nflId'].values[0])
                    displayName = selected_player_df['displayName'].values[0]
                    s = round(selected_player_df['s'].values[0] * 2.23693629205, 3)
                    text_to_append = f"nflId:{nflId}<br>displayName:{displayName}<br>Player Speed:{s} MPH"
                    hover_text_array.append(text_to_append)

                data.append(go.Scatter(x=plot_df['x'], y=plot_df['y'],
                                       mode='markers',
                                       marker=go.scatter.Marker(color=color_orders[team][0],
                                                                line=go.scatter.marker.Line(width=2,
                                                                                            color=
                                                                                            color_orders[
                                                                                                team][
                                                                                                1]),
                                                                size=10),
                                       name=team, hovertext=hover_text_array, hoverinfo='text'))
            else:
                data.append(go.Scatter(x=plot_df['x'], y=plot_df['y'],
                                       mode='markers',
                                       marker=go.scatter.Marker(
                                           color=color_orders[team][0],
                                           line=go.scatter.marker.Line(width=2,
                                                                       color=color_orders[team][1]),
                                           size=10),
                                       name=team, hoverinfo='none'))
        # add frame to slider
        slider_step = {'args': [
            [frameId],
            {'frame': {'duration': 100, 'redraw': False},
             'mode': 'immediate',
             'transition': {'duration': 0}}
        ],
            'label': str(frameId),
            'method': 'animate'}
        sliders_dict['steps'].append(slider_step)
        frames.append(go.Frame(data=data, name=str(frameId)))

    scale = 10
    layout = go.Layout(
        autosize=False,
        width=120 * scale,
        height=60 * scale,
        xaxis=dict(range=[0, 120], autorange=False, tickmode='array',
                   tickvals=np.arange(10, 111, 5).tolist(), showticklabels=False),
        yaxis=dict(range=[0, 53.3], autorange=False, showgrid=False, showticklabels=False),

        plot_bgcolor='#00B140',
        # Create title and add play description at the bottom of the chart for better visual appeal
        title=f"GameId: {gameId}, PlayId: {playId}<br>{game_clock} {quarter}Q" + "<br>" * 19 + f"{play_description}",
        updatemenus=updatemenus_dict,
        sliders=[sliders_dict]
    )

    fig = go.Figure(
        data=frames[0]['data'],
        layout=layout,
        frames=frames[1:]
    )
    # Create First Down Markers
    for y_val in [0, 53]:
        fig.add_annotation(
            x=first_down_marker,
            y=y_val,
            text=str(down),
            showarrow=False,
            font=dict(
                family="Courier New, monospace",
                size=16,
                color="black"
            ),
            align="center",
            bordercolor="black",
            borderwidth=2,
            borderpad=4,
            bgcolor="#ff7f0e",
            opacity=1
        )
    # Add Team Abbreviations in EndZone's
    for x_min in [0, 110]:
        if x_min == 0:
            angle = 270
            teamName = selected_game_df['homeTeamAbbr'].values[0]
        else:
            angle = 90
            teamName = selected_game_df['visitorTeamAbbr'].values[0]
        fig.add_annotation(
            x=x_min + 5,
            y=53.5 / 2,
            text=teamName,
            showarrow=False,
            font=dict(
                family="Courier New, monospace",
                size=32,
                color="White"
            ),
            textangle=angle
        )
    return fig
