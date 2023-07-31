Class called secret generator that has method getServerSecret
Looks for secret file, if this file doesn't exist, make one
its contents will be "1234"

This class is used by JwtService class which is initialized with a SecretGenerator (ooh lala)
(SecretGenerator is not used elsewhere, checked using funny grep command)

Ok so it turns out that after checking that "1234" is literlly the secret key, the program does nothing to change it
:facepalm:

I assume that user ID for the admin is 2 because user ID for user is 1 and user is created first

Ok cool did the funny and spent like an hour trying to perform an attack before finally figuring out to just change values in local
storage (with help of a writeup D:)

10% of time -> 90% of work
90% of time -> incompetence
