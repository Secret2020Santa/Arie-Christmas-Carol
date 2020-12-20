# -*- coding: utf-8 -*-
"""
Created Christmas Day

author: Santa Claus
"""
import sys
import os
import pygame as pg
import pygame_menu as pg_menu
import pygame_textinput as pg_textinput

# clock = None    # type: pygame.time.Clock
# mymenu = None   # type: pygame_menu.Menu
# surface = None  # type: pygame.Surface 

# Name = ['Arie Dedding']

def Game_Over():
    main_background()
    Answer('Game Over. Maybe the Christmas Spirit will find you next time')
    pg.quit()
    sys.exit()

def Try_Again(correct_titles):
    if correct_titles == 0:
        Answer('Nothing was right, try again', wait=1000)
    elif correct_titles == 1:
        Answer('One guess was right, try again', wait=1000)
        
    pass


def Show_hint(Hint_im, Hint_count):
    global surface
    
    #Get box to show hint
    rect_color = (34,168,34)
    w,h = surface.get_size()
    gap = 10

    Hints_box = (0,0,int(w/2),h)
    pg.draw.rect(surface, rect_color, Hints_box, 2)
    
    #Display hint text
    Hint_text = f'Hint Level: {Hint_count}'
    font = pg.font.SysFont(None, 30)
    Title_im = font.render(Hint_text, True, ((240,230,140)))
    Title_im_w, Title_im_h = Title_im.get_size()
    Title_loc = (int(Hints_box[0] + Hints_box[2]/2 - (Title_im_w)/2),
                 int(Hints_box[1] + gap + Title_im_h/2))
    if Hint_count != 0:
        #Resize hint image
        im_w, im_h = Hint_im.get_size()
        maxh = h - 3*gap - Title_im_h
        maxw = w - 2*gap
        scaling_h = maxh/im_h
        scaling_w = maxw/im_w
        if scaling_h > scaling_w:
            scale = scaling_w
        else:
            scale = scaling_h
        
        Hint_im = pg.transform.scale(Hint_im, (int(scale*im_w), int(scale*im_h)))
        im_w, im_h = Hint_im.get_size()
        im_loc = (int(Hints_box[0] + Hints_box[2]/2 - (im_w)/2),
                  int(Hints_box[1] + Title_im_h + Hints_box[3]/2 - (im_h)/2))
        
        surface.blit(Hint_im, im_loc)
    surface.blit(Title_im, Title_loc)
    
    pass
    
    
def Show_QuestionFuture(Q_count, Q_info, mouse_pressed):
    global surface
    
    #First get the location of the question on the screen
    rect_color = (34,168,34)
    box_color = (240,230,140)
    w,h = surface.get_size()

    Question_box = (int(w/2),0,int(w/2),h)
    pg.draw.rect(surface, rect_color, Question_box, 2)
    
    #Create the Q-header
    Q = Q_info[0]
    fontQ = pg.font.SysFont(None, 25)
    fontAns = pg.font.SysFont(None, 30)
    img_Q = fontQ.render(Q, True, (240,230,140))
    Q_w, Q_h = img_Q.get_size()
    gap = 10
    
    loc_Q = (int(Question_box[0]+Question_box[2]/2 - Q_w / 2), 100)
    
    #Then make the buttons for the question answers
    mouse = pg.mouse.get_pos()
    BUTTON_BOX = (int(Question_box[0] + gap), int(loc_Q[1] + Q_h + 2*gap), 
                  int(Question_box[2] - 2*gap), int(Question_box[3] - Q_h - 100 - 6*gap))
    pg.draw.rect(surface, box_color, BUTTON_BOX, 2)
    
    button_order = [(0,0), (1,0), (0,1), (1,1)]
    Box_w, Box_h = int(BUTTON_BOX[2]/3), int(BUTTON_BOX[3]/3)
    dx = Box_w-6*gap
    dy = Box_h-8*gap
    
    buttons = [( BUTTON_BOX[0] + 9*gap + i*(dx+Box_w) , BUTTON_BOX[1]+6*gap +j*(dy+Box_h))
           for index, (i,j) in enumerate(button_order)]
    Answer = None
    for index, button in enumerate(buttons):
        Ans = Q_info[1][index]
        img_Ans = fontAns.render(Ans, True, (0,0,0))
        A_w, A_h = img_Ans.get_size()
        
        
        loc_Ans = (button[0]+int(gap/2), button[1]+int(gap/2))
        box = (button[0], button[1], A_w+gap, A_h+gap)

        #Detect if mouse is hovering above box
        if box[0] <= mouse[0] <= box[0]+box[2] and box[1] <= mouse[1] <= box[1]+box[3]:
            box_color = (120,230,120)
            img_Ans = fontAns.render(Ans, True, (255,255,255))
            if mouse_pressed:
                Answer = index
                # print(f'Picked Answer #{Answer}')
        else:
            box_color = (240,230,140)
                
        pg.draw.rect(surface, box_color, box, 0)
        surface.blit(img_Ans, loc_Ans)
    
    mouse_pressed = False
    surface.blit(img_Q, loc_Q)
    
    return Answer, mouse_pressed
    

