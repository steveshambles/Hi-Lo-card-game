"""
Hi-Lo V2.0
A GUI High-Low card game.

By Steve Shambles
updated May 5th 2021

https://stevepython.wordpress.com/

Requirements:
---------------
pip3 install Pillow
pip3 install pygame
pip install sounddevice
pip install soundfile

'cards' folder and all its contents in current dir.
help.txt in root

Tested on Windows 7 and Linux Mint 19.1
=======================================

V2.0 changes:
----------------------
Added some sound effects

Sfx on-off switch in music menu, can have both
sfx and music on if required.

Added logo image.

Changed bg of card 'table'

Implemented rounded custom buttons.

Moved buttons to better postions.

Added a help button just to fill the gap.

Changed message area to use as a status bar
same for score area.

Moved all files into 'cards' folder, except
high_score.txt and help.txt, as problems
caused otherwise.

Changed cost of using joker to 3pts from 4pts,
I found in testing I never used it as too
expensive at 4pts and not worth it.

Changed import style of tkinter to best way.

Updated and improved some parts of the code.

Updated help file text.

PEP8 as far as I could, about 97%.

To do:
------
Look at implementing suits properly.
No pairs means no double jokers, so fix
Menu check marks are prob not done correctly
it seems like a mess, research.
Reset high score to 0 option.
"""
import os
import random
import sys
import tkinter as tk
from tkinter import messagebox
import webbrowser

from PIL import Image, ImageTk
from pygame import mixer
import sounddevice as sd
import soundfile as sf


class Glo:
    """Global store, this makes these vars Global,e.g Glo.var."""
    points_won = 0
    high_score = 0
    card1_val = 0
    card2_val = 0
    new_card = 0
    play_all = 0
    play_joker_btn = False
    random_card = 0
    random_suit = 0
    rnd_cc = 0
    sound_fx = True


mixer.init()

root = tk.Tk()
root.title('Hi-Lo V2.0')
root.resizable(False, False)
root.config(bg='forestgreen')

# Check cards folder available.
cards_check = 'cards'
check_file = os.path.isdir(cards_check)

if not check_file:
    root.withdraw()
    messagebox.showwarning('Folder Missing Error',
                           'The "cards" folder is missing\n\n'
                           'Please re-install.\n')

    root.destroy()
    sys.exit()

# Check high_score.txt available, if not create it.
hst_check = 'high_score.txt'
check_file = os.path.isfile(hst_check)
if not check_file:
    with open(hst_check, 'w') as contents:
        pass

# Pre-load icons for drop-down menu.
help_icon = ImageTk.PhotoImage(file='cards/icons/help-16x16.ico')
about_icon = ImageTk.PhotoImage(file='cards/icons/about-16x16.ico')
blog_icon = ImageTk.PhotoImage(file='cards/icons/blog-16x16.ico')
exit_icon = ImageTk.PhotoImage(file='cards/icons/exit-16x16.ico')
donation_icon = ImageTk.PhotoImage(file='cards/icons/donation-16x16.ico')
github_icon = ImageTk.PhotoImage(file='cards/icons/github-16x16.ico')
music_icon = ImageTk.PhotoImage(file='cards/icons/music-16x16.ico')

# Frame for logo.
logo_frame = tk.LabelFrame(root)
logo_frame.grid(row=0, column=0, columnspan=3)

# Frame for the buttons.
btn_frame = tk.Frame(root)
btn_frame.grid(row=1, column=1)

# Frame for the two card images.
cards_frame = tk.Frame(root, pady=15, bg='forestgreen')
cards_frame.grid(row=1, column=0)

# Frame for the change button.
chng_btn_frame = tk.Frame(root, padx=30)
chng_btn_frame.grid(row=2, column=0)

# Frame for printng the scores.
score_frame = tk.LabelFrame(root)
score_frame.grid(row=3, column=0, padx=4, columnspan=2, sticky='W'+'E')


