from entities import CacheServer
from entities import Endpoint
from entities import Request
from entities import Video
from entities import InputData


def parse_first_line(line):
    split_line = line.split(' ')
    return {
        'videos_count': int(split_line[0]),
        'endpoints_count': int(split_line[1]),
        'requests_count': int(split_line[2]),
        'cache_servers_count': int(split_line[3]),
        'cache_server_capacity': int(split_line[4]),
    }


def parse_videos(line):
    videos = []
    videos_size = line.split(' ')
    for i, video_size in enumerate(videos_size):
        videos.append(Video(size=int(video_size), video_id=i))
    return videos


def parse_endpoints_and_cache_servers(lines, endpoints_count, cache_server_size):
    endpoints = []
    cache_servers = {}
    endpoint_id = 0
    line_counter = 0
    while endpoint_id < endpoints_count:
        endpoint_data = lines[line_counter].split(' ')
        new_endpoint = Endpoint(latency=int(endpoint_data[0]))
        endpoint_id += 1
        line_counter += 1
        for i in range(0, int(endpoint_data[1])):
            cache_server_data = lines[line_counter].split(' ')
            new_cache_server = CacheServer(server_id=int(cache_server_data[0]), max_size=cache_server_size)
            cache_servers[int(cache_server_data[0])] = new_cache_server
            new_endpoint.cache_servers.append({'server': new_cache_server, 'latency': int(cache_server_data[1])})
            line_counter += 1
        endpoints.append(new_endpoint)
    return endpoints, cache_servers


def parse_requests(lines, videos, endpoints):
    requests = []
    for line in lines:
        request_data = line.split(' ')
        endpoint = endpoints[int(request_data[1])]
        new_request = Request(
            video=videos[int(request_data[0])],
            origin_endpoint=endpoint,
            requests_sum=int(request_data[2])
        )
        requests.append(new_request)
        endpoint.requests.append(new_request)
    return requests


def parse(content):
    lines = content.split('\n')
    lines = lines[:len(lines) - 1]
    general_info = parse_first_line(lines[0])
    lines = lines[1:]
    videos = parse_videos(lines[0])
    lines = lines[1:]
    (endpoints, cache_servers) = parse_endpoints_and_cache_servers(
        lines,
        general_info.get('endpoints_count'),
        general_info.get('cache_server_capacity'),
    )
    requests = parse_requests(
        lines[len(lines) - general_info.get('requests_count'):],
        videos,
        endpoints
    )
    return InputData(
        videos=videos,
        endpoints=endpoints,
        cache_servers=cache_servers,
        requests=requests
    )