def Text_print(text, text_count, t1, dt):
    # Print any text, letter by letter
    Draw_text(text[:text_count])
    if (pg.time.get_ticks() - t1 > dt * 1000) & (text_count <= len(text)):
        t1 = pg.time.get_ticks()
        text_count += 1
    
    return text_count, t1

def Show_Question(Question_count, img, info, mouse_pressed):
    global surface
    # First display the image at the top
    surface_w, surface_h = surface.get_size()
    img_w, img_h = img.get_rect().size
    
    #Scale to fit size for image
    max_h = 300
    gap = 20
    scale = max_h/img_h
    img = pg.transform.scale(img, (int(scale*img_w), int(scale*img_h)))
    img_w, img_h = img.get_rect().size
    
    loc_img = (int(surface_w/2 - img_w/2), gap)
    
    #Then display the question
    Q = info[0]
    fontQ = pg.font.SysFont(None, 30)
    fontAns = pg.font.SysFont(None, 25)
    img_Q = fontQ.render(Q, True, (0,0,0))
    Q_w, Q_h = img_Q.get_size()

    loc_Q = (int(surface_w/2 - Q_w/2), max_h + gap*2)    
    
    #Then make the buttons for the question answers
    mouse = pg.mouse.get_pos()
    BUTTON_BOX = (gap*5, max_h + gap*3 + Q_h, surface_w-gap*10, surface_h - (max_h + gap*4 + Q_h))
    pg.draw.rect(surface, (0,0,0), BUTTON_BOX, 1)
    
    button_order = [(0,0), (1,0), (0,1), (1,1)]
    Box_w, Box_h = int(BUTTON_BOX[2]/3), int(BUTTON_BOX[3]/3)
    dx = Box_w-4*gap
    dy = Box_h-2*gap
    
    
    buttons = [( BUTTON_BOX[0] + 2*gap + i*(dx+Box_w) , BUTTON_BOX[1]+gap +j*(dy+Box_h))
               for index, (i,j) in enumerate(button_order)]
    Answer = None
    for index, button in enumerate(buttons):
        
        Ans = info[1][index]
        img_Ans = fontAns.render(Ans, True, (0,0,0))
        A_w, A_h = img_Ans.get_size()
        box_color = (34,168,34)
        
        
        loc_Ans = (button[0]+int(gap/2), button[1]+int(gap/2))
        box = (button[0], button[1], A_w+gap, A_h+gap)

        #Detect if mouse is hovering above box
        if box[0] <= mouse[0] <= box[0]+box[2] and box[1] <= mouse[1] <= box[1]+box[3]:
            box_color = (68,188,68)
            img_Ans = fontAns.render(Ans, True, (255,255,255))
            if mouse_pressed:
                Answer = index
                # print(f'Picked Answer #{Answer}')
                
        pg.draw.rect(surface, box_color, box, 0)
        surface.blit(img_Ans, loc_Ans)
    
    mouse_pressed = False
    
    surface.blit(img_Q, loc_Q)
    surface.blit(img, loc_img)
    
    return Answer, mouse_pressed

def Check_Answer(Ans, Q_info):
    # Checks the result of the answer  
    Result = Q_info[1].index(Q_info[2]) == Ans
    # if Result:
    #     print('You were right!')
    # else:
    #     print('Too bad, you know jack shit')
    
    return Result


def Next_Level(lines):
    # Display text for next level
    for line in lines:
        Answer(line)
    pass


def Right_Answer():
    text = 'Bingo, you were right!'
    Answer(text)
    pass


def Wrong_Answer(Strike):
    text1 = 'No, that was far from the correct answer...'
    Answer(text1)
    text2 = f'This is strike {Strike}'
    Answer(text2)
    text3 = f'You have {3-Strike} strike(s) left'
    Answer(text3)
    
    pass
    