def show_logo():
    """Display games logo image."""
    logo_image = Image.open('cards/logo_318x199.png')
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = tk.Label(logo_frame, image=logo_photo)
    logo_label.logo_image = logo_photo
    logo_label.grid()


def play_sound(filename):
    """Play WAV file.Supply filename when calling this function."""
    data, fs = sf.read(filename, dtype='float32')
    sd.play(data, fs)


def updt_status_bar(txt):
    """Displays current action in the status bar, message to be displayed
       must be supplied when calling this function."""
    stat_bar.config(text=txt)


def update_score_bar():
    """Displays score and high score message which both
       must be supplied when calling this function."""
    # spc = 12 * ' '
    score_bar.config(text='Current Score:' + str(Glo.points_won)
                     + '  High Score:' + str(Glo.high_score))


def save_high_score():
    """Save high score to file in current dir."""
    with open('high_score.txt', 'w') as contents:
        save_it = str(Glo.high_score)
        contents.write(save_it)


def play_music(track):
    """Play background music if a track is selected in drop-down menu"""
    # Zero all menu checkmarks first.
    t1Var.set(0)
    t2Var.set(0)
    t3Var.set(0)
    t4Var.set(0)
    t5Var.set(0)
    allVar.set(0)

    if track == "1":
        mixer.music.load('cards/music/bensound-summer.mp3')
        t1Var.set(1)

    if track == "2":
        mixer.music.load('cards/music/bensound-dance.mp3')
        t2Var.set(1)

    if track == "3":
        mixer.music.load('cards/music/bensound-dreams.mp3')
        t3Var.set(1)

    if track == "4":
        mixer.music.load('cards/music/bensound-motion.mp3')
        t4Var.set(1)

    if track == "5":
        mixer.music.load('cards/music/bensound-scifi.mp3')
        t5Var.set(1)

    mixer.music.play(-1)  # Play indefinetly -1. 0 or () = play once.


def stop_music():
    """Stop music playing if selected in drop-down menu."""
    mixer.music.stop()
    t1Var.set(0)
    t2Var.set(0)
    t3Var.set(0)
    t4Var.set(0)
    t5Var.set(0)
    allVar.set(0)


def play_all_tracks():
    """Play all music tracks if play all is selected in drop-down menu"""
    t1Var.set(0)
    t2Var.set(0)
    t3Var.set(0)
    t4Var.set(0)
    t5Var.set(0)
    allVar.set(1)
    mixer.music.load('cards/music/all.mp3')
    mixer.music.play(-1)  # Play indefinetly -1. 0 or () = play once.


def start_rnd_music():
    """Pay a random music track at start up. Currently not in use."""
    rnd_track = random.randint(1, 5)
    track = str(rnd_track)
    play_music(track)


def load_high_score():
    """Load in text file containing players best score."""
    with open('high_score.txt', 'r') as contents:
        saved_high_score = contents.read()
        if saved_high_score > '':
            Glo.high_score = int(saved_high_score)


def setup_card_one():
    """Get card 1 randomly and display it."""
    get_rnd_card()
    card_one = Glo.new_card+'.png'  # Card image filename.
    Glo.card1_val = Glo.random_card  # Card number 0-14.
    card_btn_one = tk.Label(cards_frame)
    PHOTO = tk.PhotoImage(file='cards/'+str(card_one))
    card_btn_one.config(image=PHOTO)
    card_btn_one.grid(row=0, column=0, padx=2, pady=2)
    card_btn_one.photo = PHOTO


def setup_card_two():
    """Get rnd card for card 2. Only display back of card 2 though."""
    get_rnd_card()
    Glo.card2_val = Glo.random_card
    # Cheat for testing purposes.
    # print(Glo.card1_val, Glo.card2_val)

    # Stop duplicates.
    while Glo.card1_val == Glo.card2_val:
        get_rnd_card()
        Glo.card2_val = Glo.random_card

    card_btn_two = tk.Label(cards_frame)
    PHOTO2 = tk.PhotoImage(file='cards/blank.png')
    card_btn_two.config(image=PHOTO2)
    card_btn_two.grid(row=0, column=1, padx=2, pady=2)
    card_btn_two.photo = PHOTO2


