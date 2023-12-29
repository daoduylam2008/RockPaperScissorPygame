"""
Rock Paper Scissor Game GUI Application

The program is used some of the libraries which are installed from PyPI (Python Package Index)

Developed by DAO DUY LAM, PHAM MINH KHOI, LE CONG TIEN
"""
# Python Package Index
import pygame

# System Module and Libraries
import sys
import uix
import random
from PIL import Image

import networking

# Color


# Authorize information, gmail
__author1__ = "daoduylam2020@gmail.com"  # DAO DUY LAM
__author2__ = ""  # PHAM MINH KHOI
__author3__ = ""  # LE CONG TIEN

# ___ MAIN ___
FPS = 60

transform = {
    "rock": 1,
    "scissors": 2,
    "paper": 3
}

data = networking.Database()
allUsers = data.getUsersName()

uuid = data.createID()


def game_play(player, opponent) -> str:
    if player == opponent:
        return "Draw"
    elif (player == 1 and opponent == 2) or (player == 3 and opponent == 1) or (
            player == 2 and opponent == 3):
        music('win_sound')
        return "Win"
    elif (player == 1 and opponent == 3) or (player == 3 and opponent == 2) or (
            player == 2 and opponent == 1):
        music('lose_sound')
        return "Lose"
    else:
        raise ValueError("Unrecognized value")


def music(name_music):
    win_sound = pygame.mixer.Sound('data/soundeffect/win.mp3')
    lose_sound = pygame.mixer.Sound('data/soundeffect/lose.mp3')
    button_sound = pygame.mixer.Sound('data/soundeffect/button_sound.wav')
    music_background = pygame.mixer.Sound('data/soundeffect/music_background.mp3')
    match name_music:
        case 'win_sound':
            win_sound.play()
            win_sound.set_volume(0.5)
        case 'lose_sound':
            lose_sound.play()
            lose_sound.set_volume(1)
        case 'button_sound':
            button_sound.play()
            button_sound.set_volume(0.3)
        case 'music_background': music_background.play()


def readSizeScreen():
    with open('data/size.txt', 'r') as file:
        size = [i.rstrip() for i in file.readlines()]
    return size


def writeSizeScreen(size):
    with open('data/size.txt', 'w') as file:
        if size == 'small':
            file.write('680\n')
            file.write('620')
        elif size == 'medium':
            file.write('900\n')
            file.write('700')
        elif size == 'large':
            file.write('1008\n')
            file.write('888')
        elif size == 'fullscreen':
            file.write('fullscreen\n')
            file.write('fullscreen')
    pygame.quit()
    sys.exit()


class MenuView:
    def __init__(self, surface, width, height):
        self.background = None
        self.width = width
        self.height = height

        self.inputBox = uix.InputBox(surface,
                                     (surface.get_rect().center[0] - 160, surface.get_rect().center[1] - 150, 100, 60))
        self.button_singleplay = uix.Button(surface, (
        surface.get_rect().center[0] - 80, surface.get_rect().center[1] - 50, 150, 60), text='SinglePlayer',
                                            color=(204, 204, 196), bottom_rect_color=(255, 255, 255),
                                            text_color='#FFFF00')
        self.button_setting = uix.Button(surface, (
            surface.get_rect().center[0] - 80, surface.get_rect().center[1] + 150, 150, 60), text='Settings',
                                         color=(32, 178, 170), bottom_rect_color=(255, 255, 255))

        self.button_multiplay = uix.Button(surface, (
            surface.get_rect().center[0] - 80, surface.get_rect().center[1] + 50, 150, 60), text='MultiPlayer',
                                           color=(204, 204, 196), bottom_rect_color=(255, 255, 255),
                                           text_color='#FFFF00')

        self.button_quit = uix.Button(surface,
                                      (surface.get_rect().center[0] - 80, surface.get_rect().center[1] + 250, 150, 60),
                                      text='Quit', color=(204, 204, 196), bottom_rect_color=(255, 255, 255),
                                      text_color='#FFFF00')
        self.button_quit.on_press_action = self.quit

        self.groupWidget = uix.GroupWidget()
        self.groupWidget.widgets.append(self.button_singleplay)
        self.groupWidget.widgets.append(self.button_multiplay)
        self.groupWidget.widgets.append(self.button_setting)
        self.groupWidget.widgets.append(self.button_quit)
        self.groupWidget.widgets.append(self.inputBox)

    def quit(self):
        pygame.quit()
        sys.exit()

    def create_widgets(self):
        self.groupWidget.create_widget()

    def update(self, events):
        self.groupWidget.update(events)

    def image_background(self, surface):
        img = Image.open('data/background.png')
        img = img.resize((surface.get_width(),surface.get_height()),
                         Image.LANCZOS)
        img.save('data/background.png', quality=95)
        imageBackground = uix.Image(surface, 'data/background.png', (0, 0, 0, 0))
        imageBackground.rect = imageBackground.image.get_rect(
        center=imageBackground.surface.get_rect().center)
        imageBackground.create()
        pass


