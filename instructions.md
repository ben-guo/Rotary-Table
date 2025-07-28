# Connection
| Setting      | Value  |
|--------------|--------|
| Baud Rate    | 115200 |
| Data Bits    | 8      |
| Stop Bits    | 1      |
| Parity       | none   |
| Flow Control | none   | 

# Commands

## 1. Run at constant speed without specified end point

Forward direction: 
```
0x55  0xaa  0x06  0x09  speed  0x00  0x00  0x00  0xc3
```
Reverse direction: 
```
0x55  0xaa  0x06  0x0A  speed  0x00  0x00  0x00  0xc3
```

The `speed` is 2 bytes, little-endian.<br><br><br>

For example, to run forward at a speed of 2400 Hz, the instruction is: 
```
0x55  0xaa  0x06  0x09  0x60  0x09  0x00  0x00  0x00  0xc3
                          |     |
                          |     |
2400 = 0x0960           0x60  0x09
```

## 2. Run at constant speed with specified end point
Absolute motion:
```
0x55  0xaa  0x07  speed  coordinate  0xc3
```
Incremental motion:
```
0x55  0xaa  0x08  speed  steps  0xc3
```

The `speed` is 2 bytes, little-endian.  
The `coordinate` is 4 bytes, little-endian.  
The `steps` are 4 bytes, little-endian.<br><br><br>

For example, to move at 20,000 Hz to coordinate 100,000, the instruction is:
```
0x55  0xaa  0x07  0x20  0x4E  0xA0  0x86  0x01  0x00  0xc3
                    |     |     |     |     |     |
                    |     |     |     |     |     |
20,000  = 0x4E20    |     |     |     |     |     |
                  0x20  0x4E    |     |     |     |
                                |     |     |     |
100,000 = 0x000186A0            |     |     |     |
                              0xA0  0x86  0x01  0x00
```

## 3. Set coordinate
```
0x55  0xaa  0x09  coordinate  0xc3
```
The `coordinate` is 4 bytes, little-endian. 

## 4. Stop
```
0x55  0xaa  0x02  0x00  0x00  0x00  0x00  0x00  0x00  0xc3
```

## 5. Return to mechanical zero
Forward direction: 
```
0x55  0xaa  0x0b  0x09  speed  0x00  0x00  0x00  0xc3
```
Reverse direction: 
```
0x55  0xaa  0x0b  0x0a  speed  0x00  0x00  0x00  0xc3
```
The ```speed``` is 2 bytes, little-endian.