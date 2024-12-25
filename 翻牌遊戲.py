from tkinter import *
import random
def clear_frame(frame):
    # 清除指定 Frame 中的所有子部件
    for widget in frame.winfo_children():
        widget.destroy()

def start():
    randomnum=[]
    clear_frame(fr2)
    clear_frame(fr3)
    num = int(entry.get())  # 將輸入轉換為整數
    closest_factors = None  # 儲存因數對
    min_diff = float('inf')  # 初始化最小差距為無窮大
    
    for i in range(1,num//2):
        randomnum.append(i)
    
    for l in range(1, int(num**0.5) + 1):  # 只需要檢查到 num 的平方根
        if num % l == 0:  # 如果 l 是因數
            il = num // l  # 計算另一個因數
            diff = abs(il - l)  # 計算因數差距的絕對值
            if diff < min_diff:  # 如果找到更小的差距
                min_diff = diff
                closest_factors = (l, il)  # 更新最近的因數對
    
    # 格式化輸出
    if closest_factors and closest_factors[0]<=10 and closest_factors[1] <= 10:
        print(f"{num} = {closest_factors[0]} X {closest_factors[1]}")
        for i in range(closest_factors[0]):
            for l in range(closest_factors[1]):
                btn=Button(fr2,text="?",width=7,height=4)
                btn.grid(row=i,column=l,padx=5,pady=5)
                
    elif closest_factors and (closest_factors[0]>10 or closest_factors[1] > 10):
        print(f"{num} = {closest_factors[0]} X {closest_factors[1]}")
        for i in range(num//10):
            for l in range(10):
                btn=Button(fr2,text="?",width=7,height=4)
                btn.grid(row=i,column=l,padx=5,pady=5)
        for k in range(num%10):
            btn=Button(fr3,text="?",width=7,height=4)
            btn.grid(row=0,column=k,padx=5,pady=5)
             
root= Tk()
root.title("卡片配對")
root.geometry("690x900")

fr1=Frame(root)
fr1.pack(fill='x')
labnum=Label(fr1,text="卡牌數量(需為偶數):")
labnum.grid(row=0,column=0,padx=10)
entry=Entry(fr1)
entry.grid(row=0,column=1)
chbtn1=Checkbutton(fr1,text=":計時配對時間")
chbtn1.grid(row=1,column=0)
chbtn2=Checkbutton(fr1,text=":計算翻牌次數")
chbtn2.grid(row=1,column=1)
chbtn3=Checkbutton(fr1,text=":限制時間")
chbtn3.grid(row=1,column=2)
labtime1=Label(fr1,text="0:00")
labtime1.grid(row=2,column=0)
labcount=Label(fr1,text="0")
labcount.grid(row=2,column=1)
labtime2=Label(fr1,text="10:00")
labtime2.grid(row=2,column=2)
startbtn=Button(fr1,text="開始",command=start)
startbtn.grid(row=3,column=1,ipadx=20)

fr2=Frame(root)
fr2.pack()

fr3=Frame(root)
fr3.pack()







root.mainloop()