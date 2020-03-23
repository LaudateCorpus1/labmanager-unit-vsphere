from web.settings import Settings as settings

from .base import trString, trList, trId, trSaveTimestamp, trMachineState
from .enums import MachineState
from .document import *


class Machine(Document):
    unit = trString
    modified_at = trSaveTimestamp
    labels = trList
    custom_machine_name = trString
    state = trMachineState
    provider_id = trString
    requests = trList
    ip_addresses = trList
    nos_id = trString
    machine_name = trString
    machine_search_link = trString
    screenshots = trList
    snapshots = trList

    _defaults = {
                    'state': MachineState.CREATED,
                    'unit': settings.app['unit_name'],
                    'labels': [],
                    'ip_addresses': [],
                    'nos_id': '',
                    'machine_name': '',
                    'machine_search_link': '',
                    'screenshots': [],
                    'snapshots': [],
                }
