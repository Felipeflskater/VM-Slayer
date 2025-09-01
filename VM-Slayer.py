import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import winreg
import psutil
import platform


class VMSlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("VM Slayer")
        self.root.geometry("650x550")
        self.root.resizable(False, False)

        try:
            self.root.iconbitmap("icon.ico")
        except Exception as e:
            print(f"Erro ao carregar ícone: {e}")

        # Remove barra padrão do Windows
        self.root.overrideredirect(True)

        # Barra customizada
        self.title_bar = tk.Frame(self.root, bg="#2d2d2d", relief="raised", bd=0, height=30)
        self.title_bar.pack(fill="x")

        self.title_label = tk.Label(
            self.title_bar, text="VM Slayer",
            bg="#2d2d2d", fg="white", font=("Segoe UI", 10, "bold")
        )
        self.title_label.pack(side="left", padx=10)

        # Botões da barra
        self.btn_min = tk.Button(
            self.title_bar, text="—", command=self.minimize_window,
            bg="#2d2d2d", fg="white", bd=0, font=("Segoe UI", 12), width=3,
            activebackground="#404040", relief="flat"
        )
        self.btn_min.pack(side="right")

        self.btn_close = tk.Button(
            self.title_bar, text="✕", command=self.root.destroy,
            bg="#2d2d2d", fg="white", bd=0, font=("Segoe UI", 12), width=3,
            activebackground="#e74c3c", relief="flat"
        )
        self.btn_close.pack(side="right")

        # mover janela
        self.title_bar.bind("<ButtonPress-1>", self.iniciar_move)
        self.title_bar.bind("<B1-Motion>", self.arrastar_janela)
        self.title_label.bind("<ButtonPress-1>", self.iniciar_move)
        self.title_label.bind("<B1-Motion>", self.arrastar_janela)

        # Configuração do tema
        style = ttk.Style(self.root)
        style.theme_use("clam")

        # Configurações de estilo
        style.configure("TNotebook", background="#f0f0f0")
        style.configure("TNotebook.Tab", padding=[20, 8], font=("Segoe UI", 9))
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabel", background="#f0f0f0", foreground="black", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 9), padding=10)
        style.configure("TCheckbutton", background="#f0f0f0", font=("Segoe UI", 10))

        main_frame = tk.Frame(root, bg="#f0f0f0")
        main_frame.pack(expand=True, fill="both")

        # Abas
        notebook = ttk.Notebook(main_frame)
        notebook.pack(expand=True, fill="both", pady=10, padx=10)

        self.dashboard_tab = ttk.Frame(notebook)
        self.quick_tab = ttk.Frame(notebook)
        self.services_tab = ttk.Frame(notebook)

        notebook.add(self.dashboard_tab, text="📊 Dashboard")
        notebook.add(self.quick_tab, text="⚡ Otimizações rápidas")
        notebook.add(self.services_tab, text="🛠️ Serviços")

        self.setup_dashboard()
        self.setup_otimizacao()
        self.setup_services()

    def setup_dashboard(self):
        """Configuração da aba Dashboard"""
        # Container principal
        container = tk.Frame(self.dashboard_tab, bg="#f0f0f0")
        container.pack(expand=True, fill="both", padx=20, pady=20)

        title_label = tk.Label(
            container,
            text="Bem vindo ao VM-Slayer!",
            font=("Segoe UI", 16, "bold"),
            bg="#f0f0f0", fg="#2c3e50"
        )
        title_label.pack(pady=(0, 5))

        subtitle_label = tk.Label(
            container,
            text="Otimizador de VM Windows",
            font=("Segoe UI", 12),
            bg="#f0f0f0", fg="#34495e"
        )
        subtitle_label.pack(pady=(0, 30))

        # Frame para métricas
        metrics_frame = tk.Frame(container, bg="#f0f0f0")
        metrics_frame.pack(pady=10)

        self.lbl_cpu = tk.Label(
            metrics_frame, text="CPU: 0.0%",
            font=("Segoe UI", 11), bg="#f0f0f0", fg="#27ae60"
        )
        self.lbl_cpu.pack(pady=5)

        self.lbl_ram = tk.Label(
            metrics_frame, text="RAM: 58.0%",
            font=("Segoe UI", 11), bg="#f0f0f0", fg="#e74c3c"
        )
        self.lbl_ram.pack(pady=5)

        # Informações do sistema
        sistema = platform.system()
        versao = platform.version()
        release = platform.release()
        proc = platform.processor()
        ram_total = round(psutil.virtual_memory().total / (1024**3), 2)

        info_frame = tk.Frame(container, bg="#f0f0f0")
        info_frame.pack(pady=20, fill="x")

        info_labels = [
            f"Sistema Operacional: {sistema} {release} ({versao})",
            f"Processador: {proc}",
            f"Memória RAM Total: {ram_total} GB"
        ]

        for info in info_labels:
            label = tk.Label(
                info_frame, text=info,
                font=("Segoe UI", 9), bg="#f0f0f0", fg="#2c3e50",
                anchor="w"
            )
            label.pack(anchor="w", pady=5,padx=100)
        #Aviso de sujestões
        sujestao_label = tk.Label(
            container,
            text="Sugestões? Crie um issues no github do projeto.",
            font=("Segoe UI", 9, "bold"),
            bg="#f0f0f0", fg="#2c3e50"
        )
        sujestao_label.pack(pady=(30, 5))
        #link github
        link = tk.Label(
            container,
            text="Projeto no github",
            fg="#3498db", cursor="hand2",
            font=("Segoe UI", 9, "underline"),
            bg="#f0f0f0"
        )
        link.pack(anchor="w")
        link.bind("<Button-1>", lambda e: self.abrir_link("https://github.com/Felipeflskater/VM-Slayer"))

        self.atualizar_dashboard()

    def setup_otimizacao(self):
        """Configuração da aba Otimizações rápidas"""
        container = tk.Frame(self.quick_tab, bg="#f0f0f0")
        container.pack(expand=True, fill="both", padx=20, pady=20)

        # Título
        title_label = tk.Label(
            container,
            text="Clique em um botão abaixo para aplicar os ajustes.",
            font=("Segoe UI", 12, "bold"),
            bg="#f0f0f0", fg="#2c3e50"
        )
        title_label.pack(pady=(0, 30))

        # Botões de otimização
        buttons_info = [
            ("Desativar Efeitos Visuais", self.desativar_efeitos),
            ("Desativar Hibernação", self.desativar_hibernacao),
            ("Limpar Arquivos Temporários", self.limpar_temp)
        ]

        for text, command in buttons_info:
            btn = tk.Button(
                container,
                text=text,
                command=command,
                font=("Segoe UI", 10),
                bg="white",
                fg="#2c3e50",
                relief="solid",
                bd=1,
                padx=20,
                pady=10,
                cursor="hand2",
                activebackground="#ecf0f1",
                width=35
            )
            btn.pack(pady=8)

    def setup_services(self):
        """Configuração da aba Serviços"""
        container = tk.Frame(self.services_tab, bg="#f0f0f0")
        container.pack(expand=True, fill="both", padx=20, pady=20)

        # Título
        title_label = tk.Label(
            container,
            text="Painel para desativar ou reativar serviços do windows em lote.",
            font=("Segoe UI", 12, "bold"),
            bg="#f0f0f0", fg="#2c3e50"
        )
        title_label.pack(pady=(0, 20))

        checkboxes_frame = tk.Frame(container, bg="#f0f0f0")
        checkboxes_frame.pack(fill="x", pady=(0, 30))

        self.var_sysmain = tk.BooleanVar()
        self.var_search = tk.BooleanVar()
        self.var_update = tk.BooleanVar()
        self.var_bluetooth = tk.BooleanVar()
        self.var_spooler = tk.BooleanVar()

        chk_list = [
            ("Superfetch (SysMain)", self.var_sysmain),
            ("Windows Search", self.var_search),
            ("Windows Update", self.var_update),
            ("Bluetooth Support", self.var_bluetooth),
            ("Spooler de impressão", self.var_spooler)
        ]

        for texto, var in chk_list:
            chk = tk.Checkbutton(
                checkboxes_frame,
                text=texto,
                variable=var,
                font=("Segoe UI", 10),
                bg="#f0f0f0",
                fg="#2c3e50",
                activebackground="#f0f0f0",
                relief="flat",
                bd=0
            )
            chk.pack(anchor="w", pady=5)

        buttons_frame = tk.Frame(container, bg="#f0f0f0")
        buttons_frame.pack(fill="x", side="bottom")

        btn_desativar = tk.Button(
            buttons_frame,
            text="Desativar Serviços Selecionados",
            command=lambda: self.aplicar_servicos("desativar"),
            font=("Segoe UI", 10),
            bg="white",
            fg="#2c3e50",
            relief="solid",
            bd=1,
            padx=20,
            pady=10,
            cursor="hand2",
            activebackground="#ecf0f1"
        )
        btn_desativar.pack(side="left", padx=(0, 10))

        btn_reativar = tk.Button(
            buttons_frame,
            text="Reativar Serviços Selecionados",
            command=lambda: self.aplicar_servicos("ativar"),
            font=("Segoe UI", 10),
            bg="white",
            fg="#2c3e50",
            relief="solid",
            bd=1,
            padx=20,
            pady=10,
            cursor="hand2",
            activebackground="#ecf0f1"
        )
        btn_reativar.pack(side="right", padx=(10, 0))

    def atualizar_dashboard(self):
        try:
            cpu = psutil.cpu_percent(interval=1)
            ram = psutil.virtual_memory().percent

            cpu_color = "#27ae60" if cpu < 50 else "#f39c12" if cpu < 80 else "#e74c3c"
            ram_color = "#27ae60" if ram < 50 else "#f39c12" if ram < 80 else "#e74c3c"

            self.lbl_cpu.config(text=f"CPU: {cpu}%", fg=cpu_color)
            self.lbl_ram.config(text=f"RAM: {ram}%", fg=ram_color)

            self.root.after(2000, self.atualizar_dashboard)
        except:
            pass

    def executar_cmd(self, comando, as_admin=False):
        try:
            if as_admin:
                subprocess.run(
                    f'powershell -Command "Start-Process cmd -ArgumentList \'/c {comando}\' -Verb RunAs"',
                    shell=True
                )
            else:
                subprocess.run(comando, shell=True, check=True,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao executar: {comando}\n{str(e)}")
            return False

    def desativar_servico(self, nome_servico):
        return self.executar_cmd(f'sc config "{nome_servico}" start= disabled', as_admin=True)

    def ativar_servico(self, nome_servico):
        return self.executar_cmd(f'sc config "{nome_servico}" start= auto', as_admin=True)

    def desativar_efeitos(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                 r"Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects",
                                 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, "", 0, winreg.REG_DWORD, 2)
            winreg.CloseKey(key)
            messagebox.showinfo("Sucesso", "Efeitos visuais desativados!")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível desativar efeitos: {e}")

    def limpar_temp(self):
        result1 = self.executar_cmd('del /q /f /s %temp%\\*', as_admin=True)
        result2 = self.executar_cmd('cleanmgr /sagerun:1', as_admin=True)
        if result1 or result2:
            messagebox.showinfo("Limpeza", "Arquivos temporários limpos!")

    def desativar_hibernacao(self):
        if self.executar_cmd('powercfg -h off', as_admin=True):
            messagebox.showinfo("Hibernação", "Hibernação desativada.")

    def aplicar_servicos(self, acao):
        total = 0
        servicos = {
            "SysMain": self.var_sysmain.get(),
            "WSearch": self.var_search.get(),
            "wuauserv": self.var_update.get(),
            "bthserv": self.var_bluetooth.get(),
            "Spooler": self.var_spooler.get(),
        }
        for nome, selecionado in servicos.items():
            if selecionado:
                if acao == "desativar" and self.desativar_servico(nome):
                    total += 1
                elif acao == "ativar" and self.ativar_servico(nome):
                    total += 1

        if total > 0:
            messagebox.showinfo("Concluído", f"{total} serviço(s) {acao}ado(s) com sucesso!")
        else:
            messagebox.showwarning("Aviso", "Nenhum serviço foi selecionado ou houve falha na operação.")

    def abrir_link(self, url):
        import webbrowser
        webbrowser.open(url)

    # Funções de controle da janela
    def iniciar_move(self, event):
        self.xwin = event.x
        self.ywin = event.y

    def arrastar_janela(self, event):
        x = event.x_root - self.xwin
        y = event.y_root - self.ywin
        self.root.geometry(f"+{x}+{y}")

    def minimize_window(self):
        self.root.overrideredirect(False)
        self.root.iconify()

        def restore():
            self.root.deiconify()
            self.root.overrideredirect(True)

        self.root.bind("<Map>", lambda e: restore())


# Iniciar aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = VMSlayer(root)
    root.mainloop()
