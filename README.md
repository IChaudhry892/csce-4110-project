# CSCE 4110 Project

## Team Members - Group 11

* [Leann Kahal](https://github.com/lnkl26)
* [Prasuna Khadka]()
* [Ibrahim Chaudhry](https://github.com/IChaudhry892)

## Adapted IEEE Paper:

[Study of Encrypted Transmission of Private Data During Network Communication: Performance Comparison of Advanced Encryption Standard and Data Encryption Standard Algorithms](https://ieeexplore.ieee.org/document/10958823)

## Prerequisites:

This program requires **Python 3** and a virtual environment containing the necessary modules.
<br>
All required modules are incuded in the `venv` folder. 

## How to run:

### 1. Activate the virtual environment
```
$ source venv/bin/activate
```
### 2. Run the main program
```
$ python main.py
```
If **python** invokes Python 2 on your system, use `python3` instead.

## Running the Sensitivity Tests:

### Run Both AES and DES tests
```
$ python sensitivity_tests.py
```
### Run DES tests only
```
$ python sensitivity_tests.py --run-des-tests
```
### Run AES tests only
```
$ python sensitivity_tests.py --run-aes-tests
```
### Run AES tests with display blocks option
```
$ python sensitivity_tests.py --run-aes-tests-blocks
```