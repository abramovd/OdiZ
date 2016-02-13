# OdiZ - Operations on Discrete Z-numbers

**OdiZ** is a standalone application for operations on discrete Z-numbers, which we proposed by **Prof. Lofti A. Zadeh**. Z-numbers

The concept of a Z-number is intended to provide a basis for computation with numbers which are not totally reliable. More concretely, a Z-number, Z=(A,B), is an ordered pair of two fuzzy numbers:

* the first number, A, is a restriction on the values which a real-valued variable, X, can take.
* the second number, B, is a restriction on the degree of certainty that X is A. Typically, A and B are described in a natural language.

## Supported operations

* Addition
* Substraction
* Multiplication
* Division
* Minimum
* Maximum

### Installation and Running from Source Code

In order to install OdiZ on your local machine you need to complete the following steps in your terminal.

#### _Step 1_

Clone this git repo there:

```sh
$ git clone https://github.com/abramovd/OdiZ.git
```
Now you have ```OdiZ``` folder in your current directory, move there:
```sh
$ cd OdiZ
```

#### _Step 2_

OdiZ depends on Numpy, Scipy and Matplotlib packages. So, you need to install all the dependencies listed in ```requirements.txt``` with Pip:

```sh
$ pip install -r requirements.txt
```

#### _Step 3_

Now you shoud run OdiZ.py with Pythpon 2.X or 3.X (2.X is preferable).

```sh
cd OdiZ
python OdiZ.py
```


