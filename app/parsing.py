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


# def parse_videos(lines):



def parse(content):
    lines = content.split('\n')
    general_info = parse_first_line(lines[0])
    lines = lines[:-1]
    # videos = parse_videos(lines[:general_info.get('videos_count')])
    return InputData(
        videos=videos,
        # endpoints=endpoints,
        # requests=requests
    )
