#!/usr/bin/env python

'''
 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, version 3.
 This program is distributed in the hope that it will be useful, but
 WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 General Public License for more details.
 You should have received a copy of the GNU General Public License
 along with this program. If not, see <http://www.gnu.org/licenses/>.
'''

import asyncio, random
from math import floor

packets = asyncio.Queue() 

devices = {
     4 : {'name' : 'Phil'},
    24 : {'name' : 'Walt'},
    56 : {'name' : 'Coral'},
    11 : {'name' : 'Nichole'},
    12 : {'name' : 'Elin'},
    19 : {'name' : 'Zia'},
    84 : {'name' : 'Kendrick'}
    }

COMPUTER_SEND_DELAY = 2
ARDUINO_SEND_DELAY = 6


# The computer listen
async def listen():
    asyncio.get_event_loop().create_task(events_creator())
    while True:
        await asyncio.sleep(0)
        yield await packets.get()

# The computer send
async def send(dest, msg):
    delay = random.randint(0, COMPUTER_SEND_DELAY) #TODO Poison distribution
    await asyncio.sleep(delay)
    if dest == 0:
        for device_id in devices:
            asyncio.get_event_loop().create_task(device_answer(device_id, msg))
    else:
        asyncio.get_event_loop().create_task(device_answer(dest, msg))
    return True

# Emulate device's answers 
async def device_answer(dest, msg):
    import re
    if msg == 'ping':
        new_packet(dest, 'ping_back')
    elif msg == 'get name':
        new_packet(dest, f'upt name {devices[dest]["name"]}')
    elif msg == 'get n_comp':
        new_packet(dest, f'upt n_comp {floor(dest/10)+1}')
    elif re.match('get comp \d name', msg):
        comp_id = msg.split()[2]
        new_packet(dest, f'upt comp {comp_id} name comp{comp_id}')

# Create a packet sent by a device
def new_packet(src, msg, wait=False, *, random_wait=True):
    async def wait_and_pack(delay):
        await asyncio.sleep(delay)
        await packets.put((src, msg))
    delay = random.randint(0, ARDUINO_SEND_DELAY) #TODO Poison distribution
    if wait:
        return wait_and_pack(delay)
    else:
        asyncio.get_event_loop().create_task(wait_and_pack(delay))

# Random events
async def events_creator():
    while True:
        await asyncio.sleep(10)
        #new_packet(34, 'hello!')

'''
Remarks:
- We should avoid for an arduino to ping_back twice at once, i.e. when it has
  received a second ping from the computer while he was trying to answer to the
  first one. This could be generalised to any question-like packet from the
  computer, although it may need some work on the arduino's side...
'''
