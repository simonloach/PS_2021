# Tic Tac Toe protocol

## Message flow:

```
+----------+----------------+--------+----------------+----------+
| Client 1 |                | Server |                | Client 2 |
+----------+----------------+--------+----------------+----------+
|          | <------------- | MSG(0) | -------------> |          |
|          |                |        |                |          |
|          | <------------- | MSG(1) | -------------> |          |
|          |                | MSG(2) | -------------> |          |
|          |                |        |                |          |
|          |                |        | <------------- |  MSG(3)  |
|          |                | MSG(4) | -------------> |          |
|          | <------------- | MSG(5) |                |          |
|          |                |        |                |          |
|          | <------------- | MSG(2) |                |          |
|          |                |        |                |          |
|  MSG(3)  | -------------> |        |                |          |
|          | <------------- | MSG(4) |                |          |
|          |                | MSG(5) | -------------> |          |
|          |                |  ....  |                |          |
|          |                |        |                |          |
+----------+----------------+--------+----------------+----------+
```

## Message descriptions

- MSG(0) - empty message indicating that client has connected
- MSG(1) - message indicating that server found an opponent for the player and the game begun, it contains information about player cursor
- MSG(2) - empty message telling client it's his turn now
- MSG(3) - message containing two 1 byte values for X and Y using 0 based indexing
- MSG(4) - message with 1 byte (0/1) depending on validity of supplied move
- MSG(5) - message with current board. Containg 9 1 byte values for each cell
    (0 - empty, 1 - circle, 2 - cross), according to the following order:
```
+---+---+---+
| 0 | 1 | 2 |
+---+---+---+
| 3 | 4 | 5 |
+---+---+---+
| 6 | 7 | 8 |
+---+---+---+
```

## Message structure

```
+-------------------------------------------+
|        |                                  |
| MSG ID |          MESSAGE PAYLOAD         |
|        |                                  |
+-------------------------------------------+
```