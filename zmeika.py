
import json
import time
import sys,os
import curses
import keyboard as kb
from random import randint as rn
import ctypes


size = [30, 30]
os.system("mode con cols={} lines={}".format( size[0] * 2, size[1] + 1))

def create_field(size):

    arr = []
    arr.append("#" * size[0])

    for k in range( (size[1] - 2) ):
        arr.append("#{}#".format("·" * (size[0] - 2) ))
    arr.append("#" * size[0])

    return arr

def move(coors, speed):
    new_coors =[ [ coors[0][0] + speed[0], coors[0][1] + speed[1] ] ]
    for k in coors[:-1]: new_coors.append(k)
    return new_coors

def check_keys(speed):

    return [1, 0] if kb.is_pressed('d') and speed[0] != -1 else (
            [-1, 0] if kb.is_pressed('a') and speed[0] != 1 else (
            [0, 1] if kb.is_pressed("s") and speed[1] != -1 else (
            [0, -1] if kb.is_pressed("w") and speed[1] != 1 else 0)))


def add_tail(coors):
    coors.append(coors[-1])
    return coors

def draw_field(stdscr):

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    k = 0
    size = [30, 30]
    f = 0
    curses.curs_set(0)

    arr = create_field(size)
    coors = [[1, 1]]
    sweet = [rn(1, size[0] - 2), rn(1, size[1] - 2)]
    speed = [1, 0]
    play = True


    # Start colors in curses
    curses.start_color()
    for k in range(255):
        curses.init_pair(k + 1, k, curses.COLOR_BLACK)

    # Loop where k is the last character pressed
    while play:
        # Initialization
        stdscr.clear()

        f += 1
        if f%1 == 0:

            g_f = f  // 2
            key = check_keys(speed)
            if key != 0: speed = key

            coors = move(coors, speed)

            for y_ind, line in enumerate(arr):
                for x_ind, let in enumerate(line):
                    if [x_ind, y_ind] == coors[0]:
                        stdscr.addstr(y_ind, x_ind * 2, "O ", curses.color_pair(162))
                        if [x_ind, y_ind] in coors[1:]: play = False
                        if x_ind == 0 or x_ind == size[0] - 1: play = False
                        if y_ind == 0 or y_ind == size[1] - 1: play = False

                        if len(coors) == (size[0] - 2) * (size[1] - 2): play = False
                        if coors[0] == sweet: 
                            coors = add_tail(coors)
                            while True:
                                sweet = [rn(1, size[0] - 2), rn(1, size[1] - 2)]
                                if sweet not in coors: break 
                    elif [x_ind, y_ind] in coors[1:]:
                        ind =  coors.index([x_ind, y_ind])
                        ind += abs ((g_f // 2)%10 - 5)
                        stdscr.addstr(y_ind, x_ind * 2, "o ", curses.color_pair(227 + abs((ind % 10) - 5) ))

                    elif [x_ind, y_ind] == sweet:
                        stdscr.addstr(y_ind, x_ind * 2, "0 ", curses.color_pair( 29 + abs (g_f%10 - 5) ))
                    else:
                        if y_ind == 0 or y_ind == size[1] - 1: 
                            if y_ind == size[1] - 1:
                                hh = 21 - abs ( g_f%42 - 21) + x_ind
                                hh = abs(hh%34 - 17)

                            else:
                                hh = abs ( g_f%42 - 21) + x_ind
                                hh = abs( hh%34 - 17)

                            stdscr.addstr(y_ind, x_ind * 2, let + " ", curses.color_pair(233 + hh))

                        else:
                            if let == "#":
                                if x_ind == 0:
                                    hh = abs ( g_f%42 - 21) + y_ind
                                    hh = abs(hh%34 - 17)
                                else:
                                    hh = 21 - abs ( g_f%42 - 21) + y_ind
                                    hh = abs(hh%34 - 17)

                                stdscr.addstr(y_ind, x_ind * 2, let + " ", curses.color_pair(233 + hh))
                            else:
                                stdscr.addstr(y_ind, x_ind * 2, let + " ", curses.color_pair(12))






            # Refresh the screen
            stdscr.refresh()

        time.sleep(0.04)
    os.system("cls")

    with open("data_zmey.json", 'a') as f: f.close()
    with open('data_zmey.json', 'r') as file:
	    try:
	        data = json.loads(file.read())
	    except: data = [0]
    file.close()

    if len(coors) > data[0]:
        data = [len(coors)]
        with open('data_zmey.json', 'w') as file:
            json.dump(data, file)
        file.close()
        best = str(len(coors))
    else: 
        best = data[0]
    print("YOUR SCORE IS {}".format(len(coors)))
    print("BEST SCORE IS {}".format(best))


def main():
    curses.wrapper(draw_field)

main()
# if __name__ == "__main__":
#     main()
"""



import curses
import time

def main(stdscr):
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, 255):
        curses.init_pair(i + 1, i, -1)
    try:
        for i in range(0, 255):
            stdscr.addstr(str(i) + " ", curses.color_pair(i))
    except curses.ERR:
        # End of screen reached
        pass
    
    stdscr.getch()
    time.sleep(100)

curses.wrapper(main)

"""