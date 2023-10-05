
# Fresh Java #

## Overview ##

200 points

Category: [picoCTF 2022](../)

Tags: `picoCTF 2022` `Reverse Engineering` `java`

## Description ##

Can you get the flag?
Reverse engineer [this](https://artifacts.picoctf.net/c/197/KeygenMe.class) binary.

## Solution ##

We are given a java class file that asks us for our key. The hint tells us to use a java decompiler to figure out the flag. I use `cfr` to do this. The output is

```java
/*
 * Decompiled with CFR 0.152.
 */
import java.util.Scanner;

public class KeygenMe {
    public static void main(String[] stringArray) {
        Scanner scanner = new Scanner(System.in);
        System.out.println("Enter key:");
        String string = scanner.nextLine();
        if (string.length() != 34) {
            System.out.println("Invalid key");
            return;
        }
        if (string.charAt(33) != '}') {
            System.out.println("Invalid key");
            return;
        }
        if (string.charAt(32) != '9') {
            System.out.println("Invalid key");
            return;
        }
        ...
```

Going through and reading all the characters that are being compared we get the flag `picoCTF{700l1ng_r3qu1r3d_738cac89}`