def Answer(text, wait=2000):
    global surface
    
    main_background()
    font = pg.font.SysFont(None, 40)
    img_text = font.render(text, True, (0, 0, 0))
    
    surface_w, surface_h = surface.get_size()
    img_w, img_h = img_text.get_size()
    
    img_loc = (int(surface_w/2 - img_w /2), int(surface_h/2 - img_h/2))
    
    surface.blit(img_text, img_loc)
    pg.display.flip()
    pg.time.wait(wait)
    
    pass

def Riddle(timer_start, timer_img, Riddle_Answer):
    global surface
    
    #Obtain surface size
    surface_w, surface_h = surface.get_size()
    
    #Define timer
    time_passed = round((pg.time.get_ticks() - timer_start)/1000)
    max_time = 300
    time_left = max_time - time_passed
    
    if time_left < 0:
        Game_Over()
    
    timer_h = 50
    gap = 20
    font = pg.font.SysFont(None, 50)
    time_img = font.render(str(time_left), True, (0,0,0))
    
    timer_img_w, timer_img_h = timer_img.get_size()
    time_img_w, time_img_h = time_img.get_size()
    scale = timer_h/timer_img_h
    timer_img = pg.transform.scale(timer_img, (int(scale*timer_img_w),int(scale*timer_img_h)))
    timer_img_w, timer_img_h = timer_img.get_size()
    
    timer_loc = (gap, gap)
    time_loc = (int(1.5*gap+timer_img_w), int(gap + timer_img_h / 2 - time_img_h/2))
    
    #Show riddle and answer boxes
    Riddle_text = '''The accesoires in your box are hints to your gifts./nEnter your answers in the box at the bottom./nThe answers are insensitive to caps, however,/npunctuation marks are important, (apostrophes, hyphens, etc...)./n/nEnter your answer as follows:/nName of Gift1 | Name of Gift2/nBe sure to add exactly ' | ' between your two answers./nThe order does not matter/n/n1. "I'd far rather be happy than right any day."/n/n2. "It was a pleasure to burn."/n/n3. Let yourself be guided by the gift/n/n4. F = 9/5 * C + 32/n/n5. 42/n/n6. 467'''
    Riddle_draw(Riddle_text)
    
    #Show answer boxes
    Ans_size_w, Ans_size_h = Riddle_Answer.get_surface().get_size()
    Ans_box = (int(surface_w/2 - Ans_size_w/2), surface_h - gap*7)
    
    text_box = (int(surface_w/2 - Ans_size_w/2) - 5, surface_h - gap*7-5, 
                Ans_size_w+10, Ans_size_h+10)
    
    pg.draw.rect(surface, (0,0,0), text_box, 0)
    surface.blit(Riddle_Answer.get_surface(), Ans_box)
    
    surface.blit(timer_img, timer_loc)
    surface.blit(time_img, time_loc)
    
    pass

def Riddle_draw(text):
    global surface
    
    Riddle_lines = text.split('/n')
    
    font = pg.font.SysFont(None, 25)
    gap = 50
    _, Riddle_box_h = 500, 300
    Nlines = len(Riddle_lines)
    surface_w, surface_h = surface.get_size()
    
    for num, line in enumerate(Riddle_lines):
        line_img = font.render(line, True, (0,0,0))
        line_img_w, line_img_h = line_img.get_size()
        
        line_loc = (int(surface_w/2 - line_img_w /2), int(gap + Riddle_box_h/2 - line_img_h * (0.5*Nlines - num)))
        
        surface.blit(line_img, line_loc)
    pass

def Check_Riddle_Ans(Ans):
    Right_Answer = ['''the hitchhiker's guide to the galaxy''', '''fahrenheit 467''']
    Entered_Answer = Ans.split(' | ')
    
    correct_titles = 0
    for title in Entered_Answer:
        if title.lower() in Right_Answer:
            correct_titles += 1
    return correct_titles

def Draw_Strike(Count):
    global surface
    
    Strikes = 'X'*Count
    Strike_Message = 'Strikes: '+ Strikes
    
    font = pg.font.SysFont(None, 50)
    im_strike = font.render(Strike_Message, True, (0,0,0))
    
    w, h = surface.get_size()
    
    im_strike_loc = (w - im_strike.get_size()[0] - 10, 10)
    surface.blit(im_strike, im_strike_loc)
    pass
    
    
