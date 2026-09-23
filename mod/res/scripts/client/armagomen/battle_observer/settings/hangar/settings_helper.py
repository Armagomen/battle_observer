from armagomen._constants import GLOBAL

C_INTERFACE_SPLITTER = "*"


def makeTooltip(header=None, body=None, note=None, attention=None):
    parts = (('HEADER', header), ('BODY', body), ('NOTE', note), ('ATTENTION', attention),)
    res_str = u''.join(u'{{{0}}}{1}{{/{0}}}'.format(tag, text) for tag, text in parts if text is not None)
    return res_str


def getCollectionIndex(value, collection):
    index = 0
    if value in collection:
        index = collection.index(value)
    return index


def getKeyPath(settings_block, path=()):
    for key, value in settings_block.items():
        key_path = path + (key,)
        if isinstance(value, dict):
            for _path in getKeyPath(value, key_path):
                yield _path
        else:
            yield key_path


def convertDict(settings_block):
    for key in getKeyPath(settings_block):
        key = C_INTERFACE_SPLITTER.join(key)
        if GLOBAL.ENABLED != key:
            dic, param = unpackDictPath(settings_block, key)
            yield key, dic[param]


def unpackDictPath(settings_block, settingPath):
    path = settingPath.split(C_INTERFACE_SPLITTER)
    if len(path) > 1:
        for fragment in path:
            if fragment in settings_block and isinstance(settings_block[fragment], dict):
                settings_block = settings_block[fragment]
    return settings_block, path[-1]



