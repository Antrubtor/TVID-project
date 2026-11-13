import re

import imageio
import numpy


def read_pgm(filename, byteorder=">"):
    """Return image data from a raw PGM file as numpy array.
    Format specification: http://netpbm.sourceforge.net/doc/pgm.html
    """
    with open(filename, "rb") as f:
        buffer = f.read()
    try:
        temp = re.search(
            b"(^P5\\s(?:\\s*#.*[\r\n])*"
            b"(\\d+)\\s(?:\\s*#.*[\r\n])*"
            b"(\\d+)\\s(?:\\s*#.*[\r\n])*"
            b"(\\d+)\\s(?:\\s*#.*[\r\n]\\s)*)",
            buffer,
        )

        if temp is None:
            raise ValueError("Not a raw PGM file: '{filename}'")

        header, width, height, maxval = temp.groups()

    except AttributeError:
        raise ValueError(f"Not a raw PGM file: '{filename}'")

    return numpy.frombuffer(
        buffer,
        dtype="u1" if int(maxval) < 256 else byteorder + "u2",
        count=int(width) * int(height),
        offset=len(header),
    ).reshape((int(height), int(width)))


def write_ppm(path, matrix):
    imageio.imwrite(path, matrix, format="PPM-FI", flags=1)
