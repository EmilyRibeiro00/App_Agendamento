from tkinter import *
from tkcalendar import DateEntry
import sqlite3 as lite
from tkinter import messagebox
from tkinter import ttk

# ========== Cores ========== #
co0 = "#f0f3f5"  # Preta
co1 = "#feffff"  # branca
co2 = "#808080"  # cinza
co3 = "#38576b"  # valor
co4 = "#403d3d"   # letra
co5 = "#e06636"   # profit
co6 = "#038cfc"   # azul
co7 = "#ef5350"   # vermelha
co8 = "#4fa882"   # verde
co9 = "#e9edf5"   # sky blue

# ========== Funções ========== #
def inserir_dados():
    nome = entrada_nome_usuario.get()
    email = entrada_email_usuario.get()
    telefone = entrada_telefone_usuario.get()
    data = entrada_data_consulta.get_date()
    tipo = entrada_tipo_de_consulta.get()
    especializacao = entrada_espec_consulta.get()
    
    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO formulario (nome, email, telefone, dia_em, estado, assunto) VALUES (?, ?, ?, ?, ?, ?)",
                    (nome, email, telefone, data, tipo, especializacao))
        con.commit()
    mostrar_dados()
    messagebox.showinfo("Inserir", "Dados inseridos com sucesso!")


def atualizar_dados():
    try:
        id_selecionado = entrada_id.get()
        
        # Verifica se o campo de ID está vazio
        if not id_selecionado:
            messagebox.showerror("Erro", "ID não fornecido.")
            return

        # Consulta para verificar se o ID existe no banco de dados
        cur.execute("SELECT * FROM formulario WHERE id=?", (id_selecionado,))
        registro = cur.fetchone()
        
        # Se o ID não for encontrado, exibe uma mensagem e sai da função
        if not registro:
            messagebox.showerror("Erro", f"Registro com ID {id_selecionado} não encontrado.")
            return

        # Pegando os valores dos outros campos, exceto o nome
        email = entrada_email_usuario.get()
        telefone = entrada_telefone_usuario.get()
        data_consulta = entrada_data_consulta.get_date()
        tipo = entrada_tipo_de_consulta.get()
        especializacao = entrada_espec_consulta.get()

        # Atualizando o registro no banco de dados, exceto o campo Nome
        cur.execute("UPDATE formulario SET email=?, telefone=?, dia_em=?, estado=?, assunto=? WHERE id=?", 
                    (email, telefone, data_consulta, tipo, especializacao, id_selecionado))
        con.commit()
        
        # Atualiza a visualização e limpa os campos
        mostrar_dados()
        limpar_campos()
        messagebox.showinfo("Sucesso", "Registro atualizado com sucesso.")
        
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao atualizar dados: {e}")


def remover_dados():
    try:
        id = int(entrada_id.get())
        with con:
            cur = con.cursor()
            cur.execute("DELETE FROM formulario WHERE id=?", (id,))
            con.commit()

        mostrar_dados()
        messagebox.showinfo("Remover", "Dados removidos com sucesso!")
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um ID válido.")

def limpar_campos():
    entrada_id.delete(0, END)
    entrada_nome_usuario.delete(0, END)
    entrada_email_usuario.delete(0, END)
    entrada_telefone_usuario.delete(0, END)
    entrada_espec_consulta.delete(0, END)
    entrada_tipo_de_consulta.delete(0, END)



