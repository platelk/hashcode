#!/usr/bin/env python3

"""
Entry point of the app
"""

import argparse
import logging
import ntpath
import os
import sys
import time

import logic


def parse_argument():
    parser = argparse.ArgumentParser()

    parser.add_argument("-v", "--verbosity", type=str,
                        choices=["debug", "info", "warning", "error", "critical"],
                        default="debug",
                        help="increase output verbosity")
    parser.add_argument("-d", "--directory", type=str,
                        help="Path to a specific directory where all the file will be tested")
    parser.add_argument("file", type=str, action="append",
                        help="input file")
    parser.add_argument("-o", "--output", type=str, default="out",
                        help="Output directory for the answers")

    return parser.parse_args()


def set_logger(level: str) -> None:
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % level)
    logging.basicConfig(level=numeric_level)


def get_input_files(files: list, directory: str) -> list:
    if directory is not None:
        onlyfiles = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        files.extend(onlyfiles)
    for i, file_path in enumerate(files):
        if not os.access(file_path, os.R_OK):
            logging.error("file %s is not accessible, will be skiped...", file_path)
            del files[i]
    return files


def get_output_dir(path: str) -> str:
    if not os.path.exists(path):
        os.makedirs(path)
    if not os.path.isdir(path):
        logging.critical("Specified output directory is not a directory")
        sys.exit(1)
    return path


def main():
    """
    main functions
    """
    args = parse_argument()
    output_dir = ""
    files = []
    if args is not None:
        set_logger(args.verbosity)
        files = get_input_files(args.file, args.directory)
        output_dir = get_output_dir(args.output)
    logging.info("Running hashcode...")
    for file_path in files:
        logging.info("Passing on %s...", file_path)
        with open(file_path, 'r') as file:
            content = file.read()

            start_time = time.time()
            result = logic.resolve(content)
            elapse = time.time() - start_time
            logging.debug("    Resolved in %s", elapse)

            output_file_path = output_dir + "/" + ntpath.basename(file_path) + ".out"
            with open(output_file_path, "w+") as output_file:
                logging.debug("    write result in %s", output_file_path)
                output_file.write(result)
    logging.info("Finish !")

if __name__ == "__main__":
    main()