def show_card_two():
    """Reveal card two."""
    but_2a = tk.Label(cards_frame)
    photo_2a = tk.PhotoImage(file='cards/'+str(Glo.new_card)+'.png')
    but_2a.config(image=photo_2a)
    but_2a.grid(row=0, column=1, padx=2, pady=2)
    but_2a.photo = photo_2a


def get_rnd_card():
    """Get a new random card."""
    # Joker btn used, give joker.
    if Glo.play_joker_btn:
        # Create the new card.
        joker = True
        Glo.new_card = str(0)+'-'+str('joker')
        return

    joker = False
    # Note: Ace=14 (highest card), Jack=11, Queen=12, King=13.
    # Joker is wild when rnd is zero.
    Glo.random_card = random.randint(0, 13)
    Glo.random_suit = random.randint(1, 4)

    # Make ace highest card.
    if Glo.random_card == 1:
        Glo.random_card = 14

    # Mark joker if rnd = 0.
    if Glo.random_card == 0:
        joker = True

    # Choose a random suit.
    if Glo.random_suit == 1:
        card_suit = 'clubs'
    if Glo.random_suit == 2:
        card_suit = 'hearts'
    if Glo.random_suit == 3:
        card_suit = 'spades'
    if Glo.random_suit == 4:
        card_suit = 'diamonds'

    # Override suit if joker.
    if joker:
        card_suit = 'joker'

    # Create the new card.
    Glo.new_card = str(Glo.random_card)+'-'+str(card_suit)


def clicked_higher():
    """Clicked on 'Higher' button."""
    chng_crd_btn.configure(state=tk.DISABLED)
    # Correct guess, card 2 was higher, chk same card value or a joker.
    if Glo.card1_val < Glo.card2_val or Glo.card1_val == Glo.card2_val  \
       or Glo.card1_val == 0 or Glo.card2_val == 0:
        Glo.points_won = Glo.points_won + 1

        # Update highscore.
        if Glo.points_won > Glo.high_score:
            Glo.high_score = Glo.points_won

        update_score_bar()
        print_correct()

        # Print relevent game messages.
        if Glo.card1_val == Glo.card2_val:
            print_pairs()

        if Glo.card1_val == 0 or Glo.card2_val == 0:
            updt_status_bar('JOKERS ARE WILD!')

        if Glo.card1_val == 0 and Glo.card2_val == 0:
            joker_bonus()

        # Enable\disable relevent buttons.
        nxt_crd_btn.configure(state=tk.NORMAL)
        hghr_btn.configure(state=tk.DISABLED)
        lwr_btn.configure(state=tk.DISABLED)
        chng_crd_btn.configure(state=tk.DISABLED)
        play_joker_btn.configure(state=tk.DISABLED)

        # Player guessed incorrectly.
    else:
        print_wrong()
        show_card_two()
        game_over_man()
        return

    # Player was correct display card 2.
    show_card_two()


def joker_bonus():
    """When 2 jokers come up togther award bonus points."""
    updt_status_bar('3 POINTS JOKER BONUS!')
    Glo.points_won = Glo.points_won + 3
    update_score_bar()


def clicked_lower():
    """Clicked on 'Lower' button."""
    chng_crd_btn.configure(state=tk.DISABLED)

    if Glo.card1_val > Glo.card2_val or Glo.card1_val == Glo.card2_val  \
       or Glo.card1_val == 0 or Glo.card2_val == 0:
        Glo.points_won = Glo.points_won + 1

        if Glo.points_won > Glo.high_score:
            Glo.high_score = Glo.points_won

        update_score_bar()
        print_correct()

        if Glo.card1_val == Glo.card2_val:
            print_pairs()

        if Glo.card1_val == 0 or Glo.card2_val == 0:
            print_joker()

        if Glo.card1_val == 0 and Glo.card2_val == 0:
            joker_bonus()

        nxt_crd_btn.configure(state=tk.NORMAL)
        hghr_btn.configure(state=tk.DISABLED)
        lwr_btn.configure(state=tk.DISABLED)
        chng_crd_btn.configure(state=tk.DISABLED)
        play_joker_btn.configure(state=tk.DISABLED)

    else:
        print_wrong()
        show_card_two()
        game_over_man()
        return

    show_card_two()