# ========== Banco de Dados ========== #
con = lite.connect('dados.db')
with con:
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS formulario(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        nome TEXT, 
        email TEXT, 
        telefone TEXT, 
        dia_em DATE, 
        estado TEXT, 
        assunto TEXT)
    """)


# ========== Janela ========== #
janela = Tk()
janela.title("FORMULÁRIO")
janela.geometry('1180x450')
janela.configure(background=co9)
janela.resizable(width=FALSE, height=FALSE)

# ========== Dividindo a janela ========== #
frame_Sup = Frame(janela, width=310, height=50, bg=co2, relief='flat')
frame_Sup.grid(row=0, column=0)
frame_Inf = Frame(janela, width=310, height=403, bg=co1, relief='flat')
frame_Inf.grid(row=1, column=0, sticky=NSEW, padx=0, pady=1)
frame_Dir = Frame(janela, width=850, height=403, bg=co1, relief='flat')
frame_Dir.grid(row=0, column=1, rowspan=2, sticky=NSEW, padx=1, pady=0)


# Função para exibir dados no Treeview
def mostrar_dados():
    for row in tree.get_children():
        tree.delete(row)
    cur.execute("SELECT * FROM formulario")
    dados = cur.fetchall()
    for row in dados:
        tree.insert("", "end", values=row)

# Configurando o Treeview no frame_Dir
tree = ttk.Treeview(frame_Dir, columns=("ID", "Nome", "Email", "Telefone", "Data", "Tipo", "Especialidade"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Nome", text="Nome")
tree.heading("Email", text="Email")
tree.heading("Telefone", text="Telefone")
tree.heading("Data", text="Data")
tree.heading("Tipo", text="Tipo")
tree.heading("Especialidade", text="Especialidade")

tree.column("ID", width=50)
tree.column("Nome", width=100)
tree.column("Email", width=100)
tree.column("Telefone", width=100)
tree.column("Data", width=80)
tree.column("Tipo", width=80)
tree.column("Especialidade", width=100)

tree.place(x=0, y=0, width=850, height=403)

# Carregar dados ao iniciar o programa
mostrar_dados()


# ========== Label Superior ========== #
app_nome = Label(frame_Sup, text='Agendamento de Consulta', anchor=NW, font=('Ivy', 13, 'bold'), bg=co2, relief='flat')
app_nome.place(x=45, y=15)

# ========== Frame Inferior ========== #
# ID (Para atualizar/remover)
id_label = Label(frame_Inf, text='ID', anchor=NW, font=('Ivy', 10, 'bold'), bg=co1, fg=co4, relief='flat')
id_label.place(x=10, y=10)
entrada_id = Entry(frame_Inf, width=10, justify='left', relief='solid')
entrada_id.place(x=50, y=10)

# Nome
nome_usuario = Label(frame_Inf, text='Nome *', anchor=NW, font=('Ivy', 10, 'bold'), bg=co1, fg=co4, relief='flat')
nome_usuario.place(x=10, y=40)
entrada_nome_usuario = Entry(frame_Inf, width=45, justify='left', relief='solid')
entrada_nome_usuario.place(x=10, y=65)

# Email
email_usuario = Label(frame_Inf, text='Email *', anchor=NW, font=('Ivy', 10, 'bold'), bg=co1, fg=co4, relief='flat')
email_usuario.place(x=10, y=95)
entrada_email_usuario = Entry(frame_Inf, width=45, justify='left', relief='solid')
entrada_email_usuario.place(x=10, y=120)

# Telefone
telefone_usuario = Label(frame_Inf, text='Telefone *', anchor=NW, font=('Ivy', 10, 'bold'), bg=co1, fg=co4, relief='flat')
telefone_usuario.place(x=10, y=150)
entrada_telefone_usuario = Entry(frame_Inf, width=45, justify='left', relief='solid')
entrada_telefone_usuario.place(x=10, y=175)

# Data de Consulta
data_consulta = Label(frame_Inf, text='Data da Consulta *', anchor=NW, font=('Ivy', 10, 'bold'), bg=co1, fg=co4, relief='flat')
data_consulta.place(x=10, y=205)
entrada_data_consulta = DateEntry(frame_Inf, width=12, background='darkblue', foreground='white', borderwidth=2)
entrada_data_consulta.place(x=10, y=230)

# Tipo da consulta
tipo_de_consulta = Label(frame_Inf, text='Tipo *', anchor=NW, font=('Ivy', 10, 'bold'), bg=co1, fg=co4, relief='flat')
tipo_de_consulta.place(x=150, y=205)
entrada_tipo_de_consulta = Entry(frame_Inf, width=20, justify='left', relief='solid')
entrada_tipo_de_consulta.place(x=150, y=230)

# Especialidade da consulta
espec_consulta = Label(frame_Inf, text='Especialidade *', anchor=NW, font=('Ivy', 10, 'bold'), bg=co1, fg=co4, relief='flat')
espec_consulta.place(x=10, y=260)
entrada_espec_consulta = Entry(frame_Inf, width=45, justify='left', relief='solid')
entrada_espec_consulta.place(x=10, y=285)

# ========== Botões ========== #
botao_Inserir = Button(frame_Inf, text='Inserir', width=10, anchor=NW, font=('Ivy', 8, 'bold'), bg=co6, fg=co1, relief='raised', overrelief='ridge', command=inserir_dados)
botao_Inserir.place(x=10, y=325)

botao_Remover = Button(frame_Inf, text='Remover', width=10, anchor=NW, font=('Ivy', 8, 'bold'), bg=co7, fg=co1, relief='raised', overrelief='ridge', command=remover_dados)
botao_Remover.place(x=100, y=325)

botao_Atualizar = Button(frame_Inf, text='Atualizar', width=10, anchor=NW, font=('Ivy', 8, 'bold'), bg=co8, fg=co1, relief='raised', overrelief='ridge', command=atualizar_dados)
botao_Atualizar.place(x=190, y=325)

botao_Limpar = Button(frame_Inf, text='Limpar Campos', width=12, anchor=NW, font=('Ivy', 8, 'bold'), bg=co3, fg=co1, relief='raised', overrelief='ridge', command=limpar_campos)
botao_Limpar.place(x=10, y=360)




janela.mainloop()