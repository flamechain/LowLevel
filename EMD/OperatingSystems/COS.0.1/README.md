# COS

This is a x64 OS built from scratch.

## Build

Docker container:

```bash
docker build buildenv -t cos-buildenv
```

Running container:

```bash
docker run --rm -it -v %cd%:/root/env cos-buildenv
```

Running OS:

```bash
MINGW64 ~/kernel
$ make run
```
