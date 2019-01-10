from ..census import Query
from ..datatypes import StaticDatatype


class AlertState(StaticDatatype):
    _collection = 'metagame_event_state'

    def __init__(self, id):
        self.id = id
        data = super(AlertState, self).get_data(self)
        self.name = data.get('name')


class AlertType(StaticDatatype):
    _collection = 'metagame_event'

    def __init__(self, id):
        self.id = id
        data = super(AlertType, self).get_data(self)

        self.description = data.get('description')
        self.experience_bonus = data.get('experience_bonus')
        self.name = data.get('name')

        # Hard-coded descriptions of the base alert types
        # 1 and 6 are currently unused.
        base_alert_types = {'1': 'Territory Control', '2': 'Facility Type',
                            '5': 'Warpgates Stabilizing', '6': 'Conquest',
                            '8': 'Meltdown', '9': 'Unstable Meltdown',
                            '10': 'Aerial Anomalies'}

        self.type = base_alert_types[data.get('type')]