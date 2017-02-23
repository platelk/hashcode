"""
This is where the magic happen
"""
from entities import *
from collections import OrderedDict
import itertools

import parsing
import output

def resolve(content: str) -> str:
    input_data = parsing.parse(content)
    calculate_output(input_data.endpoints)
    # for _, cache_toi in input_data.cache_servers.items():
    #     print(cache_toi.videos)
    return output.format_output(input_data.cache_servers)


def calculate_one_output(endpoints):
    for endpoint in endpoints:
        cache_servers = endpoint.cache_servers[::]
        cache_servers.append({"server": None, "latency": endpoint.latency})
        cache_servers = sorted(cache_servers, key=lambda x: x["latency"])
        cache_servers = [c["server"] for c in cache_servers]
        temp_videos = [list(g) for k, g in itertools.groupby(endpoint.requests, key=lambda r: r.video.id)]
        videos = {}
        for v in temp_videos:
            if v[0].video not in videos:
                videos[v[0].video] = 0
            videos[v[0].video] += (v[0].video.size * sum([tmp.requests_sum for tmp in v]))
        if len(videos) == 0:
            continue
        videos = OrderedDict(sorted(videos.items(),key=lambda x: x[1])[::-1])
        select_video = list(videos.keys())[0]
        for i, cache in enumerate(cache_servers):
            if cache is None or cache.available_size >= select_video.size:
                if cache is not None:
                    cache.add_video(select_video)
                for i, r in enumerate(endpoint.requests):
                    if r.video.id == select_video.id:
                        endpoint.requests.remove(r)
                break


def calculate_output(endpoints):
    for _ in itertools.count(1):
        calculate_one_output(endpoints)
        end = True
        for e in endpoints:
            if len(e.requests) > 0:
                end = False
                break
        if end is True:
            break

   

if __name__ == "__main__":
    es = [Endpoint(600), Endpoint(900), Endpoint(700)]

    caches = [CacheServer(1, 50000), CacheServer(2, 65000)]

    videos = [Video(50, 1), Video(100, 2), Video(200, 3)]

    es[0].requests.extend([Request(videos[0], es[0], 500), Request(videos[0], es[0], 200)])
    es[0].requests.extend([Request(videos[1], es[0], 300)])

    es[1].requests.extend([Request(videos[1], es[1], 300)])

    es[0].cache_servers.append({"server": caches[0], "latency": 1000})
    es[0].cache_servers.append({"server": caches[1], "latency": 500})
    es[1].cache_servers.append({"server": caches[1], "latency": 800})

    for i, cache in enumerate(caches):
        print(cache.videos)
