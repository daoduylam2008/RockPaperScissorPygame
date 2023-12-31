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
import requests


def internet_connection():
	try:
		response = requests.get("https://dns.tutorialspoint.com", timeout=5)
		return True
	except requests.ConnectionError:
		return False


if internet_connection():
	import networking
	error = "connected"
else:
	import non_network as networking
	error = "unconnected"
import MachineLearning

# Authorize information, gmail
__author1__ = "daoduylam2020@gmail.com"  # DAO DUY LAM
__author2__ = "phamminhkhoi10122008@gmail.com"  # PHAM MINH KHOI
__author3__ = "ltien9505@gmail.com"  # LE CONG TIEN

# ___ MAIN ___


FPS = 90

transform = {
	"": 0,
	"rock": 1,
	"scissors": 2,
	"paper": 3
}

data = networking.Database()
allUsers = data.getUsersName()

uuid = data.createID()

user = networking.User("", uuid)


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
		case 'music_background':
			music_background.play()


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
	user.resetUserData()

	pygame.quit()
	sys.exit()


class MenuView:
	BUTTON_COLOR = (204, 204, 196)
	BUTTON_RECT_COLOR = (255, 255, 255)
	BUTTON_TEXT_COLOR = '#FFFF00'
	BUTTON_QUIT_COLOR = (32, 178, 170)

	def __init__(self, surface, width, height):
		self.background = None
		self.width = width
		self.height = height

		self.inputBox = uix.InputBox(surface,
									 (surface.get_rect().center[0] - 160, surface.get_rect().center[1] - 150, 100, 60))
		self.button_singleplay = self.create_button(surface, 'SinglePlayer', -50)
		self.button_setting = self.create_button(surface, 'Settings', 150, self.BUTTON_QUIT_COLOR)
		self.button_multiplay = self.create_button(surface, 'MultiPlayer', 50)
		self.button_quit = self.create_button(surface, 'Quit', 250)

		self.button_quit.on_press_action = self.close

		self.groupWidget = uix.GroupWidget()
		self.groupWidget.widgets.extend(
			[self.button_singleplay, self.button_multiplay, self.button_setting, self.button_quit, self.inputBox])

		self.background_image = pygame.image.load('data/menu.png')
		self.background_image = pygame.transform.scale(self.background_image, (int(self.width), int(self.height)))

	def create_button(self, surface, text, y_offset, color=BUTTON_COLOR):
		button = uix.Button(surface, (
			surface.get_rect().center[0] - 80, surface.get_rect().center[1] + y_offset, 150, 60), text=text,
							color=color, bottom_rect_color=self.BUTTON_RECT_COLOR,
							text_color=self.BUTTON_TEXT_COLOR)

		return button

	def close(self):
		try:
			user.resetUserData()
		except:
			print("No user to delete")
		pygame.quit()
		sys.exit()

	def create_widgets(self):
		self.groupWidget.create_widget()

	def update(self, events):
		self.groupWidget.update(events)

	def image_background(self, surface):
		surface.blit(self.background_image, (0, 0))


