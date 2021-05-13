#!/usr/bin/env python

import sys
import json
import os

from classes.Actions import Actions

# debug output?
debug = 0


def save(savefile, adventure):
	orig_stdout = sys.stdout
	if not os.path.isfile(savefile):
		with open(savefile, "x") as f:
			sys.stdout = f
			print(json.dumps(adventure))
	else:
		with open(savefile, "w") as f:
			sys.stdout = f
			print(json.dumps(adventure))
	sys.stdout = orig_stdout
	print("\nGespeichert.\n")

def main(argv):
	adv = 'None'
	filename = argv[0]
	savefilename = filename+'.save'
	# oeffne die json-datei
	try:
		if os.path.isfile(savefilename):
			with open(savefilename) as adv_file:
				adv = json.load(adv_file)
		else:
			with open(filename) as adv_file:
				adv = json.load(adv_file)
	except:
		print("Unexpected error:", sys.exc_info()[0])
		raise

	if debug == 1 and adv != 'None':
		print('##########')
		print(str(adv))
		print('##########')

	end = 0
	room = None
	usr_input = ''
	while end == 0:
		# set starting point
		if room == None:
			print("Willkommen in deinem Text-Adventure. Um das Spiel zu beenden, gib bitte 'ende' ein.")
			room = adv['start']

		##### check user inputs start #####

		# check if the user wants to quit
		if usr_input == 'ende' or usr_input == 'quit':
			# Spiel speichern
			save(savefilename, adv)
			print("Bye bye!")
			sys.exit(0)

		# check if the user selected an exit
		if usr_input in adv[room]['exits']:
			room = adv[room]['exits'][usr_input]

		# zerteile die User-Eingabe bei den Freizeichen und speichere eine Liste
		usr_input_arr = usr_input.lower().split(' ')


		# begin of output 
		print("##############################")

		actions = Actions(adv, debug)

		# Aktionen können auf Dingen ausgeführt werden, die hinter der Aktion folgen
		# Beispiel: "untersuche busch" -> action=untersuche
		what = ''
		what = " ".join(usr_input_arr[1:])
		action = usr_input_arr[0]

		# with 'u' or 'e' (examine) you can examine something
		if  action == 'untersuche' or action == 'examine':
			actions.examine(what, room)
		elif action == 'nimm' or action == 'take':
			# wenn man etwas nimmt, verschwindet es aus dem raum und muss also in adv[] entfernt werden
			# dies geschieht in actions.take(), welches uns das veränderte adv[] zurück gibt
			adv = actions.take(what, room)
		elif action == 'speichern' or action == 'save':
			save(savefilename, adv)
		elif action == 'inventar' or action == 'inventory' or action == 'inv':
			actions.inventory()
		elif action in adv['actions']:
			print(adv['actions'][usr_input_arr[0]])
			print()
		else:
			if usr_input != '':
				print("Das kannst du nicht tun.")

		##### check user inputs end ####'

		# Raumbeschreibung
		print(adv[room]['description'])
		# Objekte zum Mitnehmen, die hier herumliegen
		for object in adv[room]['objects']:
			if object in adv['portables']:
				if debug:
					print(str(adv['portables'][object]))
				print("Hier liegt " + adv['portables'][object]['name'] + ".")
		print("Du siehst folgende Ausgänge:")
		for direction in adv[room]['exits']:
			print(direction + ' -> ' + adv[room]['exits'][direction])
		
		# end of output
		print("##############################")

		# ask for input
		usr_input = input('Was willst du tun? ').rstrip()

if __name__ == '__main__':
	main(sys.argv[1:])

