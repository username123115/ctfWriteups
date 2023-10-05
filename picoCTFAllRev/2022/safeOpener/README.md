
# Safe Opener #

## Overview ##

100 points

Category: [picoCTF 2022](../)

Tags: `picoCTF 2022` `Reverse Engineering`

## Description ##

Can you open this safe? I forgot the key to my safe but this program is supposed to help me with retrieving the lost key. Can you help me unlock my safe? Put the password you recover into the picoCTF flag format like:
`picoCTF{password}`

## Solution ##

The program asks us for a password. If we look inside the java file we can see that it is base64 encoding our input and comparing it against a string.

```java
...

    Base64.Encoder encoder = Base64.getEncoder();

...

        System.out.print("Enter password for the safe: ");
        key = keyboard.readLine();

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

The base64 encoded string is `cGwzYXMzX2wzdF9tM18xbnQwX3RoM19zYWYz`, running it through a base64 decoder we get the password `pl3as3_l3t_m3_1nt0_th3_saf3`. The flag is `picoCTF{pl3as3_l3t_m3_1nt0_th3_saf3}`.

