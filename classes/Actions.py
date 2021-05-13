class Actions:
	adv = None
	debug = 0

	def __init__(self, adv, debug):
		self.adv = adv
		self.debug = int(debug)

	def inventory(self):
		print()
		print("Inventar: ")
		for item in self.adv['inventory']:
			print(self.adv['portables'][item]['name'])
		print()

	def examine(self, what, room):
		if self.debug:
			print("What: " + what)
		if what in self.adv[room]['objects']:
			print()
			print(self.adv['objects'][what])
			print()
		elif what in self.adv['inventory']:
			print()
			print(self.adv['portables'][what]['description'])
			print()
		else:
			print(self.adv['default_no_object'])

	def take(self, what, room):
		if self.debug:
			print("take() called with:\nwhat='"+what+"'\nroom='"+room+"'")
		
		# prüfe ob das Objekt sich im aktuellen Raum befindet
		if what not in self.adv[room]['objects']:
			print("\nSowas siehst du hier nicht.\n")
			return self.adv
		
		# zum Inventar hinzufügen
		self.adv['inventory'].append(what)
		
		# aus dem raum entfernen
		self.adv[room]['objects'].remove(what)

		print("Du nimmst " + what.capitalize()+".")

		return self.adv