class SinglePlayerView:
    def __init__(self, surface, width, height, back, who_win, input_text):
        self.width = width
        self.height = height
        self.who_win = who_win
        self.input_text = input_text
        self.clicked = False
        self.imageBot_choice_list = []
        self.numberPlayerChoice = 1

        self.button_rock = uix.Button(surface, (
        surface.get_rect().bottomright[0] - 300, surface.get_rect().bottomright[1] - 80, 90, 50), 'Rock', '#ff6680',
                                      bottom_rect_color='#ed7700', text_color='black', text_size=23)
        self.button_rock.on_press_action = self.rock

        self.button_scissors = uix.Button(surface, (
        surface.get_rect().bottomright[0] - 200, surface.get_rect().bottomright[1] - 80, 90, 50), 'Scissors', '#ff6680',
                                          bottom_rect_color='#ed7700', text_color='black', text_size=23)
        self.button_scissors.on_press_action = self.scissors

        self.button_paper = uix.Button(surface, (
        surface.get_rect().bottomright[0] - 100, surface.get_rect().bottomright[1] - 80, 90, 50), 'Paper', '#ff6680',
                                       bottom_rect_color='#ed7700',
                                       text_color='black', text_size=23)
        self.button_paper.on_press_action = self.paper

        self.button_back = uix.Button(surface, (0, 0, 70, 30), 'Back', '#ff6680', bottom_rect_color='#ed7700',
                                      text_color='black', text_size=20)
        self.button_back.on_press_action = back

        self.groupWidget_single = uix.GroupWidget()
        self.groupWidget_single.widgets.append(self.button_rock)
        self.groupWidget_single.widgets.append(self.button_scissors)
        self.groupWidget_single.widgets.append(self.button_paper)
        self.groupWidget_single.widgets.append(self.button_back)

        # The Image Rock Paper Scissors in Single Player View for player
        self.imagePlayer = uix.ImageAnimation(surface, rect=(20, surface.get_rect().bottomright[1] - 235, 100, 100),
                                              imageFolder='data/scissors_animation/', scale=(230, 230), flip=False,
                                              fps=60, angle=0)

        # The Image Rock Paper Scissors in Single Player View for bot
        self.imageBot = uix.ImageAnimation(surface, rect=(surface.get_rect().topright[0] - 260, 10, 100, 100),
                                           imageFolder='data/scissors_animation/', scale=(230, 230),
                                           flip=True, fps=90, angle=90)

        # Blit the text win or lose or draw
        self.who_will_win = uix.Text(surface, (
            surface.get_rect().center[0] - 53, surface.get_rect().center[1] - 20, 50, 50),
                                     size=64,
                                     color='white', text=self.who_win)
        # The Player Name
        self.playerName = uix.Text(surface, (50, surface.get_rect().bottomright[1] - 100, 50, 50), size=32,
                                   color='black',
                                   text=self.input_text)
        # The Bot nAME
        self.bot = uix.Text(surface, (surface.get_rect().topright[0] - 130, 80, 50, 50), size=32, color='black',
                            text='Bot')

    def create_widgets(self):
        self.groupWidget_single.create_widget()

    def update(self, events):
        self.groupWidget_single.update(events)

    def rock(self):
        self.who_win, self.numberPlayerChoice = self.which_button_rpg_clicked('Rock')
        self.imagePlayer.imageFolder = 'data/rock_animation/'
        music('button_sound')

    def paper(self):
        self.who_win, self.numberPlayerChoice = self.which_button_rpg_clicked('Paper')
        self.imagePlayer.imageFolder = 'data/paper_animation/'
        music('button_sound')
    def scissors(self):
        self.who_win, self.numberPlayerChoice = self.which_button_rpg_clicked('Scissors')
        self.imagePlayer.imageFolder = 'data/scissors_animation/'
        music('button_sound')

    def which_button_rpg_clicked(self, playerChoice):
        self.clicked = True

        self.imageBot.returnIndex()
        self.imagePlayer.returnIndex()

        imageBot_choice = random.randint(1, 3)
        self.imageBot_choice_list.append(imageBot_choice)
        self.imageBot_choice_list = self.imageBot_choice_list[-1:]

        match self.imageBot_choice_list[-1]:
            case 1:
                self.imageBot.imageFolder = 'data/rock_animation/'
            case 2:
                self.imageBot.imageFolder = 'data/scissors_animation/'
            case 3:
                self.imageBot.imageFolder = 'data/paper_animation/'
        match playerChoice:
            case 'Paper':
                self.numberPlayerChoice = 3

            case 'Rock':
                self.numberPlayerChoice = 1

            case 'Scissors':
                self.numberPlayerChoice = 2

        self.who_win = game_play(self.numberPlayerChoice, self.imageBot_choice_list[-1])
        return self.who_win, self.numberPlayerChoice


