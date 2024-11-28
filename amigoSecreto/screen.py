import random
from tkinter import Tk, Label, Entry, Button, Toplevel, Text, StringVar, Listbox
from tkinter import ttk

# cores 
co1 = "#3ab746"  # verde
co2 = "#ffffff"  # branco 
co3 = "#fffafa"  # gelo
co4 = "#00c0e7"  # azul

class AmigoSecretoApp:
    def __init__(self, add_participant_func, get_participants_func, register_present_func, send_message_func, register_draw_func, get_draws_func):
        self.add_participant_func = add_participant_func
        self.get_participants_func = get_participants_func
        self.register_present_func = register_present_func 
        self.send_message_func = send_message_func
        self.register_draw_func = register_draw_func
        self.get_draws_func = get_draws_func

        self.participantes = []
        self.root = Tk()
        self.root.title("Amigo Secreto do 2º BI")
        self._build_ui()

    def _build_ui(self):
        Label(self.root, text="Digite o nome do participante: ", font=('Verdana', 12)).pack(pady=(10, 5))  
        self.entrada_nome = Entry(self.root, font=(('Verdana'), 12), width=30, fg='black')  
        self.entrada_nome.pack(padx=20, pady=10)
        self.entrada_nome.configure(highlightthickness=1, relief="solid")  

        Button(self.root, text="Adicionar Participante", command=self.adicionar_participante, width=30, height=2, compound="center", anchor="center", overrelief="groove", font=(('Verdana', 10)), bg=co1, fg=co2).pack()

        Label(self.root, text="Participantes:", font=(('Verdana'), 12), compound="center", anchor="center").pack(pady=(20, 5))

        # Tabela com Treeview
        self.tree = ttk.Treeview(self.root, columns=("ID", "Nome"), show="headings", height=10)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.pack(padx=20, pady=10)

        Button(self.root, text="Sortear Amigos", command=self.sortear_amigos, width=30, height=2, compound="center", anchor="center", overrelief="groove", font=(('Verdana'), 10), bg=co4, fg=co2).pack(padx=60, pady=10)
        Button(self.root, text="Cadastrar Presente", command=self.cadastrar_presente, width=30, height=2, compound="center", anchor="center", overrelief="groove", font=(('Verdana'), 10), bg=co4, fg=co2).pack(padx=60, pady=10)
        Button(self.root, text="Enviar Mensagem", command=self.enviar_mensagem, width=30, height=2, compound="center", anchor="center", overrelief="groove", font=(('Verdana'), 10), bg=co4, fg=co2).pack(padx=60, pady=10)

        self.resultado_label = Label(self.root, text="")
        self.resultado_label.pack()
        self.atualizar_lista_participantes()

    def atualizar_lista_participantes(self):
        self.participantes = self.get_participants_func()
        for row in self.tree.get_children():
            self.tree.delete(row)
        for participante in self.participantes:
            self.tree.insert("", "end", values=(participante[0], participante[1]))

    def adicionar_participante(self):
        nome = self.entrada_nome.get()
        if nome:
            self.add_participant_func(nome)
            self.entrada_nome.delete(0)
            self.atualizar_lista_participantes()

    def sortear_amigos(self):
        if len(self.participantes) < 2:
            self.resultado_label.config(text="Adicione pelo menos 2 participantes para o sorteio.")
            return
        random.shuffle(self.participantes)
        pares = [(self.participantes[i][1], self.participantes[(i + 1) % len(self.participantes)][1]) for i in range(len(self.participantes))]
        self.resultado_label.config(text="\n".join([f"{a} tirou {b}" for a, b in pares]))

    def cadastrar_presente(self):
        selecionado = self.tree.selection()
        if not selecionado:
            self.resultado_label.config(text="Selecione um participante para cadastrar o presente.")
            return

        participante_id = self.participantes[int(selecionado[0])][0]
        janela_presente = Toplevel(self.root)
        janela_presente.title("Cadastrar Presente")

        Label(janela_presente, text="Descreva o presente:").pack()
        presente_entry = Entry(janela_presente)
        presente_entry.pack()

        def salvar_presente():
            presente = presente_entry.get()
            if presente:
                self.register_present_func(participante_id, presente)  
                janela_presente.destroy()

        Button(janela_presente, text="Salvar", command=salvar_presente).pack()

    def enviar_mensagem(self):
        if len(self.participantes) < 2:
            self.resultado_label.config(text="Adicione pelo menos 2 participantes para enviar mensagens.")
            return

        janela_mensagem = Toplevel(self.root)
        janela_mensagem.title("Enviar Mensagem")

        Label(janela_mensagem, text="Remetente:").pack()
        remetente_menu = Listbox(janela_mensagem, exportselection=False)
        remetente_menu.pack()
        for _, nome in self.participantes:
            remetente_menu.insert(nome)

        Label(janela_mensagem, text="Destinatário:").pack()
        destinatario_menu = Listbox(janela_mensagem, exportselection=False)
        destinatario_menu.pack()
        for _, nome in self.participantes:
            destinatario_menu.insert(nome)

        Label(janela_mensagem, text="Mensagem:").pack()
        mensagem_text = Text(janela_mensagem, height=5, width=40, font=(('Verdana'), 10))
        mensagem_text.pack()

        def enviar():
            remetente_id = self.participantes[remetente_menu.curselection()[0]][0]
            destinatario_id = self.participantes[destinatario_menu.curselection()[0]][0]
            mensagem = mensagem_text.get("1.0").strip()
            if mensagem:
                self.send_message_func(remetente_id, destinatario_id, mensagem)
                janela_mensagem.destroy()

        Button(janela_mensagem, text="Enviar", command=enviar).pack()

    def run(self):
        self.root.mainloop()
