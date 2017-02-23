#!/usr/bin/env python3

def get_used_caches_count(cache_list):
    caches_used = 0

    for i, cache in cache_list.items():
        if cache.max_size != cache.available_size:
            caches_used += 1

    return caches_used


def format_output(cache_list):
    output_str = str(get_used_caches_count(cache_list)) + "\n"

    for i, cache in cache_list.items():
        if cache.max_size != cache.available_size:
            output_str += str(cache.id)

            for j, video in cache.videos.items():
                output_str += " " + str(video.id)

            output_str += "\n"

    return output_str
