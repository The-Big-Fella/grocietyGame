# grocietyGame


## BackEnd

### Start the backend

```bash
make shell 

make install_deps

# mocking the backend
make start_mock_backend

# start the normal backend
make start_backend
```



# protocol

## reading from serial connection

### Packet Structure

Each packet represents the full state of a single controller.

| Sync      | msg      | Controller | Control    | Control Entries        |
|-----------|----------|------------|------------|------------------------|
| SYNC (1B) |TYPE (1B) |ID (1B)     | Count (1B) | (2 bytes each)         |

### Control Entry Format

Each control entry consists of exactly 2 bytes:

| Control ID | Value      |
|------------|------------|
| (1 byte)   | (1 byte)   |

### example packet : 

`\xAA\0x00\cx00\x04\x00\x00\x01\x00\x02\x00\x03\x00`

### mocking

to mock the serial communication between the controller and the grocietyGame
we use socat. in the `make start_mock_backend` commando

```bash
sudo socat -d -d \
  PTY,link=/dev/ttyV0,raw,echo=0 \
  PTY,link=/dev/ttyV1,raw,echo=0
```