class SinglePlayerView:

	def __init__(self, surface, width, height, back, who_win, input_text):
		self.width = width
		self.height = height
		self.who_win = who_win
		self.input_text = input_text
		self.clicked = False
		self.imageBot_choice_list = []
		self.numberPlayerChoice = 1

		self.button_action = {
			'rock': self.rock,
			'paper': self.paper,
			'scissors': self.scissors
		}
		self.buttons = {name: self.create_buttons(surface, name.capitalize(), action) for name, action in
						self.button_action.items()}

		self.button_back = uix.Button(surface, (0, 0, 70, 30), 'Back', '#ff6680', bottom_rect_color='#ed7700',
									  text_color='black', text_size=20)
		self.button_back.on_press_action = back

		self.groupWidget_single = uix.GroupWidget()
		self.groupWidget_single.widgets.extend(self.buttons.values())
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
									 color='black', text=self.who_win)
		# The Player Name
		self.playerName = uix.Text(surface, (50, surface.get_rect().bottomright[1] - 100, 50, 50), size=32,
								   color='black',
								   text=self.input_text)
		# The Bot nAME
		self.bot = uix.Text(surface, (surface.get_rect().topright[0] - 130, 80, 50, 50), size=32, color='black',
							text='Bot')

		self.backgroundImageSinglePlayer = pygame.image.load('data/background.png')
		self.backgroundImageSinglePlayer = pygame.transform.scale(self.backgroundImageSinglePlayer,
																  (int(self.width) + 90, int(self.height) + 90))

	def create_buttons(self, surface, text, action, x_offset=0):
		match text:
			case 'Rock':
				x_offset = 300
			case 'Scissors':
				x_offset = 200
			case 'Paper':
				x_offset = 100
		button = uix.Button(surface, rect=(
			surface.get_rect().bottomright[0] - x_offset, surface.get_rect().bottomright[1] - 80, 90, 50), text=text,
							color='#ff6680', bottom_rect_color='#ed7700', text_color='black', text_size=23)
		button.on_press_action = action
		return button

	def create_widgets(self):
		self.groupWidget_single.create_widget()

	def update(self, events):
		self.groupWidget_single.update(events)

	def rock(self):
		self.who_win, self.numberPlayerChoice = self.which_button_rpg_clicked(1)
		self.imagePlayer.imageFolder = 'data/rock_animation/'
		music('button_sound')

	def paper(self):
		self.who_win, self.numberPlayerChoice = self.which_button_rpg_clicked(3)
		self.imagePlayer.imageFolder = 'data/paper_animation/'
		music('button_sound')

	def scissors(self):
		self.who_win, self.numberPlayerChoice = self.which_button_rpg_clicked(2)
		self.imagePlayer.imageFolder = 'data/scissors_animation/'
		music('button_sound')

	def which_button_rpg_clicked(self, playerChoice):
		self.clicked = True

		self.imageBot.returnIndex()
		self.imagePlayer.returnIndex()
		difficulty = self.getDifficulty()

		if difficulty == "easy":
			imageBot_choice = MachineLearning.Computer().easy()
		elif difficulty == "medium":
			imageBot_choice = MachineLearning.Computer().medium()
		elif difficulty == "hard":
			imageBot_choice = MachineLearning.Computer().hard()
		else:
			imageBot_choice = MachineLearning.Computer().easy()

		self.imageBot_choice_list.append(imageBot_choice)
		self.imageBot_choice_list = self.imageBot_choice_list[-1:]

		rpg_choice = {1: 'rock',
					  2: 'scissors',
					  3: 'paper'
					  }
		ourState = {
			'Win': '4',
			'Lose': '5',
			'Draw': '6'
		}

		self.imageBot.imageFolder = 'data/' + rpg_choice[self.imageBot_choice_list[-1]] + '_animation/'

		self.who_win = game_play(playerChoice, self.imageBot_choice_list[-1])

		with open('data/history.txt', 'a') as file:
			file.write(str(playerChoice))
		with open('data/history1.txt', 'a') as file1:
			file1.write(ourState[self.who_win])

		return self.who_win, self.numberPlayerChoice

	def backgroundImageSingle(self, surface):
		surface.blit(self.backgroundImageSinglePlayer, (-50, -50))

	def getDifficulty(self):
		with open("data/difficulty.txt", 'r') as f:
			return f.readline()