def Check_FutAns(Ans, Q_info):
    if Q_info[1].count(Q_info[2]) > 1:
        Result = True
    else:
        Result = Q_info[1].index(Q_info[2]) == Ans 
    
    return Result
    
def Last_Showing(Hint_Count, Hint_Folder, Hint_Files):
    global surface
    
    w, h = surface.get_size()
    gap = 20
    
    #Create main header
    Gold_color = (38,186,38)
    Text = f'Merry Christmas!! View your {Hint_Count} hint(s) below'
    font = pg.font.SysFont(None, 50)
    Title_im = font.render(Text, True, Gold_color)
    
    Title_w, Title_h = Title_im.get_size()
    Title_loc = (int(w/2 - Title_w/2),
                 gap)
    
    Hint_locs = [(0,0),   (4,0),   (8,0),
                 (0,1),(3,1),(6,1),(9,1)]
    
    for index, file in enumerate(Hint_Files[:Hint_Count]):
        locs = Hint_locs[index]
        im = pg.image.load(Hint_Folder+file)
        im_w,im_h = im.get_size()
        
        #Find box borders
        if index < 3:
            Box_w = int(w / 3)
        else:
            Box_w = int(w / 4)
        Box_h = (h-2*gap-Title_h) / 2 - gap
        Box = (int(gap + locs[0]/12 * w),
               int(2*gap + Title_h + locs[1] * Box_h),
               int(Box_w), int(Box_h))
        
        #Resize image
        scaling_w = (Box_w-gap)/im_w
        scaling_h = (Box_h-gap)/im_h
        if scaling_h > scaling_w:
            scale = scaling_w
        else:
            scale = scaling_h
        im = pg.transform.scale(im, (int(scale*im_w), int(scale*im_h)))
        im_w, im_h = im.get_size()
        im_loc = (int(Box[0] + (Box_w - im_w)/2 + gap/2),
                  int(Box[1] + (Box_h - im_h)/2 + gap/2))
        
        
        pg.draw.rect(surface, (0,0,0), Box, 2)
        surface.blit(im, im_loc)
    if Hint_Count < 7:
        index = 6
        file = Hint_Files[-1]
        locs = Hint_locs[index]
        im = pg.image.load(Hint_Folder+file)
        im_w,im_h = im.get_size()
        
        #Find box borders
        if index < 3:
            Box_w = int(w / 3)
        else:
            Box_w = int(w / 4)
        Box_h = (h-2*gap-Title_h) / 2 - gap
        Box = (int(gap + locs[0]/12 * w),
               int(2*gap + Title_h + locs[1] * Box_h),
               int(Box_w), int(Box_h))
        
        #Resize image
        scaling_w = (Box_w-gap)/im_w
        scaling_h = (Box_h-gap)/im_h
        if scaling_h > scaling_w:
            scale = scaling_w
        else:
            scale = scaling_h
        im = pg.transform.scale(im, (int(scale*im_w), int(scale*im_h)))
        im_w, im_h = im.get_size()
        im_loc = (int(Box[0] + (Box_w - im_w)/2 + gap/2),
                  int(Box[1] + (Box_h - im_h)/2 + gap/2))
        
        
        pg.draw.rect(surface, (0,0,0), Box, 2)
        surface.blit(im, im_loc)
        
    surface.blit(Title_im, Title_loc)
    
    pass