class ServerView(uix.Widget):
    def __init__(self, surface, on_back_press):
        rect = (0, 0, surface.get_width(), surface.get_height())
        super().__init__(surface, rect)

        self.view = uix.GroupWidget()
        self.button_rock = uix.Button(surface, (
        surface.get_rect().bottomright[0] - 300, surface.get_rect().bottomright[1] - 80, 90, 50), 'Rock', '#ff6680',
                                      bottom_rect_color='#ed7700', text_color='black', text_size=23)

        self.button_scissors = uix.Button(surface, (
        surface.get_rect().bottomright[0] - 200, surface.get_rect().bottomright[1] - 80, 90, 50), 'Scissors', '#ff6680',
                                          bottom_rect_color='#ed7700', text_color='black', text_size=23)

        self.button_paper = uix.Button(surface, (
        surface.get_rect().bottomright[0] - 100, surface.get_rect().bottomright[1] - 80, 90, 50), 'Paper', '#ff6680',
                                       bottom_rect_color='#ed7700',
                                       text_color='black', text_size=23)

        self.button_back = uix.Button(self.surface, (0, 0, 70, 30), 'Back', '#ff6680', bottom_rect_color='#ed7700',
                                      text_color='black', text_size=20)

        # Action for button
        self.button_rock.on_press_action = self.on_rock_press
        self.button_paper.on_press_action = self.on_paper_press
        self.button_scissors.on_press_action = self.on_scissors_press
        self.button_back.on_press_action = on_back_press

        self.view.widgets.append(self.button_rock)
        self.view.widgets.append(self.button_back)
        self.view.widgets.append(self.button_paper)
        self.view.widgets.append(self.button_scissors)

    def create(self):
        self.view.create_widget()

    def update(self, events):
        self.view.update(events)

    def on_rock_press(self): pass

    def on_scissors_press(self): pass

    def on_paper_press(self): pass


