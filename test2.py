import networking

host = int(input("chọn server hay client: "))


def gameplay(server, client, host=""):
	print("server chọn" , server)
	print("client chọn", client)
	if server == client:
		print("draw")
	elif (server == "keo" and client == "bao") or (server == "bua" and client == "keo") or (server == "bao" and client == "bua"):
		if host == "server":
			print("win")
		else:
			print("lose")
	else:
		if host == "client":
			print("win")
		else:
			print("lose")


if host == 1:
	uuid = "000000"
	name = input("Tên: ")
	user = networking.User(name, uuid)

	server = networking.Server(user)
	server.createRoom()

	while True:
		server.updateChoice("")

		choice = input("chọn: ")
		server.updateChoice(choice)
		while True:
			client = server.clientChoice()
			if client != "":
				gameplay(server.getChoice(), client, "server")
				break
			else:
				continue


elif host == 0:
	uuid = "000001"
	name = input("ten: ")
	room = input("phong: ")
	user = networking.User(name, uuid)

	client = networking.Client(user)
	client.joinRoom(room)

	while True:
		client.updateChoice("")

		choice = input("chọn: ")
		client.updateChoice(choice)

		while True:
			server = client.serverChoice()
			if server != "":
				gameplay(server, client.getChoice(), "client")
				break
			else:
				continue