class ServerView(uix.Widget):
	def __init__(self, surface, on_back_press):
		rect = (0, 0, surface.get_width(), surface.get_height())
		super().__init__(surface, rect)
		# Networking
		self.server = networking.Server(user)
		try:
			self.server.createRoom()
		except:
			pass
		self.room = self.server.provideRoomID()
		self.isJoin = False
		self.isChoose = False
		self.who_win = ""

		# View
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
									 color='black', text=self.who_win)
		self.message = ""
		self.messageText = uix.Text(self.surface, (150, 20, 100, 60), color=(255, 0, 0),
									size=40,
									text=self.message)

		# Action for button
		self.button_rock.on_press_action = self.on_rock_press
		self.button_paper.on_press_action = self.on_paper_press
		self.button_scissors.on_press_action = self.on_scissors_press
		self.button_back.on_press_action = on_back_press

		self.view.widgets.append(self.button_rock)
		self.view.widgets.append(self.button_back)
		self.view.widgets.append(self.button_paper)
		self.view.widgets.append(self.button_scissors)
		self.view.widgets.append(self.imagePlayer)
		self.view.widgets.append(self.imageOpponent)

	def create(self):
		self.who_will_win.create(self.who_win)
		self.messageText.create(self.message)
		self.view.create_widget()

	def update(self, events):
		self.message = "Room ID:" + self.room
		try:
			client = self.server.clientChoice()
		except:
			client = "101"
			print("123")
		if not self.isChoose:
			self.server.updateChoice("")
		else:
			self.who_win = "Choose rock paper or scissors"
		if client != "":
			try:
				self.who_win = game_play(transform[self.server.getChoice()], transform[client])
			except:
				pass

			if self.isChoose:
				self.imageOpponent.imageFolder = "data/" + client + "_animation/"
			self.isChoose = False
		elif client == "" and self.isChoose:
			self.who_win = "Wait your opponent"
		if client == "101":
			self.who_win = "Wait your opponent to join the room\nThe room id:" + self.server.provideRoomID()
		self.view.update(events)

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
		self.server.updateChoice(choice)
		self.isChoose = True


class ClientView(uix.Widget):
	def __init__(self, surface, on_back_press):
		self.server = None
		rect = (0, 0, surface.get_width(), surface.get_height())
		super().__init__(surface, rect)

		self.who_win = "Fight"

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
									 color='black', text=self.who_win)  # Action for button
		self.message = ""
		self.messageText = uix.Text(self.surface, (self.surface.get_rect().center[0] - 160,
												   self.surface.get_rect().center[1] - 170, 100, 60), color=(255, 0, 0),
									text=self.message)

		self.button_rock.on_press_action = self.on_rock_press
		self.button_paper.on_press_action = self.on_paper_press
		self.button_scissors.on_press_action = self.on_scissors_press
		self.button_back.on_press_action = on_back_press

		self.view.widgets.append(self.button_rock)
		self.view.widgets.append(self.button_back)
		self.view.widgets.append(self.button_paper)
		self.view.widgets.append(self.button_scissors)
		self.view.widgets.append(self.imagePlayer)
		self.view.widgets.append(self.imageOpponent)

		# networking
		self.room = ""
		self.client = networking.Client(user)
		self.isJoin = False
		self.isChoose = False

	def create(self):
		self.who_will_win.create(self.who_win)
		self.messageText.create(self.message)
		self.view.create_widget()

	def update(self, events):
		if not self.isJoin:
			self.client.joinRoom(self.room)
			print("Joined to room id:", self.room)
			self.isJoin = True
		self.view.update(events)

		server = self.client.serverChoice()
		if not self.isChoose:
			self.client.updateChoice("")
		else:
			self.who_win = "Choose rock paper or scissors"
		if server != "":
			try:
				self.who_win = game_play(transform[self.client.getChoice()], transform[server])
			except:
				pass

			if self.isChoose:
				self.imageOpponent.imageFolder = "data/" + server + "_animation/"
			self.isChoose = False
		elif server == "" and self.isChoose:
			self.who_win = "Wait your opponent"

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
		self.isChoose = True