class ClientView(uix.Widget):
    def __init__(self, surface, on_back_press, room, user=None):
        rect = (0, 0, surface.get_width(), surface.get_height())
        super().__init__(surface, rect)

        self.who_win = "Fight"
        self.room = room
        self.user = user

        self.client = networking.Client

        self.view = uix.GroupWidget()
        self.button_rock = uix.Button(surface, (
            surface.get_rect().bottomright[0] - 300, surface.get_rect().bottomright[1] - 80, 90, 50), 'Rock', '#ff6680',
                                      bottom_rect_color='#ed7700', text_color='black', text_size=23)

        self.button_scissors = uix.Button(surface, (
            surface.get_rect().bottomright[0] - 200, surface.get_rect().bottomright[1] - 80, 90, 50), 'Scissors',
                                          '#ff6680',
                                          bottom_rect_color='#ed7700', text_color='black', text_size=23)

        self.button_paper = uix.Button(surface, (
            surface.get_rect().bottomright[0] - 100, surface.get_rect().bottomright[1] - 80, 90, 50), 'Paper',
                                       '#ff6680',
                                       bottom_rect_color='#ed7700',
                                       text_color='black', text_size=23)

        self.button_back = uix.Button(self.surface, (0, 0, 70, 30), 'Back', '#ff6680', bottom_rect_color='#ed7700',
                                      text_color='black', text_size=20)

        self.imagePlayer = uix.ImageAnimation(surface, rect=(20, surface.get_rect().bottomright[1] - 235, 100, 100),
                                              imageFolder='data/rock_animation/', scale=(230, 230), flip=False,
                                              fps=60, angle=0)

        # The Image Rock Paper Scissors in Single Player View for bot
        self.imageOpponent = uix.ImageAnimation(surface, rect=(surface.get_rect().topright[0] - 260, 10, 100, 100),
                                           imageFolder='data/rock_animation/', scale=(230, 230),
                                           flip=True, fps=90, angle=90)

        self.who_will_win = uix.Text(surface, (
            surface.get_rect().center[0] - 53, surface.get_rect().center[1] - 20, 50, 50),
                                     size=64,
                                     color='white', text=self.who_win)        # Action for button
        self.button_rock.on_press_action = self.on_rock_press
        self.button_paper.on_press_action = self.on_paper_press
        self.button_scissors.on_press_action = self.on_scissors_press
        self.button_back.on_press_action = on_back_press

        self.view.widgets.append(self.button_rock)
        self.view.widgets.append(self.button_back)
        self.view.widgets.append(self.button_paper)
        self.view.widgets.append(self.button_scissors)
        self.view.widgets.append(self.imagePlayer)

        # networking
        self.client = networking.Client(self.user)
        self.isJoin = False

    def create(self):
        self.view.create_widget()

    def update(self, events):
        if not self.isJoin:
            try:
                self.client.joinRoom(self.room)
                self.isJoin = True
            except: pass

        self.view.update(events)
        self.server = self.client.serverChoice()

    def on_rock_press(self):
        self.imagePlayer.imageFolder = "data/rock_animation/"
        music('button_sound')
        self.play("rock")

    def on_scissors_press(self):
        self.imagePlayer.imageFolder = "data/scissors_animation/"
        music('button_sound')
        self.play("scissors")

    def on_paper_press(self):
        self.imagePlayer.imageFolder = "data/paper_animation/"
        music('button_sound')
        self.play("paper")

    def play(self, choice):
        self.client.updateChoice(choice)
        if self.server != "":
            self.who_win = game_play(transform[choice], self.server)


