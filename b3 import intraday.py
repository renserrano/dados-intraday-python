from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import mysql.connector
from mysql.connector import errorcode
import os.path
from datetime import datetime


try:
    conexao = mysql.connector.connect(user='root',
                                      password='******',
                                      host='127.0.0.1',
                                      database='dados_b3',
                                      charset='utf8')

    print("conectou com sucesso!")
except mysql.connector.Error as error:

    if error.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database não existe")
    elif error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Usuário ou senha inválidos")
    else:
        print(error)
else:        
    cursor = conexao.cursor()

    bg_color = '#f0f0f0'
    fg_color = '#000'
    filename = ''

    app=Tk()
    app.title("Import B3 IntraDay")
    app.geometry("521x270")
    
    def btnOpenFileClick():
        global filename
        filename = filedialog.askopenfilename()
        if os.path.isfile(filename):
            btnIntraDay["state"] = "normal"
        else:
            btnIntraDay["state"] = "disabled"

    def btnIntraDayClick():
        arquivo_entrada = open(filename, 'r')
        for linha in arquivo_entrada:
            GravarTradeIntraDay(linha)
        messagebox.showinfo("App", "Importação Concluída com Sucesso!")

    def GravarTradeIntraDay(linha):
        RptDt, TckrSymb, UpdActn, GrssTradAmt, TradQty, NtryTm, TradId, TradgSsnId, TradDt = linha.split(';')
        if not RptDt.isalpha():
            query = (f"INSERT INTO trade_intraday (RptDt, TckrSymb, UpdActn, GrssTradAmt, TradQty, NtryTm, TradId, TradgSsnId, TradDt)" +
                     " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ")
            cursor.execute(query, (RptDt, TckrSymb, UpdActn, GrssTradAmt.replace(',', '.'), TradQty.replace(',', '.'), NtryTm, TradId, TradgSsnId, TradDt))
            conexao.commit()

    app.configure(background=bg_color)

    btnOpenFile=Button(app,
                       text="Abrir arquivo desejado...",
                       background=bg_color,
                       foreground=fg_color,
                       command=btnOpenFileClick)

    btnOpenFile.place(x=10,
                      y=10,
                      width=150,
                      height=30)

    btnIntraDay=Button(app,
                       text="Importar IntraDay",
                       background=bg_color,
                       foreground=fg_color,
                       state="disabled",
                       command=btnIntraDayClick)

    btnIntraDay.place(x=10, y=50, width=150, height=30)

    app.mainloop()

    cursor.close()
    conexao.close()