def Past(text, text_count, t1, dt, text_print, Question_count, img, mouse_pressed, Strike_count):
    global surface
    # Define the Past part of the game
    Question_info = [('When did these babies enter your life?', ['August 2019', 'October 2019', 'November 2019', 'December 2019'], 'August 2019'),
                     ('What theme park where you in?', ['Walibi', 'Efteling', 'Bobbejaanland', 'Six Flags'], 'Walibi'),
                     ('What country did you go skiing here?', ['France', 'Austria', 'Switzerland', 'Germany'], 'France'),
                     ('When did you start dating this angel?', ['21 January 2018','21 February 2018', '12 January 2018', '12 February 2018'], '12 January 2018'),
                     ('What city did you visit here?', ['Munich', 'Hamburg', 'Amsterdam', 'Berlin'], 'Berlin'),
                     ('Who died during this adventure?', ['Mustafa', 'Sadia', 'Sumant', 'Erik'], 'Sadia'),
                     ('What happened at this party?', ['Sumant threw up', 'Sadiarie was born', 'Mustafa hit on a 30-year old', 'Erik got some'], 'Sadiarie was born'),
                     ('What happened at this party?', ['Erik tore his pants and later passed out', 'Tim made out with a 30-year old', 'Sumant and Dani got into a club', 'Sadia and Stavrini made out'], 'Erik tore his pants and later passed out'),
                     ('Who created this great meme?', ['Mustafa', 'Stavrini', 'Sadia', 'Erik'], 'Stavrini'),
                     ('Who instantly regretted posting this online where it will last forever?', ['Sadia', 'Sumant', 'Erik', 'Mustafa'], 'Sumant'),
                     ('Where did you get a glimps of this "Tower"?', ['Sweden', 'Germany', 'Belgium', 'Norway'], 'Norway')]        
    newQ = False
    if text_print:
        text_count, t1 = Text_print(text, text_count, t1, dt)
    else:
        Ans, mouse_pressed = Show_Question(Question_count, img, Question_info[Question_count], mouse_pressed)
        Draw_Strike(Strike_count)
        if Ans != None:
            Result = Check_Answer(Ans, Question_info[Question_count])
            if Result:
                # Question_count = 10
                Question_count += 1
                newQ = True
                Right_Answer()
            else:
                Strike_count+=1
                Wrong_Answer(Strike=Strike_count)
                if Strike_count == 3:
                    Game_Over()
        
    return text_count, t1, Question_count, newQ, mouse_pressed, Strike_count
    

def Present(text, text_count, t1, dt, text_print, timer_start, timer_img, Riddle_Answer, Riddle_Ans):
    # Define the Present part of the game    
    correct_titles = 0    
    if text_print:
        text_count, t1 = Text_print(text, text_count, t1, dt)
    else:
        if Riddle_Ans != None:
            correct_titles = Check_Riddle_Ans(Riddle_Ans)
            if correct_titles != 2:
                Try_Again(correct_titles)
                # print('Nothing was right, try again')
            else:
                Right_Answer()
        else:
            Riddle(timer_start, timer_img, Riddle_Answer)

        
    return text_count, t1, correct_titles
    
    
def Future(text, text_count, t1, dt, text_print, Right_Count, Hint_Count, Hint_img, Question_count, mouse_pressed):
    # Define the Future part of the game
    
    Question_info = [('What is the current boy-to-girl ratio in the group?', ['6:7', '7:6', '8:5', '9:4'], '7:6'),
                     ('How many people here studied Aerospace Engineering?', ['Three', 'Four', 'Five', 'Six'], 'Five'),
                     ('How many people here studied/study in Amsterdam?', ['Two', 'Three', 'Four', 'Five'], 'Four'),
                     ('Who is the youngest of this group?', ['Naomi', 'Erik', 'Loebna', 'Stavrini'], 'Naomi'),
                     ('Who is the oldest of this group?', ['Mustafa', 'Sadia', 'Arie', 'Zahra'], 'Arie'),
                     ('How many internationals are in the group?', ['Four','Five','Six','Seven'], 'Four'),
                     ('How many people have roots in Asia (All of Asia)?', ['One', 'Two', 'Three', 'Four'], 'Four'),
                     ("How do you spell the name of Sumant's girlfriend?", ['Aksheja', 'Aksheya', 'Akshaya', 'Akshaja'], 'Akshaya'),
                     ('How many couples are currently present?', ['One', 'Two', 'Three', 'Four'], 'Three'),
                     ('How many people are single here?', ['One','Two','Three','Four'], 'Three'),
                     ('How many nationalities are represented?', ['Six', 'Five', 'Four', 'Three'], 'Three'),
                     ('Who is the greatest sibling one could ever have?', ['Erik', 'Erik', 'Erik', 'Erik'], 'Erik')]
    newH = False
    if text_print:
        text_count, t1 = Text_print(text, text_count, t1, dt)
    else:
        Show_hint(Hint_img, Hint_Count)
        Ans, mouse_pressed = Show_QuestionFuture(Question_count, Question_info[Question_count], mouse_pressed)
        if Ans != None:
            Result = Check_FutAns(Ans, Question_info[Question_count])
            Question_count += 1
            if Result:
                Right_Count += 1
                if (Right_Count-1) % 2 == 0:
                    Hint_Count += 1
                    newH = True
                    Answer(f'That was correct, you have earned Hint {Hint_Count}')
                else:
                    Answer('That was correct')
            else:
                Answer('No, be better if you want to see your gift')
        
    return text_count, t1, Right_Count, Hint_Count, Question_count, newH, mouse_pressed