def print_joker():
    """Print 'Jokers are wild' in-game message."""
    updt_status_bar('JOKERS ARE WILD!')


def print_correct():
    """Print 'Well done' in-game message."""
    if Glo.sound_fx:
        play_sound(r'cards/sfx/correct.wav')
    updt_status_bar('WELL DONE! CLICK NEXT')


def print_wrong():
    """Print 'Unlucky' in-game message."""
    if Glo.sound_fx:
        play_sound(r'cards/sfx/lose.wav')
    updt_status_bar('UNLUCKY!')


def print_higher_or_lower():
    '''Print 'Higher or Lower in-game message.'''
    updt_status_bar('HIGHER OR LOWER?')


def print_pairs():
    """Print 'pairs are good' in-game message."""
    updt_status_bar('PAIRS ARE GOOD!')


def print_changed_card():
    """Print 'Change 1st card costs 1pt' in-game message."""
    updt_status_bar('CHANGE CARD COSTS 1pt.')


def print_used_joker():
    """Print 'Playing joker costs 4pt' in-game message."""
    updt_status_bar('PLAYING JOKER COSTS 3 Points')


def clicked_next():
    """Clicked on 'Next' button."""
    setup_card_one()
    setup_card_two()
    print_higher_or_lower()

    if Glo.card1_val == 14:
        updt_status_bar('ACES ARE HIGH!')
    if Glo.card1_val == 0:
        updt_status_bar('JOKERS ARE WILD!')

    update_score_bar()
    nxt_crd_btn.configure(state=tk.DISABLED)
    hghr_btn.configure(state=tk.NORMAL)
    lwr_btn.configure(state=tk.NORMAL)

    # Only light up change card button if have at least 1pt.
    chng_crd_btn.configure(state=tk.DISABLED)
    if Glo.points_won > 0:
        chng_crd_btn.configure(state=tk.NORMAL)

    # Only light up Joker button if have at least 3pts.
    play_joker_btn.configure(state=tk.DISABLED)
    if Glo.points_won > 2:
        play_joker_btn.configure(state=tk.NORMAL)


def game_over_man():
    """Game over because player guessed incorrectly."""
    msg = ''
    ask_yn = ''

    if Glo.points_won > Glo.high_score or Glo.points_won > 0 and Glo.points_won == Glo.high_score:
        Glo.high_score = Glo.points_won
        play_sound(r'cards/sfx/new_hs.wav')

        save_high_score()
        msg = 'G A M E  O V E R  M A N\n\nCongratulations, a new high score!\n\nPlay another game?'

    else:
        msg = 'G A M E  O V E R  M A N\n\n  Play another game?'

    ask_yn = messagebox.askyesno('Hi-Lo', msg)

    if not ask_yn:
        stop_music()
        root.destroy()
        sys.exit()
    if Glo.sound_fx:
        play_sound(r'cards/sfx/new_game.wav')
    new_game()


def clicked_change():
    """Clicked on the enabled 'change' button."""
    # Deduct point for using change card.
    if Glo.sound_fx:
        play_sound(r'cards/sfx/change_card.wav')

    Glo.points_won -= 1
    update_score_bar()
    setup_card_one()
    setup_card_two()
    chng_crd_btn.configure(state=tk.DISABLED)
    play_joker_btn.configure(state=tk.DISABLED)
    print_changed_card()


