# myscale

This is just a very simplified version of the [Xiaomi_Scale.py](https://github.com/lolouk44/hassio-addons/blob/master/mi-scale/src/Xiaomi_Scale.py) script to work with the Mi Scale 1. The reason for this project is that the original script was coupled to `MTQQ` and this one **only** provides the data that the scale sends.

## Installation

Just create a new Python environment and add the dependency.

```
       $ python3 -m venv venv
       $ . ./venv/bin/activate
(venv) $ pip3 install bluepy
```

As you might want to run the script as a non root user, just do this.

```
sudo setcap 'cap_net_raw,cap_net_admin+eip' $(find venv -name bluepy-helper)
```

## Usage

```
$ bluetoothctl devices | grep MI_SCALE
Device 88:0F:10:95:6D:4F MI_SCALE

(venv) $ ./myscale.py 88:0F:10:95:6D:4F
{'weight': 73.4, 'unit': 'kg', 'timestamp': '2022-04-18T19:42:15'}
```