class SelectClientServerView(uix.Widget):
    def __init__(self, surface, back_action, user):
        rect = (0, 0, surface.get_width(), surface.get_height())
        super().__init__(surface, rect)

        # Networking
        self.user = user
        # View
        self.view = uix.GroupWidget()

        # Layer for view
        self.layer = {
            "selection": True,
            "server": False,
            "client": False
        }

        # Create the button for view
        self.roomInputBox = uix.InputBox(self.surface, (
            self.surface.get_rect().center[0] - 150, self.surface.get_rect().center[1] - 150, 100, 60))
        self.joinRoomButton = uix.Button(self.surface, (
            self.surface.get_rect().center[0] - 80, self.surface.get_rect().center[1] - 50, 160, 60), text='Join Room',
                                         color=(204, 204, 196), bottom_rect_color=(255, 255, 255),
                                         text_color='#FFFF00')
        self.joinRoomButton.on_press_action = self.joinRoom

        self.createRoomButton = uix.Button(self.surface, (
            self.surface.get_rect().center[0] - 80, self.surface.get_rect().center[1] + 50, 160, 60),
                                           text='Create Room',
                                           color=(32, 178, 170), bottom_rect_color=(255, 255, 255))
        self.createRoomButton.on_press_action = self.createRoomButton

        self.button_back = uix.Button(surface, (0, 0, 70, 30), 'Back', '#ff6680', bottom_rect_color='#ed7700',
                                      text_color='black', text_size=20)
        self.button_back.on_press_action = back_action

        self.view.widgets = [
            self.roomInputBox,
            self.joinRoomButton,
            uix.Separator(self.surface,
                          (self.surface.get_rect().center[0] - 80, self.surface.get_rect().center[1] + 25, 150, 2),
                          (0, 0, 0)),
            self.createRoomButton,
            self.button_back
        ]
        self.serverView = ServerView(self.surface, self.backToSelection)
        self.clientView = ClientView(self.surface, self.backToSelection, self.roomInputBox.text, self.user)

    def update(self, events):
        if self.layer["selection"]:
            self.view.update(events)
        elif self.layer['server']:
            self.serverView.update(events)

        elif self.layer['client']:
            room = self.roomInputBox.text
            self.clientView.room = room
            self.clientView.update(events)

    def create(self):
        if self.layer["selection"]:
            self.view.create_widget()
        elif self.layer['server']:
            self.serverView.create()
        elif self.layer['client']:
            self.clientView.room = self.roomInputBox.text
            self.clientView.create()

    def joinRoom(self):
        self.layer['selection'] = False
        self.layer['server'] = False
        self.layer['client'] = True

    def createRoom(self):
        self.layer['selection'] = False
        self.layer['server'] = True
        self.layer['client'] = False

    def backToSelection(self):
        self.layer['selection'] = True
        self.layer['server'] = False
        self.layer['client'] = False


class MultiPlayerView(uix.Widget):
    def __init__(self, surface, back_action):
        rect = (0, 0, surface.get_width(), surface.get_height())
        super().__init__(surface, rect)

        self.view = uix.GroupWidget()

        # Networking
        self.user = None

        self.selectionView = SelectClientServerView(surface, back_action, self.user)

        self.view.widgets = [
            self.selectionView
        ]

    def create(self):
        self.view.create_widget()

    def update(self, events):
        self.view.update(events)


