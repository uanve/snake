import tkinter as tk
from random import randint
from PIL import Image, ImageTk


MOVE_INCREMENT = 20
MOVES_PER_SECOND = 1000
GAME_SPEED = 1000 // MOVES_PER_SECOND

moves = ['Down','Right', 'Down','Right', 'Down','Right']


class Snake(tk.Canvas):
    def __init__(self):
        super().__init__(
            width=600, height=620, background="black", highlightthickness=0
        )

        self.snake_positions = [(100, 100), (80, 100), (60, 100)]
        self.food_position = self.set_new_food_position()
        self.direction = "Right"
        self.i = 0

        self.score = 0

        self.load_assets()
        self.create_objects()

        self.bind_all("<Key>", self.on_key_press)

        self.pack()

        self.after(GAME_SPEED, self.perform_actions)

    def load_assets(self):
        try:
            self.snake_body_image = Image.open("./assets/snake.png")
            self.snake_body = ImageTk.PhotoImage(self.snake_body_image)

            self.food_image = Image.open("./assets/food.png")
            self.food = ImageTk.PhotoImage(self.food_image)
        except IOError as error:
            root.destroy()
            raise

    def create_objects(self):
        self.create_text(
            35, 12, text=f"Score: {self.score}", tag="score", fill="#fff", font=10
        )

        for x_position, y_position in self.snake_positions:
            self.create_image(
                x_position, y_position, image=self.snake_body, tag="snake"
            )

        self.create_image(*self.food_position, image=self.food, tag="food")
        self.create_rectangle(7, 27, 593, 613, outline="#525d69")


    def check_collisions(self):
        head_x_position, head_y_position = self.snake_positions[0]

        return (
            # head_x_position in (0, 600)
            # or head_y_position in (20, 620)
            # or 
            (head_x_position, head_y_position) in self.snake_positions[1:]
        )

    def check_food_collision(self):
        if self.snake_positions[0] == self.food_position:
            self.score += 1
            self.snake_positions.append(self.snake_positions[-1])

            self.create_image(
                *self.snake_positions[-1], image=self.snake_body, tag="snake"
            )
            self.food_position = self.set_new_food_position()
            self.coords(self.find_withtag("food"), *self.food_position)

            score = self.find_withtag("score")
            self.itemconfigure(score, text=f"Score: {self.score}", tag="score")

    def end_game(self):
        self.delete(tk.ALL)
        self.create_text(
            self.winfo_width() / 2,
            self.winfo_height() / 2,
            text=f"Game over! You scored {self.score}!",
            fill="#fff",
            font=14
        )

    def move_snake(self):
        head_x_position, head_y_position = self.snake_positions[0]

        if self.direction == "Left":
            if head_x_position == 20:
                new_head_position = (580, head_y_position)
            else:
                new_head_position = (head_x_position - MOVE_INCREMENT, head_y_position)

        elif self.direction == "Right":
            if head_x_position == 580:
                new_head_position = (20, head_y_position)
            else:
                new_head_position = (head_x_position + MOVE_INCREMENT, head_y_position)

        elif self.direction == "Down":
            if head_y_position==600:
                new_head_position = (head_x_position, 40)
            else:
                new_head_position = (head_x_position, head_y_position + MOVE_INCREMENT)
        elif self.direction == "Up":
            if head_y_position == 40:
                new_head_position = (head_x_position, 600)
            else:
                new_head_position = (head_x_position, head_y_position - MOVE_INCREMENT)

        self.snake_positions = [new_head_position] + self.snake_positions[:-1]

        for segment, position in zip(self.find_withtag("snake"), self.snake_positions):
            self.coords(segment, position)

    def on_key_press(self, e):
        new_direction = e.keysym

        all_directions = ("Up", "Down", "Left", "Right")
        opposites = ({"Up", "Down"}, {"Left", "Right"})

        if (
            new_direction in all_directions
            and {new_direction, self.direction} not in opposites
        ):
            self.direction = new_direction

    def next_move(self):
        # new_direction = moves[self.i]
        # self.i+=1
        # self.direction = new_direction

        head_x_position, head_y_position = self.snake_positions[0]

        if (head_x_position,head_y_position) == (580,580):
            self.direction = 'Up'
        
        elif (head_x_position,head_y_position) == (580,40):
            self.direction = 'Left'

        elif (self.direction == 'Left') and head_x_position == 20:
            self.direction = 'Down'
        
        elif (self.direction == 'Down') and head_x_position == 20:
            self.direction = 'Right'

        elif 60 <= head_y_position <=560: 
            if (self.direction == 'Right') and head_x_position == 560:
                self.direction = 'Down'
            
            elif (self.direction == 'Down') and head_x_position == 560:
                self.direction = 'Left'

        


    def perform_actions(self):
        if self.check_collisions():
            self.end_game()

        self.next_move()
        self.check_food_collision()
        self.move_snake()

        self.after(GAME_SPEED, self.perform_actions)

    def set_new_food_position(self):
        while True:
            x_position = randint(1, 29) * MOVE_INCREMENT
            y_position = randint(3, 29) * MOVE_INCREMENT
            food_position = (x_position, y_position)

            if food_position not in self.snake_positions:
                return food_position



root = tk.Tk()
root.title("Snake")
root.resizable(False, False)
root.tk.call("tk", "scaling", 4.0)

board = Snake()

root.mainloop()