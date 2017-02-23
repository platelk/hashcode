"""
List entities returned by the parsing
"""


class InputData:
    def __init__(self, videos, endpoints, requests):
        self.videos = videos
        self.endpoints = endpoints
        self.requests = requests


class Video:
    def __init__(self, size=0):
        self.size = size


class Endpoint:
    def __init__(self, latency=0):
        self.latency = latency
        self.cache_servers = []


class CacheServer:
    def __init__(self, server_id=0, latency=0):
        self.id = server_id
        self.latency = latency


class Request:
    def __init__(self, video_id, origin_endpoint, requests_sum):
        self.video_id = video_id
        self.origin_endpoint = origin_endpoint
        self.requests_sum = requests_sum
