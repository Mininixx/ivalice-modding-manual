"""Read PE metadata and bytes at preferred VAs. Never attaches to a process."""
import argparse
import hashlib
import json
from pathlib import Path
import struct


def inspect(data, addresses, size):
    def unpack(fmt, offset):
        width = struct.calcsize(fmt)
        if offset < 0 or offset + width > len(data):
            raise ValueError('truncated PE header')
        return struct.unpack_from(fmt, data, offset)

    if data[:2] != b'MZ':
        raise ValueError('missing MZ signature')
    pe, = unpack('<I', 0x3C)
    if data[pe:pe + 4] != b'PE\0\0':
        raise ValueError('missing PE signature')
    machine, sections, timestamp = unpack('<HHI', pe + 4)
    optional_size, = unpack('<H', pe + 20)
    optional = pe + 24
    magic, = unpack('<H', optional)
    if magic != 0x20B or optional_size < 64:
        raise ValueError('expected a PE32+ optional header')
    image_base, = unpack('<Q', optional + 24)
    image_size, headers_size = unpack('<II', optional + 56)
    table = optional + optional_size
    if sections == 0 or table + sections * 40 > len(data):
        raise ValueError('invalid section table')
    regions = []
    for index in range(sections):
        header = table + index * 40
        virtual_size, rva, raw_size, raw = unpack('<IIII', header + 8)
        regions.append((rva, max(virtual_size, raw_size), raw_size, raw))

    result = {
        'bytes': len(data),
        'sha256': hashlib.sha256(data).hexdigest(),
        'sha1': hashlib.sha1(data).hexdigest(),
        'machine': hex(machine),
        'preferred_image_base': hex(image_base),
        'size_of_image': image_size,
        'timestamp': hex(timestamp),
        'regions': [],
    }
    for va in addresses:
        rva = va - image_base
        if rva < 0 or rva + size > image_size:
            raise ValueError(f'VA {va:#x} is outside the image')
        offset = None
        if rva + size <= headers_size:
            offset = rva
        else:
            candidates = [(start, raw_size, raw) for start, span, raw_size, raw in regions
                          if start <= rva and rva + size <= start + span]
            if len(candidates) != 1:
                raise ValueError(f'VA {va:#x} has no unique containing section')
            start, raw_size, raw = candidates[0]
            if rva + size > start + raw_size:
                raise ValueError(f'VA {va:#x} includes virtual-only bytes')
            offset = raw + rva - start
        if offset < 0 or offset + size > len(data):
            raise ValueError(f'VA {va:#x} has a truncated raw range')
        result['regions'].append({'preferred_va': hex(va), 'rva': hex(rva),
                                  'file_offset': hex(offset),
                                  'hex': data[offset:offset + size].hex(' ')})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('executable', type=Path)
    parser.add_argument('--va', action='append', type=lambda value: int(value, 0), default=[])
    parser.add_argument('--size', type=int, default=16)
    args = parser.parse_args()
    if not 1 <= args.size <= 4096:
        parser.error('--size must be between 1 and 4096 bytes')
    try:
        result = inspect(args.executable.read_bytes(), args.va, args.size)
    except (OSError, ValueError, struct.error) as error:
        parser.error(str(error))
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
