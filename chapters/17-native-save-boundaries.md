# 17. Native save boundaries

[← Chapter index](../README.md#chapters)

Vanilla saves have a native serialization and load path. A new resource or runtime object is not persisted simply because it exists in memory.

## Identify the serialization boundary

Follow the game's save operation from its UI request through serialization, wrapping/encoding and file replacement. Follow loading in the reverse direction. Distinguish the on-disk file, a decoded buffer and the runtime records populated from it.

This manual does not publish a complete vanilla save schema, encryption routine or checksum coverage. Do not write an inferred decoded-buffer offset directly into an on-disk save. File length alone does not identify a compatible format.

## Recover fields from controlled differences

Work with copies of saves whose meaningful changes are known. For a candidate field, compare multiple examples that vary only the relevant value, then establish the serializer and reader that access it. Account for timestamps, compression, encryption and checksums before interpreting a binary diff.

A field specification needs offset, width, encoding, range, owner and checksum participation. A pointer-sized number that changes every launch is not automatically a persistent actor identifier. Keep unknown bytes unchanged.

The following code only locates differing byte runs; it does not decode or patch saves:

```python
def changed_runs(a, b):
    if len(a) != len(b):
        raise ValueError('lengths differ; identify the container first')
    runs, start = [], None
    for i, (left, right) in enumerate(zip(a, b)):
        if left != right and start is None:
            start = i
        if left == right and start is not None:
            runs.append((start, i))
            start = None
    if start is not None:
        runs.append((start, len(a)))
    return runs
```

## Separate new persistence from the native format

An extension that needs new saved data must define and implement its own persistence contract, versioning and association with the correct native save. Appending bytes is not assumed to be supported by the stock reader. Do not reuse padding or overwrite native arrays because they appear unused in one file.

Only persistent values belong in such a contract. Actor pointers, pending native calls, render resources and thread-local state must be reconstructed after load. A save error message can have several causes; trace the failing native operation before assigning it to disk capacity or changing file contents.

---

[← Previous chapter](16-replacing-status-icons-without-square-borders.md) · [Chapter index](../README.md#chapters) · [Next chapter →](18-license-boards-prices-and-purchase-previews.md)
