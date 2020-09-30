# pync

Keep two directories in sync with Python.

In a terminal, in the same directory of pync.py, type:

```sh
python3 pync.py <source> <dest> [--no-recursion]
```

or

```sh
chmod u+x pync.sh
./pync.sh  <source> <dest> [--no-recursion]
```

Use absolute paths for `source` and `dest` directories.

With `--no-recursion` triggers only in the exact location.

It is also possible to install:

```sh
cp pync.py ~/.local/bin/pync
chmod u+x ~/.local/bin/pync
```

And then:

```bash
pync <source> <dest> [--no-recursion]
```
