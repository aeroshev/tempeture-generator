from typing import Iterator
import random


_template = "{date}, {area}, {sensor}, {value};"


def get_data() -> Iterator[str]:
    while True:
        output = _template.format(
            date='',
            area='',
            sensor='',
            value=''
        )
        yield output