def clicked_joker():
    """Clicked on the enabled joker button."""
    # Deduct 3 points for using joker.
    if Glo.sound_fx:
        play_sound(r'cards/sfx/play_joker.wav')
    Glo.points_won -= 3
    update_score_bar()
    Glo.play_joker_btn = True
    get_rnd_card()  # will choose joker.
    show_card_two()
    play_joker_btn.configure(state=tk.DISABLED)
    chng_crd_btn.configure(state=tk.DISABLED)
    Glo.play_joker_btn = False
    nxt_crd_btn.configure(state=tk.NORMAL)
    hghr_btn.configure(state=tk.DISABLED)
    lwr_btn.configure(state=tk.DISABLED)
    print_used_joker()


def new_game():
    """Start a new game, retaining high score"""
    Glo.points_won = 0
    update_score_bar()
    print_higher_or_lower()
    clicked_next()


def about_menu():
    """Display about program info if selected in drop-down menu."""
    messagebox.showinfo('About', 'Hi-Lo V2.0\nMIT Licence.\n\n'
                        'By Steve Shambles\n(c) May 2021.\n')


def help_menu():
    """How to use the program, menu help text."""
    webbrowser.open('help.txt')


def visit_blog():
    """Visit my python blog if selected in drop-down menu."""
    webbrowser.open('https://stevepython.wordpress.com/python-posts-quick-index/')


def visit_bensound():
    """Visit bensound.com blog if selected in drop-down menu."""
    webbrowser.open('https://bensound.com/')


def exit_game():
    """Quit program yes-no requestor."""
    ask_exit = messagebox.askyesno('Exit game',
                                   'Are you sure you want to exit?')
    if ask_exit:
        stop_music()
        root.destroy()
        sys.exit()


def donate_me():
    """In the vain hope someone generous likes this program enough to
       reward my work.Yeah, right! """
    webbrowser.open("https:\\paypal.me/photocolourizer")


def get_source_code():
    """Send user to GitHub repo of this source code."""
    webbrowser.open('https://github.com/steveshambles/Hi-Lo-card-game')


def sfx_switch():
    """Toggle sounfx on and off and set or unset menu checkmark."""
    if Glo.sound_fx:
        Glo.sound_fx = False
        sfoffVar.set(1)
        sfonVar.set(0)
        return
    Glo.sound_fx = True
    sfoffVar.set(0)
    sfonVar.set(1)


# Higher-Lower buttons etc.
hghr_btn = tk.Button(chng_btn_frame, command=clicked_higher)
hghr_photo = tk.PhotoImage(file='cards/btns/btn_higher.png')
hghr_btn.config(image=hghr_photo, relief=tk.FLAT)
hghr_btn.grid(row=0, column=0)

lwr_btn = tk.Button(chng_btn_frame, command=clicked_lower)
lwr_photo = tk.PhotoImage(file='cards/btns/btn_lower.png')
lwr_btn.config(image=lwr_photo, relief=tk.FLAT)
lwr_btn.grid(row=0, column=1)

nxt_crd_btn = tk.Button(chng_btn_frame, command=clicked_next)
nxt_crd_photo = tk.PhotoImage(file='cards/btns/btn_next.png')
nxt_crd_btn.config(image=nxt_crd_photo, relief=tk.FLAT)
nxt_crd_btn.grid(row=0, column=2)
nxt_crd_btn.configure(state=tk.DISABLED)

chng_crd_btn = tk.Button(chng_btn_frame, command=clicked_change)
chng_crd_photo = tk.PhotoImage(file='cards/btns/btn_change.png')
chng_crd_btn.config(image=chng_crd_photo, relief=tk.FLAT)
chng_crd_btn.grid(row=1, column=0, pady=10, sticky='W')
chng_crd_btn.configure(state=tk.DISABLED)

help_btn = tk.Button(chng_btn_frame, command=help_menu)
help_photo = tk.PhotoImage(file='cards/btns/btn_help.png')
help_btn.config(image=help_photo, relief=tk.FLAT)
help_btn.grid(row=1, column=2)

play_joker_btn = tk.Button(chng_btn_frame, command=clicked_joker)
play_joker_photo = tk.PhotoImage(file='cards/btns/btn_joker.png')
play_joker_btn.config(image=play_joker_photo, relief=tk.FLAT)
play_joker_btn.grid(row=1, column=1)
play_joker_btn.configure(state=tk.DISABLED)

