from tkinter import *
from tkinter.ttk import *
from tkVideoPlayer import TkinterVideo 
import pygame
pygame.mixer.init()
music = pygame.mixer.music

def fine(prompt_win):
    music.stop()
    prompt_win.destroy()

def not_fine(prompt_win):
    print("CALLING 911...")
    music.stop()
    prompt_win.destroy()
    music.load("alarm-car-or-home-62554.mp3")
    music.play(loops=10)


def main():
    
    music.load("emergency-alarm-with-reverb-29431.mp3")
    music.play(loops=10)
    root=Tk()
    root.attributes("-fullscreen", True)
    root.config(background="#f5ffd4")


    ################################# PLAY INTRO VIDEO #################################

    vid_frame= Frame(root)
    vid_frame.pack(expand=True, fill=BOTH)

    vid =  TkinterVideo(vid_frame, scaled=True)
    vid.load("b4.mp4")
    vid.pack(expand=True, fil=BOTH)
    vid.play()

    vid.bind("<<Ended>>", lambda e: vid_frame.destroy())
    # root.after(4300, vid_frame.destroy)

    ###################################################################################


    ########################## STYLE ############################

    style = Style()


    ########################### MAKING PROMPT WIN #################################


    prompt_win =  Toplevel(root)
    prompt_win.propagate(False)
    prompt_win.title("PROMPT")

    prompt_win.config(background="#434242", height= 642.52, width= 982.677)


    ############################# LABELING QUESTION #############################


    # style.configure("are_you_fine.TLabel", padding = (15,15,0,0))
    are_you_fine = Label(prompt_win, text="ARE YOU FINE?", font=('',40), style= "are_you_fine.TLabel")
    are_you_fine.pack()

    are_you_fine.update()

    width = are_you_fine.winfo_width()

    are_you_fine.place(x=(982.677-width)/2, rely=0.3)           #### LABEL DONE 


    ############################# Making YES/NO #############################


    style.configure("prompt_but.TButton", font=('',28))

    yes_fine = Button(prompt_win, text="YES", style="prompt_but.TButton", command= lambda: fine(prompt_win))
    yes_fine.pack()
    yes_fine.update()

    width = yes_fine.winfo_width()


    yes_fine.place(x=491.3385 - width -80 , rely=0.6)


    no_fine = Button(prompt_win, text="NO", style="prompt_but.TButton", command= lambda: not_fine(prompt_win))
    no_fine.pack()
    no_fine.update()

    width = no_fine.winfo_width()


    no_fine.place(x=491.3385 +  80, rely=0.6)

    #############################  #############################




    root.mainloop()

if __name__ == "__main__":
    main()