"""
Hi-Lo V1.67
A GUI High-Low card game.

By Steve Shambles
updated Oct 21st 2020

https://stevepython.wordpress.com/

Requirements:
---------------
pip3 install pygame

'cards' folder and all its contents in current dir.
=================================
V1.67: Linted with Pylint. Added download cards folder option if missing.
V1.66: Removed unecessary error pop up when high_score.text missing.
V1.65: Added play random music track when game starts.
V1.64: Cosmetics and code tidy changes caused by new joker feature.
V1.63: Play joker feature added. Costs 4pts. Deals a joker for 2nd card.
V1.62: Realigned frames and buttons to bbe more precise, still cant get
       it perfect, but within a pixel or 2.
V1.61: Changed game tactic. Can now change card any time as long as you
       have 1pt or more. Each change costs 1pt off your score.
       Makes for better, longer, more fun and more tactical game.
V1.60: Fixed new menu check mark duplicate bugs.
V1.59: Added "play all" music option in music menu.
V1.58: Added menu check marks in the music menu (badly done code,but works)
V1.57: Added menu items, donate, get source code and visit new blog.
V1.56: Fixed high score bug when both score and hs were zero, said new hs.
V1.55: fixed game over bug, music didnt stop and gui wasn't destroyed properly.
"""
import os
from tkinter import Button, DISABLED, E, Frame, IntVar, Label, LabelFrame
from tkinter import messagebox, Menu, NORMAL, PhotoImage, Tk, W
import random
import sys
import webbrowser

from pygame import mixer


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


mixer.init()

root = Tk()
root.title('Hi-Lo V1.67')
root.resizable(False, False)

# Check cards folder available.
cards_check = 'cards'
check_file = os.path.isdir(cards_check)

if not check_file:
    root.withdraw()
    ask_yn = messagebox.askyesno('Folder Error', 'The "cards" folder is missing\n\n'
                                 'Would you like to download\n'
                                 'a new copy? 30Mb zip.')

    if ask_yn:
        webbrowser.open('http://www.mediafire.com/file/m1qjzcnkjy6o3jn/cards-folder-oct-2020.zip/file')

    root.destroy()
    sys.exit()

# Check high_score.txt available, if not create it.
hst_check = 'high_score.txt'
check_file = os.path.isfile(hst_check)

if not check_file:
    with open(hst_check, 'w') as contents:
        pass

# Frame for the buttons.
btn_frame = Frame(root)
btn_frame.grid(row=0, column=1, padx=4)

# Frame for the two card images.
cards_frame = LabelFrame(root, pady=1)
cards_frame.grid(row=0, column=0, padx=4, pady=0)

# Frame for the change button.
chng_btn_frame = Frame(root, pady=2)
chng_btn_frame.grid(padx=0, row=1, column=0)

# Frame for printng the scores.
score_frame = LabelFrame(root)
score_frame.grid(row=2, column=0, padx=4, columnspan=2, sticky=W+E)

# Frame for printing messages.
msg_frame = LabelFrame(root)
msg_frame.grid(row=3, column=0, padx=4, pady=4, columnspan=2, sticky=W+E)


def about_menu():
    """Display about program info if selected in drop-down menu."""
    messagebox.showinfo('About', 'Hi-Lo V1.67 Freeware.\n\n'
                        'By Steve Shambles Oct 2020.\n')

def help_menu():
    """How to use the program, menu help text."""
    messagebox.showinfo('How To...', 'Play Hi-Lo.\n\n'
                        'This game is very simple to play.\n\n'
                        'All you have to do is guess if the face down\n'
                        'card on the right will be higher or lower than\n'
                        'the card shown on the left.\n\n'
                        'If you have at least 1pt the "CHANGE CARD"\n'
                        'button Will become available.\n'
                        'Click the change card button if you want\n'
                        'to change a bad card, this will costs you 1pt,\n'
                        'with no guarantee of getting a better card.\n\n'
                        'A Joker is wild, i.e. counted as anything.\n'
                        'If you turn over two jokers together you will\n'
                        'be awarded a bonus of 3pts.\n\n'
                        'If you have 4pts or more the "JOKER" button will\n'
                        'become availble to you at a cost of 4pts per use.\n'
                        'This will deal you a guaranteed joker on card two,\n'
                        'ensuring a win to the next round.\n\n'
                        'Any pair also gives you a win to the next round.\n\n'
                        'Aces are counted as the highest card.\n\n'
                        'Your high score will be saved to disc and reloaded\n'
                        'the next time you play.\n\n'
                        'Enjoy.')

