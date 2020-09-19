# Import libraries
from tkinter import Tk, Menu, Canvas, mainloop
import tkinter as tk, json, cv2, os, numpy as np, random, time, keyboard
from PIL import Image, ImageTk

class NFS():
    def __init__(self, gui, score_json_path):

        # Additional variable
        # Time variables
        self.start_time = time.time()
        self.t = 25
        self.mp = 1
        self.b = 0

        # Distance control variables
        self.road = 10
        self.x_dir = 0
        self.y_dir = 0

        # Scoring variables
        self.cur_score = 0
        self.score_json_path = score_json_path
        with open(self.score_json_path, 'r') as file:
            self.json_data = json.load(file)
            self.highest_score = self.json_data["Highest_Score"]
        
        # Canvas initialization
        self.canvas_center = Canvas(gui, width = 366, height = 768, bg='gray')
        self.canvas_left = Canvas(gui, width = 500, height = 768, bg='green')
        self.canvas_right = Canvas(gui, width = 500, height = 768, bg='green')

        # Road divider
        self.divider_0 = self.canvas_center.create_rectangle(150, -282.5, 170, -169.5, fill="white")
        self.divider_1 = self.canvas_center.create_rectangle(150, -56.5, 170, 56.5, fill="white")
        self.divider_2 = self.canvas_center.create_rectangle(150, 169.5, 170, 282.5, fill="white")
        self.divider_3 = self.canvas_center.create_rectangle(150, 395.5, 170, 508.5, fill="white")
        self.divider_4 = self.canvas_center.create_rectangle(150, 621.5, 170, 734.5, fill="white")

        # Car initialization
        raw_img = Image.open(os.path.join(os.path.expanduser('~'), "Personal_folder", "Knowledge", "Program_files", "Python", "Games", "images", "rsz_F1.png"))
        raw_car = ImageTk.PhotoImage(raw_img)
        self.canvas_center.image = raw_car
        self.raw_car = raw_car
        self.car = self.canvas_center.create_image(183, 500, image = raw_car)

        # Creating road limit (left)
        self.block_left = self.canvas_left.create_rectangle(400, 0, 500, 768, fill="black")
        self.block_left_0 = self.canvas_left.create_rectangle(400, -200, 500, -150, fill="red")
        self.block_left_1 = self.canvas_left.create_rectangle(400, -100, 500, -50, fill="red")
        self.block_left_2 = self.canvas_left.create_rectangle(400, 0, 500, 50, fill="red")
        self.block_left_3 = self.canvas_left.create_rectangle(400, 100, 500, 150, fill="red")
        self.block_left_4 = self.canvas_left.create_rectangle(400, 200, 500, 250, fill="red")
        self.block_left_5 = self.canvas_left.create_rectangle(400, 300, 500, 350, fill="red")
        self.block_left_6 = self.canvas_left.create_rectangle(400, 400, 500, 450, fill="red")
        self.block_left_7 = self.canvas_left.create_rectangle(400, 500, 500, 550, fill="red")
        self.block_left_8 = self.canvas_left.create_rectangle(400, 600, 500, 650, fill="red")
        self.block_left_9 = self.canvas_left.create_rectangle(400, 700, 500, 750, fill="red")
        self.block_left_10 = self.canvas_left.create_rectangle(400, 800, 500, 850, fill="red")

        # Creating road limit (right)
        self.block_right = self.canvas_right.create_rectangle(0, 0, 100, 768, fill="black")
        self.block_right_0 = self.canvas_right.create_rectangle(0, -200, 100, -150, fill="red")
        self.block_right_1 = self.canvas_right.create_rectangle(0, -100, 100, -50, fill="red")
        self.block_right_2 = self.canvas_right.create_rectangle(0, 0, 100, 50, fill="red")
        self.block_right_3 = self.canvas_right.create_rectangle(0, 100, 100, 150, fill="red")
        self.block_right_4 = self.canvas_right.create_rectangle(0, 200, 100, 250, fill="red")
        self.block_right_5 = self.canvas_right.create_rectangle(0, 300, 100, 350, fill="red")
        self.block_right_6 = self.canvas_right.create_rectangle(0, 400, 100, 450, fill="red")
        self.block_right_7 = self.canvas_right.create_rectangle(0, 500, 100, 550, fill="red")
        self.block_right_8 = self.canvas_right.create_rectangle(0, 600, 100, 650, fill="red")
        self.block_right_9 = self.canvas_right.create_rectangle(0, 700, 100, 750, fill="red")
        self.block_right_10 = self.canvas_right.create_rectangle(0, 800, 100, 850, fill="red")

        # Text initialization
        self.text = self.canvas_left.create_text(100,50,font="Times 20 italic bold", text = "Score: {}\nHighest score: {}".format(self.cur_score, self.highest_score))

        # Road Block
        x = random.randint(30, 300)
        self.block = self.canvas_center.create_image(x, 50, image = raw_car)

        # Packing up
        self.canvas_left.pack(side=tk.LEFT)
        self.canvas_right.pack(side=tk.RIGHT)
        self.canvas_center.pack()
        self.move_road()

    def move_road(self):
        # Road Automation
        cur_time = time.time()
        _, _, _, yr2 = self.canvas_left.bbox(self.block_left_0)
        _, _, _, yl2 = self.canvas_left.bbox(self.block_left_10)
        _, _, _, yd2 = self.canvas_center.bbox(self.divider_0)
        xc1, yc1, xc2, yc2 = self.canvas_center.bbox(self.car)
        xb1, yb1, xb2, yb2 = self.canvas_center.bbox(self.block)
        if yd2 <= 56:
            self.canvas_center.move(self.divider_0, 0, self.road)
            self.canvas_center.move(self.divider_1, 0, self.road)
            self.canvas_center.move(self.divider_2, 0, self.road)
            self.canvas_center.move(self.divider_3, 0, self.road)
            self.canvas_center.move(self.divider_4, 0, self.road)
        else:
            self.canvas_center.move(self.divider_0, 0, self.road-226)
            self.canvas_center.move(self.divider_1, 0, self.road-226)
            self.canvas_center.move(self.divider_2, 0, self.road-226)
            self.canvas_center.move(self.divider_3, 0, self.road-226)
            self.canvas_center.move(self.divider_4, 0, self.road-226)
        if yr2 <= 49 and yl2 >= 650:
            self.canvas_left.move(self.block_left_0, 0, self.road)
            self.canvas_left.move(self.block_left_1, 0, self.road)
            self.canvas_left.move(self.block_left_2, 0, self.road)
            self.canvas_left.move(self.block_left_3, 0, self.road)
            self.canvas_left.move(self.block_left_4, 0, self.road)
            self.canvas_left.move(self.block_left_5, 0, self.road)
            self.canvas_left.move(self.block_left_6, 0, self.road)
            self.canvas_left.move(self.block_left_7, 0, self.road)
            self.canvas_left.move(self.block_left_8, 0, self.road)
            self.canvas_left.move(self.block_left_9, 0, self.road)
            self.canvas_left.move(self.block_left_10, 0, self.road)
            self.canvas_right.move(self.block_right_0, 0, self.road)
            self.canvas_right.move(self.block_right_1, 0, self.road)
            self.canvas_right.move(self.block_right_2, 0, self.road)
            self.canvas_right.move(self.block_right_3, 0, self.road)
            self.canvas_right.move(self.block_right_4, 0, self.road)
            self.canvas_right.move(self.block_right_5, 0, self.road)
            self.canvas_right.move(self.block_right_6, 0, self.road)
            self.canvas_right.move(self.block_right_7, 0, self.road)
            self.canvas_right.move(self.block_right_8, 0, self.road)
            self.canvas_right.move(self.block_right_9, 0, self.road)
            self.canvas_right.move(self.block_right_10, 0, self.road)
            self.canvas_center.move(self.car, self.x_dir, self.y_dir)
            self.canvas_center.move(self.block, 0, self.road - 5)
            self.canvas_left.itemconfigure(self.text, text="Score: {}\nRecent score: {}\nHighest score: {}".format(self.cur_score, self.b, self.highest_score))
            
        elif yr2 >= 50:
            self.canvas_left.move(self.block_left_0, 0, self.road-100)
            self.canvas_left.move(self.block_left_1, 0, self.road-100)
            self.canvas_left.move(self.block_left_2, 0, self.road-100)
            self.canvas_left.move(self.block_left_3, 0, self.road-100)
            self.canvas_left.move(self.block_left_4, 0, self.road-100)
            self.canvas_left.move(self.block_left_5, 0, self.road-100)
            self.canvas_left.move(self.block_left_6, 0, self.road-100)
            self.canvas_left.move(self.block_left_7, 0, self.road-100)
            self.canvas_left.move(self.block_left_8, 0, self.road-100)
            self.canvas_left.move(self.block_left_9, 0, self.road-100)
            self.canvas_left.move(self.block_left_10, 0, self.road-100)
            self.canvas_right.move(self.block_right_0, 0, self.road-100)
            self.canvas_right.move(self.block_right_1, 0, self.road-100)
            self.canvas_right.move(self.block_right_2, 0, self.road-100)
            self.canvas_right.move(self.block_right_3, 0, self.road-100)
            self.canvas_right.move(self.block_right_4, 0, self.road-100)
            self.canvas_right.move(self.block_right_5, 0, self.road-100)
            self.canvas_right.move(self.block_right_6, 0, self.road-100)
            self.canvas_right.move(self.block_right_7, 0, self.road-100)
            self.canvas_right.move(self.block_right_8, 0, self.road-100)
            self.canvas_right.move(self.block_right_9, 0, self.road-100)
            self.canvas_right.move(self.block_right_10, 0, self.road-100)
            self.canvas_center.move(self.car, self.x_dir, self.y_dir)
            self.canvas_center.move(self.block, 0, self.road - 5)
            self.canvas_left.itemconfigure(self.text, text="Score: {}\nRecent score: {}\nHighest score: {}".format(self.cur_score, self.b, self.highest_score))
            
        if (yb2 >= yc1 and yb1 <= yc2 and xb1 <= xc2 and xb2 >= xc1) or (yb2 >= yc1 and yb1 <= yc2 and xb2 <= xc1 and xb1 >= xc2):
            self.canvas_left.move(self.block_left_0, 0, 0)
            self.canvas_left.move(self.block_left_1, 0, 0)
            self.canvas_left.move(self.block_left_2, 0, 0)
            self.canvas_left.move(self.block_left_3, 0, 0)
            self.canvas_left.move(self.block_left_4, 0, 0)
            self.canvas_left.move(self.block_left_5, 0, 0)
            self.canvas_left.move(self.block_left_6, 0, 0)
            self.canvas_left.move(self.block_left_7, 0, 0)
            self.canvas_left.move(self.block_left_8, 0, 0)
            self.canvas_left.move(self.block_left_9, 0, 0)
            self.canvas_left.move(self.block_left_10, 0, 0)
            self.canvas_right.move(self.block_right_0, 0, 0)
            self.canvas_right.move(self.block_right_1, 0, 0)
            self.canvas_right.move(self.block_right_2, 0, 0)
            self.canvas_right.move(self.block_right_3, 0, 0)
            self.canvas_right.move(self.block_right_4, 0, 0)
            self.canvas_right.move(self.block_right_5, 0, 0)
            self.canvas_right.move(self.block_right_6, 0, 0)
            self.canvas_right.move(self.block_right_7, 0, 0)
            self.canvas_right.move(self.block_right_8, 0, 0)
            self.canvas_right.move(self.block_right_9, 0, 0)
            self.canvas_right.move(self.block_right_10, 0, 0)
            self.canvas_center.move(self.car, 0, 0)
            self.x_dir = 0
            self.y_dir = 0
            self.road = 10
            if self.cur_score > self.highest_score:
                self.json_data["Highest_Score"] = self.cur_score
                with open(self.score_json_path, 'w') as file:
                    json.dump(self.json_data, file, indent=4)
            with open(self.score_json_path, 'r') as file:
                self.json_data = json.load(file)
                self.highest_score = self.json_data["Highest_Score"]
            self.b = self.cur_score
            self.cur_score = 0
            self.mp = 1
            self.obstacle()
            self.start_time = time.time()
            self.canvas_left.itemconfigure(self.text, text="Score: {}\nRecent score: {}\nHighest score: {}".format(self.cur_score, self.b, self.highest_score))
            
        elif xc1 <= 0:
            self.canvas_left.move(self.block_left_0, 0, 0)
            self.canvas_left.move(self.block_left_1, 0, 0)
            self.canvas_left.move(self.block_left_2, 0, 0)
            self.canvas_left.move(self.block_left_3, 0, 0)
            self.canvas_left.move(self.block_left_4, 0, 0)
            self.canvas_left.move(self.block_left_5, 0, 0)
            self.canvas_left.move(self.block_left_6, 0, 0)
            self.canvas_left.move(self.block_left_7, 0, 0)
            self.canvas_left.move(self.block_left_8, 0, 0)
            self.canvas_left.move(self.block_left_9, 0, 0)
            self.canvas_left.move(self.block_left_10, 0, 0)
            self.canvas_right.move(self.block_right_0, 0, 0)
            self.canvas_right.move(self.block_right_1, 0, 0)
            self.canvas_right.move(self.block_right_2, 0, 0)
            self.canvas_right.move(self.block_right_3, 0, 0)
            self.canvas_right.move(self.block_right_4, 0, 0)
            self.canvas_right.move(self.block_right_5, 0, 0)
            self.canvas_right.move(self.block_right_6, 0, 0)
            self.canvas_right.move(self.block_right_7, 0, 0)
            self.canvas_right.move(self.block_right_8, 0, 0)
            self.canvas_right.move(self.block_right_9, 0, 0)
            self.canvas_right.move(self.block_right_10, 0, 0)
            self.canvas_center.move(self.car, self.x_dir+175, 0)
            self.x_dir = 0
            self.y_dir = 0
            self.road = 10
            if self.cur_score > self.highest_score:
                self.json_data["Highest_Score"] = self.cur_score
                with open(self.score_json_path, 'w') as file:
                    json.dump(self.json_data, file, indent=4)
            with open(self.score_json_path, 'r') as file:
                self.json_data = json.load(file)
                self.highest_score = self.json_data["Highest_Score"]
            self.b = self.cur_score
            self.cur_score = 0
            self.start_time = time.time()
            self.mp = 1
            #self.obstacle()
            self.canvas_left.itemconfigure(self.text, text="Score: {}\nRecent score: {}\nHighest score: {}".format(self.cur_score, self.b, self.highest_score))
            
        elif xc2 >= 366:
            self.canvas_left.move(self.block_left_0, 0, 0)
            self.canvas_left.move(self.block_left_1, 0, 0)
            self.canvas_left.move(self.block_left_2, 0, 0)
            self.canvas_left.move(self.block_left_3, 0, 0)
            self.canvas_left.move(self.block_left_4, 0, 0)
            self.canvas_left.move(self.block_left_5, 0, 0)
            self.canvas_left.move(self.block_left_6, 0, 0)
            self.canvas_left.move(self.block_left_7, 0, 0)
            self.canvas_left.move(self.block_left_8, 0, 0)
            self.canvas_left.move(self.block_left_9, 0, 0)
            self.canvas_left.move(self.block_left_10, 0, 0)
            self.canvas_right.move(self.block_right_0, 0, 0)
            self.canvas_right.move(self.block_right_1, 0, 0)
            self.canvas_right.move(self.block_right_2, 0, 0)
            self.canvas_right.move(self.block_right_3, 0, 0)
            self.canvas_right.move(self.block_right_4, 0, 0)
            self.canvas_right.move(self.block_right_5, 0, 0)
            self.canvas_right.move(self.block_right_6, 0, 0)
            self.canvas_right.move(self.block_right_7, 0, 0)
            self.canvas_right.move(self.block_right_8, 0, 0)
            self.canvas_right.move(self.block_right_9, 0, 0)
            self.canvas_right.move(self.block_right_10, 0, 0)
            self.canvas_center.move(self.car, self.x_dir-175, 0)
            self.x_dir = 0
            self.y_dir = 0
            self.road = 10
            if self.cur_score > self.highest_score:
                self.json_data["Highest_Score"] = self.cur_score
                with open(self.score_json_path, 'w') as file:
                    json.dump(self.json_data, file, indent=4)
            with open(self.score_json_path, 'r') as file:
                self.json_data = json.load(file)
                self.highest_score = self.json_data["Highest_Score"]
            self.b = self.cur_score
            self.cur_score = 0
            self.mp = 1
            #self.obstacle()
            self.start_time = time.time()
            self.canvas_left.itemconfigure(self.text, text="Score: {}\nRecent score: {}\nHighest score: {}".format(self.cur_score, self.b, self.highest_score))
            
        if yb1 >=700:
            self.cur_score += 1
            self.obstacle()
        if cur_time - self.start_time >=10:
            if self.road <= 30:
                self.road += 3
            self.start_time = time.time()
        self.canvas_center.after(self.t, self.move_road)

    def obstacle(self):
        x = random.randint(30, 300)
        self.canvas_center.coords(self.block, x, -30)
    
    def accelaration(self, event):
        self.y_dir = self.y_dir - 3

    def brake(self, event):
        self.y_dir = self.y_dir + 3

    def right(self, event):
        self.x_dir = self.x_dir + self.road * .5

    def left(self, event):
        self.x_dir = self.x_dir - self.road * .5



if __name__ == "__main__": 
  
    # object of class Tk, resposible for creating 
    # a tkinter toplevel window
    master = Tk()
    master.title("Need For Speed")
    master.geometry("1366x768")
    score_json_path = os.path.join(os.path.expanduser('~'), "Personal_folder", "Knowledge", "Program_files", "Python", "Games", "score.json")
    game = NFS(master, score_json_path)

    # This will bind arrow keys to the tkinter 
    # toplevel which will navigate the image or drawing 
    master.bind("<KeyPress-Up>", lambda e: game.accelaration(e)) 
    master.bind("<KeyPress-Down>", lambda e: game.brake(e))
    master.bind("<KeyPress-Left>", lambda e: game.left(e))
    master.bind("<KeyPress-Right>", lambda e: game.right(e))

    # Infnite loop breaks only by interrupt
    mainloop()