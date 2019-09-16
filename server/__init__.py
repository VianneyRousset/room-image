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
import aiohttp_jinja2
import jinja2

import server.tools

import settings

games = dict()
routes = web.RouteTableDef()

@routes.get('/')
async def home(request):
    #return web.Response(text='hello')
    return web.Response(text=f'available games are {games.keys()}')

@routes.get('/{game_name}')
async def devices_index(request):
    game_name = request.match_info['game_name']
    context = {'game_name' : game_name}
    response = aiohttp_jinja2.render_template('monitor.jinja2',
                                              request, context)
    return response 

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
    devices = tools.read_devices(game.room)
    loop = request.app.loop
    async with sse_response(request) as resp:
        while True:
            devices = tools.read_devices(game.room)
            await resp.send(json.dumps(devices)) # or what constitue them...
            async with game.room:
                await game.room.wait('devices')
    return resp


app = web.Application()
aiohttp_jinja2.setup(app,
    loader=jinja2.FileSystemLoader('server/templates'))
app.add_routes(routes)

def start():
    web.run_app(app)