class Settings:
    def __init__(self, surface, width, height, func_back, view, SettingsView):
        self.width = width
        self.height = height
        self.surface = surface
        self.view = view
        self.SettingsView = SettingsView

        self.resizeWindow = uix.Button(surface, (
            surface.get_rect().center[0] - 80, surface.get_rect().center[1] - 50, 150, 60), text='Resize Window',
                                       color=(204, 204, 196), bottom_rect_color=(255, 255, 255),
                                       text_color='#FFFF00')
        self.resizeWindow.on_press_action = self.resize

        self.difficulty = uix.Button(surface,
                                     (surface.get_rect().center[0] - 80, surface.get_rect().center[1] + 50, 150, 60),
                                     text='SinglePlayer', color=(204, 204, 196), bottom_rect_color=(255, 255, 255),
                                     text_color='#FFFF00')
        self.chooseDifficulty = self.choose_difficulty

        self.button_back = uix.Button(surface, (0, 0, 70, 30), 'Back', '#ff6680', bottom_rect_color='#ed7700',
                                      text_color='black', text_size=20)
        self.button_back.on_press_action = func_back

        self.groupWidget_settings = uix.GroupWidget()
        self.groupWidget_settings.widgets.append(self.resizeWindow)
        self.groupWidget_settings.widgets.append(self.button_back)

        self.groupWidget_resize = uix.GroupWidget()

    def create_widgets(self):
        self.groupWidget_settings.create_widget()

    def update(self, events):
        self.groupWidget_settings.update(events)

    def resize(self):
        self.SettingsView['Resize Window'] = True
        resizeSmallButton = uix.Button(self.surface, (
        self.surface.get_rect().center[0] - 80, self.surface.get_rect().center[1] - 150, 150, 60), text='Small',
                                       color=(204, 204, 196), bottom_rect_color=(255, 255, 255), text_color='#FFFF00')
        resizeSmallButton.on_press_action = self.resize_small

        resizeMediumButton = uix.Button(self.surface, (
        self.surface.get_rect().center[0] - 80, self.surface.get_rect().center[1] - 50, 150, 60), text='Medium',
                                        color=(204, 204, 196), bottom_rect_color=(255, 255, 255), text_color='#FFFF00')
        resizeMediumButton.on_press_action = self.resize_medium

        resizeLargeButton = uix.Button(self.surface, (
        self.surface.get_rect().center[0] - 80, self.surface.get_rect().center[1] + 50, 150, 60), text='Large',
                                       color=(204, 204, 196), bottom_rect_color=(255, 255, 255), text_color='#FFFF00')
        resizeLargeButton.on_press_action = self.resize_large

        resizeFullScreenButton = uix.Button(self.surface, (
        self.surface.get_rect().center[0] - 80, self.surface.get_rect().center[1] + 150, 150, 60), text='Full Screen',
                                            color=(204, 204, 196), bottom_rect_color=(255, 255, 255),
                                            text_color='#FFFF00')
        resizeFullScreenButton.on_press_action = self.resize_fullscreen

        resizeBackButton = uix.Button(self.surface, (0, 0, 70, 30), 'Back', '#ff6680', bottom_rect_color='#ed7700',
                                      text_color='black', text_size=20)
        resizeBackButton.on_press_action = self.resize_back

        self.label_anouncement = uix.Text(self.surface, (
        self.surface.get_rect().center[0] - 240, self.surface.get_rect().center[1] - 250, 150, 60),
                                          text='After resize your screen game, you need to restart game', color='black')

        self.groupWidget_resize.widgets.append(resizeSmallButton)
        self.groupWidget_resize.widgets.append(resizeMediumButton)
        self.groupWidget_resize.widgets.append(resizeLargeButton)
        self.groupWidget_resize.widgets.append(resizeFullScreenButton)
        self.groupWidget_resize.widgets.append(resizeBackButton)

    def resizeCreateUpdate(self, events):
        self.groupWidget_resize.create_widget()
        self.groupWidget_resize.update(events)
        self.label_anouncement.create(text='After resize your screen game, you need to restart')

    def resize_back(self):
        self.SettingsView['Resize Window'] = False

    def resize_small(self):
        writeSizeScreen('small')

    def resize_medium(self):
        writeSizeScreen('medium')

    def resize_large(self):
        writeSizeScreen('large')

    def resize_fullscreen(self):
        writeSizeScreen('fullscreen')

    def choose_difficulty(self):
        pass


