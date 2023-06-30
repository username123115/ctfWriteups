
PicoCTF Babygame0: Writeup

Starting the game we see that our player starts in a 30 x 90 grid of dots. 
![The map upon starting the game](images/babygameWriteup0.png)


The objective of the game seems to be to get to the flag which is the X on the bottom right. We can use 'wasd' to control our character to move towards the X, but upon reaching it, we do not get a flag.
![Output upon reaching the flag](images/babygameWriteup1.png)

Using Ghidra we get the following decompiler output


![Ghidra output 1/2](images/babygameWriteup2.png)

![Ghidra output 2/2](images/babygameWriteup3.png)

**local_aa0** should be the map because the map has 30 x 90 = 2700 tiles. It is also passed to the map initialization function.
We know the flag has coordinates 0x1d and 0x59 so from where the game checks for a win, we can see that **local_aac** and **local_aa8**  corresponds to the height and width of the player. Furthermore, the function init_player  shows that these are both initiated to 4. From init_player we can also see that a third variable is modified, this variable should be **local_aa4**. Near the end of main this value is checked against zero, if it is not zero, the win function is called, which will print out our flag. Because this variable is initiated to zero, we must find a way to change this value. 

![Function init_player](images/babygameWriteup4.png)

Now to rename some variables in the decompiler output and bundle the player data into a struct so we can more easily see what's happening. Note that all the fields in the struct are aligned to 4 bytes.

![playerStruct](images/babygameWriteup8.png)
After cleaning up main (some code at top omitted):


![Cleaned up decompiler output](images/babygameWriteup5.png)

We see that we must first change winFlag before getting to the end of the map, our input is sent to the move_player function so it seems most promising to examine that.

![move_player function](images/babygameWriteup6.png)
The game starts by writing to the position the player is at with the value 0x23, or a dot ".". It then updates the position of the player based on the key pressed, there are also some special moves that can change the character the player is displayed as or move the player to the 'X'. Finally, the game writes player_tile to the area of the map which the player's new position. Because the game does not check if the player is moving out of bounds, we can get the game to write to areas outside of the map array. This means we can use this flaw to change the value of the win flag! The only thing we need to figure out now is the location of the winflag in memory relative to the beginning of the map.

![Layout of all variables on stack](images/babygameWriteup7.png)

The base memory address of map is 0xaac - 0xaa0 = 0xc bytes above the base memory address of player, so in order to access the first field of player we would access map[-12]  (map is an array of type undefined which has length one byte), however we want to access the last field of player, which is 0x8 bytes above the base address, or map[8-12] = map[-4]. move_player updates the map by multiplying player height by 0x5a and adding that to player width, so one way we can easily access map[-4] is by moving to the top left corner, which will set player height and width to zero, and moving left 4 times. This will move the player onto the win flag, causing the move_player to overwrite it to a nonzero value. You can then press 'p' to instantly solve and print out the flag. Trying this on a challenge instance results in the flag picoCTF{gamer_m0d3_enabled_fff873ca}


![Output after changing player win flag](images/babygameWriteup9.png)

