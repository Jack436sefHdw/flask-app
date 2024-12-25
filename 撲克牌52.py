from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import random
import time

def load_images():
    """加载所有卡片图片并存储在字典中"""
    suits = ["心", "桃", "菱", "梅"]
    images = {}
    for suit in suits:
        for number in range(1, 14):  # 1-13号卡片
            file_name = f"{suit}{number}.png"
            print(file_name)
            images[f"{suit}{number}"] = PhotoImage(file=file_name)
    return images

def update_timer():
    global start_time, lab1, matched_pairs, card_values

    if start_time is not None and matched_pairs < len(card_values) // 2:
        elapsed_time = int(time.time() - start_time)
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        lab1.config(text=f"計時配對時間:{minutes}:{seconds:02}")
        root.after(1000, update_timer)
    elif matched_pairs == len(card_values) // 2:
        elapsed_time = int(time.time() - start_time)
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        lab1.config(text=f"總時間:{minutes}:{seconds:02}")

def flip_card(btn, card_index):
    global first_card, second_card, buttons, card_values, matched_pairs, flip_count

    if btn.image_shown:
        return

    btn.config(image=images[card_values[card_index]])
    btn.image_shown = True
    flip_count += 1
    lab2.config(text=f"計算翻牌次數:{flip_count}")

    if first_card is None:
        first_card = (btn, card_index)
        print(card_values[first_card[1]])
    elif second_card is None:
        second_card = (btn, card_index)
        print(card_values[second_card[1]])
        root.update()
        time.sleep(0.5)

        # 只检查数字部分是否相同
        first_card_value = int(card_values[first_card[1]][1:])  # 取数字部分
        second_card_value = int(card_values[second_card[1]][1:])  # 取数字部分

        if first_card_value == second_card_value:
            matched_pairs += 1
            first_card[0]["state"] = "disabled"
            second_card[0]["state"] = "disabled"
        else:
            first_card[0].config(image=back_image)
            first_card[0].image_shown = False
            second_card[0].config(image=back_image)
            second_card[0].image_shown = False

        first_card = None
        second_card = None

        if matched_pairs == len(card_values) // 2:
            messagebox.showinfo("恭喜", f"你贏了！總翻牌次數：{flip_count}")

def start_game():
    global buttons, card_values, matched_pairs, flip_count, start_time, first_card, second_card

    buttons = []
    first_card = None
    second_card = None
    matched_pairs = 0
    flip_count = 0
    start_time = time.time()

    lab1.config(text="計時配對時間:0:00")
    lab2.config(text="計算翻牌次數:0")
    clear_frame(fr2)

    card_values = random.sample([f"{suit}{number}" for suit in ["心", "桃", "菱", "梅"] for number in range(1, 14)], 52)
    print(card_values)
    random.shuffle(card_values)

    closest_factors = (4, 13)  # Adjust based on card count or make it dynamic

    for i in range(closest_factors[0]):
        for j in range(closest_factors[1]):
            idx = i * closest_factors[1] + j
            btn = Button(fr2, image=back_image, command=lambda b=idx: flip_card(buttons[b], b))
            btn.grid(row=i, column=j, padx=5, pady=5)
            btn.image_shown = False
            buttons.append(btn)

    update_timer()

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

root = Tk()
root.title("卡片配對遊戲")
root.geometry("800x600")

images = load_images()
back_image = PhotoImage(file="back.png")

# Global variables
first_card = None
second_card = None
matched_pairs = 0
flip_count = 0
start_time = None
buttons = []

frame1 = Frame(root)
frame1.pack(fill="x")
Label(frame1, text="卡牌數量 (偶數，2-52):").pack(side="left", padx=10)
entry = Entry(frame1)
entry.pack(side="left")

start_btn = Button(frame1, text="開始", command=start_game)
start_btn.pack(side="left", padx=10)

lab1 = Label(frame1, text="計時配對時間:0:00")
lab1.pack(side="right", padx=10)
lab2 = Label(frame1, text="計算翻牌次數:0")
lab2.pack(side="right", padx=10)

fr2 = Frame(root)
fr2.pack()

root.mainloop()
