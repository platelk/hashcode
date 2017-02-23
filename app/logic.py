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

    calculate_output(input_data.endpoints, input_data.cache_servers)
    return output.format_output(input_data.cache_servers)


def calculate_one_endpoint_output(endpoint, optimize=False):
    cache_servers = endpoint.cache_servers[::]
    cache_servers.append({"server": None, "latency": endpoint.latency})
    cache_servers = sorted(cache_servers, key=lambda x: x["latency"])
    cache_servers = [c["server"] for c in cache_servers]
    temp_videos = [list(g) for k, g in itertools.groupby(endpoint.requests, key=lambda r: r.video.id)]
    videos = {}
    for v in temp_videos:
        if v[0].video not in videos:
            videos[v[0].video] = 0
        videos[v[0].video] += sum([tmp.requests_sum for tmp in v])
    if len(videos) == 0:
        return
    videos = OrderedDict(sorted(videos.items(),key=lambda x: x[1])[::-1])
    select_video = list(videos.keys())[0]

    if optimize is False:
        for i, cache in enumerate(cache_servers):
            if cache is not None and select_video in cache.videos:
                for i, r in enumerate(endpoint.requests):
                    if r.video.id == select_video.id:
                        endpoint.requests.remove(r)
                return
    for i, cache in enumerate(cache_servers):
        if cache is None or cache.available_size >= select_video.size:
            if cache is not None and select_video not in cache.videos:
                cache.add_video(select_video)
            for i, r in enumerate(endpoint.requests):
                if r.video.id == select_video.id:
                    endpoint.requests.remove(r)
            break

def calculate_one_output(endpoints, optimize=False):
    endpoints = sorted(endpoints, key=lambda e: sum([r.requests_sum for r in e.requests]))

    for endpoint in endpoints:
        calculate_one_endpoint_output(endpoint, optimize)


def calculate_output(endpoints, caches):
    for e in endpoints:
        e.save_requests()

    for _ in itertools.count(1):
        calculate_one_output(endpoints)
        end = True
        for e in endpoints:
            if len(e.requests) > 0:
                end = False
                break
        if end is True:
            break
    for e in endpoints:
        e.restore()
    for _ in itertools.count(1):
        calculate_one_output(endpoints, True)
        end = True
        for e in endpoints:
            if len(e.requests) > 0:
                end = False
                break
        if end is True:
            break

if __name__ == "__main__":
    es = [Endpoint(1000), Endpoint(500)]

    caches = [CacheServer(1, 100), CacheServer(2, 100), CacheServer(3, 100)]

    videos = [Video(50, 0), Video(50, 1), Video(80, 2), Video(80, 3), Video(110, 4)]

    es[0].requests.extend([Request(videos[2], es[0], 1500), Request(videos[3], es[0], 500), Request(videos[0], es[0], 1000)])
    es[1].requests.extend([Request(videos[0], es[1], 1000)])

    es[0].cache_servers.append({"server": caches[0], "latency": 100})
    es[0].cache_servers.append({"server": caches[1], "latency": 300})
    es[0].cache_servers.append({"server": caches[2], "latency": 200})

    calculate_output(es, caches)

    for i, cache in enumerate(caches):
        print("cache " + str(i) + " | used " + str(cache.max_size - cache.available_size) + " / " + str(cache.max_size))
        for v in cache.videos:
            print("\t" + str(v.id))
