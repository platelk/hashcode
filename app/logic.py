"""
This is where the magic happen
"""
from entities import *
from collections import OrderedDict
import itertools

def resolve(content: str) -> str:
    return "nothing"


def calculate_output(endpoints):
    for endpoint in endpoints:
        cache_servers = [c["server"] for c in sorted(endpoint.cache_server, key=lambda x: x["latency"])]
        temp_videos = [list(g) for k, g in itertools.groupby(endpoint.requests, key=lambda r: r.video.id)]
        videos = {}
        for v in temp_videos:
            if v.video_id not in videos:
                videos[v.video] = 0
            videos[v.video] += v.requests_sum
        videos = OrderedDict(sorted(videos.items()))
        select_video = list(videos.keys())[0]
        for cache in cache_servers:
            if cache.available_size > select_video.size:
                cache.add_video(select_video)
                for i, r in enumerate(endpoint.requests):
                    if r.video.id == select_video.id:
                        del endpoint[i]
                break 

if __name__ == "__main__":
    print("Lol")
    es = [Endpoint(300), Endpoint(500), Endpoint(800)]
 
    caches = [CacheServer(1, 50000), CacheServer(2, 65000)]

    es[0].requests.extend([Request(1, es[0], 500), Request(1, es[0], 200)])
    es[0].requests.extend([Request(2, es[0], 300)])

    es[0].cache_servers.extend(caches)
    es[1].cache_servers.append(caches[1])

    calculate_output(es) 
