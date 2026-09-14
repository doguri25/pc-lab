# PC LAB v2.3.0 source archive

The GitHub connector used to publish this repository has a per-request text transfer limit. To preserve the complete v2.3.0 project without losing files, the full source snapshot is stored here as Base64 chunks of one `tar.xz` archive.

## Restore

From the repository root:

```bash
python source-archive/restore_source.py
```

The complete snapshot will be extracted to `restored-source/`.

The archive includes the v2.3.0 source modules, documentation, tests, release metadata, and standalone HTML builds that were present in the source package at publication time.

## Files

- `part-00.b64` … `part-09.b64`: ordered Base64 chunks
- `restore_source.py`: concatenates, decodes and extracts the archive

Do not reorder or edit the chunk files.
