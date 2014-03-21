#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
It's a client for Tic Tac Toe game.

Usecase: run it after server's started.
"""

from __future__ import print_function
import tic_tac_common as ttc

import socket
import sys
import os
import readline
import json, re


# ---------------------------------------------------------------------------- #

gf = ttc.GAME_FIELD

# ---------------------------------------------------------------------------- #


def main():

	s = get_client_socket()

	try:
		# get hello
		hello_msg = ttc.get_msg_from_socket(s)
		print("\n{0}\n".format(hello_msg))

		print(''' add here some rules ''')

		### loop for a game, untill winner or ^C
		while True:


			#B get a step from user
			msg = raw_input(">: ")


			# convert to json, if it correct (int int)
			step_json = convert_step_to_json(msg)
			ttc.d(step_json)
			if step_json is False:
				print("Bad string. Please, try again.")
				continue;


			#B send step to the server
			s.sendall(step_json)


			#B get server answer about user step
			res = ttc.get_msg_from_socket(s, exception=False, ex=True)


			# if error - ask step again (continue;)
			print("server says: {0}".format(res))
			# if ...
			# 	continue
			# if correct, apply it to the gameplay


			#B get server step
			server_step = ttc.get_msg_from_socket(s)


			# print it | show a winner(exit)
			# perfom some work with game field
			print("server step: {0}\n".format(server_step))

	except KeyboardInterrupt, k:
		print ("Shutting down...")

	s.close()
	sys.exit(0)


# ---------------------------------------------------------------------------- #
# -------------------- H E L P E R S ----------------------------------------- #
# ---------------------------------------------------------------------------- #


def get_client_socket ():
	"""
	Create client socket and connect to the server
	"""
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		print("Connecting to the server...")
		s.connect((ttc.SERVER_IP, ttc.SERVER_PORT))
		print("Connected to {0}:{1}.".format(ttc.SERVER_IP, ttc.SERVER_PORT))
		return s
	except Exception as exp:
		print("Looks like server not ready yet =\\")
		repr(exp)
		sys.exit(1)



def convert_step_to_json (msg):
	"""
	Try to convert input into json like (int, int)

	return
		json, if input correct
		False, if not correct
	"""
	ttc.d("input: %s" %msg)

	parts = re.split("\s*", msg)

	ttc.d(parts)

	try:
		row = int(float(parts[0]))
		col = int(float(parts[1]))
	except Exception as exp:
		print("Oops: {0}".format(exp))
		return False

	answer = {}
	answer["step"] = [row, col]

	return json.dumps(answer)

# ---------------------------------------------------------------------------- #

if __name__ == "__main__":
	main()
