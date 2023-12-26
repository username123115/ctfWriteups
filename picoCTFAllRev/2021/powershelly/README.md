
# Powershelly #

## Overview ##

180 points

Category: [picoCTF 2021](../)

Tags: `picoCTF 2021` `Reverse Engineering`

## Description ##

It's not a bad idea to learn to read Powershell. We give you the output, but do you think you can find the input? 

[rev_PS.ps1](https://mercury.picoctf.net/static/e55e1f4349d14408f6bac82f9bcb5aab/rev_PS.ps1) 
[output.txt](https://mercury.picoctf.net/static/e55e1f4349d14408f6bac82f9bcb5aab/output.txt)

## Solution ##

The script isn't too hard to read, but I don't have a way to run it on my system, so the first thing I did was setup an environment to run.

I did this by pulling a powershell image and running it in docker

```
docker container run -it --rm -v=./:/stuff mcr.microsoft.com/powershell
```

The output of the script are a bunch of numbers and the structure of the input isn't really clear.

The script reads the input file two times, the first time into the `$out` variable using `Get-Content` and the second time into the `$enc` variable using `[System.IO.File]::ReadAllBytes`

### Format of input file ###

There are then three checks that need to be passed before the program starts generating output.

The first check ensures the input file has 5 or less lines by checking the length of `$out`, which is an array containing all the lines of the input.
It then checks that the total number of characters in the input file is equal to 9245 (calculated in the variable `$numLength`). 
If these fail the script outputs "Wrong format 5" and exits

The second check ensures that the bytes of the file only have the values 49, 48, 10, 13, 32 which translate to "1", "0", "\n", "\r", and " ".
This is good to know as it hints that the main content of the files is going to be a bunch of 1's and 0's. 
If the file contains any other characters, the script outputs "Wrong format 1/0/" and exits.

The final check occurs while creating the contents of the dictionary `$blocks`.
The script iterates through every line in the file by iterating through `$out`.
Each line is split into an array of substrings using the `Split()` method where the deliminator is a space. This array is stored in the variable `$r`.
A for loop with the variable `$j` is used to iterate through `$r`, as `$j` indexes into `$r` and goes from 0 to one less then the length of `$r`.

The script checks if `$r[$j].Length` is equal to 6 for all `$r` and `$j`.
It will output "Wrong Format 6" and exit if this condition fails.
If the condition doesn't fail the script appends `$r[$j]` to `$blocks[$j]`

This hints that the structure of the input file looks like

```
B B B B B B B ...
B B B B B B B ...
B B B B B B B ...
...
```

Where a B represents 6 characters.
Any key `j` of `$blocks` consists of all the blocks of the `jth` column of the input file.

### Scramble ###

There is a function called `Scramble` that takes as parameters a column of blocks and a random seed.

It combines the blocks into one long string, scrambles the string, and maps every '1' to a '11' and '0' to a '00'. 
It then interprets the string as a binary number and returns an integer.
This can be reversed by shrinking the '11's and '00's into '1's and '0's and finding what index of the old string every index of the new string belongs to.

An implementation of a function to unscramble a scrambled string can be found in [solve.py](./solve.py)

```python
#found later by obtaining a scrambled string
rawLength = 30
def unScramble(binString, seed):
    order = ["x" for i in range(rawLength)]

    for i in range(rawLength):
        #print(order)
        y = (i * seed) % rawLength
        while order[y] != "x":
            y = (y + 1) % rawLength
        order[y] = i

    scrambled = []
    #get rid of the "0b"
    binString = binString[2:]
    for i in range(rawLength):
        c = binString[i * 2:i*2+2]
        if c == "00":
            scrambled.append('0')
        elif c == "11":
            scrambled.append('1')
        else:
            print(f"Invalid string: {c}")

    result = ["_" for i in range(rawLength)]
    for index, charOrder in enumerate(order):
        #indexth element of scrambled was originally charOrderth
        result[charOrder] = scrambled[index]
    blocks = []
    for block in range(rawLength // 6):
        b = result[6 * block: 6 * block + 6]
        b = "".join(b)
        blocks.append(b)

    return blocks
```

With this out of the way, we only need to obtain the seeds and the scrambled strings


### Getting scrambled strings ###

Now if we just get all the scrambled strings and unscramble them, we can place the blocks back together and get an input!

Unfortunately, we can't just get the scrambled strings by converting the integers in the output file to a binary string, as they have been xor-red with other numbers before being written to the output file.

When looking at the end of the script, every block gets scrambled at stored in the variable `$fun`, where it gets xor-red with a random number and the previously written number `$result` before getting written to the file. (In the case of the first number written, `$result` is set to 0 so this xor doesn't change the result)

```powershell

for ($i=0; $i -lt $blocks.count ; $i++)
{

  $fun = Scramble -block $blocks[$i] -seed $seeds[$i]
  ...
  $result = $fun -bxor $result -bxor $randoms[$i]
  $output_file += $result
}
```

We have all the numbers written to the file, so we can xor all of the numbers in the file with the previous number (except for the first one, which remains unchanged) to get the result of `$fun -bxor $randoms[$i]` for a given `$i`, so the only thing remaining to get the scrambled strings is to find the values of `$randoms`. 
Fortunately, `$randoms` comes from the function `Random-Gen`, so we can just run it in our solve script.

`$randoms = Random-Gen`

```powershell
function Random-Gen {
  $list1 = @()
  for ($i=1; $i -lt ($blocks.count + 1); $i++)
  {
    $y = ((($i * 327) % 681 ) + 344) % 313
    $list1 += $y
  }
  return $list1
}
```

This will generate `$blocks.count` random numbers, and we know `$blocks.count` is 264 as our output file has 264 numbers which each correspond to a mangled block.

Here is an excerpt from the [solve script](./solve.py) that finds the original scrambled blocks and puts them in the array `original`

```python
with open('output.txt') as f:
    output = [int(x) for x in f.readlines()]

blockCounts = 264
seeds = []
randoms = []
original = []
scrambled = []

for i in range(blockCounts):
    j = i + 1
    seeds.append((j * 127) % 500)

for i in range(blockCounts):
    j = i + 1
    y = (((j * 327) % 681) + 344) % 313
    randoms.append(y)

r = 0
for i in range(blockCounts):
    if (i != 0):
        r = output[i - 1]
    original.append((output[i] ^ randoms[i]) ^ r)
```

Along with this, the script also finds all the seeds needed to unscramble the strings. The only thing that is missing now is to find the value of `$raw.Length` in the `Scramble()` function as we need to know how many characters will be in the unscrambled string.

We can find this out by taking the length of the binary string of any of the scrambled strings we found. 
Then we divide by 2 as every bit in the original string gets doubled in the scrambled string.

```python

# subtract 2 because of the '0b' that bin() puts at the beginning of a string
length = len(bin(original[0])) - 2
rawLength = length // 2
```

The value of rawLength is 30, meaning that every column contains 5 blocks (because every block has 6 characters) indicating that our input will have 5 lines.

Here we print out the binary strings derived from our scrambled numbers and unscramble. Because the `unScramble` function defined above automatically takes care of splitting up the unscrambled strings back into arrays of 6 character strings, we just need to take care of adding these columns in the correct rows and printing them out.

```python
binStrings = []
for x in original:
    y = bin(x)
    binStrings.append(y)

final = ["" for i in range(5)]
for i in range(blockCounts):
    good = unScramble(binStrings[i], seeds[i])
    for j in range(len(good)):
        final[j] += good[j] + " "

for s in final:
    print(s)

```

And now we have the original input! We can confirm this by running the script on the input and diffing it between the given and generated output.txt. 
(Note that the script checks if the input has 9245 characters but I had to change it to 9240, most likely because I'm missing a \r at the end of my lines in my input.txt)

### Reversing Input ###

Unfortunately, we're not done, because we have a bunch of blocks that don't seem to mean anything (no ascii art >:( )

However, every row has only two unique numbers in their blocks, so maybe it's binary?

My script [solveInput.py](./solveInput.py) assumes that numbers with more zeroes are 1's and converts each row of the input file into one giant binary string. I then split the strings into blocks of 8 bits and interprets them as ascii characters, which works for 4 out of 5 rows of blocks!


```
['picoCTF{2018highw@y_2_pow3r$hel!}', 'picoCTF{2018highw@y_2_pow3r"hel!}', 'picoCTF{2018highw@y_2_pow3r$hel!}', 'picoCTF{2018highw@y_2_pow3r$hel!}', '\x8f\x96\x9c\x90¼«¹\x84ÍÏÎÇ\x97\x96\x98\x97\x88¿\x86\xa0Í\xa0\x8f\x90\x88Ì\x8dÛ\x97\x9a\x93Þ\x82']
```

The flag is `picoCTF{2018highw@y_2_pow3r$hel!}`

