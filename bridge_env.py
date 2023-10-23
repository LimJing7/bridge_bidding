# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 13:35:48 2023

@author: Lim Jing
"""

from contract_score import Contract
from useful_enums import Bid, Position, Vuln


import json
import gymnasium as gym
from gymnasium import spaces
import pygame
import numpy as np


class Bridge(gym.Env):
    metadata = {"render_modes": ["ansi"], "render_fps": 4}

    def __init__(self, render_mode=None, base_type=None):
        self.base_type = base_type
        self.all_hands = json.load(open('./data/Hands_000001_000011.json'))
        self.all_makes = json.load(open('./data/Scores_000001_000011.json'))
        self.n_boards = len(self.all_hands)

        # Observations are dictionaries.
        # bid_history is a sequence of bids
        # hand is a 52 bit vector C2-A, D2-A, H2-A, S2-A
        # vuln is a 1 bit vector showing if it's vulnerable
        self.observation_space = spaces.Dict({
            'bid_history': spaces.Sequence(spaces.Discrete(5*7+3)),
            'hand': spaces.MultiBinary(52),
            'vuln': spaces.MultiBinary(1)
        })

        # We have 5*7 actions + pass, double, redouble
        self.action_space = spaces.Discrete(5*7+3)


        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        """
        If human-rendering is used, `self.window` will be a reference
        to the window that we draw to. `self.clock` will be a clock that is used
        to ensure that the environment is rendered at the correct framerate in
        human-mode. They will remain `None` until human-mode is used for the
        first time.
        """
        self.window = None
        self.clock = None
        
    def _parse_suit(self, suit_str: str):
        output = [0]*13
        for card in suit_str:
            try:
                output[int(card)-2] = 1
            except ValueError:
                if card == 'T':
                    output[8] = 1
                elif card == 'J':
                    output[9] = 1
                elif card == 'Q':
                    output[10] = 1
                elif card == 'K':
                    output[11] = 1
                elif card == 'A':
                    output[12] = 1
        return output
        
    def _parse_hand(self, hand_dict):
        club_list = self._parse_suit(hand_dict['C'])
        diamond_list = self._parse_suit(hand_dict['D'])
        heart_list = self._parse_suit(hand_dict['H'])
        spade_list = self._parse_suit(hand_dict['S'])
        return club_list + diamond_list + heart_list + spade_list

    def _parse_hands(self, hands_dict):
        output = {Position.NORTH: self._parse_hand(hands_dict['N']),
                  Position.EAST:  self._parse_hand(hands_dict['E']),
                  Position.SOUTH: self._parse_hand(hands_dict['S']),
                  Position.WEST:  self._parse_hand(hands_dict['W'])}
        return output

    def _parse_makes(self, makes_dict):
        output = {Position.NORTH: makes_dict['N'],
                  Position.EAST:  makes_dict['E'],
                  Position.SOUTH: makes_dict['S'],
                  Position.WEST:  makes_dict['W']}
        return output
        
    
    def _load_board(self):
        self.board_id = int(self.np_random.random() * (self.n_boards-1)) + 1
        self.current_board = self._parse_hands(self.all_hands[f'{self.board_id}'])
        self.current_makes = self._parse_makes(self.all_makes[f'{self.board_id}'])
    
    
    def _get_obs(self):
        hand_vector = self.current_board[self.current_position]
        vuln = self._get_vuln()
        return {'bid_history': self.bid_history,
                'hand': hand_vector,
                'vuln': vuln}
    
    def _get_reward(self):
        """
        compute the reward of the latest bid relative to passing

        Returns
        -------
        int
            reward difference from passing

        """
        latest_bid = self.bid_history[-1]
        latest_bid_name = latest_bid.name
        if latest_bid == Bid.P:
            return 0
        else:
            current_contract = Contract(level=latest_bid_name[-1], suit=latest_bid_name[:-1], doubles='', vuln=self._get_vuln())
            current_score = current_contract.score(self.current_makes[self.current_position][latest_bid_name[:-1]])
            self.score_info.append(current_score)
            reward = current_score - self.prev_score
            self.prev_score = current_score
        return reward

    def _get_info(self):
        return self.score_info
    
    def _get_vuln(self):
        if self.vuln == Vuln.NONE:
            return 0
        elif self.vuln == Vuln.ALL:
            return 1
        elif self.vuln == Vuln.NS:
            if self.current_position == Position.NORTH or self.current_position == Position.SOUTH:
                return 1
            else:
                return 0
        elif self.vuln == Vuln.EW:
            if self.current_position == Position.EAST or self.current_position == Position.WEST:
                return 1
            else:
                return 0
        return 0
    
    def _check_terminated(self):
        if len(self.bid_history) < 4:
            return False
        if self.bid_history[-3:] == [Bid.P, Bid.P, Bid.P]:
            return True
        else:
            return False
        
    def reset(self, seed=None, options=None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)
    
        self._load_board()
        self.bid_history = []
        self.score_info = []
        self.current_position = Position(self.np_random.choice(list(Position)))
        self.vuln = Vuln(self.np_random.choice(list(Vuln)))

        observation = self._get_obs()
        info = self._get_info()
        self.prev_score = 0
    
        if self.render_mode == "human":
            self._render_frame()
    
        return observation, info
        
        
    def step(self, action):
        self.bid_history.append(Bid(action))
        
        observation = self._get_obs()
        reward = self._get_reward()
        info = self._get_info()
        
        self.bid_history.append(Bid.P)  # opponents are passing
        terminated = self._check_terminated()
        self.current_position = Position((self.current_position+2)%4)
    
        if self.render_mode == "human":
            self._render_frame()
    
        return observation, reward, terminated, False, info
