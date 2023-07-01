from os import getcwd

def dectobin(deczahl):
	counter = 8
	binary = [0,0,0,0,0,0,0,0]
	while counter > 0:
		binary[counter - 1] = deczahl % 2
		deczahl = deczahl / 2
		counter = counter - 1
	return binary

print("Bitte versichern Sie sich, dass Sie die von DVB-Viewer generierte .ini-Datei als 'Channels.ini' im selben Ordner wie dieses Skript gespeichert haben. \n")
print("Bitte versichern Sie sich, dass das Arbeitsverzeichnis Ihrer Konsole dem Verzeichnis entspricht, in dem die 'Channels.ini' gespeichert ist.\n")
rightip = False
ip = "0.0.0.0"
#erhalten der IP vom Nutzer
while rightip != True:
	print("Bitte geben Sie die IP-Adresse oder den Hostnamen Ihres RTSP-SAT>IP-Servers ein: \n")
	try:
		ip = str(raw_input())
	except NameError:
		ip = str(input())
	rightstr = False
	applied = "n"
	while rightstr != True:
		print("Die IP-Adresse / der Hostname des SAT>IP-Servers lautet " + ip + ", ist das richtig? (y/n)")
		try:
			applied = str(raw_input())
		except NameError:
			applied = str(input())
		if applied != "y" and applied != "n":
			print("Bitte geben Sie entweder 'y' fuer ja oder 'n' fuer nein ein.")
		else:
			rightstr = True
	if applied == "y":
		rightip = True
	else:
		rightip = False
print("Die IP " + ip + " ist die richtige IP.")

channelstr = open('Channels.ini','r', encoding='utf-8', errors='ignore')
channels = channelstr.read()
m3u = open('satip.m3u', 'w')
dest = "#EXTM3U\n"

i = 0
#channels = channels[channels.find("[Channel" +str(0)+"]"):len(channels)]
#print(channels)
channelNumber = 0
while channels:
	name = "#EXTINF:0," + str(i+1) + ". " + channels[channels.find("Name=")+5 : channels.find("\n", channels.find("Name=")+5)] + "\n"
	puffer = "#EXTVLCOPT:network-caching=1000\n"
	dest = dest + name + puffer
	freq = channels[channels.find("Frequency=") + 10 : channels.find("\n", channels.find("Frequency=") + 10)]
	pol = channels[channels.find("Polarity=") + 9 : channels.find("\n", channels.find("Polarity=") + 9)]
	satmod = channels[channels.find("SatModulation=") + 14 : channels.find("\n", channels.find("SatModulation=") + 14)]
	binarr = dectobin(int(satmod))
#	Bit 0..1: Modulation (00 = Auto, 01 = QPSK, 10 = 8PSK, 11 = 16QAM)
#	Bit 2: Modulation system (0 = DVB-S, 1 = DVB-S2)
#	Bit 3..4: Roll-Off (00 = 0.35, 01 = 0.25, 10 = 0.20, 11 = None)
#	Bit 5..6: Spectral Inversion (00 = not set, 01 = auto, 10 = normal, 11 = inverted)
#	Bit 7: Pilot Symbols (0 = off, 1 = on)
	ro = "0.35"
	if binarr[3] == 0 and binarr[4] == 1:
		ro = "0.25"
	elif binarr[3] == 1 and binarr[4] == 0:
		ro = "0.20"
	elif binarr[3] == 1 and binarr[4] == 1:
		ro = "none"

	msys = "dvbs2"
	if binarr[5] == 0:
		msys = "dvbs"

	mtype = "qpsk"
	if binarr[6] == 1 and binarr[7] == 0:
		mtype = "8psk"
	elif binarr[6] == 1 and binarr[7] == 1:
		mtype = "16qam"

	plts = "off"
	if binarr[0] == 1:
		plts = "on"

	sr = channels[channels.find("Symbolrate=") + 11 : channels.find("\n", channels.find("Symbolrate=") + 11)]

	fec = channels[channels.find("FEC=") + 4 : channels.find("\n", channels.find("FEC=") + 4)]
	if fec == "1":
		fec = "23"
	elif fec == "2":
		fec = "34"
	elif fec == "3":
		fec = "56"
	elif fec == "4":
		fec = "78"
	else:
		fec = "9a"

	pat_pid = str(0)
	sdt_pid = str(17)
	sit_pid = str(18)
	vid_pid = channels[channels.find("VPID=") + 5 : channels.find("\n", channels.find("VPID=") + 5)]
	aud_pid = channels[channels.find("APID=") + 5 : channels.find("\n", channels.find("APID=") + 5)]
	pmt_pid = channels[channels.find("PMTPID=") + 7 : channels.find("\n", channels.find("PMTPID=") + 7)]
	txt_pid = channels[channels.find("TelePID=") + 8 : channels.find("\n", channels.find("TelePID=") + 8)]

	url = "rtsp://" + ip + "/?src=1&freq=" + freq + "&pol=" + pol + "&ro=" + ro + "&msys=" + msys + "&mtype=" + mtype + "&plts=" + plts + "&sr=" + sr + "&fec=" + fec + "&pids=" + pat_pid + ","+ sdt_pid + ","+ sit_pid + ","+ vid_pid + ","+ aud_pid + ","+ pmt_pid + "," + txt_pid + "\n"
	dest = dest + url
	i = i+1
	cpos = channels.find("[Channel" + str(i) + "]")
	if cpos != -1:
		channels = channels[cpos:len(channels)]
	else:
		channels = 0
m3u.write(dest)
