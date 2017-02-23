"""
List entities returned by the parsing
"""


class InputData:
    def __init__(self, videos, endpoints, requests, cache_servers):
        self.videos = videos
        self.endpoints = endpoints
        self.cache_servers = cache_servers
        self.requests = requests


class Video:
    def __init__(self, size=0, video_id=0):
        self.size = size
        self.id = video_id


class Endpoint:
    def __init__(self, latency=0):
        # Latency to datacenter
        self.latency = latency
        # List of maps
        self.cache_servers = []
        self.requests = []
        self._save_requests = []

    def save_requests(self):
        self._save_requests = self.requests[::]

    def restore(self):
        self.requests = self._save_requests


class CacheServer:
    def __init__(self, server_id=0, max_size=0):
        self.id = server_id
        self.available_size = max_size
        self.videos = []
        self.max_size = max_size

    def add_video(self, video):
        self.videos.append(video)
        self.available_size -= video.size


class Request:
    def __init__(self, video, origin_endpoint, requests_sum):
        self.video = video
        self.origin_endpoint = origin_endpoint
        self.requests_sum = requests_sum
