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
# 1. Pypy
# 2. Handle floats as ints
# 3. Custom hashing
# 4. Avoid branch predictions with high odds of failure
# 5. SIMD


def process_line(line: str) -> tuple[str, float]:
    station, temperature = line.split(";")
    return station, float(temperature)


def main() -> None:
    data = {}
    with open("measurements.txt", "r") as f:
        for line in f:
            station, temperature = process_line(line)
            if station in data:
                data[station]["min"] = min(temperature, data[station]["min"])
                data[station]["max"] = max(temperature, data[station]["max"])
                data[station]["sum"] = temperature + data[station]["sum"]
                data[station]["count"] += 1
            else:
                data[station] = {
                    "min": temperature,
                    "max": temperature,
                    "sum": temperature,
                    "count": 1,
                }

    aggregate_data = {}
    for station, datum in data.items():
        aggregate_data[station] = f"{datum['min']}|{datum['sum'] / datum['count']:.1f}|{datum['max']}"

    print(dict(sorted(aggregate_data.items())))


if __name__ == "__main__":
    main()
