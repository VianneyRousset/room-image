def read_puzzles(game):
    puzzles = dict()
    j = 0
    for node in game.roots:
        conds = dict()
        i = 0
        for cond in node.conds:
            conds[f'{i}'] = {'title' : f'condition {i}',
                             'description' : 'no description',
                             'state' : 'active'}
            i += 1
        puzzles[f'{j}'] = {'i' : 0, 'j' : 0,
                           'title' : 'node', 'state' : 'active',
                           'description' : 'no description',
                           'color_index' : 0, 'djs' : [],
                           'conditions' : conds}
        
        j += 1
    return puzzles

def read_devices(game):
    devices = dict()
    for device in game.room.devices.values():
        devices[device.name] = {'comps' : list(device.comps.keys())}
    return devices

