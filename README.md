This is a project for importing names and faces into Anki.

# Setup

## Dependencies

- Anki
- AnkiServer
- python2.7
- python-gflags

## How to install python-gflags

```
pip install python-gflags
```

## How to get AnkiServer to work

You should install [Anki](https://apps.ankiweb.net/) first. Then use the following instructions to get the `anki` python package.

0. Install AnkiServer:

```
pip install AnkiServer
```

1. Get path to python home:

```
export PYTHONHOME=$(python -c "from distutils.sysconfig import get_python_lib; import os; parts = get_python_lib().split(os.path.sep)[:-3]; print(os.path.sep.join(parts))")
```

2. Add AnkiServer to PYTHONPATH:

```
export PYTHONPATH=$PYTHONPATH:$PYTHONHOME/anki-bundled
```

# Example Usage

1. First, you need to create a new Profile in Anki. Let's say the name you chose is `darold`.

2. After creating a profile, quit Anki. You should now have a file at `/Users/$USERNAME/Documents/Anki/darold/collection.anki2`.

3. Create the deck!

```
export PYTHONIOENCODING=utf-8
python main.py \
--collection_path /Users/$USERNAME/Documents/Anki/darold/collection.anki2 \
--deck_name my-example-deck \
--input example.json
```

Feel free to create your own `example.json` file with your own set of names and urls.