def Final_words(text, text_count, t1, dt, text_print, Hint_count, HintFolder, HintFiles):
    # Enter Screen with final words to thank user for playing
    if text_print:
        text_count, t1 = Text_print(text, text_count, t1, dt)
    else:
        Last_Showing(Hint_count, HintFolder, HintFiles)
    
    return text_count, t1


def Draw_text(text):
    # Type string on the screen
    global surface
    
    lines = text.split('/n')
    Nlines = len(lines)
    font = pg.font.SysFont(None, 30)
    surface_w, surface_h = surface.get_size()
    for num, line in enumerate(lines):
        if len(line) != 0:
            if line[-1] == '/':
                line = line[:-1]
        img = font.render(line, True, (0, 0, 0))
        img_w, img_h = img.get_size()
        
        loc = (int(surface_w/2 - img_w /2), int(surface_h/2 - img_h * (0.5*Nlines - num)))
        
        surface.blit(img, loc)
    pass

def start_the_game(Name):
    global surface
    global mymenu
    global clock
    
    name = Name.get_value()
    mymenu.disable()
    mouse_pressed = False
    
    Level = 0
    
    Start_text = f'''Dear {name},/nSanta has been watching you closely for the last year./nI saw you've had a tough 2020 like many peers among you./nSadly, I've noticed you're losing your Christmas Spirit as a result./nThough the days may be shorter, the nights darker and the temperatures lower,/nChristmas is a time to forget about our sorrows and regrets,/nto be thankful for what we have and be hopeful about the future./n/nNormally, I would send my three helpers to help you remember the Christmas Spirit./nYet, due to the current COVID-19 restrictions, we'll be taking a different approach./nThis program was writen for self-service purposes./nYou'll be going through the past, present and future by yourself./nShould you pass these trials, the key to your reward (besides from the Christmas Spirit)/nshall be shown to you. Merry Christmas {name} and good luck. You will need it./n/nPress the 'enter' key to continue'''
    text_count = 0
    
    Past_text = "Hello, I am the digital spirit of the past, where you will start your journey./nI will help you remember what good things happened before 2020./n/nI will show you some photos and a question that goes with this photo./nYour job is to click on the right answers/n/nNormally I'd kill you if you gave the wrong answer, but since I am not here,/nI shall punish you in a different manner. You get three strikes. Don't use them all./n/nPress the 'enter' key to continue"
    Past_folder = './Past/'
    Past_files = ['Kitties.jpeg', 'Theme_Park.jpg', 'SkiSki.jpg', 'Beauty.jpg',
                  'Berlin.jpg', 'Party.jpg', 'Sadiarie.jpg', 'Rip_Erik.jpg',
                  'Mustafa.jpg', 'Regret.jpg', 'ErikJR.jpg']
    
    
    Present_text = f"Well done for passing the first trial, {name}./n I am the digital ghost of the present./n/nDO NOT BE FOOLED/nI am not the ghost of the time-present, but of the gift-present./nI have added two accesoires to your gift along the locked chest./nThese give a hint as to what gifts are inside./nIt will be your goal to decipher my riddle and guess what your gifts are./nYou are given 300 seconds and unlimited tries to complete it./n/nMay you succeed, you may continue to the last trial./nMay you fail, however, you might never see your gifts come to light./nGood luck/n/nPress the 'enter' key to continue"
    
    Future_text = f'''You've done well to come so far, {name}./nThis last trial shall decide if that was the Christmas Spirit or luck./nI am the digital ghost of the future./n/nWe have locked your gifts away and hid the key somewhere in your house./nBe not afraid as I only slightly carressed your face whilst you were asleep./nYou appear to sleep with your eyes open.../nAnyway I am rambling on. You will get a series of questions./nMay you succesfully pass this last trial,/nthe path to the key shall slowly reveal itself./n/nBe right and you shall be rewarded./nBe wrong and you may never be able to open your gift./nGood luck my son, the final trial awaits you./n/nPress the 'enter' key to continue'''
    Hint_folder = './Hints/'
    Hint_files = ['Hint1.PNG', 'Hint2.PNG', 'Hint3.PNG', 'Hint4.PNG', 'Hint5.PNG', 'Hint6.PNG', 'Finale.jpg']
    
    t1 = pg.time.get_ticks()
    dt = 0.01
    timer_start = None
    timer_img = pg.image.load('Timer.png')
    timer_img = timer_img.convert_alpha()
    text_print = None
    correct_titles = 0
    skip = True
    Strike_count = 0
    Hint_Count = 0
    Final_Text = None
    
    
    while True:
        draw_background()

        #-----------------------------------
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
                return
            if event.type == pg.MOUSEBUTTONDOWN:
                if Level == 3:
                    mouse_pressed = True
                if Level == 1:
                    mouse_pressed = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    if (Level == 4) & (text_print==True):
                        if text_count < len(Final_Text):
                            text_count = len(Final_Text)
                        else:
                            text_print = False
                    if (Level == 3) & (text_print==True):
                        if text_count < len(Future_text):
                            text_count = len(Future_text)
                        else:
                            text_print = False
                            timer_start = pg.time.get_ticks()
                    if (Level == 2) & (text_print==True) :
                        if text_count < len(Present_text):
                            text_count = len(Present_text)
                        else:
                            text_print = False
                            timer_start = pg.time.get_ticks()
                            Riddle_Answer = pg_textinput.TextInput(text_color=(255,255,255),
                                                                   cursor_color=(255,255,255),
                                                                   font_size=25)
                            skip = True
                            
                    if (Level == 1) & (text_print==True):
                        if text_count < len(Past_text):
                            text_count = len(Past_text)
                        else:
                            newQ = True
                            text_print = False
                    
                    if Level == 0:
                        if text_count < len(Start_text):
                            text_count = len(Start_text)
                        else:
                            Level += 1
                            text_count = 0
                            t1 = pg.time.get_ticks()
                            Question_count = 0
                            text_print = True
                            newQ = None
                            Past_img = None
        
        #Check if level one is passed
        if Level == 1:
            if Question_count == len(Past_files)-1:
                Question_count = 0
                Level += 1
                # correct_titles = 0
                Next_Level(['Great job, you have passed your first trial of the past', 'I shall take my leave now, yet your journey is far from over', f'Tread carefully {name}'])
                text_print = True
                text_count = 0
                t1 = pg.time.get_ticks()
                Riddle_Answer = None
                Riddle_Ans = None
                Strike_count = 0

                # Right_Count = 0
                # Hint_Count = 0
                # newH = False
                # # newQ = True
                # Future_img = None
                
                # Hint_Count = 3
                # newH = True
                # t1 = pg.time.get_ticks()
                # text_print = 0
                # text_count = 0
                # if Hint_Count < 3:
                #     Var_text = f'''I am extremely dissapointed, {name}/nYou have only earned yourself {Hint_Count} hint(s)./nGood luck searching your needle in a haystack./nYour Christmas Spirit flame is nearly out./n'''
                # elif Hint_Count < 6:
                #     Var_text = f'''I am dissapointed in you, {name}/nYou have earned a mediocre {Hint_Count} hints./n Though your search may be tough, it does not seem hopeless./nYour Christmas Spirit flame is burning sadly./n'''
                # else:
                #     Var_text = f'''You have done well and made me proud, {name}/nTo earn yourself a whopping {Hint_Count} hints will surely help your search./nYour Christmas spirit flame is burning strong and fiercely./n'''
                # Constant_text = "/n/nI'd like to thank you for participating in this Christmas Carol, {name}./nThough the challenges may be tough, I do hope you enjoyed the experience./nYou have been the first human on Earth to try out this sophisticated software./n/nLastly, I'd like to ask you to rate your experience on www.SantaClaus-DigiClaus.com/nYour feedback will only help us improve not just our customers, but also ourselves./n/nPress the 'enter' key to continue and view your hints."
                # Final_text = Var_text + Constant_text
                
        #Check if level two is passed
        elif Level == 2:
            if correct_titles == 2:
                Level += 1
                Next_Level(['You have done well to pass the second trial of the present', f'Your final challenge awaits you, {name}', 'I believe you can retrieve your Christmas Spirit'])
                text_print = True
                text_count = 0
                t1 = pg.time.get_ticks()
                Right_Count = 0
                Hint_Count = 0
                Question_count = 0
                newH = False
                # newQ = True
                Future_img = None
        #Check if level three is passed
        elif Level == 3:
            if Question_count == 11:
                Level+=1
                newH = True
                t1 = pg.time.get_ticks()
                text_print = True
                text_count = 0
                if Right_Count < 3:
                    Var_text = f'''I am extremely dissapointed, {name}/nYou have only earned yourself {Right_Count} hint(s)./nGood luck searching your needle in a haystack./nYour Christmas Spirit flame is nearly out./n'''
                elif Right_Count < 6:
                    Var_text = f'''I am dissapointed in you, {name}/nYou have earned a mediocre {Right_Count} hints./n Though your search may be tough, it does not seem hopeless./nYour Christmas Spirit flame is burning sadly./n'''
                else:
                    Var_text = f'''You have done well and made me proud, {name}/nTo earn yourself a whopping {Right_Count} hints will surely help your search./nYour Christmas spirit flame is burning strong and fiercely./n'''
                Constant_text = "/n/nI'd like to thank you for participating in this Christmas Carol, {name}./nThough the challenges may be tough, I do hope you enjoyed the experience./nYou have been the first human on Earth to try out this sophisticated software./n/nLastly, I'd like to ask you to rate your experience on www.SantaClaus-DigiClaus.com/nYour feedback will only help us improve not just our customers, but also ourselves./n/nPress the 'enter' key to continue and view your hints."
                Final_text = Var_text + Constant_text
                
        #Starting sequence
        if Level == 0:
            text_count, t1 = Text_print(Start_text, text_count, t1, dt)
            
        #Past sequence
        elif Level == 1:
            # print('We are in the Past')
            if newQ:
                Past_img = pg.image.load(Past_folder+Past_files[Question_count])
                newQ = False
        
            text_count, t1, Question_count, newQ, mouse_pressed, Strike_count = \
                    Past(Past_text, text_count, t1, dt, text_print,
                         Question_count, Past_img, mouse_pressed, Strike_count)
        
        #Present sequence
        elif Level == 2:
            # print('We are in the Present')
            if (text_print == False):
                Riddle_Ans = None
                if Riddle_Answer.update(events):
                    if not skip:
                        Riddle_Ans = Riddle_Answer.get_text()
                    else:
                        skip = False
                    Riddle_Answer.clear_text()
                
            text_count, t1, correct_titles = Present(Present_text, text_count, t1, dt, text_print,
                                     timer_start, timer_img, Riddle_Answer, Riddle_Ans)
        
        #Future sequence
        elif Level == 3:
            if newH:
                Future_img = pg.image.load(Hint_folder+Hint_files[Hint_Count-1])
                newH = False
            text_count, t1, Right_Count, Hint_Count, Question_count, newH, mouse_pressed \
                = Future(Future_text, text_count, t1, dt, text_print, Right_Count, Hint_Count, Future_img, Question_count, mouse_pressed)
        
        #Final sequence
        else:
            # if newH:
            #     Hint = pg.image.load(Hint_folder+Hint_files[Hint_Count-1])
            #     newH = False
            text_count, t1 = Final_words(Final_text, text_count, t1, dt, text_print, Hint_Count, Hint_folder, Hint_files)
        pg.display.flip()
        
    pass

