
"""
公版格式
"""

from tkinter import *
from tkinter import messagebox
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import datetime, time

def DecryptLicense():
    try:
        key = b"~~~~"
        readTXT = open("./License.txt","rb")
        encrypted_data = readTXT.readline()
        readTXT.readline()
        Validity = readTXT.readline()
        Validity = Validity.decode('utf-8').split(":")[1].strip()
        readTXT.close()
        # print(encrypted_data, type(encrypted_data))
        # 對 base64 編碼的資料進行解碼
        cipher_text = base64.b64decode(encrypted_data)

        # 初始化 AES 解密器
        decipher = AES.new(key, AES.MODE_ECB)

        # 解密訊息
        plain_text = decipher.decrypt(cipher_text).rstrip(b'\0').decode()
        # print("解密後的訊息:", plain_text)

        deadlineDate = "0000-00-00"
        # print(Validity)
        if plain_text != "0000-00-00":
            deadlineDate = datetime.datetime.strptime(plain_text,'%Y-%m-%d').date()
        currentDate = datetime.date.today()

        if Validity!=plain_text:
            msg = "Key與日期限制不相符"
            return False, msg
        elif (deadlineDate=="0000-00-00" or (deadlineDate>=currentDate)):
            return True, None
        else:
            msg = f"程式已於 {deadlineDate} 到期"
            return False, msg
        
    except Exception as e:
        return e, None
        

if __name__=="__main__":
    try:
        Flag, msg= DecryptLicense()
        if isinstance(Flag, Exception):
            raise Flag

        if Flag:            
            view=Tk()
            view.geometry('640x430+230+150')
            view.resizable(False, False) 
            view.mainloop()
        else:
            messagebox.showerror("錯誤", msg)

    except Exception as e:
        messagebox.showerror("錯誤", f"{str(e)}")


