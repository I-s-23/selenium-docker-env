# selenium_task

## startup

```bash
Xvfb :99 -ac &
touch ~/.Xauthority && xauth generate :99 . trusted && xauth add ${HOST}:99 . $(xxd -l 16 -p /dev/urandom) && xauth list
```

## command

```bash
  python app/main.py
```


## issue


## refalene

