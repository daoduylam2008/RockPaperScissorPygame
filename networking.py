import firebase_admin
from firebase_admin import credentials, db

networkError = False
# Create environment for firebase
cred = credentials.Certificate("data/serviceKey/serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
	'databaseURL': "https://rockpaperscissor-6753d-default-rtdb.asia-southeast1.firebasedatabase.app/"
})
class User:
	def __init__(self, username, uuid, choice=""):
		self.username = username
		self.uid = uuid
		self.choice = choice
		self.highestScore = 0

	def getData(self):
		return {
			self.username: {
				"username": self.username,
				"id": self.uid,
				"choice": self.choice,
				"highest_score": self.highestScore,
			}
		}

	def updateToData(self):
		# Write data directly to database
		data = db.reference("/")
		data.child("Users/").update(self.getData())

	def resetUserData(self):
		# After using data we should delete user data to prevent from overloading
		data = db.reference("/")
		data.child("Users/"+self.username+"/").set({})


class Server:
	def __init__(self, user: User):
		self.user = user
		self.room = db.reference("room/")

	def createRoom(self):
		print(self.user.getData())
		self.room.update(
			{
				self.user.uid: self.user.getData()
			}
		)

	def updateChoice(self, choice):
		self.user.choice = choice
		self.room.child(self.user.uid + "/" + self.user.username).update({"choice": choice})

	def provideRoomID(self) -> str:
		return self.user.uid

	def getChoice(self) -> str:
		return self.user.choice

	def clientChoice(self) -> str:
		userInRoom = self.room.child(self.provideRoomID()).get()

		client = {}

		for user in userInRoom:
			if user != self.user.username:
				client = userInRoom[user]
		try:
			return client["choice"]
		except:
			return ""

	def resetRoomData(self):
		self.room.child(self.provideRoomID()).set({})


class Client:
	def __init__(self, user: User):
		self.user = user
		self.room = db.reference("room/")

	def joinRoom(self, room_id: str) -> bool:
		self.room = self.room.child(room_id + "/")
		userInRoom = 0
		try:
			for i in self.room.get():
				userInRoom += 1
		except:
			userInRoom = -1

		if userInRoom == 1:
			self.room.update(self.user.getData())
			print("tham gia vô vòng", room_id)
			return True
		elif userInRoom == -1:
			print("Khong tim thay")
			return False
		else:
			print("Phòng đầy người")
			return False

	def updateChoice(self, choice):
		self.user.choice = choice
		self.room.child(self.user.username).update({"choice": choice})

	def getChoice(self) -> str:
		return self.user.choice

	def serverChoice(self) -> str:
		userInRoom = self.room.get()

		server = {}

		for user in userInRoom:
			if user != self.user.username:
				server = userInRoom[user]
		try:
			return server["choice"]
		except:
			return ""

	def resetData(self):
		self.room.child(self.user.username).set({})


class Database:
	def __init__(self):
		self.ref = db.reference("/")

	def getUsersName(self) -> list:
		listOfUsers = []
		try:
			for user in self.ref.child("Users/").get():
				listOfUsers.append(user)
		except:
			self.ref.update({
				"Users": {
					"*": "*"
				},

				"room": {
					"*":"*"
				}

			})
			for user in self.ref.child("Users/").get():
				listOfUsers.append(user)
		return listOfUsers

	def getRooms(self) -> list:
		rooms = []
		for room in self.ref.child("room/").get():
			rooms.append(room)
		return rooms

	def getIDS(self) -> list:
		IDS = []
		users = self.getUsersName()
		users.remove("*")
		for user in users:
			IDS.append(self.ref.child("Users/" + user + "/").get()["id"])

		return IDS

	def createID(self) -> str:
		IDS = self.getIDS()
		max_id = [i for i in range(1, 999999)]
		availableID = max_id
		try:
			for i in IDS:
				for j in max_id:
					if int(i) - j == 0:
						availableID.remove(j)
		except:
			availableID = [1]

		return str((6 - len(str(availableID[0])))*"0" + str(availableID[0]))

