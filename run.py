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

import settings
settings.testing = 'b3'

import asyncio, sys
import server

async def main(loop):
    from games import b3
    server.games['b3'] = b3

async def start_tasks(app):
    app['game'] = app.loop.create_task(main(app.loop))

import server
server.app.on_startup.append(start_tasks)
server.start()