def visit_blog():
    """Visit my python blog if selected in drop-down menu."""
    webbrowser.open('https://stevepython.wordpress.com/')

def visit_new_blog():
    """Visit my python blog if selected in drop-down menu."""
    webbrowser.open('https://pyshambles.blogspot.com/')

def visit_bensound():
    """Visit bensound.com blog if selected in drop-down menu."""
    webbrowser.open('https://bensound.com/')

def save_high_score():
    """Save high score to file in current dir."""
    with open('high_score.txt', 'w') as contents:
        save_it = str(Glo.high_score)
        contents.write(save_it)

def play_music(track):
    """Play background music if a track is selected in drop-down menu"""
    # zero all menu checkmarks first.
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
    # zero all menu checkmarks first.
    t1Var.set(0)
    t2Var.set(0)
    t3Var.set(0)
    t4Var.set(0)
    t5Var.set(0)
    allVar.set(0)

def play_all_tracks():
    """Play all music tracks if play all is selected in drop-down menu"""
    # zero all menu checkmarks first.
    t1Var.set(0)
    t2Var.set(0)
    t3Var.set(0)
    t4Var.set(0)
    t5Var.set(0)
    allVar.set(1)
    mixer.music.load('cards/music/all.mp3')
    mixer.music.play(-1)  # Play indefinetly -1. 0 or () = play once.

def start_rnd_music():
    """Pay a random music track at start up."""
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
    card_btn_one = Button(cards_frame)
    PHOTO = PhotoImage(file='cards/'+str(card_one))
    card_btn_one.config(image=PHOTO)
    card_btn_one.grid(row=0, column=0, padx=2, pady=2)
    card_btn_one.photo = PHOTO

def setup_card_two():
    """Get rnd card for card 2. Only display back of card 2 though."""
    get_rnd_card()
    Glo.card2_val = Glo.random_card
    card_btn_two = Button(cards_frame)
    PHOTO2 = PhotoImage(file='cards/blank.png')
    card_btn_two.config(image=PHOTO2)
    card_btn_two.grid(row=0, column=1, padx=2, pady=2)
    card_btn_two.photo = PHOTO2

def show_card_two():
    """Reveal card two."""
    but_2a = Button(cards_frame)
    photo_2a = PhotoImage(file='cards/'+str(Glo.new_card)+'.png')
    but_2a.config(image=photo_2a)
    but_2a.grid(row=0, column=1, padx=2, pady=2)
    but_2a.photo = photo_2a

def get_rnd_card():
    """Get a new random card."""

    # Pass btn used, give joker.
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
    chng_crd_btn.configure(state=DISABLED)
    # Correct guess, card 2 was higher, same card value or a joker.
    if Glo.card1_val < Glo.card2_val or Glo.card1_val == Glo.card2_val  \
       or Glo.card1_val == 0 or Glo.card2_val == 0:
        Glo.points_won = Glo.points_won + 1

        # Update highscore.
        if Glo.points_won > Glo.high_score:
            Glo.high_score = Glo.points_won

        update_score()
        print_correct()

        # Print relevent game messages.
        if Glo.card1_val == Glo.card2_val:
            print_pairs()

        if Glo.card1_val == 0 or Glo.card2_val == 0:
            print_joker()

        if Glo.card1_val == 0 and Glo.card2_val == 0:
            joker_bonus()

        # Enable\disable relevent buttons.
        nxt_crd_btn.configure(state=NORMAL)
        hghr_btn.configure(state=DISABLED)
        lwr_btn.configure(state=DISABLED)

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
    msg_label = Label(msg_frame, fg='blue',
                      text='3 POINTS JOKER BONUS!          ')
    msg_label.grid(row=2, column=0, pady=2, sticky=W)
    Glo.points_won = Glo.points_won + 3
    update_score()

def clicked_lower():
    """Clicked on 'Lower' button."""
    chng_crd_btn.configure(state=DISABLED)

    if Glo.card1_val > Glo.card2_val or Glo.card1_val == Glo.card2_val  \
       or Glo.card1_val == 0 or Glo.card2_val == 0:
        Glo.points_won = Glo.points_won + 1

        if Glo.points_won > Glo.high_score:
            Glo.high_score = Glo.points_won

        update_score()
        print_correct()

        if Glo.card1_val == Glo.card2_val:
            print_pairs()

        if Glo.card1_val == 0 or Glo.card2_val == 0:
            print_joker()

        if Glo.card1_val == 0 and Glo.card2_val == 0:
            joker_bonus()

        nxt_crd_btn.configure(state=NORMAL)
        hghr_btn.configure(state=DISABLED)
        lwr_btn.configure(state=DISABLED)

    else:
        print_wrong()
        show_card_two()
        game_over_man()
        return

    show_card_two()

