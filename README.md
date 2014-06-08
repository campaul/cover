# cover

Album art manager

## Dependencies

`cover` depends on Python 3 and PyGObject. I've had trouble installing PyGObject with pip, so I recommend installing it manually or with your system's package manager if you have trouble. If you do this, you'll need to use the `--system-site-packages` argument with virtualenv.

```bash
virtualenv --system-site-packages -p /usr/bin/python3 env
source env/bin/activate
```

## Usage

You can fetch album art from the command line by providing an artist and album name.

```bash
python -m cover 'Red Hot Chili Peppers' 'Stadium Arcadium'
```
