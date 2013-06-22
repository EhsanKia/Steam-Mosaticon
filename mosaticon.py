import sys
import requests
from PIL import Image
from StringIO import StringIO


# Computes the average color of the icon (using bg_color on transparent pixels)
def get_average(img):
    red, blue, green = 0, 0, 0
    w, h = img.size
    pixels = img.load()
    for i in range(w):
        for j in range(h):
            r, g, b, a = pixels[i, j]
            red   += (a * r + (255 - a) * bg_color[0])/255.0
            green += (a * g + (255 - a) * bg_color[1])/255.0
            blue  += (a * b + (255 - a) * bg_color[2])/255.0
    return map(lambda x: int(x / (w * h)), [red, blue, green])


# Computes euclidian distance between two color
def dist(a, b):
    dx, dy, dz = a[0]-b[0], a[1]-b[1], a[2]-a[2]
    return dx*dx + dy*dy + dz*dz


# Goes through the list of emoticons and finds the closest to target
def get_closest(elist, target_color):
    # Applies transparency if available
    if len(target_color) > 3:
        target_color = map(lambda x: int(x*target_color[3]/255), target_color[:3])

    # Sets best to infinity and loops through icons to find closest
    best_dist = float('inf')
    for n, color in elist:
        d = dist(color, target_color)
        if d < best_dist:
            best_name, best_dist = n, d

    return best_name


# Prints instruction if not enough arguments are given
if len(sys.argv) < 3:
    print "Usage: mosaticon.py steamid imagefile [target_width [target_height]]"
    sys.exit(0)

# Loads the inventory json
inv_url = "http://steamcommunity.com/id/{}/inventory/json/753/6/".format(sys.argv[1])
try:
    inv_json = requests.get(inv_url).json()
except:
    print "Invalid steamid"
    sys.exit(0)
if not inv_json['success']:
    print "Parsing inventory failed"
    sys.exit(0)

# Grabs the name of all the emoticons
emote_names = [item['name'] for item in inv_json['rgDescriptions'].values() if item['tags'][2]['name'] == 'Emoticon']
emote_names = map(lambda e: str(e.strip(':')), emote_names)

# Load emoticon data
bg_color = (40, 40, 40)  # Background color of steamchat
emote_url = "http://cdn.steamcommunity.com/economy/emoticon/"
emote_data = []

for name in emote_names:  # Download each emoticon and get average color in a dict
    response = requests.get(emote_url + name)
    img = Image.open(StringIO(response.content))
    emote_data.append((name, get_average(img)))

try:  # Tries to open the target image
    target_name = sys.argv[2]
    target_img = Image.open(target_name)
except:
    print "Invalid file"
    sys.exit(0)

# Figures out target dimentions
if len(sys.argv) > 4:
    target_size = map(int, (sys.argv[3], sys.argv[4]))
elif len(sys.argv) == 4:
    target_size = map(int, (sys.argv[3], sys.argv[3]))
else:
    cw, ch = target_img.size 
    target_size = (25, int(25.0*ch/cw))

# Resize image and grab pixels
resized_img = target_img.resize(target_size)
target_px = resized_img.load()

# For each pixel, find closest emoticon and add it to the output
name_length = (4, 2) # The lenght of your steam name + time (emoticon, dot)
print_str = ".\n"
count = 2
for y in range(target_size[1]):
    for x in range(target_size[0]):
        emote = get_closest(emote_data, target_px[x, y])
        print_str += ":{}:".format(emote)
        count += 2

    count += len(print_str) + 1

    if count > 12200:  # Character limit per message
        print "\n\n-----\n"
        count = 0
        # This removes icons to compensate for the length of your name
        print_str = '.'*name_length[1] + ':' + '::'.join(print_str.split('::')[name_length[0]:])

    print print_str
    print_str = ""