# Create the score bar.
score_frame = tk.Frame(root)
score_frame.grid(row=3, column=0, sticky='W' + 'E')
score_bar = tk.Label(score_frame,
                     font='20',
                     text='',
                     bd=1,
                     bg='indianred',
                     fg='black',
                     relief=tk.SUNKEN, anchor=tk.W)
score_bar.pack(side=tk.BOTTOM, fill=tk.X)

# Create the status bar.
stat_frame = tk.Frame(root)
stat_frame.grid(row=4, column=0, sticky='W' + 'E')
stat_bar = tk.Label(stat_frame,
                    font='20',
                    text='',
                    bd=1,
                    bg='steelblue',
                    fg='white',
                    relief=tk.SUNKEN, anchor=tk.W)
stat_bar.pack(side=tk.BOTTOM, fill=tk.X)

# Drop-down menu.
menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='Menu', menu=file_menu)
file_menu.add_command(label='About', compound='left',
                      image=about_icon, command=about_menu)
file_menu.add_command(label='Help', compound='left',
                      image=help_icon, command=help_menu)
file_menu.add_separator()
file_menu.add_command(label='Make small donation', compound='left',
                      image=donation_icon, command=donate_me)
file_menu.add_command(label='Get Python sorce code', compound='left',
                      image=github_icon, command=get_source_code)
file_menu.add_separator()
file_menu.add_command(label='Visit Blog', compound='left',
                      image=blog_icon, command=visit_blog)
file_menu.add_separator()
file_menu.add_command(label='Quit', compound='left',
                      image=exit_icon, command=exit_game)

# Set up menu tick for music menu.
# I don't think I am doing this the best way
# It can't be this convoluted can it?
# More research needed.
t1Var = tk.IntVar()
t2Var = tk.IntVar()
t3Var = tk.IntVar()
t4Var = tk.IntVar()
t5Var = tk.IntVar()
allVar = tk.IntVar()
file_menu2 = tk.Menu(menu_bar, tearoff=0)
musicVar = tk.IntVar()
sfonVar = tk.IntVar()
sfoffVar = tk.IntVar()
musicVar.set(0)
allVar.set(0)
sfonVar.set(1)
sfoffVar.set(0)

menu_bar.add_cascade(label='Music', menu=file_menu2)
file_menu2.add_checkbutton(label='Play Summer', compound='left',
                           image=music_icon,
                           variable=t1Var, command=lambda: play_music("1"))
file_menu2.add_checkbutton(label='Play Dance', compound='left',
                           image=music_icon,
                           variable=t2Var, command=lambda: play_music("2"))
file_menu2.add_checkbutton(label='Play Dreams', compound='left',
                           image=music_icon,
                           variable=t3Var, command=lambda: play_music("3"))
file_menu2.add_checkbutton(label='Play Motion', compound='left',
                           image=music_icon,
                           variable=t4Var, command=lambda: play_music("4"))
file_menu2.add_checkbutton(label='Play SciF1', compound='left',
                           image=music_icon,
                           variable=t5Var, command=lambda: play_music("5"))
file_menu2.add_separator()

file_menu2.add_checkbutton(label='Play All Tracks',
                           variable=allVar, command=play_all_tracks)
file_menu2.add_command(label='Stop music',
                       command=stop_music)
file_menu2.add_command(label='Free music from Bensound.com',
                       command=visit_bensound)
file_menu2.add_separator()

file_menu2.add_checkbutton(label='Sound Effects ON',
                           variable=sfonVar,
                           command=sfx_switch)
file_menu2.add_checkbutton(label='Sound Effects OFF',
                           variable=sfoffVar,
                           command=sfx_switch)

root.config(menu=menu_bar)

# Checks for a click on the main window X icon.
root.protocol("WM_DELETE_WINDOW", exit_game)

# Main.
if Glo.sound_fx:
    play_sound(r'cards/sfx/startup.wav')
show_logo()
load_high_score()
new_game()

root.mainloop()
