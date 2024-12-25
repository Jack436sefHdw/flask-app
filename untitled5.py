from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import random
import time

def load_images():
    global images
    """加载所有卡片图片并存储在字典中"""
    suits = ["心", "桃", "菱", "梅"]
    images = {}
    for suit in suits:
        for number in range(1, 14):  # 1-13号卡片
            file_name = f"{suit}{number}.png"
            try:
                images[f"{suit}{number}"] = PhotoImage(file=file_name)
            except Exception as e:
                print(f"Error loading image {file_name}: {e}")
    # 加載新卡牌圖片
    # images["醜0"] = PhotoImage(file="醜0.png")
    # images["丑0"] = PhotoImage(file="丑0.png")
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
    global first_card, second_card, buttons, card_values, matched_pairs, flip_count, is_flipping

    # Return if the card is already shown or if another match is being checked
    if btn.image_shown or is_flipping:
        return

    btn.config(image=images[card_values[card_index]])
    btn.image_shown = True
    flip_count += 1
    lab2.config(text=f"計算翻牌次數:{flip_count}")

    if first_card is None:
        first_card = (btn, card_index)
    elif second_card is None:
        second_card = (btn, card_index)
        is_flipping = True  # Set the flipping state to True
        root.after(500, check_match)  # 延遲檢查匹配

def check_match():
    global first_card, second_card, buttons, card_values, matched_pairs, is_flipping

    first_card_value = card_values[first_card[1]][1:]
    second_card_value = card_values[second_card[1]][1:]

    if first_card_value == second_card_value:
        matched_pairs += 1
        first_card[0]["state"] = "disabled"
        second_card[0]["state"] = "disabled"
    else:
        # Flip back the cards
        first_card[0].config(image=back_image)
        first_card[0].image_shown = False
        second_card[0].config(image=back_image)
        second_card[0].image_shown = False

    # Reset cards and allow new moves
    first_card = None
    second_card = None

    # Unset the flipping state
    is_flipping = False

    # Check if the game is won
    if matched_pairs == len(card_values) // 2:
        messagebox.showinfo("恭喜", f"你贏了！總翻牌次數：{flip_count}")

def start_game():
    global buttons, card_values, matched_pairs, flip_count, start_time, first_card, second_card, is_flipping,images,back_image

    images = load_images()
    back_image = PhotoImage(file="back.png")

    # Global variables
    first_card = None
    second_card = None
    matched_pairs = 0
    flip_count = 0
    start_time = None
    buttons = []
    start_time = time.time()
    is_flipping = False

    lab1.config(text="計時配對時間:0:00")
    lab2.config(text="計算翻牌次數:0")
    clear_frame(fr2)
    clear_frame(fr3)

    # 增加兩張特殊卡牌 "醜0" 和 "丑0"
    card_values = random.sample(
        [f"{suit}{number}" for suit in ["心", "桃", "菱", "梅"] for number in range(1, 14)] ,
        52
    )
    random.shuffle(card_values)

    for i in range(5):
        for j in range(10):
            idx = i * 10 + j
            btn = Button(fr2, image=back_image, command=lambda b=idx: flip_card(buttons[b], b))
            btn.grid(row=i, column=j, padx=5, pady=5)
            btn.image_shown = False
            buttons.append(btn)

    for k in range(2):  # 新增的卡片顯示在第六行
        idx = 50 + k
        btn = Button(fr3, image=back_image, command=lambda b=idx: flip_card(buttons[b], b))
        btn.grid(row=0, column=k, padx=5, pady=5)
        btn.image_shown = False
        buttons.append(btn)

    update_timer()

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

root = Tk()
root.title("卡片配對遊戲")
root.geometry("800x600")



frame1 = Frame(root)
frame1.pack(fill="x")
Label(frame1, text="卡牌數量 (偶數，2-54):").pack(side="left", padx=10)
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
fr3 = Frame(root)
fr3.pack()

root.mainloop()
