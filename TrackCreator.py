#Track generator

import tkinter as tk
import numpy as np
from scipy.interpolate import splprep, splev
import matplotlib.pyplot as plt
window_Width = 700
window_Height = 700
DotSize = 10
class Example(tk.Frame):
    '''Illustrate how to drag items on a Tkinter canvas'''

    def __init__(self, parent):

        tk.Frame.__init__(self, parent)

        # create a canvas

        self.canvas = tk.Canvas(width=window_Width, height=window_Height,background="blue")
        self.canvas.pack(side=tk.LEFT)
        self.Track = tk.PhotoImage(width=1, height=1)
        self.w = tk.Label(root,image=self.Track,width=window_Width, height=window_Height, bg="red", fg="white")
        self.w.pack(side=tk.RIGHT)
        # this data is used to keep track of an 
        # item being dragged
        self._drag_data = {"x": 0, "y": 0, "item": None}
        self.points=[350, 350]
        # create a couple of movable objects

        self.canvas.create_polygon(window_Width/2, window_Height/2, window_Width/2, 100, outline="black",fill='',width=15, tags="line")
        self.canvas.create_polygon(window_Width/2, window_Height/2, window_Width/2, 100, outline="white",fill='',width=10, tags="line2")
        
        self.canvas.create_oval(window_Width/2-1, window_Height/2-1, window_Width/2+1, window_Height/2+1,outline="red", fill='black')
        self.canvas.create_text(window_Width/2, window_Height/2, fill="red", text="▲")


        self.canvas.create_rectangle(window_Width-60, 0, window_Width, 25, tags="button1", fill='red')
        self.canvas.create_text(window_Width-30, 15, tags="button1", text="Add Point")

        self.canvas.create_rectangle(window_Width-60, 30, window_Width, 55, tags="button2", fill='green')
        self.canvas.create_text(window_Width-30, 45, tags="button2", text="Export")


        self._create_token((window_Width/2, 15), "red")
        
        # add bindings for clicking, dragging and releasing over
        # any object with the "token" tag
        self.canvas.tag_bind("token", "<ButtonPress-1>", self.on_token_press)
        self.canvas.tag_bind("token", "<ButtonRelease-1>", self.on_token_release)
        self.canvas.tag_bind("token", "<B1-Motion>", self.on_token_motion)
        self.canvas.tag_bind("button1", "<ButtonPress-1>", self.on_button_press)
        self.canvas.tag_bind("button2", "<ButtonPress-1>", self.on_button_press2)

    def _create_token(self, coord, color):
        '''Create a token at the given coordinate in the given color'''
        (x,y) = coord
        self.canvas.create_oval(x-DotSize, y-DotSize, x+DotSize, y+DotSize, 
                                outline="red", fill=color, tags="token")

    def on_token_press(self, event):
        '''Begining drag of an object'''
        # record the item and its location
        self._drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def on_button_press(self, event):
        '''Begining drag of an object'''
        # record the item and its location
        # self.canvas.postscript(file="file_name.ps", colormode='color')
        self._create_token((window_Width/2, 10), "red")
        print("Click")

    def on_button_press2(self, event):
        '''Begining drag of an object'''
        # record the item and its location
        print("EXPORTING")
        pts = np.reshape(np.array(self.points), (-1, 2))
        print(pts)
        tck, u = splprep(pts.T, u=None, s=0.0, per=1) 
        u_new = np.linspace(u.min(), u.max(), 10000)
        x_new, y_new = splev(u_new, tck, der=0)
        plt.axis([0, window_Width, 0, window_Height])
        plt.gca().set_aspect('equal', adjustable='box')
        plt.plot(350,350,marker='o',color='silver')
        plt.plot(x_new, y_new,c='black', linewidth=4.0)
        plt.plot(x_new, y_new,c='white', linewidth=3.0)
        #Center Lane
        #plt.plot(x_new, y_new,c='black', ls='dashed',linewidth=0.25)
        plt.axis('off')
        plt.gca().invert_yaxis()
        plt.savefig('track.png', bbox_inches='tight', dpi=1500)
        plt.clf()
        self.Track = tk.PhotoImage(file="track.png").subsample(9)
        self.w.configure(image=self.Track)
        #plt.show()
        print("SAVED")

    def on_token_release(self, event):
        '''End drag of an object'''
        # reset the drag information
        self._drag_data["item"] = None
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0

    def on_token_motion(self, event):
        '''Handle dragging of an object'''
        # compute how much the mouse has moved
        delta_x = event.x - self._drag_data["x"]
        delta_y = event.y - self._drag_data["y"]
        # move the object the appropriate amount
        self.canvas.move(self._drag_data["item"], delta_x, delta_y)
        # record the new position
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y
        tic_tags = self.canvas.find_withtag("token")
        self.points = [window_Width/2,window_Height/2]
        for tag in tic_tags:
            
            #points.extend(self.canvas.coords(tag)[:2])
            self.points.extend([x + y for x, y in zip(self.canvas.coords(tag)[:2], [DotSize,DotSize])])
        l = self.canvas.find_withtag("line")
        self.canvas.coords(l,self.points)
        l = self.canvas.find_withtag("line2")
        self.canvas.coords(l,self.points)
if __name__ == "__main__":
    root = tk.Tk()
    Example(root).pack(fill="both", expand=True)
    root.mainloop()