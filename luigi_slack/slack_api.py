import json
from slackclient import SlackClient

class SlackAPI(object):
    
    def __init__(self, token):
        self.client = SlackClient(token)
        self._all_channels = []

    def get_channel_names(self):
        res = self.client.api_call('channels.list')
        channels = json.loads(res.decode())
        return [channel['name'] for channel in channels]

    def get_channel_ids(self):
        res = self.client.api_call('channels.list')
        channels = json.loads(res.decode())
        return [channel['id'] for channel in channels]

    def _get_channels(self):
        res = self.client.api_call('channels.list')
        channels = json.loads(res.decode())
        return channels['channels']

    def get_channels(self, reload_channels=False):
        if not self._all_channels or reload_channels:
            self._all_channels = self._get_channels()
        return self._all_channels

    def channel_name_to_id(self, names):
        name_to_id = []
        for name in names:
            for channel in self._all_channels:
                if channel['name'] == name:
                    name_to_id.append({'name': channel['name'], 'id': channel['id']})
        return name_to_id

    def bulk_message(self, message, channels=[]):
        channel_map = self.channel_name_to_id(channels)
        print(channel_map)
        for channel in channel_map:
            self.client.api_call('chat.postMessage',
                                 text=message,
                                 channel=channel['id'],
                                 username='Luigi-Slack Bot')
