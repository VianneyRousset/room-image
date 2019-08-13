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

import asyncio, sys
from lib.escapegame import Network, Bus

async def call_devices(bus):
    print('dring...')
    #cs = (bus.send(device_id + 0x0, 'ping') for device_id in range(64))
    #await asyncio.gather(*cs)
    await bus.send(0x00, 'ping') #broadcast

async def main():
    net = Network()
    for i in range(1):
        bus = Bus()
        net.add_bus(bus)

    while True:
        line = await asyncio.get_running_loop().run_in_executor(None, sys.stdin.readline)
        if line[:-1] == 'r':
            asyncio.create_task(call_devices(bus))

if __name__ == "__main__":
    asyncio.run(main())
