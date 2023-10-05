
# Safe Opener #

## Overview ##

100 points

Category: [picoCTF 2022](../)

Tags: `picoCTF 2022` `Reverse Engineering`

## Description ##

Can you open this safe? I forgot the key to my safe but this [program](https://artifacts.picoctf.net/c/83/SafeOpener.java) is supposed to help me with retrieving the lost key. Can you help me unlock my safe? Put the password you recover into the picoCTF flag format like: 
`picoCTF{password}`

## Solution ##

If we run the java file it asks us for a password. If we look at whats happening we can see that our key gets base64 encoded and compared with the password that has also been base64 encoded.

```java
...
    Base64.Encoder encoder = Base64.getEncoder();
...
        encodedkey = encoder.encodeToString(key.getBytes());
        System.out.println(encodedkey);
              
        isOpen = openSafe(encodedkey);
...
    public static boolean openSafe(String password) {
        String encodedkey = "cGwzYXMzX2wzdF9tM18xbnQwX3RoM19zYWYz";
        
        if (password.equals(encodedkey)) {
            System.out.println("Sesame open");
            return true;
        }
        else {
            System.out.println("Password is incorrect\n");
            return false;
        }
    }



```

Base64 decoding the string `cGwzYXMzX2wzdF9tM18xbnQwX3RoM19zYWYz` gives the password `pl3as3_l3t_m3_1nt0_th3_saf3`

The flag is `picoCTF{pl3as3_l3t_m3_1nt0_th3_saf3}`
