#!/bin/bash
python3 ./sender.py # sends salted and encrypted flag to server and saves the output in server_resp.txt
sleep 1
python3 ./decrypt0r.py # removes the salt from the server response and recomposes the flag
