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

import server

if __name__ == "__main__":
    asyncio.run(main())

async def main():
    from games import b3
    # basically only launch the server/user interfaces

'''
if __name__ == "__main__":
    server.add_game(b3.Game())
    server.start()

    import logging
    logging.basicConfig(level=logging.DEBUG)

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(asyncio.gather(main(com, loop), discuss(com)))
    finally:
        loop.close()
'''
