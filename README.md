# CSCE 4110 Project

## Team Members - Group 11

* [Leann Kahal](https://github.com/lnkl26)
* [Prasuna Khadka]()
* [Ibrahim Chaudhry](https://github.com/IChaudhry892)

## Adapted IEEE Paper:

[Study of Encrypted Transmission of Private Data During Network Communication: Performance Comparison of Advanced Encryption Standard and Data Encryption Standard Algorithms](https://ieeexplore.ieee.org/document/10958823)

## Prerequisites:

This program requires **Python 3** and a virtual environment containing the necessary modules.

All required modules are included in the `venv` folder. 

## How to run:

### 1. Activate the virtual environment

```bash
$ source venv/bin/activate
```

### 2. Run the main program

```python
$ python main.py
```

If **python** invokes Python 2 on your system, use `python3` instead.

## Running the Sensitivity Tests:

### Run Both AES and DES tests

```python
$ python sensitivity_tests.py
```

### Run DES tests only

```python
$ python sensitivity_tests.py --run-des-tests
```

### Run AES tests only

```python
$ python sensitivity_tests.py --run-aes-tests
```

### Run AES tests with display blocks option

```python
$ python sensitivity_tests.py --run-aes-tests-blocks
```

## Running Encryption Efficiency Tests

### To Run AES Tests

```python
$ python encryption_efficiency_test.py --run-aes-test
```

### To Run DES Tests

```python
$ python encryption_efficiency_test.py --run-des-test
```

## Running Security Tests

### To Run AES Tests

```python
$ python security_test.py --run-aes-test
```

### To Run DES Tests

```python
$ python security_test.py --run-des-test
```

## Running Attack Resistance Tests

Before running the tests, packets must be generated. This can be done by running the following `bash` command in the `data` directory:

```bash
$ cd data
$ bash packet_generate.sh
```

If you're running the program on a MacOS, packets must be generated this way:

```bash
$ cd data
$ chmod +x packet_generate_mac.sh
$ ./packet_generate_mac.sh
```

### To Run AES Tests

```python
$ python attack_resistance_test.py --run-aes-test
```

### To Run DES Tests

```python
$ python attack_resistance_test.py --run-des-test
```
