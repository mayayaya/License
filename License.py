from tkcalendar import DateEntry
from tkinter import * 
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import babel.numbers

def getAuthority(*args, **kwargs):
    if High.get()=="1":
        cal["state"]="disabled"
    elif High.get()=="0":
        cal["state"]="readonly"

def Generate(*args, **kwargs):    
    if High.get()=="1":
        message = b"0000-00-00"
    elif High.get()=="0":
        # selected_date = cal.get()
        # print(selected_date, type(selected_date))
        # yyyy,mm,dd=selected_date.split("/")
        # print(yyyy,mm,dd)
        message = f"{cal.get()}"
        message = bytes( message, encoding = "utf8")
        # print(message ,type(message))

    # 生成隨機密鑰
    key = get_random_bytes(24)  #我用24 # 16位密鑰，實際使用時需要更強的密鑰
    print(key)

    # 初始化 AES 加密器
    cipher = AES.new(key, AES.MODE_ECB)

    # 要加密的訊息，這裡將訊息補足到 AES 區塊大小的倍數
    # message = b"2023-12-14"
    while len(message) % 16 != 0:  # 確保訊息是 AES 區塊大小的倍數
        message += b'\0'

    # 加密訊息
    cipher_text = cipher.encrypt(message)
    # 將加密後的訊息進行 base64 編碼並寫入文字檔案
    encrypted_data = base64.b64encode(cipher_text)
    # print("加密後的訊息:", encrypted_data)

    licenseTXT = open("./License.txt","wb")
    licenseTXT.write(encrypted_data)
    if High.get()=="1":
        text = "\n\n#Validity period : 0000-00-00"
    else:
        text = f"\n\n#Validity period : {cal.get()}"
    licenseTXT.write(text.encode('utf-8'))
    licenseTXT.close()

    # #解密
    # readTXT = open("./License.txt","rb")
    # encrypted_data = readTXT.readline()
    # readTXT.close()
    # # print(encrypted_data, type(encrypted_data))
    
    # # 對 base64 編碼的資料進行解碼
    # cipher_text = base64.b64decode(encrypted_data)

    # # 初始化 AES 解密器
    # decipher = AES.new(key, AES.MODE_ECB)

    # # 解密訊息
    # plain_text = decipher.decrypt(cipher_text)
    # print("解密後的訊息:", plain_text.rstrip(b'\0').decode())

if __name__=="__main__":
    
    view=Tk()
    view.title("License Creator")
    view.geometry('330x130+330+260')
    view.resizable(False, False) #x,y不能縮放

    Top_Frame=Frame(view)
    Top_Frame.pack(fill='x', padx=10, pady=10)

    cal_lab=Label(Top_Frame, text="Validity period:", padx=10, pady=10, font=('微軟正黑體',14,"bold" ))
    cal_lab.grid(column=0, row=0, sticky=E)
    cal = DateEntry(Top_Frame, width=12, background='white', state="readonly", date_pattern="yyyy-mm-dd",
                    font=('微軟正黑體',10,"bold" ), foreground='black', borderwidth=2)
    cal.grid(column=1, row=0, sticky=E)
    High=StringVar()
    High_check=Checkbutton(Top_Frame, variable=High, onvalue='1', offvalue='0', 
                           padx=5, command= getAuthority)#
    High_check.grid(column=2, row=0, sticky=W)
    High_check.deselect()   # 開始時不要勾選

    Generate_btn = Button(view, text='Generate', font=('微軟正黑體',14, "bold"),height=1, 
                          background="#87D4A6", command=Generate)
    Generate_btn.pack(fill='x', padx=20)


    view.mainloop()