def update_score():
    """Update score."""
    # Note, the spacing is important to erase prev message.
    msg_label = Label(score_frame,  \
    text='Score :'+str(Glo.points_won)+'    Best :'+str(Glo.high_score)+'          ')
    msg_label.grid(row=0, column=1, pady=4, sticky=W)

def print_aces_are_high():
    """Print 'Aces are high' in-game message."""
    msg_label = Label(msg_frame, fg='blue', text='ACES ARE HIGH!                 ')
    msg_label.grid(row=2, column=0, pady=4, sticky=W)

def print_joker():
    """Print 'Jokers are wild' in-game message."""
    msg_label = Label(msg_frame, fg='blue', text='JOKERS ARE WILD!          ')
    msg_label.grid(row=2, column=0, pady=2, sticky=W)

def print_correct():
    """Print 'Well done' in-game message."""
    msg_label = Label(msg_frame, fg='green', text='WELL DONE! CLICK NEXT')
    msg_label.grid(row=2, column=0, pady=2, sticky=W)

def print_wrong():
    """Print 'Unlucky' in-game message."""
    msg_label = Label(msg_frame, fg='red', text='UNLUCKY!                    ')
    msg_label.grid(row=2, column=0, pady=2, sticky=W)

def print_higher_or_lower():
    '''Print 'Higher or Lower in-game message.'''
    msg_label = Label(msg_frame, fg='blue', text='HIGHER OR LOWER?           ')
    msg_label.grid(row=2, column=0, pady=2, sticky=W)

def print_pairs():
    """Print 'pairs are good' in-game message."""
    msg_label = Label(msg_frame, text='PAIRS ARE GOOD!                  ')
    msg_label.grid(row=2, column=0, pady=2, sticky=W)

def print_changed_card():
    """Print 'Change 1st card costs 1pt' in-game message."""
    msg_label = Label(msg_frame, fg='red', text='CHANGE CARD COSTS 1pt.     ')
    msg_label.grid(row=2, column=0, pady=2, sticky=W)

def print_used_joker():
    """Print 'Playing joker costs 4pt' in-game message."""
    msg_label = Label(msg_frame, fg='red', text='PLAYING JOKER COSTS 4pts        ')
    msg_label.grid(row=2, column=0, pady=2, sticky=W)

def clicked_next():
    """Clicked on 'Next' button."""
    setup_card_one()
    setup_card_two()
    print_higher_or_lower()

    if Glo.card1_val == 14:
        print_aces_are_high()

    update_score()
    nxt_crd_btn.configure(state=DISABLED)
    hghr_btn.configure(state=NORMAL)
    lwr_btn.configure(state=NORMAL)

    # Only light up change card button if have at least 1pt.
    chng_crd_btn.configure(state=DISABLED)
    if Glo.points_won > 0:
        chng_crd_btn.configure(state=NORMAL)

    # Only light up pass button if have at least 4pts.
    play_joker_btn.configure(state=DISABLED)
    if Glo.points_won > 3:
        play_joker_btn.configure(state=NORMAL)

def game_over_man():
    """Game over because player guessed incorrectly."""
    msg = ''
    ask_yn = ''

    if Glo.points_won > Glo.high_score or Glo.points_won > 0 and Glo.points_won == Glo.high_score:
        Glo.high_score = Glo.points_won
        save_high_score()
        msg = '       G A M E  O V E R  M A N  \n\n\n Congratulations, a new high score!\n\n          Play another game?'

    else:
        msg = 'G A M E  O V E R  M A N\n\n  Play another game?'

    ask_yn = messagebox.askyesno('Hi-Lo', msg)

    if not ask_yn:
        stop_music()
        root.destroy()
        sys.exit()

    new_game()

def clicked_change():
    """Clicked on the enabled 'change' button."""
    # Deduct point for using change card.
    Glo.points_won -= 1
    update_score()
    setup_card_one()
    setup_card_two()
    chng_crd_btn.configure(state=DISABLED)
    print_changed_card()

