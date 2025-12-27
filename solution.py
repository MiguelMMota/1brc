#
#  Copyright 2023 The original authors
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

# TODO: efficiency ideas:
# 1. Custom hashing
# 2. "|".join(item) instead of f"{_min}|{_sum/_count:.1f}|{_max}"
# 3. More efficient data aggregation and dict sorting?
# 4. Use string formatting to print ints as single decimal place floats instead of doing multiplication

from collections import defaultdict
from copy import deepcopy
import math
import mmap
import multiprocessing
import os


CPU_COUNT = os.cpu_count()
MMAP_PAGE_SIZE = os.sysconf("SC_PAGE_SIZE")
DEFAULT_DATUM = [math.inf, -math.inf, 0, 0]


def process_chunk(file_path, start_byte, end_byte):
    offset = (start_byte // MMAP_PAGE_SIZE) * MMAP_PAGE_SIZE
    data = defaultdict(lambda: deepcopy(DEFAULT_DATUM))

    with open(file_path, "rb") as file:
        length = end_byte - offset

        with mmap.mmap(
            file.fileno(), length, access=mmap.ACCESS_READ, offset=offset
        ) as mm:
            mm.seek(start_byte - offset)
            for line in iter(mm.readline, b""):
                semicolon_pos = line.find(b';')
                station = line[:semicolon_pos]
                
                temp_bytes = line[semicolon_pos+1:]

                # if the first byte is less than b'0' (i..e: it's b'-'), offset will be 1. Otherwise (i.e.: it's a digit, it will be 0)
                offset = 1 - temp_bytes[0] // 48
                # if the first byte is "-", offset is 1, and sign is 1-2=-1. If the first byte is a digit, offset is 0, and sign is 1-0=1
                sign = 1 - 2 * offset
                # NB: the alternative to the code above is adding an if-statement to check if the first byte is b'-', but we're likely to
                # incur high penalties from CPU branch predicition, assuming the odds of the character being in the dataset are close to 50%

                temperature = (temp_bytes[offset] - 48) * 10

                # TODO: this will now only ever go over the digit before the decimal place if there are two digits
                # before the decimal place. I wonder if there's a better way to do this, instead of slicing the list
                # for a single iteration.
                for b in temp_bytes[offset+1:-3]:  # lines end with ".[digit]\n" (or r"\.\d\n"), which we want to ignore for now
                    temperature += b - 48  # ord(b'0')
                    temperature *= 10

                temperature += temp_bytes[-2] - 48  # ord(b'0'). We check the penultimate character, because the line ends with "\n"
                temperature *= sign

                entry = data[station]
                entry[0] = min(temperature, entry[0])
                entry[1] = max(temperature, entry[1])
                entry[2] += temperature
                entry[3] += 1

    return data


def main():
    file_size_bytes = os.path.getsize("measurements.txt")
    base_chunk_size = file_size_bytes // CPU_COUNT
    chunks = []

    with open("measurements.txt", "r+b") as f:
        with mmap.mmap(
            f.fileno(), length=0, access=mmap.ACCESS_READ
        ) as mm:
            start_byte = 0
            for _ in range(CPU_COUNT):
                # If mmaped_file.find(...) is -1 (b"\n") not found, mmap.find(...) + 1 will be 0, which will default to file_size_bytes
                end_byte = mm.find(b"\n", min(start_byte + base_chunk_size, file_size_bytes)) + 1 or file_size_bytes
                chunks.append(("measurements.txt", start_byte, end_byte))
                start_byte = end_byte

    with multiprocessing.Pool(processes=CPU_COUNT) as p:
        results = p.starmap(process_chunk, chunks)

    data = defaultdict(lambda: deepcopy(DEFAULT_DATUM))
    for result in results:
        for station, item in result.items():
            entry = data[station]
            entry[0] = min(item[0], entry[0])
            entry[1] = max(item[1], entry[1])
            entry[2] += item[2]
            entry[3] += item[3]

    aggregate_data = {}
    for station, (_min, _max, _sum, _count) in data.items():
        aggregate_data[station.decode('utf-8')] = f"{0.1*_min:.1f}|{0.1*_sum/_count:.1f}|{0.1*_max:.1f}"

    print(dict(sorted(aggregate_data.items())))


if __name__ == "__main__":
    main()
