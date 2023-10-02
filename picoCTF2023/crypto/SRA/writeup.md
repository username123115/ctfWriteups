# SRA #

## Overview ##

400 points

Category: [Crypto](../)

Tags: `picoCTF 2023` `Cryptography` `RSA`

## Description ##

I just recently learnt about the SRA public key cryptosystem... or wait, was it supposed to be RSA?

Hmmm, I should probably check... 

Connect to the program on our server: nc saturn.picoctf.net PORT

Download the program: [chal.py](https://artifacts.picoctf.net/c/297/chal.py)

## Solution ##

Looking at the challenge file, we see that this challenge is encrypting a message `pride` into the ciphertext `anger`, the challenge gives us the ciphertext `anger` and the private key `envy` and asks for the plaintext `pride`. While we have the private key, we are unable to decrypt the message as we do not have the public modulus `lust`, the product of the two primes `gluttony` and `greed`. In order to solve this challenge, we must find the product of the two primes. Luckily, most of the thinking was done for me in [this stack overflow article](https://crypto.stackexchange.com/questions/81615/calculating-rsa-public-modulus-from-private-exponent-and-public-exponent)

First, I will refer to the ciphertext `anger` as `c`, the private key `envy` as `d`, the primes as `p` and `q`, and the public exponent = 65537 as `e`.

We know that `d` * `e` is congruent to 1 modulo `(p - 1)* (q - 1)`, meaning that `(p - 1)(q - 1)` divides `ed - 1`. Therefore by factoring `ed - 1` we can guess the values of `p - 1` and `q - 1` and thus the values of the primes themselves. We can write `ed - 1` as `k * (p - 1) * (q - 1)`. 

After factoring `ed - 1`, we have many combinations of factors to choose for `k`, `p - 1`, and `q - 1`, however there are some restrictions we can impose. `k` must be less than `e` and `p - 1` and `q - 1` should be divisible by 2. Therefore, we can instead factor `ed - 1`/4 into `k * [(p - 1) / 2] * [(q - 1) / 2]` reducing two 2's from our list of factors. The two largest factors of `ed - 1` should be factors of `p - 1` and `q - 1` as they are too large to go into `k` and `q` and `p` should be of around the same order of magnitude. The way I will determine if `p` and `q` is of around the same order of magnitude is the way described in the link above, by seeing if `max(p, q) < 2min(p, q)` 

Now, I will make a tree of a possible factors of `k`, `(p - 1) / 2`, and `(q - 1) / 2`. The tree will start with `k` = 1, `(p - 1) / 2` = largest factor of `ed - 1`, `(q - 1) / 2` = second largest factor of `ed - 1`. Every time the tree branches a factor from the remaining possible factors will be multiplied to one of the three values. Parts of the tree will stop branching if the following happens:

```
k >= e
size of p and q exceed 128 bits
```

When the last node of the tree is reached, we check if `p` and `q` have similar magnitudes and if they are prime. If they are, we add them to the potential candidates. 