class RockPaperScissor:
    def __init__(self):
        self.imageBot_choice = None
        self.width = readSizeScreen()[0]
        self.height = readSizeScreen()[1]

        if self.width == 'fullscreen':
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((int(self.width), int(self.height)))

        self.clock = pygame.time.Clock()

        self.view = {
            'Main Menu': True,
            'SinglePlay Menu': False,
            'Settings Menu': False,
            "MultiPlay Mene": False,
            'Back': False
        }
        self.SetingsView = {
            'Resize Window': False,
            'Difficulty': False
        }

        self.playerChoice = ''
        self.numberPlayerChoice = 0
        self.imageBot_choice_list = []
        self.who_win = 'Fight'
        self.clicked = False

        # Main widgets which contain all widget on screen but at first it's empty
        # You have to add your own widget after creating it
        # Use this code to add widget: self.groupWidgets.widgets.append(<widget>)

        # The Menu Screen
        self.menuView = MenuView(self.screen, self.width, self.height)  # Create the menu
        self.menuView.button_singleplay.on_press_action = self.single_play
        self.menuView.button_setting.on_press_action = self.setting
        self.menuView.button_multiplay.on_press_action = self.multi_play

        # The Single Player View
        self.singlePlayerView = SinglePlayerView(self.screen, self.width, self.height,
                                                 self.back, self.who_win, self.menuView.inputBox.text)

        # The Settings View
        self.settingsView = Settings(self.screen, self.width, self.height, self.back, self.view, self.SetingsView)

        # The Multi Player View
        self.multiPlayerView = MultiPlayerView(self.screen, self.back)

        # Message
        self.message = ""
        self.messageText = uix.Text(self.screen, (self.screen.get_rect().center[0] - 160, self.screen.get_rect().center[1] - 170, 100, 60), color=(255, 0, 0))
        music('music_background')

        # Networking
        self.user = None

    def run(self):

        while True:
            self.screen.fill((0,0,0))
            # Fill the screen with BLACK instead of an empty screen
            self.menuView.image_background(self.screen)

            # Event
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.close()
            if self.message != "":
                self.messageText.create(self.message)
            if self.view['SinglePlay Menu']:
                self.singlePlayerView.create_widgets()
                self.singlePlayerView.update(events)

                self.singlePlayerView.imagePlayer.create()
                self.singlePlayerView.imageBot.create()

                if self.singlePlayerView.clicked:
                    self.singlePlayerView.imagePlayer.update(events)
                    self.singlePlayerView.imageBot.update(events)

                    self.singlePlayerView.who_will_win.create(self.singlePlayerView.who_win)
                self.singlePlayerView.playerName.create(self.menuView.inputBox.text)
                self.singlePlayerView.bot.create('Bot')
            elif self.view['Settings Menu']:

                if self.settingsView.SettingsView['Resize Window']:
                    self.settingsView.resizeCreateUpdate(events)
                else:
                    self.settingsView.create_widgets()
                    self.settingsView.update(events)
            elif self.view['Main Menu']:
                self.menuView.create_widgets()
                self.menuView.update(events)
            elif self.view['MultiPlay Menu']:
                try:
                    self.user = networking.User(self.menuView.inputBox.text, uuid)
                    self.multiPlayerView.user = self.user
                    self.multiPlayerView.update(events)
                    self.multiPlayerView.create()
                except: pass

            # Update and set FPS
            self.clock.tick(FPS)
            # self.screen.blit(self.view1,(0,0))

            pygame.display.flip()
            pygame.display.update()

    def single_play(self):
        self.view['SinglePlay Menu'] = True
        self.view['Settings Menu'] = False
        self.view['MultiPlay Menu'] = False
        self.view['Main Menu'] = False

    def multi_play(self):
        if self.menuView.inputBox.text == "":
            self.message = "Please type your name"
        elif self.multiPlayerView.selectionView.roomInputBox.text == "":
            self.message = "Please type your room"
            self.message = ""
            self.view['SinglePlay Menu'] = False
            self.view['Settings Menu'] = False
            self.view['MultiPlay Menu'] = True
            self.view['Main Menu'] = False

    def back(self):
        self.view['SinglePlay Menu'] = False
        self.view['Settings Menu'] = False
        self.view['MultiPlay Menu'] = False
        self.view['Main Menu'] = True

    ##########
    # Warning: This code has to be inside the setting view class, not here
    def setting(self):
        self.view['SinglePlay Menu'] = False
        self.view['Settings Menu'] = True
        self.view['MultiPlay Menu'] = False
        self.view['Main Menu'] = False

    def backSettings(self):
        self.SetingsView['Resize Window'] = False
        self.view['Settings Menu'] = True

    ##########

    def multiplayer_play(self):
        pass

    def close(self):
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = RockPaperScissor()
    game.run()
    # except Exception as bug:
    #     print(bug)
    #     game.close()
