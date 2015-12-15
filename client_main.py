import sys
import argparse

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, GdkPixbuf, GLib

from client.ClientMessage import ClientMessage
from common.Message import Message
from common.MessageEnum import MessageEnum
from common.TurnEnum import TurnEnum
from common.PlayerEnum import PlayerEnum
from observer.observer import Observer, observerObject

class CluelessApp(object):
    def __init__(self):
        self._init_variable_names()
        
        self._builder = Gtk.Builder()
        self._builder.add_from_file(r'.\view\Clueless.glade')
        self._set_images()
        self._create_objects()
        
        self._connect_signals()
        self._connect_window.show()
        
        self._client_message = ClientMessage()
        self._client_message.set_gui_callback(self._poll)
        
        self._turn_state = None
        
    def _set_images(self):
        """Setup buffers and initial states"""
        #=======================================================================
        # Room buffers
        #=======================================================================
        room_width = 150
        room_height = 150
        hallway_width = 80
        hallway_height = 80
        card_width = 165
        card_height = 250
        token_width = 25
        token_height = 25
        
        self._study_buf = self._pixbuf_scale(self._study_room_path, room_width, room_height)
        self._hall_buf = self._pixbuf_scale(self._hall_room_path, room_width, room_height)
        self._lounge_buf = self._pixbuf_scale(self._lounge_room_path, room_width, room_height)
        self._library_buf = self._pixbuf_scale(self._library_room_path, room_width, room_height)
        self._billiard_buf = self._pixbuf_scale(self._billiard_room_path, room_width, room_height)
        self._dining_buf = self._pixbuf_scale(self._dining_room_path, room_width, room_height)
        self._conservatory_buf = self._pixbuf_scale(self._conservatory_room_path, room_width, room_height)
        self._ballroom_buf = self._pixbuf_scale(self._ballroom_path, room_width, room_height)
        self._kitchen_buf = self._pixbuf_scale(self._kitchen_room_path, room_width, room_height)
        
        self._hallway_s_h_buf = self._pixbuf_scale(self._hallway_path, hallway_width, hallway_height)
        self._hallway_h_l_buf = self._pixbuf_scale(self._hallway_path, hallway_width, hallway_height)
        self._hallway_s_l_buf = self._pixbuf_scale(self._hallway_path, hallway_width, hallway_height)
        self._hallway_l_d_buf = self._pixbuf_scale(self._hallway_path, hallway_width, hallway_height)
        self._hallway_l_bi_buf = self._pixbuf_scale(self._hallway_path, hallway_width, hallway_height)
        self._hallway_l_c_buf = self._pixbuf_scale(self._hallway_path, hallway_width, hallway_height)
        self._hallway_d_k_buf = self._pixbuf_scale(self._hallway_path, hallway_width, hallway_height)
        self._hallway_c_ba_buf = self._pixbuf_scale(self._hallway_path, hallway_width, hallway_height)
        self._hallway_ba_k_buf = self._pixbuf_scale(self._hallway_path, hallway_width, hallway_height)
        self._hallway_d_bi_buf = self._pixbuf_scale(self._hallway_path, hallway_width, hallway_height)
        self._hallway_h_bi_buf = self._pixbuf_scale(self._hallway_path, hallway_width, hallway_height)
        self._hallway_ba_bi_buf = self._pixbuf_scale(self._hallway_path, hallway_width, hallway_height)
        
        #=======================================================================
        # Card buffers
        #=======================================================================
        # Blank
        self._blank_card_buf = self._pixbuf_scale(self._blank_path, card_width, card_height)
        
        # People
        self._colonel_mustard_card_buf = self._pixbuf_scale(self._colonel_mustard_card_path, card_width, card_height)
        self._miss_scarlet_card_buf = self._pixbuf_scale(self._miss_scarlet_card_path, card_width, card_height)
        self._mr_green_card_buf = self._pixbuf_scale(self._mr_green_card_path, card_width, card_height)
        self._mrs_peacock_card_buf = self._pixbuf_scale(self._mrs_peacock_card_path, card_width, card_height)
        self._mrs_white_card_buf = self._pixbuf_scale(self._mrs_white_card_path, card_width, card_height)
        self._professor_plum_card_buf = self._pixbuf_scale(self._professor_plum_card_path, card_width, card_height)
        
        self._people_card_buffers = [self._miss_scarlet_card_buf,
                                     self._colonel_mustard_card_buf,
                                     self._professor_plum_card_buf,
                                     self._mr_green_card_buf,
                                     self._mrs_white_card_buf,
                                     self._mrs_peacock_card_buf,
                                    ]
        
        # Rooms
        self._study_card_buf = self._pixbuf_scale(self._study_room_path, card_width, card_height)
        self._hall_card_buf = self._pixbuf_scale(self._hall_room_path, card_width, card_height)
        self._lounge_card_buf = self._pixbuf_scale(self._lounge_room_path, card_width, card_height)
        self._library_card_buf = self._pixbuf_scale(self._library_room_path, card_width, card_height)
        self._billiard_card_buf = self._pixbuf_scale(self._billiard_room_path, card_width, card_height)
        self._dining_card_buf = self._pixbuf_scale(self._dining_room_path, card_width, card_height)
        self._conservatory_card_buf = self._pixbuf_scale(self._conservatory_room_path, card_width, card_height)
        self._ballroom_card_buf = self._pixbuf_scale(self._ballroom_path, card_width, card_height)
        self._kitchen_card_buf = self._pixbuf_scale(self._kitchen_room_path, card_width, card_height)
        
        self._room_card_buffers = [self._study_card_buf,
                                   self._hall_card_buf,
                                   self._lounge_card_buf,
                                   self._dining_card_buf,
                                   self._kitchen_card_buf,
                                   self._ballroom_card_buf,
                                   self._conservatory_card_buf,
                                   self._library_card_buf,
                                   self._billiard_card_buf,
                                   ]
        
        # Weapons
        self._candlestick_card_buf = self._pixbuf_scale(self._candlestick_card_path, card_width, card_height)
        self._knife_card_buf = self._pixbuf_scale(self._knife_card_path, card_width, card_height)
        self._lead_pipe_card_buf = self._pixbuf_scale(self._lead_pipe_card_path, card_width, card_height)
        self._revolver_card_buf = self._pixbuf_scale(self._revolver_card_path, card_width, card_height)
        self._rope_card_buf = self._pixbuf_scale(self._rope_card_path, card_width, card_height)
        self._wrench_card_buf = self._pixbuf_scale(self._wrench_card_path, card_width, card_height)
        
        self._weapon_card_buffers = [self._candlestick_card_buf,
                                     self._rope_card_buf,
                                     self._lead_pipe_card_buf,
                                     self._revolver_card_buf,
                                     self._wrench_card_buf,
                                     self._knife_card_buf,
                                    ]
        
        #=======================================================================
        # Token buffers
        #=======================================================================
        # People
        self._colonel_mustard_token_buf = self._pixbuf_scale(self._colonel_mustard_token_path, token_width, token_height)
        self._miss_scarlet_token_buf = self._pixbuf_scale(self._miss_scarlet_token_path, token_width, token_height)
        self._mr_green_token_buf = self._pixbuf_scale(self._mr_green_token_path, token_width, token_height)
        self._mrs_peacock_token_buf = self._pixbuf_scale(self._mrs_peacock_token_path, token_width, token_height)
        self._mrs_white_token_buf = self._pixbuf_scale(self._mrs_white_token_path, token_width, token_height)
        self._professor_plum_token_buf = self._pixbuf_scale(self._professor_plum_token_path, token_width, token_height)
        
        self._people_token_buffers = [self._miss_scarlet_token_buf,
                                      self._colonel_mustard_token_buf,
                                      self._professor_plum_token_buf,
                                      self._mr_green_token_buf,
                                      self._mrs_white_token_buf,
                                      self._mrs_peacock_token_buf,
                                     ]
        
        # Weapons
        self._candlestick_token_buf = self._pixbuf_scale(self._candlestick_token_path, token_width, token_height)
        self._knife_token_buf = self._pixbuf_scale(self._knife_token_path, token_width, token_height)
        self._lead_pipe_token_buf = self._pixbuf_scale(self._lead_pipe_token_path, token_width, token_height)
        self._revolver_token_buf = self._pixbuf_scale(self._revolver_token_path, token_width, token_height)
        self._rope_token_buf = self._pixbuf_scale(self._rope_token_path, token_width, token_height)
        self._wrench_token_buf = self._pixbuf_scale(self._wrench_token_path, token_width, token_height)
        
        self._weapon_token_buffers = [self._candlestick_token_buf,
                                      self._rope_token_buf,
                                      self._lead_pipe_token_buf,
                                      self._revolver_token_buf,
                                      self._wrench_token_buf,
                                      self._knife_token_buf,
                                     ]
        
        #=======================================================================
        # Initial Setup
        #=======================================================================
        
        # Board        
        self._set_button_image(self._builder.get_object(self._study_room), self._study_buf)
        self._set_button_image(self._builder.get_object(self._hallway_s_h), self._hallway_s_h_buf)
        self._set_button_image(self._builder.get_object(self._hall_room), self._hall_buf)
        self._set_button_image(self._builder.get_object(self._hallway_h_l), self._hallway_h_l_buf)
        self._set_button_image(self._builder.get_object(self._lounge_room), self._lounge_buf)
        self._set_button_image(self._builder.get_object(self._hallway_s_l), self._hallway_s_l_buf)
        self._set_button_image(self._builder.get_object(self._hallway_l_d), self._hallway_l_d_buf)
        self._set_button_image(self._builder.get_object(self._library_room), self._library_buf)
        self._set_button_image(self._builder.get_object(self._hallway_l_bi), self._hallway_l_bi_buf)
        self._set_button_image(self._builder.get_object(self._billiard_room), self._billiard_buf)
        self._set_button_image(self._builder.get_object(self._dining_room), self._dining_buf)
        self._set_button_image(self._builder.get_object(self._hallway_l_c), self._hallway_l_c_buf)
        self._set_button_image(self._builder.get_object(self._hallway_d_k), self._hallway_d_k_buf)
        self._set_button_image(self._builder.get_object(self._conservatory_room), self._conservatory_buf)
        self._set_button_image(self._builder.get_object(self._hallway_c_ba), self._hallway_c_ba_buf)
        self._set_button_image(self._builder.get_object(self._ballroom), self._ballroom_buf)
        self._set_button_image(self._builder.get_object(self._hallway_ba_k), self._hallway_ba_k_buf)
        self._set_button_image(self._builder.get_object(self._kitchen_room), self._kitchen_buf)
        self._set_button_image(self._builder.get_object(self._hallway_d_bi), self._hallway_d_bi_buf)
        self._set_button_image(self._builder.get_object(self._hallway_h_bi), self._hallway_h_bi_buf)
        self._set_button_image(self._builder.get_object(self._hallway_ba_bi), self._hallway_ba_bi_buf)
        
        self._room_objects = [self._builder.get_object(self._study_room),
                              self._builder.get_object(self._hall_room),
                              self._builder.get_object(self._lounge_room),
                              self._builder.get_object(self._dining_room),
                              self._builder.get_object(self._kitchen_room),
                              self._builder.get_object(self._ballroom),
                              self._builder.get_object(self._conservatory_room),
                              self._builder.get_object(self._library_room),
                              self._builder.get_object(self._billiard_room),
                              self._builder.get_object(self._hallway_s_h),
                              self._builder.get_object(self._hallway_h_l),
                              self._builder.get_object(self._hallway_l_d),
                              self._builder.get_object(self._hallway_d_k),
                              self._builder.get_object(self._hallway_ba_k),
                              self._builder.get_object(self._hallway_c_ba),
                              self._builder.get_object(self._hallway_l_c),
                              self._builder.get_object(self._hallway_s_l),
                              self._builder.get_object(self._hallway_h_bi),
                              self._builder.get_object(self._hallway_d_bi),
                              self._builder.get_object(self._hallway_ba_bi),
                              self._builder.get_object(self._hallway_l_bi)
                             ]
        
        for i in range(0, len(self._room_objects)):
            self._room_objects[i].set_sensitive(False)
            self._room_objects[i].connect('clicked', self._move, i + 1)
        
        img = Gtk.Image()
        img.set_from_pixbuf(self._blank_card_buf)
        
        self._builder.get_object(self._suggest_person).set_always_show_image(True)
        self._builder.get_object(self._suggest_person).set_image(img)

        img = Gtk.Image()
        img.set_from_pixbuf(self._blank_card_buf)
        
        self._builder.get_object(self._suggest_room).set_always_show_image(True)
        self._builder.get_object(self._suggest_room).set_image(img)
        
        img = Gtk.Image()
        img.set_from_pixbuf(self._blank_card_buf)
        
        self._builder.get_object(self._suggest_weapon).set_always_show_image(True)
        self._builder.get_object(self._suggest_weapon).set_image(img)
        
        #=======================================================================
        # People picker
        #=======================================================================
        # for i in range(0, len(self._people_picker)):
            # self._people_picker[i].set_from_pixbuf(self._people_card_buffers[i])
        
    def _create_objects(self):
        #=======================================================================
        # Windows
        #=======================================================================
        self._board_window = self._builder.get_object(self._board_window_name)
        self._connect_window = self._builder.get_object(self._connect_window_name)
        self._lobby_window = self._builder.get_object(self._lobby_window_name)
        self._person_select_window = self._builder.get_object(self._person_select)
        self._weapon_select_window = self._builder.get_object(self._weapon_select)
        self._room_select_window = self._builder.get_object(self._room_select)
        
        #=======================================================================
        # Connect window objects
        #=======================================================================
        self._connect_button_object = self._builder.get_object(self._connect_button)
        self._ip_entry_object = self._builder.get_object(self._ip_entry)
        self._port_entry_object = self._builder.get_object(self._port_entry)
        self._connect_label_object = self._builder.get_object(self._connect_label)
        
        #======================================================================
        # Lobby window objects
        #======================================================================
        self._lobby_button_object = self._builder.get_object(self._lobby_button)
        
        self._player_objects = []
        for p in self._players:
            self._player_objects.append(self._builder.get_object(p))
        
        #=======================================================================
        # Board window objects
        #=======================================================================
        self._accuse_button_object = self._builder.get_object(self._accuse_button)
        self._action_button_object = self._builder.get_object(self._action_button)
        
        self._accuse_button_object.connect('clicked', self._accuse)
        self._action_button_object.connect('clicked', self._suggest)
        
        self._suggest_person_object = self._builder.get_object(self._suggest_person)
        self._suggest_weapon_object = self._builder.get_object(self._suggest_weapon)
        self._suggest_room_object = self._builder.get_object(self._suggest_room)
        
        self._pass_button_object = self._builder.get_object(self._pass_button)
        self._pass_button_object.connect('clicked', self._pass)
        
        self._end_turn_button_object = self._builder.get_object(self._end_turn_button)
        self._end_turn_button_object.connect('clicked', self._end_turn)
        
        #=======================================================================
        # People view objects
        #=======================================================================
        for i in range(0, len(self._people_card_window_buttons)):
            button = self._builder.get_object(self._people_card_window_buttons[i])
            button.set_always_show_image(True)
            img = Gtk.Image()
            img.set_from_pixbuf(self._people_card_buffers[i])
            button.set_image(img)
            
        #=======================================================================
        # Weapon view objects
        #=======================================================================
        for i in range(0, len(self._weapon_card_window_buttons)):
            button = self._builder.get_object(self._weapon_card_window_buttons[i])
            button.set_always_show_image(True)
            img = Gtk.Image()
            img.set_from_pixbuf(self._weapon_card_buffers[i])
            button.set_image(img)
            
        #=======================================================================
        # Room view objects
        #=======================================================================
        for i in range(0, len(self._room_card_window_buttons)):
            button = self._builder.get_object(self._room_card_window_buttons[i])
            button.set_always_show_image(True)
            img = Gtk.Image()
            img.set_from_pixbuf(self._room_card_buffers[i])
            button.set_image(img)
        
    def _init_variable_names(self):
        """Initialize paths to assets."""
        
        #=======================================================================
        # Relative path to the asset folder 
        #=======================================================================
        self._asset_path = r'view\assets\\'
        
        #=======================================================================
        # Window names for the different views
        #=======================================================================
        self._board_window_name = 'board_window'
        self._connect_window_name = 'connect_window'
        self._lobby_window_name = 'lobby_window'
        self._person_select = 'people_selection_window'
        self._weapon_select = 'weapon_selection_window'
        self._room_select = 'room_selection_window'
        
        #=======================================================================
        # Object names from the board view
        #=======================================================================
        # Rooms
        self._study_room = 'study_room'
        self._hall_room = 'hall_room'
        self._lounge_room = 'lounge_room'
        self._library_room = 'library_room'
        self._billiard_room = 'billiard_room'
        self._dining_room = 'dining_room'
        self._conservatory_room = 'conservatory_room'
        self._ballroom = 'ballroom_room'
        self._kitchen_room = 'kitchen_room'
        
        # Hallways
        self._hallway_s_h = 'study_hall_hallway'
        self._hallway_h_l = 'hall_lounge_hallway'
        self._hallway_s_l = 'study_library_hallway'
        self._hallway_l_d = 'lounge_dining_room_hallway'
        self._hallway_l_bi = 'library_billiard_room_hallway'
        self._hallway_l_c = 'library_conservatory_hallway'
        self._hallway_d_k = 'dining_room_kitchen_hallway'
        self._hallway_c_ba = 'conservatory_ballroom_hallway'
        self._hallway_ba_k = 'ballroom_kitchen_hallway'
        self._hallway_d_bi = 'dining_room_billiard_room_hallway'
        self._hallway_ba_bi = 'ballroom_billiard_room_hallway'
        self._hallway_h_bi = 'hall_billiard_room_hallway'
        
        # Suggestion cards
        self._suggest_person = 'suggest_person'
        self._suggest_weapon = 'suggest_weapon'
        self._suggest_room = 'suggest_room'
        
        # Status label
        self._status_label = 'status_label'
        
        #=======================================================================
        # Object names from the connect view
        #=======================================================================
        self._ip_entry = 'ip_entry'
        self._port_entry = 'port_entry'
        self._connect_button = 'connect_button'
        self._connect_label = 'connect_status_label'
        
        #=======================================================================
        # Object names from the lobby view
        #=======================================================================
        self._lobby_button = 'lobby_ready_button'
        
        self._players = ['player_label_1',
                         'player_label_2',
                         'player_label_3',
                         'player_label_4',
                         'player_label_5',
                         'player_label_6',
                         ]
        
        #=======================================================================
        # Object names from the board view
        #=======================================================================
        self._accuse_button = 'accuse_button'
        self._action_button = 'action_button'
        
        #=======================================================================
        # Hand Grid
        #=======================================================================
        self._hand_grid = 'grid_hand'
        
        self._hand_grid_images = ['hand_image1',
                                  'hand_image2',
                                  'hand_image3',
                                  'hand_image4',
                                  'hand_image5',
                                  'hand_image6',
                                  'hand_image7',
                                  'hand_image8',
                                  'hand_image9',
                                 ]
        
        self._pass_button = 'pass_button'
        self._end_turn_button = 'end_turn_button'
        
        #=======================================================================
        # People images
        #=======================================================================        
        self._people_card_window_buttons = ['people_button_1',
                                            'people_button_2',
                                            'people_button_3',
                                            'people_button_4',
                                            'people_button_5',
                                            'people_button_6',
                                           ]
        
        self._weapon_card_window_buttons = ['weapon_button_1',
                                            'weapon_button_2',
                                            'weapon_button_3',
                                            'weapon_button_4',
                                            'weapon_button_5',
                                            'weapon_button_6',
                                           ]
        
        self._room_card_window_buttons = ['room_button_1',
                                          'room_button_2',
                                          'room_button_3',
                                          'room_button_4',
                                          'room_button_5',
                                          'room_button_6',
                                          'room_button_7',
                                          'room_button_8',
                                          'room_button_9',
                                         ]
        
        #=======================================================================
        # Image path building
        #=======================================================================
        # Rooms
        self._ballroom_path = self._asset_path + r'Ballroom.png'
        self._billiard_room_path = self._asset_path + r'BilliardRoom.png'
        self._blank_path = self._asset_path + r'Blank.png'
        self._conservatory_room_path = self._asset_path + r'Conservatory.png'
        self._dining_room_path = self._asset_path + r'DiningRoom.png'
        self._envelope_path = self._asset_path + r'Envelope.png'
        self._hall_room_path = self._asset_path + r'Hall.png'
        self._hallway_path = self._asset_path + r'Hallway.png'
        self._kitchen_room_path = self._asset_path + r'Kitchen.png'
        self._library_room_path = self._asset_path + r'Library.png'
        self._lounge_room_path = self._asset_path + r'Lounge.png'
        self._room_selection_box_path = self._asset_path + r'Selection.png'
        self._study_room_path = self._asset_path + r'Study.png'
        
        # People
        self._colonel_mustard_card_path = self._asset_path + r'ColonelMustard_Card.png'  
        self._miss_scarlet_card_path = self._asset_path + r'MissScarlet_Card.png'
        self._mr_green_card_path = self._asset_path + r'MrGreen_Card.png'
        self._mrs_peacock_card_path = self._asset_path + r'MrsPeacock_Card.png'
        self._mrs_white_card_path = self._asset_path + r'MrsWhite_Card.png'
        self._professor_plum_card_path = self._asset_path + r'ProfessorPlum_Card.png'
        
        self._colonel_mustard_token_path = self._asset_path + r'ColonelMustard_Token.png'  
        self._miss_scarlet_token_path = self._asset_path + r'MissScarlet_Token.png'
        self._mr_green_token_path = self._asset_path + r'MrGreen_Token.png'
        self._mrs_peacock_token_path = self._asset_path + r'MrsPeacock_Token.png'
        self._mrs_white_token_path = self._asset_path + r'MrsWhite_Token.png'
        self._professor_plum_token_path = self._asset_path + r'ProfessorPlum_Token.png'
        
        # Weapons
        self._candlestick_card_path = self._asset_path + r'Candlestick_Card.png'
        self._knife_card_path = self._asset_path + r'Knife_Card.png'
        self._lead_pipe_card_path = self._asset_path + r'Leadpipe_Card.png'
        self._revolver_card_path = self._asset_path + r'Revolver_Card.png'
        self._rope_card_path = self._asset_path + r'Rope_Card.png'
        self._wrench_card_path = self._asset_path + r'Wrench_Card.png'
        
        self._candlestick_token_path = self._asset_path + r'Candlestick_Token.png'
        self._knife_token_path = self._asset_path + r'Knife_Token.png'
        self._lead_pipe_token_path = self._asset_path + r'Leadpipe_Token.png'
        self._revolver_token_path = self._asset_path + r'Revolver_Token.png'
        self._rope_token_path = self._asset_path + r'Rope_Token.png'
        self._wrench_token_path = self._asset_path + r'Wrench_Token.png'
        
    def _setup_grid(self):
        hand = self._client_message.get_cards()
        
        counter = 0
        
        if hand[0]:
            for i in range(0, len(hand[0])):
                self._set_button_image(self._builder.get_object(self._hand_grid_images[counter]), self._people_card_buffers[hand[0][i] - 1])
                self._builder.get_object(self._hand_grid_images[counter]).connect('clicked', self._disprove, 0, i)
                counter = counter + 1
            
        if hand[1]:
            for i in range(0, len(hand[1])):
                self._set_button_image(self._builder.get_object(self._hand_grid_images[counter]), self._weapon_card_buffers[hand[1][i] - 1])
                self._builder.get_object(self._hand_grid_images[counter]).connect('clicked', self._disprove, 1, i)
                counter = counter + 1
            
        if hand[2]:
            for i in range(0, len(hand[2])):
                self._set_button_image(self._builder.get_object(self._hand_grid_images[counter]), self._room_card_buffers[hand[2][i] - 1])
                self._builder.get_object(self._hand_grid_images[counter]).connect('clicked', self._disprove, 2, i)
                counter = counter + 1
            
        for i in range(counter, len(self._hand_grid_images)):
            self._builder.get_object(self._hand_grid_images[i]).hide()
        
    def _pixbuf_scale(self, path, width, height):
        return GdkPixbuf.Pixbuf.new_from_file(path).scale_simple(width, height, GdkPixbuf.InterpType.BILINEAR)
    
    def _connect_signals(self):
        self._connect_button_object.connect('clicked', self._connect_to_server)
        self._lobby_button_object.connect('clicked', self._ready_up)
        self._connect_window.connect('delete_event', self._exit_app)
        self._lobby_window.connect('delete_event', self._exit_app)
        self._board_window.connect('delete_event', self._exit_app)
        
        self._suggest_person_object.connect('clicked', self._open_person_select)
        self._suggest_weapon_object.connect('clicked', self._open_weapon_select)
        self._suggest_room_object.connect('clicked', self._open_room_select)
        
        for i in range(0, len(self._people_card_window_buttons)):
            self._builder.get_object(self._people_card_window_buttons[i]).connect('clicked', self._person_selected, self._people_card_buffers[i])
            
        for i in range(0, len(self._weapon_card_window_buttons)):
            self._builder.get_object(self._weapon_card_window_buttons[i]).connect('clicked', self._weapon_selected, self._weapon_card_buffers[i])
            
        for i in range(0, len(self._room_card_window_buttons)):
            self._builder.get_object(self._room_card_window_buttons[i]).connect('clicked', self._room_selected, self._room_card_buffers[i])
        
    def _poll(self):
        print 'Polling!'
        if self._lobby_window.get_visible():
            is_ready = True
            lobby = self._client_message.return_client_model_instance().get_lobby_list()
            player_string = PlayerEnum.to_string(self._client_message.return_client_model_instance().get_character())
            print player_string
            for i in range(0, len(lobby)):
                self._player_objects[i].set_text(lobby[i][0])
                self._player_objects[i].show()
                if lobby[i][1] == False:
                    is_ready = False
            if is_ready and len(lobby) >= 2:
                self._lobby_window.hide()
                self._setup_grid()
                GLib.idle_add(self._board_window.show)
        elif self._board_window.get_visible():
            suggestion = self._client_message.get_suggestion()
            self._set_tokens()
            if suggestion:
                # Suggestion
                self._set_button_image(self._suggest_person_object, self._people_card_buffers[suggestion[0] - 1])
                self._set_button_image(self._suggest_weapon_object, self._weapon_card_buffers[suggestion[1] - 1])
                self._set_button_image(self._suggest_room_object, self._room_card_buffers[suggestion[2] - 1])
            if self._client_message.return_client_model_instance().is_my_turn():
                if self._turn_state is None:
                    self._turn_state = TurnEnum.MOVE
                    
                    valid_moves = self._client_message.return_client_model_instance().get_valid_moves(self._client_message.return_client_model_instance().get_character_position())
                    if valid_moves:
                        for m in valid_moves:
                            self._room_objects[m].set_sensitive(True)
                    else:
                        self._end_turn_button_object.set_sensitive(True)
                        
                if self._turn_state is TurnEnum.SUGGEST:
                    self._suggest_person_object.set_sensitive(True)
                    self._suggest_weapon_object.set_sensitive(True)
                    self._suggest_room_object.set_sensitive(True)
                    self._check_enable_suggest_buttons()                
            else:
                if self._client_message.return_client_model_instance().get_disprove_status():
                    hand = self._client_message.get_cards()
                    if not self._has_valid_disprove(suggestion, hand):
                        self._pass_button_object.set_sensitive(True)
                self._suggest_person_object.set_sensitive(False)
                self._suggest_weapon_object.set_sensitive(False)
                self._suggest_room_object.set_sensitive(False)
                self._action_button_object.set_sensitive(False)
                self._accuse_button_object.set_sensitive(False)
        
    def _connect_to_server(self, widget):
        try:
            connected = self._client_message.connect_to_server(self._ip_entry_object.get_text(), int(self._port_entry_object.get_text()))
            
            # Create the observer
            if connected == True:
                obsObj = observerObject()
                observer = Observer(obsObj.subject)
                observer.registerCallback(self._client_message.handle_message)
                
                self._connect_window.hide()
                self._lobby_window.show()
            else:
                self._connect_label_object.set_text('Failed to connect to server.')
                self._connect_label_object.show()
        except ValueError:
            self._connect_label_object.set_text('Invalid port.')
            self._connect_label_object.show()
        
    def _ready_up(self, widget):
        self._client_message.send_message(Message(MessageEnum.LOBBY_READY, 1, [True]))
        self._lobby_button_object.set_sensitive(False)
        
    def _init_board(self):
        pass
        
    def _exit_app(self, widget, data=None):
        # self._client_message.close_connection()
        sys.exit()
        
    def _set_ip(self, ip):
        self._ip_entry_object.set_text(ip)
        
    def _set_port(self, port):
        self._port_entry_object.set_text(port)
        
    def _open_person_select(self, widget):
        GLib.idle_add(self._person_select_window.show)
        
    def _person_selected(self, widget, *data):
        img = Gtk.Image()
        img.set_from_pixbuf(data[0])
        self._suggest_person_object.set_image(img)
        self._person_select_window.hide()
        
        self._check_enable_suggest_buttons()
        
    def _open_weapon_select(self, widget):
        GLib.idle_add(self._weapon_select_window.show)
        
    def _weapon_selected(self, widget, *data):
        img = Gtk.Image()
        img.set_from_pixbuf(data[0])
        self._suggest_weapon_object.set_image(img)
        self._weapon_select_window.hide()
        
        self._check_enable_suggest_buttons()
        
    def _open_room_select(self, widget):
        GLib.idle_add(self._room_select_window.show)
        
    def _room_selected(self, widget, *data):
        img = Gtk.Image()
        img.set_from_pixbuf(data[0])
        self._suggest_room_object.set_image(img)
        self._room_select_window.hide()
        
        self._check_enable_suggest_buttons()
        
    def _check_enable_suggest_buttons(self):
        if self._suggest_person_object.get_image().get_pixbuf() is not self._blank_card_buf and self._suggest_weapon_object.get_image().get_pixbuf() is not self._blank_card_buf and self._suggest_room_object.get_image().get_pixbuf() is not self._blank_card_buf:
            self._action_button_object.set_sensitive(True)
            self._accuse_button_object.set_sensitive(True)
            
    def _set_button_image(self, button_obj, pixbuf):
        img = Gtk.Image()
        img.set_from_pixbuf(pixbuf)
        button_obj.set_always_show_image(True)
        button_obj.set_image(img)
        
    def _move(self, widget, *data):
        for i in self._room_objects:
            i.set_sensitive(False)
            
        self._turn_state = TurnEnum.SUGGEST
        print data[0]
        self._client_message.send_message(Message(MessageEnum.MOVE, 1, [data[0]]))
        
    def _disprove(self, widget, *data):
        card_type = data[0]
        card_value = data[1]
        
        message_args = [None, None, None]
        
        message_args[card_type] = card_value
        
        self._client_message.return_client_model_instance().set_disprove_status(False)
        self._client_message.send_message(Message(MessageEnum.SUGGEST, 1, message_args))
        
    def _suggest(self, widget):
        message_args = [self._people_card_buffers.index(self._suggest_person_object.get_image().get_pixbuf()),
                        self._weapon_card_buffers.index(self._suggest_weapon_object.get_image().get_pixbuf()),
                        self._room_card_buffers.index(self._suggest_room_object.get_image().get_pixbuf()),
                       ]
        print message_args
        self._client_message.send_message(Message(MessageEnum.SUGGESTION_BEGIN, 1, message_args))
        
    def _pass(self, widget):
        self._pass_button_object.set_sensitive(False)
        
        message_args = [None, None, None]
        
        self._client_message.return_client_model_instance().set_disprove_status(False)
        self._client_message.send_message(self._client_message.send_message(MessageEnum.SUGGEST, 1, message_args))
        
    def _end_turn(self, widget):
        self._end_turn_button_object.set_sensitive(False)
        self._turn_state = TurnEnum.SUGGEST
        self._client_message.send_message(Message(MessageEnum.TURN_OVER, 1, [True]))
        
    def _accuse(self, widget):
        message_args = [self._people_card_buffers.index(self._suggest_person_object.get_image().get_pixbuf()),
                        self._weapon_card_buffers.index(self._suggest_weapon_object.get_image().get_pixbuf()),
                        self._room_card_buffers.index(self._suggest_room_object.get_image().get_pixbuf()),
                       ]
        
        self._client_message.send_message(Message(MessageEnum.ACCUSE, 1, message_args))
        
    def _has_valid_disprove(self, suggestion, hand):
        retval = False
        for s in suggestion:
            for h in hand:
                if s == h:
                    retval = True
                    self._builder.get_object(self._hand_grid_images[s]).set_sensitive(True)
        return retval
    
    def _set_tokens(self):
        room_dict = {}
        
        for p, r in self._client_message.return_client_model_instance().get_character_position_list().iteritems():
            if not r in room_dict:
                room_dict[r] = []
            room_dict[r].append(p)
            
        for r, p_list in room_dict.iteritems():
            col = 0
            row = 0
            
            dest_pixbuf = Gtk.Image().new_from_pixbuf(self._room_objects[r - 1].get_image().get_pixbuf()).get_pixbuf()
            
            for l in p_list:
                src_pixbuf = Gtk.Image().new_from_pixbuf(self._people_token_buffers[l - 1]).get_pixbuf()
                src_pixbuf.composite(dest_pixbuf, 5 + (35 * col), 5 + (35 * row), 25, 25, 0, 0, 1, 1, GdkPixbuf.InterpType.BILINEAR, 255)
                col = col + 1
                if col > 2:
                    col = 0
                    row= row + 1
            
        # Show weapons - not working
        #=======================================================================
        # for w, r in self._client_message.return_client_model_instance().get_weapon_position_list().iteritems():
        #     if not r in room_dict:
        #         room_dict[r] = []
        #     room_dict[r].append(w)
        #     
        # for r, w_list in room_dict.iteritems():
        #     col = 0
        #     row = 0
        #     
        #     dest_pixbuf = Gtk.Image().new_from_pixbuf(self._room_objects[r - 1].get_image().get_pixbuf()).get_pixbuf()
        #     
        #     for l in w_list:
        #         src_pixbuf = Gtk.Image().new_from_pixbuf(self._weapon_token_buffers[l - 1]).get_pixbuf()
        #         src_pixbuf.composite(dest_pixbuf, 120 - (35 * col), 120 - (35 * row), 25, 25, 0, 0, 1, 1, GdkPixbuf.InterpType.BILINEAR, 255)
        #         col = col + 1
        #         if col > 2:
        #             col = 0
        #             row= row + 1
        #=======================================================================
            
        
            
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Host info for Clueless')
    parser.add_argument('-i', help='IP Address')
    parser.add_argument('-p', help='Port')
    
    args = parser.parse_args()
    
    app = CluelessApp()
    
    if args.i:
        app._set_ip(args.i)
    if args.p:
        app._set_port(args.p)
    
    Gtk.main()