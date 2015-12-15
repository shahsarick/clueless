import sys

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, GdkPixbuf

from client.ClientMessage import ClientMessage
from observer.observer import Observer, observerObject


class CluelessApp(object):
    def __init__(self):
        self._init_variable_names()
        
        self._builder = Gtk.Builder()
        self._builder.add_from_file(r'.\view\Clueless.glade')
        self._set_images()
        self._create_objects()
        self._setup_grid()
        self._board_window = self._builder.get_object(self._board_window_name)
        self._connect_window = self._builder.get_object(self._connect_window_name)
        self._lobby_window = self._builder.get_object(self._lobby_window_name)
        
        self._connect_signals()
        self._connect_window.show()
        
        self._client_message = ClientMessage()
        
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
        # People        
        self._colonel_mustard_card_buf = self._pixbuf_scale(self._colonel_mustard_card_path, card_width, card_height)
        self._miss_scarlet_card_buf = self._pixbuf_scale(self._miss_scarlet_card_path, card_width, card_height)
        self._mr_green_card_buf = self._pixbuf_scale(self._mr_green_card_path, card_width, card_height)
        self._mrs_peacock_card_buf = self._pixbuf_scale(self._mrs_peacock_card_path, card_width, card_height)
        self._mrs_white_card_buf = self._pixbuf_scale(self._mrs_white_card_path, card_width, card_height)
        self._professor_plum_card_buf = self._pixbuf_scale(self._professor_plum_card_path, card_width, card_height)
        
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
        
        # Weapons
        self._candlestick_card_buf = self._pixbuf_scale(self._candlestick_card_path, card_width, card_height)
        self._knife_card_buf = self._pixbuf_scale(self._knife_card_path, card_width, card_height)
        self._lead_pipe_card_buf = self._pixbuf_scale(self._lead_pipe_card_path, card_width, card_height)
        self._revolver_card_buf = self._pixbuf_scale(self._revolver_card_path, card_width, card_height)
        self._rope_card_buf = self._pixbuf_scale(self._rope_card_path, card_width, card_height)
        self._wrench_card_buf = self._pixbuf_scale(self._wrench_card_path, card_width, card_height)
        
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
        
        # Weapons
        self._candlestick_token_buf = self._pixbuf_scale(self._candlestick_token_path, token_width, token_height)
        self._knife_token_buf = self._pixbuf_scale(self._knife_token_path, token_width, token_height)
        self._lead_pipe_token_buf = self._pixbuf_scale(self._lead_pipe_token_path, token_width, token_height)
        self._revolver_token_buf = self._pixbuf_scale(self._revolver_token_path, token_width, token_height)
        self._rope_token_buf = self._pixbuf_scale(self._rope_token_path, token_width, token_height)
        self._wrench_token_buf = self._pixbuf_scale(self._wrench_token_path, token_width, token_height)
        
        #=======================================================================
        # Initial Setup
        #=======================================================================
        
        # Board
        self._builder.get_object(self._study_room).set_from_pixbuf(self._study_buf)
        self._builder.get_object(self._hallway_s_h).set_from_pixbuf(self._hallway_s_h_buf)
        self._builder.get_object(self._hall_room).set_from_pixbuf(self._hall_buf)
        self._builder.get_object(self._hallway_h_l).set_from_pixbuf(self._hallway_h_l_buf)
        self._builder.get_object(self._lounge_room).set_from_pixbuf(self._lounge_buf)
        self._builder.get_object(self._hallway_s_l).set_from_pixbuf(self._hallway_s_l_buf)
        self._builder.get_object(self._hallway_l_d).set_from_pixbuf(self._hallway_l_d_buf)
        self._builder.get_object(self._library_room).set_from_pixbuf(self._library_buf)
        self._builder.get_object(self._hallway_l_bi).set_from_pixbuf(self._hallway_l_bi_buf)
        self._builder.get_object(self._billiard_room).set_from_pixbuf(self._billiard_buf)
        self._builder.get_object(self._dining_room).set_from_pixbuf(self._dining_buf)
        self._builder.get_object(self._hallway_l_c).set_from_pixbuf(self._hallway_l_c_buf)
        self._builder.get_object(self._hallway_d_k).set_from_pixbuf(self._hallway_d_k_buf)
        self._builder.get_object(self._conservatory_room).set_from_pixbuf(self._conservatory_buf)
        self._builder.get_object(self._hallway_c_ba).set_from_pixbuf(self._hallway_c_ba_buf)
        self._builder.get_object(self._ballroom).set_from_pixbuf(self._ballroom_buf)
        self._builder.get_object(self._hallway_ba_k).set_from_pixbuf(self._hallway_ba_k_buf)
        self._builder.get_object(self._kitchen_room).set_from_pixbuf(self._kitchen_buf)
        self._builder.get_object(self._hallway_d_bi).set_from_pixbuf(self._hallway_d_bi_buf)
        self._builder.get_object(self._hallway_h_bi).set_from_pixbuf(self._hallway_h_bi_buf)
        self._builder.get_object(self._hallway_ba_bi).set_from_pixbuf(self._hallway_ba_bi_buf)
        
        # Suggestion
        self._builder.get_object(self._suggest_person).set_from_pixbuf(self._colonel_mustard_card_buf)
        self._builder.get_object(self._suggest_weapon).set_from_pixbuf(self._candlestick_card_buf)
        self._builder.get_object(self._suggest_room).set_from_pixbuf(self._study_card_buf)
        
    def _create_objects(self):
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
        
        #=======================================================================
        # Board window objects
        #=======================================================================
        self._accuse_button_object = self._builder.get_object(self._accuse_button)
        self._action_button_object = self._builder.get_object(self._action_button)
        
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
        hand = [self._ballroom_card_buf, self._conservatory_card_buf, self._colonel_mustard_card_buf, self._revolver_card_buf]
        for i in range(0, len(hand)):
            self._builder.get_object(self._hand_grid_images[i]).set_from_pixbuf(hand[i])
        for i in range(len(self._hand_grid_images) - len(hand) - 1, len(self._hand_grid_images)):
            self._builder.get_object(self._hand_grid_images[i]).hide()
        # grid_object.show()
        
    def _pixbuf_scale(self, path, width, height):
        return GdkPixbuf.Pixbuf.new_from_file(path).scale_simple(width, height, GdkPixbuf.InterpType.BILINEAR)
    
    def _connect_signals(self):
        self._connect_button_object.connect('clicked', self._connect_to_server)
        self._lobby_button_object.connect('clicked', self._ready_up)
        self._connect_window.connect('delete_event', self._exit_app)
        self._lobby_window.connect('delete_event', self._exit_app)
        self._board_window.connect('delete_event', self._exit_app)
        
    print 'Need to pass poll into the client'
    def _poll(self):
        if self._lobby_window.visible:
            pass
        elif self._board_window.visible:
            # if phase is...
            pass
        
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
        
    print 'Need to send message to server for lobby button'
    def _ready_up(self, widget):
        self._lobby_window.hide()
        self._board_window.show()
        
    def _exit_app(self, widget, data=None):
        # self._client_message.close_connection()
        sys.exit()
        
        
if __name__ == '__main__':
    app = CluelessApp()
    Gtk.main()