def clicked_joker():
    """Clicked on the enabled 'pass' button."""
    # Deduct 4 points for using pass.
    Glo.points_won -= 4
    update_score()
    Glo.play_joker_btn = True
    get_rnd_card()  # will choose joker.
    show_card_two()
    play_joker_btn.configure(state=DISABLED)
    chng_crd_btn.configure(state=DISABLED)
    Glo.play_joker_btn = False
    nxt_crd_btn.configure(state=NORMAL)
    hghr_btn.configure(state=DISABLED)
    lwr_btn.configure(state=DISABLED)
    print_used_joker()

def new_game():
    """Start a new game, retaining high score"""
    Glo.points_won = 0
    update_score()
    print_higher_or_lower()
    clicked_next()

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
       reward my work."""
    webbrowser.open("https:\\paypal.me/photocolourizer")

def get_source_code():
    """Send user to GitHub repo of this source code."""
    webbrowser.open('https://github.com/steveshambles/Hi-Lo-card-game')


# Higher-Lower buttons.
hghr_btn = Button(btn_frame, bg='limegreen', text='HIGHER',
                  command=clicked_higher)
hghr_btn.grid(row=0, column=0, pady=3, padx=3, sticky=W+E)
lwr_btn = Button(btn_frame, bg='indianred', text='LOWER ',
                 command=clicked_lower)
lwr_btn.grid(row=1, column=0, pady=3, padx=3, sticky=W+E)
nxt_crd_btn = Button(btn_frame, bg='orange', text='NEXT',
                     command=clicked_next)
nxt_crd_btn.grid(row=2, column=0, pady=3, padx=3, sticky=W+E)
nxt_crd_btn.configure(state=DISABLED)

# The change button.
chng_crd_btn = Button(chng_btn_frame, bg='yellow', text='   CHANGE   ',
                      command=clicked_change)
chng_crd_btn.grid(row=1, column=0, padx=0, pady=0)

play_joker_btn = Button(chng_btn_frame, bg='plum', text='    JOKER    ',
                        command=clicked_joker)
play_joker_btn.grid(row=1, column=1, padx=0, pady=6)

# Disable joker btn until have at least 4pts.
play_joker_btn.configure(state=DISABLED)

# Drop-down menu.
menu_bar = Menu(root)
file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='Menu', menu=file_menu)
file_menu.add_command(label='About', command=about_menu)
file_menu.add_command(label='Help', command=help_menu)
file_menu.add_separator()
file_menu.add_command(label='Make small donation', command=donate_me)
file_menu.add_command(label='Get Python sorce code', command=get_source_code)
file_menu.add_separator()
file_menu.add_command(label='Visit Old Blog', command=visit_blog)
file_menu.add_command(label='Visit New Blog', command=visit_new_blog)
file_menu.add_separator()
file_menu.add_command(label='Quit', command=exit_game)

# set up menu tick for accents menu
t1Var = IntVar()
t2Var = IntVar()
t3Var = IntVar()
t4Var = IntVar()
t5Var = IntVar()
allVar = IntVar()

file_menu2 = Menu(menu_bar, tearoff=0)
musicVar = IntVar()
musicVar.set(0)
allVar.set(0)

menu_bar.add_cascade(label='Music', menu=file_menu2)
file_menu2.add_checkbutton(label='Play Summer',
                           variable=t1Var, command=lambda: play_music("1"))
file_menu2.add_checkbutton(label='Play Dance',
                           variable=t2Var, command=lambda: play_music("2"))
file_menu2.add_checkbutton(label='Play Dreams',
                           variable=t3Var, command=lambda: play_music("3"))
file_menu2.add_checkbutton(label='Play Motion',
                           variable=t4Var, command=lambda: play_music("4"))
file_menu2.add_checkbutton(label='Play SciF1',
                           variable=t5Var, command=lambda: play_music("5"))
file_menu2.add_separator()
file_menu2.add_checkbutton(label='Play All Tracks',
                           variable=allVar, command=play_all_tracks)
file_menu2.add_command(label='Stop music',
                       command=stop_music)
file_menu2.add_command(label='Free music from Bensound.com',
                       command=visit_bensound)

root.config(menu=menu_bar)

# Checks for a click on the main window X icon.
root.protocol("WM_DELETE_WINDOW", exit_game)

# Main.
load_high_score()
start_rnd_music()
new_game()

root.mainloop()