class SelectClientServerView(uix.Widget):
	def __init__(self, surface, back_action):
		rect = (0, 0, surface.get_width(), surface.get_height())
		super().__init__(surface, rect)

		# Networking

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
			self.surface.get_rect().center[0] - 80, self.surface.get_rect().center[1] - 50, 160, 60),
										 text='Join Room',
										 color=(32, 178, 170), bottom_rect_color=(255, 255, 255))
		self.joinRoomButton.on_press_action = self.joinRoom

		self.createRoomButton = uix.Button(self.surface, (
			self.surface.get_rect().center[0] - 80, self.surface.get_rect().center[1] + 50, 160, 60),
										   text='Create Room',
										   color=(32, 178, 170), bottom_rect_color=(255, 255, 255))
		self.createRoomButton.on_press_action = self.createRoom

		self.button_back = uix.Button(surface, (0, 0, 70, 30), 'Back', '#ff6680', bottom_rect_color='#ed7700',
									  text_color='black', text_size=20)
		self.button_back.on_press_action = back_action

		self.message = ""
		self.messageText = uix.Text(self.surface, (self.surface.get_rect().center[0] - 160,
												   self.surface.get_rect().center[1] - 170, 100, 60), color=(255, 0, 0),
									text=self.message)

		self.view.widgets = [
			self.roomInputBox,
			self.joinRoomButton,
			uix.Separator(self.surface,
						  (self.surface.get_rect().center[0] - 80, self.surface.get_rect().center[1] + 25, 150, 2),
						  (0, 0, 0)),
			self.createRoomButton,
			self.button_back,
		]
		self.serverView = ServerView(self.surface, self.backToSelection)
		self.clientView = ClientView(self.surface, self.backToSelection)

	def update(self, events):
		if self.layer["selection"]:
			self.view.update(events)
		elif self.layer['server']:
			self.serverView.update(events)
		elif self.layer['client']:
			self.clientView.update(events)

	def create(self):
		if self.message != "":
			self.messageText.create(self.message)
		if self.layer["selection"]:
			self.view.create_widget()
		elif self.layer['server']:
			self.serverView.create()
		elif self.layer['client']:
			self.clientView.create()

	def joinRoom(self):
		if self.roomInputBox.text not in data.getRooms():
			self.message = "Type room again"
		else:
			self.message = ""
			self.clientView.room = self.roomInputBox.text
			self.layer['selection'] = False
			self.layer['server'] = False
			self.layer['client'] = True

	def createRoom(self):
		print("Created room successfully")
		self.layer['selection'] = False
		self.layer['server'] = True
		self.layer['client'] = False

	def backToSelection(self):
		user.resetUserData()
		print("Reset user data")
		self.layer['selection'] = True
		self.layer['server'] = False
		self.layer['client'] = False


class MultiPlayerView(uix.Widget):
	def __init__(self, surface, back_action):
		rect = (0, 0, surface.get_width(), surface.get_height())
		super().__init__(surface, rect)

		self.view = uix.GroupWidget()

		# Networking
		self.user_infor = None

		self.selectionView = SelectClientServerView(surface, back_action)

		self.view.widgets = [
			self.selectionView
		]

	def create(self):
		self.view.create_widget()

	def update(self, events):
		self.view.update(events)


