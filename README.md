Steam-Mosaticon
===============

# Description
This script will create a mosaic of an image using your Steam emoticons.


# Examples
![P](http://i.imgur.com/8FrwZmn.png)
![Pikachu](http://i.imgur.com/8FrwZmn.png) ![Squirtle](http://i.imgur.com/cdsApq4.png)


# Installation
You'll need [Python 2.x](http://www.python.org/download/releases/2.7.5/), [requests](http://docs.python-requests.org/en/latest/) and [PIL](http://www.pythonware.com/products/pil/).
Then simply download and use the script (mosaticon.py)


# Usage
`mosaticon.py <steamid> <imagefile> [<width> [<height>]]

where:
- **steamid** is your profile name (steamcommunity.com/id/XXXXXXX)
- **imagefile** is the path to the image you want to create a mosaic of
- **width** is the number of emoticons to use horizontally
- **height** is the number of emoticons to use vertically

if height is not provided, aspect ratio of the image is used.
If neither is provided, 25 is used as the width.

WARNING: Your profile might need to be public for the script to work, since it scans your inventory
to gather a list of emoticons you own and can use. Do also note that because of this, the result
of the script will look better the more emoticons you own.


# Output
The script will output the text you'll need to paste. It outputs to stdout by default though,
so you'll it to redirect it to a file (`mosaticon.py bla bla bla > output.txt`)

If the output is too long to fit into a message, it'll be split up into piece.
You'll need to paste each piece in succession. Also, since the Steam client has an artificial limit of 2048 characters, 
**you'll need to use the [web chat interface](steamcommunity.com/chat/)** which can paste up to 12288 characters.
There might be a way of uncapping the client through skin editing, but I couldn't get it working.


# Extra information
When you are pasting multiple pieces, your name will push the first line of text a bit.
To conpensate for this, I remove a few emoticons, and add a few dots.
For example, [my name](http://i.imgur.com/H25Fn30.png) is roughly 3.4 emoticons wide, so I remove 4 emoticons and 2 dots (each dot is ~0.2 emote).
You can change this according to the length of your name by changing `name_length`.
First value is the number of emoticons to remove, second is the number of dots to add.

The script uses the background color for transparent pixels in the emoticons to get a more accurate result.
On the default skin this is (40, 40, 40). If you have a custom skin and you like to change this, modify `bg_color`.

Each emoticons name has a different lenght, so you may need to play with the width and height to get it to fit
in 1 or 2 parts. Roughly, each piece holds around 1000 emotes, so 32x32 would fit in one piece and 45x45 for two.

If you have any issues, you can message me on Steam:
http://steamcommunity.com/id/Ph0X




