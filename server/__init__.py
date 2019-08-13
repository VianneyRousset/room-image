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

from aiohttp import web
from aiohttp_sse import sse_response
import asyncio
import json

import server.tools

games = dict()
routes = web.RouteTableDef()

@routes.get('/')
async def home(request):
    #return web.Response(text='hello')
    return web.Response(text=f'available games are {games.keys()}')

@routes.get('/{game_name}')
async def game(request):
    game_name = request.match_info['game_name']
    return web.Response(text=f'you can get the puzzles description at /{game_name}/puzzles')

@routes.get('/{game_name}/puzzles')
async def puzzles(request):
    game_name = request.match_info['game_name']
    game = games[game_name]
    loop = request.app.loop
    async with sse_response(request) as resp:
        while True:
            puzzles = tools.read_puzzles(game)
            await resp.send(json.dumps(puzzles))
            await asyncio.sleep(1, loop=loop) # replace it with waiting on change
    return resp

@routes.get('/{game_name}/devices')
async def devices(request):
    game_name = request.match_info['game_name']
    game = games[game_name]
    devices = tools.read_devices(game)
    loop = request.app.loop
    async with sse_response(request) as resp:
        while True:
            devices = tools.read_devices(game)
            print(json.dumps(devices))
            await resp.send(json.dumps(devices))
            async with game.room.devices_changed:
                await game.room.devices_changed.wait()
    return resp

@routes.get('/{game_name}/devices_index')
async def devices_index(request):
    d = """
        <html>
        <body>
            <script>
                var evtSource = new EventSource("/b3/devices");
                evtSource.onmessage = function(e) {
                    document.getElementById('response').innerText = e.data
                }
            </script>
            <h1>Response from server:</h1>
            <div id="response"></div>
        </body>
    </html>
    """
    return web.Response(text=d, content_type='text/html')

app = web.Application()
app.add_routes(routes)

def start():
    web.run_app(app)

