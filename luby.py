import os
import argparse
import importlib
from flask import Flask, Blueprint

# ANSI Cores
RESET = "\033[0m"
VERDE = "\033[92m"
VERMELHO = "\033[91m"
AZUL = "\033[94m"
AMARELO = "\033[93m"

caminho = os.getcwd() #os.path.dirname(__file__)

def bprint(text: str):
    print(f"{VERDE}[+] {text}{RESET}")

def eprint(text: str):
    print(f"{VERMELHO}[!] {text}{RESET}")

def okprint(text: str):
    print(f"{AZUL}[✔] {text}{RESET}")

def wprint(text: str):
    print(f"{AMARELO}[?] {text}{RESET}")

def start_app():
    pastas = {
        "routes": "routes",
        "static": "static",
        "css": "static/css",
        "js": "static/js",
        "uploads": "static/uploads",
        "img": "static/img"
    }

    files = {
        "app.py": """import os
import importlib
from flask import Flask, Blueprint

app = Flask(__name__)
app.secret_key = "mdmdln s asdasnjçasn s asdsnasdfsd"
app.debug = True

def register_blueprints(app):
    routes_dir = os.path.join(os.path.dirname(__file__), "routes")
    routes = [name for name in os.listdir(routes_dir)
              if os.path.isdir(os.path.join(routes_dir, name))
              and "__init__.py" in os.listdir(os.path.join(routes_dir, name))]

    for route in routes:
        try:
            module = importlib.import_module(f"routes.{route}")
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, Blueprint):
                    app.register_blueprint(attr)
                    break
        except Exception as e:
            pass

register_blueprints(app)
""",
        "models.py": "# Arquivo de Models",
        f"{pastas['routes']}/__init__.py": "# So para ser considerado um pacote python",
        f"{pastas['css']}/base.css": "/* Codigo Css do app */",
        f"{pastas['js']}/app.js": "// Script js para o app",
        "requeriments.txt": "flask\npeewee"
    }

    create = False
    for n, p in pastas.items():
        dir_path = os.path.join(caminho, p)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
            create = True

    if create:
        for file, content in files.items():
            file_path = os.path.join(caminho, file)
            if not os.path.exists(file_path):
                with open(file_path, "w") as arq:
                    arq.write(content)

    okprint("Projeto iniciado com sucesso.")

def create_app(nome: str):
    _base = os.path.join(caminho, "routes")
    module_path = os.path.join(_base, nome)

    if not os.path.exists(module_path):
        os.makedirs(os.path.join(module_path, "templates"), exist_ok=True)
        with open(os.path.join(module_path, "__init__.py"), "w") as arq:
            arq.write(f"""import os
from flask import (
    Blueprint,
    request,
    url_for,
    redirect,
    session,
    render_template
)

{nome} = Blueprint(
    "{nome}",
    __name__,
    url_prefix="/{nome}",
    template_folder=os.path.join(os.path.dirname(__file__), "templates")
)
""")
        okprint(f"Módulo '{nome}' criado com sucesso.")
    else:
        eprint(f"Módulo '{nome}' já existe.")

def main():
    parser = argparse.ArgumentParser(
        description=f"{AMARELO}Gerador de projeto Flask - Ricardo Cayoca{RESET}"
    )
    subparsers = parser.add_subparsers(dest="command")

    # Subcomando: start
    subparsers.add_parser("start", help="Cria a estrutura básica do projeto")

    # Subcomando: create
    create_parser = subparsers.add_parser("create", help="Cria um novo módulo de rotas")
    create_parser.add_argument("nome", help="Nome do módulo")

    args = parser.parse_args()

    if args.command == "start":
        start_app()
    elif args.command == "create":
        create_app(args.nome)
    else:
        parser.print_help()
        print(f"""\n{AMARELO}Desenvolvido por Ricardo Cayoca{RESET} — v0.0.1""")

if __name__ == "__main__":
    main()
