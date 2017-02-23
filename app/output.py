#!/usr/bin/env python3

def get_used_caches_count(cache_list):
    caches_used = 0

    for cache in cache_list:
        if cache_list[cache].max_size != cache_list[cache].available_size:
            caches_used += 1

    return caches_used


def format_output(cache_list):
    output_str = str(get_used_caches_count(cache_list)) + "\n"

    for cache in cache_list:
        if cache_list[cache].max_size != cache_list[cache].available_size:
            output_str += str(cache.id)

            for video in cache_list[cache].videos:
                output_str += " " + str(cache_list[cache].videos[video].id)

            output_str += "\n"

    return output_str