class Settings:
	BUTTON_COLOR = (204, 204, 196)
	BUTTON_RECT_COLOR = (255, 255, 255)
	BUTTON_TEXT_COLOR = '#FFFF00'
	BUTTON_QUIT_COLOR = (32, 178, 170)

	def __init__(self, surface, width, height, func_back, view, settingView):
		self.groupWidget_chooseDifficulty = None
		self.labelAnouncementEasy = None
		self.width = width
		self.height = height
		self.surface = surface
		self.view = view
		self.settingsView = settingView

		self.resizeWindow = self.create_button(surface, 'Resize Window', -150)
		self.resizeWindow.on_press_action = self.resize

		self.difficulty = self.create_button(surface, 'Difficulty', -50)
		self.difficulty.on_press_action = self.choose_difficulty

		self.button_back = uix.Button(surface, (0, 0, 70, 30), 'Back', '#ff6680', bottom_rect_color='#ed7700',
									  text_color='black', text_size=20)
		self.button_back.on_press_action = func_back

		self.groupWidget_settings = uix.GroupWidget()
		self.groupWidget_settings.widgets.extend([self.resizeWindow, self.button_back, self.difficulty])

		self.groupWidget_resize = uix.GroupWidget()

		self.difficultyString = "Default difficulty is Medium"

	def create_button(self, surface, text, y_offset, color=BUTTON_COLOR):
		button = uix.Button(surface, (
			surface.get_rect().center[0] - 80, surface.get_rect().center[1] + y_offset, 150, 60), text=text,
							color=color, bottom_rect_color=self.BUTTON_RECT_COLOR,
							text_color=self.BUTTON_TEXT_COLOR)
		return button

	def create_widgets(self):
		self.groupWidget_settings.create_widget()

	def update(self, events):
		self.groupWidget_settings.update(events)

	def resize(self):
		self.settingsView['Resize Window'] = True

		resizeSmallButton = self.create_button(self.surface, 'Small', -150)
		resizeSmallButton.on_press_action = self.resize_small

		resizeMediumButton = self.create_button(self.surface, 'Medium', -50)
		resizeMediumButton.on_press_action = self.resize_medium

		resizeLargeButton = self.create_button(self.surface, 'Large', 50)
		resizeLargeButton.on_press_action = self.resize_large

		resizeFullScreenButton = self.create_button(self.surface, 'Full Screen', 150)
		resizeFullScreenButton.on_press_action = self.resize_fullscreen

		resizeBackButton = uix.Button(self.surface, (0, 0, 70, 30), 'Back', '#ff6680', bottom_rect_color='#ed7700',
									  text_color='black', text_size=20)
		resizeBackButton.on_press_action = self.resize_back

		self.label_anouncement = uix.Text(self.surface, (
			self.surface.get_rect().center[0] - 240, self.surface.get_rect().center[1] - 250, 150, 60),
										  text='After resize your screen game, you need to restart game', color='black')

		self.groupWidget_resize.widgets.append(resizeSmallButton)
		self.groupWidget_resize.widgets.extend(
			[resizeSmallButton, resizeMediumButton, resizeLargeButton, resizeFullScreenButton, resizeBackButton])

	def resizeCreateUpdate(self, events):
		self.groupWidget_resize.create_widget()
		self.groupWidget_resize.update(events)
		self.label_anouncement.create(text='After resize your screen game, you need to restart')

	def resize_back(self):
		self.settingsView['Resize Window'] = False

	def resize_small(self):
		writeSizeScreen('small')

	def resize_medium(self):
		writeSizeScreen('medium')

	def resize_large(self):
		writeSizeScreen('large')

	def resize_fullscreen(self):
		writeSizeScreen('fullscreen')

	def on_easy(self):
		with open("data/difficulty.txt", 'w') as f:
			f.write("easy")

		self.difficultyString = "Difficulty: Easy"

	def on_medium(self):
		with open("data/difficulty.txt", 'w') as f:
			f.write("medium")

		self.difficultyString = "Difficulty: Medium"

	def on_hard(self):
		with open("data/difficulty.txt", 'w') as f:
			f.write("hard")

		self.difficultyString = "Difficulty: Hard"

	def choose_difficulty(self):
		self.settingsView['Difficulty'] = True

		easyButton = self.create_button(self.surface, text='Easy Mode', y_offset=-50)
		mediumButton = self.create_button(self.surface, text="Medium mode", y_offset=50)
		difficultyButton = self.create_button(self.surface, text='Difficult Mode', y_offset=+150)

		easyButton.on_press_action = self.on_easy
		mediumButton.on_press_action = self.on_medium
		difficultyButton.on_press_action = self.on_hard

		resizeBackButtonDiff = uix.Button(self.surface, (0, 0, 70, 30), 'Back', '#ff6680', bottom_rect_color='#ed7700',
										  text_color='black', text_size=20)
		resizeBackButtonDiff.on_press_action = self.resizeBackButtonDiff

		self.labelAnouncementEasy = uix.Text(self.surface, (
			self.surface.get_rect().center[0] - 140, self.surface.get_rect().center[1] - 250, 150, 60),
											 text=self.difficultyString, color='black')

		self.groupWidget_chooseDifficulty = uix.GroupWidget()
		self.groupWidget_chooseDifficulty.widgets.extend(
			[easyButton, mediumButton, difficultyButton, resizeBackButtonDiff])

	def chooseDifficultyCreateUpdate(self, events):
		self.groupWidget_chooseDifficulty.create_widget()
		self.groupWidget_chooseDifficulty.update(events)
		with open("data/difficulty.txt", 'r') as f:
			difficulty = f.readline()
			self.difficultyString = "Difficult: " + difficulty
		self.labelAnouncementEasy.create(text=self.difficultyString)

	def resizeBackButtonDiff(self):
		self.settingsView['Difficulty'] = False