def start_music():
    pg.mixer.music.load('christmas_music.mp3')
    pg.mixer.music.play(-1,0.0)

def draw_background():
    bg = pg.image.load('background.jpg')
    
    surface.blit(bg, (0,0))

def game_menu(surface):
    font = pg_menu.font.FONT_MUNRO
    # bg = pg_menu.baseimage.BaseImage('Background.jpg')
    size = surface.get_size()
    
    my_theme = pg_menu.themes.Theme(background_color = (0,0,0,100),
                                    title_bar_style=pg_menu.widgets.MENUBAR_STYLE_SIMPLE,
                                    menubar_close_button = False,
                                    title_background_color=(34,139,34),
                                    title_font = font,
                                    title_font_size = 50,
                                    title_font_color=(255,255,255),
                                    title_offset = (120,0),
                                    widget_font=font,
                                    widget_font_color=(240,240,240,50))
    menu = pg_menu.Menu(size[1]-300, size[0]-300, "Arie's Christmas Carol",
                        theme=my_theme)
    Name = menu.add_text_input('Name :', default='Arie Dedding')
    menu.add_button('Remember the Christmas Spirit', start_the_game, Name)
    menu.add_button('Maybe next year', pg_menu.events.EXIT)
    menu.center_content()
    
    return menu

# Main program
# def main():
    
pg.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'

bg_image = pg.image.load('background.jpg')
window = bg_image.get_size()
surface = pg.display.set_mode(window)

mymenu = game_menu(surface)

start_music()

def main_background():
    global surface
    draw_background()

# Game Loop
loop = True
while loop:
    
    draw_background()
    
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
            break
            
    mymenu.mainloop(surface,main_background,fps_limit=60)
        
    pg.display.flip()
    

pg.quit()