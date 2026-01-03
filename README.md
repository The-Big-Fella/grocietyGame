# grocietyGame


## BackEnd
- start backend : `make start_backend`

### backend setup
- create a virtual venv `make create_venv`
- activate virtual venv `make activate_venv`
- install deps `make install_deps`

### update deps
when installed new dep update the dependencies
- update deps `make update_deps`


# protocol

## reading from serial connection

### Packet Structure

Each packet represents the full state of a single controller.

+-----------+-----------+--------------------------------------+
| Sync      | Controller | Control    | Control Entries        |
| SYNC (1B) |ID (1B)     | Count (1B) | (2 bytes each)         |
+-----------+-----------+--------------------------------------+

### Control Entry Format

Each control entry consists of exactly 2 bytes:

+------------+------------+
| Control ID | Value      |
| (1 byte)   | (1 byte)   |
+------------+------------+

example : `\xAA\x00\x04\x00\x00\x01\x00\x02\x00\x03\x00`