class RockPaperScissor:
	def __init__(self):
		self.imageBot_choice = None
		self.width, self.height = self.readSizeScreen()
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
		# The Multi Player View
		self.multiPlayerView = MultiPlayerView(self.screen, self.back)

		# The Settings View
		self.settingsView = Settings(self.screen, self.width, self.height, self.back, self.view, self.SetingsView)

		music('music_background')
		# Message
		self.message = ""
		self.messageText = uix.Text(self.screen,
									(self.screen.get_rect().center[0] - 160,
									 self.screen.get_rect().center[1] - 170, 100, 60),
									color=(255, 0, 0))

	def run(self):

		while True:
			self.screen.fill((0, 0, 0))
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
				self.singlePlayerView.backgroundImageSingle(self.screen)

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

				if self.settingsView.settingsView['Resize Window']:
					self.settingsView.resizeCreateUpdate(events)
				elif self.settingsView.settingsView['Difficulty']:
					self.settingsView.chooseDifficultyCreateUpdate(events)
				else:
					self.settingsView.create_widgets()
					self.settingsView.update(events)
			elif self.view['Main Menu']:
				self.menuView.create_widgets()
				self.menuView.update(events)
			elif self.view['MultiPlay Menu']:
				self.multiPlayerView.update(events)
				self.multiPlayerView.create()

			# Update and set FPS
			self.clock.tick(FPS)

			pygame.display.flip()
			pygame.display.update()

	def single_play(self):
		self.view['SinglePlay Menu'] = True
		self.view['Settings Menu'] = False
		self.view['MultiPlay Menu'] = False
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

	def multi_play(self):
		if error == "unconnected":
			self.message = "Please connect to your network and restart the program"
		elif error == "connected":
			if self.menuView.inputBox.text == "":
				self.message = "Please type your name"
			elif self.menuView.inputBox.text in data.getUsersName():
				self.message = "This name has been used"
			elif self.multiPlayerView.selectionView.roomInputBox.text == "":
				self.message = "Please type your room"
				self.message = ""

				self.view['SinglePlay Menu'] = False
				self.view['Settings Menu'] = False
				self.view['MultiPlay Menu'] = True
				self.view['Main Menu'] = False
				user.username = self.menuView.inputBox.text

				print("Update user's data")
				user.updateToData()

	def close(self):
		# self.user.resetUserData()
		pygame.quit()
		sys.exit()

	@staticmethod
	def readSizeScreen():
		with open('data/size.txt', 'r') as file:
			size = [i.rstrip() for i in file.readlines()]
		return size


if __name__ == "__main__":
	game = RockPaperScissor()
	game.run()
