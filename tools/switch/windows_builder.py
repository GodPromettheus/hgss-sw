#!/usr/bin/env python3
"""Windows GUI for the local Nintendo Switch build in this repository.

The ROM is passed to WSL on the user's machine. This program does not upload,
copy, package, or commit ROMs or build outputs.
"""
from __future__ import annotations

import queue
import shlex
import subprocess
import threading
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


GAMES = {
    "Pokémon SoulSilver + HeartGold (ROM SoulSilver EUA)": "hgss",
    "Pokémon Black 2": "black2",
    "Pokémon White 2": "white2",
    "Pokémon Black": "black",
    "Pokémon White": "white",
    "Todos os seis jogos (ROM SoulSilver EUA)": "all",
}


class SwitchBuilder(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("HGSS-SW | Construtor local para Switch")
        self.geometry("760x560")
        self.minsize(640, 440)
        self.events: queue.Queue[tuple[str, str]] = queue.Queue()
        self.running = False

        self.game = tk.StringVar(value=next(iter(GAMES)))
        self.rom = tk.StringVar()
        self.repo = Path(__file__).resolve().parents[2]

        self._make_widgets()
        self.after(100, self._drain_events)

    def _make_widgets(self) -> None:
        root = ttk.Frame(self, padding=18)
        root.pack(fill="both", expand=True)
        root.columnconfigure(1, weight=1)
        root.rowconfigure(5, weight=1)

        ttk.Label(root, text="Construtor local para Nintendo Switch",
                  font=("Segoe UI", 16, "bold")).grid(row=0, column=0, columnspan=3, sticky="w")
        ttk.Label(
            root,
            text=("Gera os arquivos do projeto a partir da sua cópia local. "
                  "A ROM e os resultados ficam no seu computador."),
            wraplength=690,
        ).grid(row=1, column=0, columnspan=3, sticky="w", pady=(5, 16))

        ttk.Label(root, text="Jogo ou pacote:").grid(row=2, column=0, sticky="w", pady=4)
        self.game_box = ttk.Combobox(root, textvariable=self.game, values=list(GAMES),
                                     state="readonly")
        self.game_box.grid(row=2, column=1, columnspan=2, sticky="ew", pady=4)

        ttk.Label(root, text="Sua ROM (.nds):").grid(row=3, column=0, sticky="w", pady=4)
        ttk.Entry(root, textvariable=self.rom).grid(row=3, column=1, sticky="ew", pady=4)
        self.browse_button = ttk.Button(root, text="Selecionar…", command=self._choose_rom)
        self.browse_button.grid(row=3, column=2, sticky="e", padx=(8, 0), pady=4)

        ttk.Label(root, text=f"Projeto: {self.repo}", wraplength=690).grid(
            row=4, column=0, columnspan=3, sticky="w", pady=(4, 8)
        )

        self.log = tk.Text(root, height=12, wrap="word", state="disabled")
        self.log.grid(row=5, column=0, columnspan=3, sticky="nsew")
        scroll = ttk.Scrollbar(root, command=self.log.yview)
        scroll.grid(row=5, column=3, sticky="ns")
        self.log.configure(yscrollcommand=scroll.set)

        actions = ttk.Frame(root)
        actions.grid(row=6, column=0, columnspan=3, sticky="ew", pady=(12, 0))
        actions.columnconfigure(0, weight=1)
        self.status = ttk.Label(actions, text="Pronto")
        self.status.grid(row=0, column=0, sticky="w")
        self.build_button = ttk.Button(actions, text="Gerar arquivos do Switch",
                                       command=self._start_build)
        self.build_button.grid(row=0, column=1, sticky="e")

        self._append_log(
            "Requer WSL2 com Ubuntu 24.04, git, CMake, Ninja, Python 3 e devkitPro "
            "(switch-dev e switch-sdl2), conforme o guia do projeto."
        )
        self._append_log(
            "O resultado fica em build-sd/switch dentro desta cópia local do projeto. "
            "A ROM não é incluída no pacote."
        )

    def _choose_rom(self) -> None:
        path = filedialog.askopenfilename(
            title="Selecione uma ROM que você possui",
            filetypes=[("ROM de Nintendo DS", "*.nds"), ("Todos os arquivos", "*.*")],
        )
        if path:
            self.rom.set(path)

    def _start_build(self) -> None:
        if self.running:
            return
        if not (self.repo / "tools" / "switch" / "build_game.sh").is_file():
            messagebox.showerror(
                "Projeto não encontrado",
                "Este programa precisa estar dentro da pasta hgss-sw, junto do código do projeto.",
            )
            return
        rom_path = Path(self.rom.get()).expanduser()
        if not rom_path.is_file() or rom_path.suffix.lower() != ".nds":
            messagebox.showerror("ROM necessária", "Selecione um arquivo .nds que exista.")
            return

        game_key = self.game.get()
        game_code = GAMES.get(game_key)
        if not game_code:
            return

        self.running = True
        self.build_button.configure(state="disabled")
        self.browse_button.configure(state="disabled")
        self.status.configure(text="Build em andamento…")
        self._append_log(f"\nIniciando build: {game_key}")
        threading.Thread(
            target=self._build_worker,
            args=(game_code, rom_path.resolve()),
            daemon=True,
        ).start()

    def _build_worker(self, game_code: str, rom_path: Path) -> None:
        # Quote Windows paths for Bash; wslpath converts them inside Ubuntu.
        repo_arg = shlex.quote(str(self.repo))
        rom_arg = shlex.quote(str(rom_path))
        command = (
            f"repo=$(wslpath -u -- {repo_arg}) && "
            f"rom=$(wslpath -u -- {rom_arg}) && "
            'cd "$repo" && '
            f"bash tools/switch/build_game.sh {shlex.quote(game_code)} \"$rom\""
        )
        try:
            process = subprocess.Popen(
                ["wsl.exe", "--exec", "bash", "-lc", command],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                bufsize=1,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
            assert process.stdout is not None
            for line in process.stdout:
                self.events.put(("log", line.rstrip()))
            code = process.wait()
            self.events.put(("done", str(code)))
        except FileNotFoundError:
            self.events.put(("error", "Não encontrei wsl.exe. Instale/ative o WSL2 e o Ubuntu 24.04."))
        except Exception as exc:
            self.events.put(("error", str(exc)))

    def _drain_events(self) -> None:
        try:
            while True:
                kind, value = self.events.get_nowait()
                if kind == "log":
                    self._append_log(value)
                else:
                    self.running = False
                    self.build_button.configure(state="normal")
                    self.browse_button.configure(state="normal")
                    if kind == "done" and value == "0":
                        self.status.configure(text="Build concluído")
                        self._append_log(
                            "\nConcluído. Veja build-sd/switch nesta cópia local do projeto."
                        )
                        messagebox.showinfo(
                            "Build concluído",
                            "Arquivos gerados em build-sd/switch. A ROM não foi empacotada. "
                            "Copie apenas os arquivos necessários para o cartão SD.",
                        )
                    else:
                        message = value if kind == "error" else (
                            f"O build terminou com erro (código {value}). "
                            "Consulte o log e confirme os pré-requisitos do WSL."
                        )
                        self.status.configure(text="Build interrompido ou com erro")
                        self._append_log(f"\n{message}")
                        messagebox.showerror("Build não concluído", message)
        except queue.Empty:
            pass
        self.after(100, self._drain_events)

    def _append_log(self, line: str) -> None:
        self.log.configure(state="normal")
        self.log.insert("end", line + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")


if __name__ == "__main__":
    SwitchBuilder().mainloop()
