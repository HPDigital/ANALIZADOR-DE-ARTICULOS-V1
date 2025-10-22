import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from pathlib import Path
from typing import Optional

from .config import load_env, get_openai_api_key
from .pdf_reader import leer_pdf, truncar_texto
from .analyzer import analizar_documento, DEFAULT_MODEL


class AnalizadorGUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Analizador de Artículos - OpenAI")
        self.root.minsize(900, 600)

        # Variables de estado
        self.var_pdf = tk.StringVar()
        self.var_model = tk.StringVar(value=DEFAULT_MODEL)
        self.var_max_chars = tk.IntVar(value=30000)
        self.var_max_tokens = tk.StringVar(value="")  # vacío = None
        self.var_env_path = tk.StringVar(value="")
        self.var_use_env_key = tk.BooleanVar(value=True)
        self.var_api_key = tk.StringVar(value="")

        self._build_ui()

    def _build_ui(self) -> None:
        container = ttk.Frame(self.root, padding=10)
        container.pack(fill=tk.BOTH, expand=True)

        # Panel superior de opciones
        opts = ttk.LabelFrame(container, text="Opciones")
        opts.pack(fill=tk.X)

        # Fila PDF
        row_pdf = ttk.Frame(opts)
        row_pdf.pack(fill=tk.X, pady=4)
        ttk.Label(row_pdf, text="PDF:").pack(side=tk.LEFT)
        ent_pdf = ttk.Entry(row_pdf, textvariable=self.var_pdf)
        ent_pdf.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=6)
        ttk.Button(row_pdf, text="Seleccionar...", command=self._select_pdf).pack(side=tk.LEFT)

        # Fila modelo y límites
        row_params = ttk.Frame(opts)
        row_params.pack(fill=tk.X, pady=4)
        ttk.Label(row_params, text="Modelo:").pack(side=tk.LEFT)
        ttk.Entry(row_params, width=20, textvariable=self.var_model).pack(side=tk.LEFT, padx=6)

        ttk.Label(row_params, text="Max chars:").pack(side=tk.LEFT, padx=(12, 0))
        sp_chars = ttk.Spinbox(row_params, from_=1000, to=500000, increment=1000, textvariable=self.var_max_chars, width=10)
        sp_chars.pack(side=tk.LEFT, padx=6)

        ttk.Label(row_params, text="Max tokens (salida):").pack(side=tk.LEFT, padx=(12, 0))
        ttk.Entry(row_params, width=10, textvariable=self.var_max_tokens).pack(side=tk.LEFT, padx=6)

        # Fila .env y API key
        row_env = ttk.Frame(opts)
        row_env.pack(fill=tk.X, pady=4)
        ttk.Label(row_env, text=".env (opcional):").pack(side=tk.LEFT)
        ent_env = ttk.Entry(row_env, textvariable=self.var_env_path)
        ent_env.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=6)
        ttk.Button(row_env, text="Buscar .env", command=self._select_env).pack(side=tk.LEFT)

        row_key = ttk.Frame(opts)
        row_key.pack(fill=tk.X, pady=4)
        chk = ttk.Checkbutton(row_key, text="Usar OPENAI_API_KEY del entorno", variable=self.var_use_env_key, command=self._toggle_key_entry)
        chk.pack(side=tk.LEFT)
        ttk.Label(row_key, text="API key (opcional):").pack(side=tk.LEFT, padx=(12, 0))
        self.ent_key = ttk.Entry(row_key, textvariable=self.var_api_key, show="*")
        self.ent_key.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=6)
        self._toggle_key_entry()

        # Botones de acción
        actions = ttk.Frame(container)
        actions.pack(fill=tk.X, pady=(8, 4))
        self.btn_analyze = ttk.Button(actions, text="Analizar", command=self._on_analyze)
        self.btn_analyze.pack(side=tk.LEFT)

        ttk.Button(actions, text="Guardar resultado", command=self._save_output).pack(side=tk.LEFT, padx=8)
        ttk.Button(actions, text="Limpiar", command=self._clear_output).pack(side=tk.LEFT)

        # Barra de progreso y estado
        status = ttk.Frame(container)
        status.pack(fill=tk.X, pady=(2, 6))
        self.prog = ttk.Progressbar(status, mode="indeterminate")
        self.prog.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.var_status = tk.StringVar(value="Listo")
        ttk.Label(status, textvariable=self.var_status).pack(side=tk.RIGHT)

        # Salida de texto
        out_frame = ttk.LabelFrame(container, text="Resultado del análisis")
        out_frame.pack(fill=tk.BOTH, expand=True)
        self.txt_out = tk.Text(out_frame, wrap=tk.WORD)
        self.txt_out.pack(fill=tk.BOTH, expand=True)

    def _toggle_key_entry(self) -> None:
        state = tk.DISABLED if self.var_use_env_key.get() else tk.NORMAL
        self.ent_key.configure(state=state)

    def _select_pdf(self) -> None:
        path = filedialog.askopenfilename(title="Seleccionar PDF", filetypes=[("PDF", "*.pdf")])
        if path:
            self.var_pdf.set(path)

    def _select_env(self) -> None:
        path = filedialog.askopenfilename(title="Seleccionar archivo .env", filetypes=[(".env", ".env"), ("Todos", "*.*")])
        if path:
            self.var_env_path.set(path)

    def _save_output(self) -> None:
        content = self.txt_out.get("1.0", tk.END).strip()
        if not content:
            messagebox.showinfo("Guardar", "No hay contenido para guardar.")
            return
        out = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Texto", "*.txt"), ("Markdown", "*.md"), ("Todos", "*.*")])
        if out:
            Path(out).write_text(content, encoding="utf-8")
            messagebox.showinfo("Guardar", f"Resultado guardado en:\n{out}")

    def _clear_output(self) -> None:
        self.txt_out.delete("1.0", tk.END)
        self.var_status.set("Listo")

    # Lógica de análisis en thread para no bloquear la UI
    def _on_analyze(self) -> None:
        pdf = self.var_pdf.get().strip()
        if not pdf:
            messagebox.showerror("Error", "Selecciona un archivo PDF.")
            return
        if not Path(pdf).exists():
            messagebox.showerror("Error", "La ruta del PDF no existe.")
            return

        # Deshabilitar botón y arrancar progreso
        self.btn_analyze.configure(state=tk.DISABLED)
        self.prog.start(10)
        self.var_status.set("Analizando…")

        t = threading.Thread(target=self._analyze_worker, daemon=True)
        t.start()

    def _resolve_api_key(self) -> Optional[str]:
        env_path = self.var_env_path.get().strip() or None
        load_env(env_path)
        if self.var_use_env_key.get():
            return get_openai_api_key()
        # Manual override
        key = self.var_api_key.get().strip()
        return key or None

    def _analyze_worker(self) -> None:
        try:
            api_key = self._resolve_api_key()
            if not api_key:
                raise RuntimeError("No se encontró OPENAI_API_KEY. Define en .env o escribe la clave.")

            pdf_path = self.var_pdf.get().strip()
            model = self.var_model.get().strip() or DEFAULT_MODEL

            try:
                max_tokens_val = int(self.var_max_tokens.get().strip()) if self.var_max_tokens.get().strip() else None
            except ValueError:
                raise RuntimeError("Max tokens debe ser un número entero o vacío.")

            # Leer y truncar
            texto = leer_pdf(pdf_path)
            texto = truncar_texto(texto, int(self.var_max_chars.get()))

            # Llamada a OpenAI
            resultado = analizar_documento(
                contenido=texto,
                api_key=api_key,
                model=model,
                max_tokens=max_tokens_val,
            )

            self._set_output(resultado)
            self._set_status("Completado")
        except Exception as e:
            self._set_output("")
            self._show_error(str(e))
            self._set_status("Error")
        finally:
            self._reset_progress()

    # Métodos seguros para actualizar UI desde el thread
    def _set_output(self, text: str) -> None:
        def do():
            self.txt_out.delete("1.0", tk.END)
            if text:
                self.txt_out.insert(tk.END, text)
        self.root.after(0, do)

    def _set_status(self, text: str) -> None:
        self.root.after(0, lambda: self.var_status.set(text))

    def _reset_progress(self) -> None:
        def do():
            self.prog.stop()
            self.btn_analyze.configure(state=tk.NORMAL)
        self.root.after(0, do)

    def _show_error(self, msg: str) -> None:
        self.root.after(0, lambda: messagebox.showerror("Error", msg))


def main() -> int:
    root = tk.Tk()
    # ttk theme por defecto
    try:
        style = ttk.Style()
        if "vista" in style.theme_names():
            style.theme_use("vista")
    except Exception:
        pass
    AnalizadorGUI(root)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

