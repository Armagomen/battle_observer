class DialogButtons(object):

    def __init__(self, submit, handle=None):
        self._submit = submit
        self._handle = handle

    def getLabels(self):
        labels = list()
        labels.append({'id': 'submit', 'label': self._submit, 'focused': True})
        if self._handle is not None:
            labels.append({'id': 'handle', 'label': self._handle, 'focused': False})
        return labels
