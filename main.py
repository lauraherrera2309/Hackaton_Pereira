import os, sys, time, json, subprocess
from tkinter import filedialog, Tk
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

import engine, report_gen

console = Console()

def check_data(): return os.path.exists("final_report.json")

def cleanup():
    if os.path.exists("final_report.json"): os.remove("final_report.json")
    console.print("[dim]  [*] Intelligence cache cleared. Cleanup complete.[/dim]")

def get_path():
    root = Tk(); root.withdraw(); root.attributes("-topmost", True)
    path = filedialog.asksaveasfilename(defaultextension=".pdf", initialfile="Audit_Report.pdf", title="Save Report")
    root.destroy(); return path

def show_header():
    os.system('clear')
    console.print("""
       ⢰⢏⣀⡀⠀⠠⡐⠬⠁⠐⠒⢈⢐⢄⠀⠀⠀⠀⠀⠀⠀
       ⠘⠷⢿⠟⠉⠀⠀⠀⡠⡰⠐⠉⠟⠇⢂⠀⠀⠀⠀⠀⠀
       ⠀⠀⠀⠀⢀⠒⠀⡭⠉⠝⡠⢊⠀⠤⠀⠀⠀⢹⠀⠀⠀⠀⠀⠀
       ⠀⠀⠀⠀⠸⠀⠀⣄⢂⡼⢋⡉⣉⣙⢡⣔⡠⠋⠀⠀⠀⠀⠀⠀
       ⠀⠀⠀⠀⠸⠀⠰⢁⠜⡇⡉⠾⠹⢩⠬⡟⡇⠀⠀⠀⠀⠀⠀⠀
       ⠀⠀⠀⠀⠀⠀⠢⢕⢧⡄⡇⠐⡦⣅⢦⣗⢱⠀⠀⠀⠀⠀⠀⠀
       ⠀⠀⠀⠀⠀⠀⠀⠀⢡⣀⠡⢀⡀⠀⣆⢀⠞⠀⠀⠀⠀⠀⠀⠀
       ⠀⠀⠀⠀⠀⠀⠀⠀⡘⡛⢸⣁⠄⡖⡾⣧⡀⠀⠀⠀⠀⠀⠀⠀
       ⠀⠀⠀⠀⠀⡠⣮⠁⠄⠃⠐⠅⡏⡈⣧⠁⢘⢕⡀⠀⠀⠀⠀⠀
       ⠀⠀⠀⠀⡘⣀⠀⠌⠄⡀⠀⢪⢴⣧⣿⡃⠀⢒⡈⢢⡀⠀⠀⠀
       ⠀⠀⠀⠀⢇⠏⠀⠈⢫⡃⣀⣈⠉⢀⡉⡍⢀⣉⢋⣀⠙⠔⢦⠀
       ⠀⠀⠀⠀⠀⠣⡀⠀⠀⠊⢄⠣⠀⢉⠀⠀⠀⡄⡀⡶⠀⠘⢁⠇
       ⠀⠀⠀⠀⠀⠀⠈⠢⡀⠀⠀⠀⠀⢸⠀⠤⠀⡿⠍⠀⠀⢠⠎⠀
       ⠀⠀⠀⠀⠀⠀⠀⠀⠈⢦⠤⠤⠄⢸⠀⠀⢀⠃⠩⠴⢀⠎⠀⠀
       ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢄⠀⠀⠀⠈⠐⠈⠀⠀⡗⠉⠀⠀⠀
       ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⠀⠀⠀⠀⠀⠀⠀⠇⠀⠀⠀⠀
       ⢀⠄⠠⠄⡀⠀⠀⠀⠀⠀⠀⠆⠀⠀⠀⠀⠀⢠⠝⠀⠀⠀⠀⠀
       ⠈⠺⣍⠐⢄⠁⠒⠀⠀⠐⠊⠀⠀⠀⠀⢀⠤⠊⠀⠀⠀⠀⠀⠀
       ⠀⠀⠈⠀⠀⠑⠠⣀⠀⠀⠀⢀⣀⠤⠒⠁⠀⠀⠀⠀⠀⠀⠀⠀
    """, style="bold cyan")
    console.print(Panel("[bold white]TLS AKINATOR v1.0[/bold white]\n[dim]Web Defense Operation - Universidad Nacional de Colombia[/dim]", border_style="blue", expand=False))

def main():
    proc = None
    while True:
        show_header()
        ready = check_data()
        active = proc and proc.poll() is None
        
        table = Table(show_header=False, border_style="dim")
        table.add_column("Op", style="cyan"); table.add_column("Action"); table.add_column("Status")
        
        if active:
            table.add_row("[ ]", "Individual Analysis", "[bold red]BLOCKED[/bold red]", style="dim")
            table.add_row("[ ]", "Batch Analysis", "[bold red]BLOCKED[/bold red]", style="dim")
            table.add_row("[ ]", "Launch Web Dashboard", "[bold red]ALREADY RUNNING[/bold red]", style="dim")
            table.add_row("[ ]", "Generate Executive PDF", "[bold red]BLOCKED[/bold red]", style="dim")
            table.add_row("[s]", "STOP Web Dashboard Server", "[bold yellow]ACTIVE[/bold yellow]", style="yellow")
            table.add_row("[ ]", "Exit System (Stop server first)", "[bold red]LOCKED[/bold red]", style="dim")
            console.print(table)
            choice = Prompt.ask("\n>> Select operation [s]", choices=["s"], default="s")
        else:
            table.add_row("[1]", "Individual Analysis", "[bold green]READY[/bold green]")
            table.add_row("[2]", "Batch Analysis (targets.txt)", "[bold green]READY[/bold green]")
            c3, c4 = ("magenta", "white") if ready else ("red", "red")
            s3 = "[bold green]READY[/bold green]" if ready else "[bold red]LOCKED[/bold red]"
            table.add_row("[3]", "Launch Web Dashboard (Streamlit)", s3, style=c3)
            table.add_row("[4]", "Generate & Save Executive PDF", s3, style=c4)
            table.add_row("[q]", "Exit System & Cleanup", "[bold cyan]EXIT[/bold cyan]")
            console.print(table)
            choice = Prompt.ask("\n>> Select operation [1/2/3/4/q]", choices=["1", "2", "3", "4", "q"], default="1")

        if choice == "s":
            if proc: proc.terminate()
            console.print("\n[yellow][!] Server stopped.[/yellow]"); time.sleep(1); continue
        if choice == "q": cleanup(); break
        
        if choice in ["3", "4"] and not ready:
            console.print("\n[bold red][!] Intelligence missing.[/bold red]"); time.sleep(2); continue

        if choice == "1":
            t = Prompt.ask("\n[bold cyan]Target[/bold cyan]")
            with console.status(f"Scanning {t}..."):
                res = engine.full_extraction_pipeline(t)
                with open("final_report.json", "w") as f: json.dump([res], f, indent=4)
        elif choice == "2":
            if not os.path.exists("targets.txt"): console.print("[red]Missing targets.txt[/red]")
            else:
                with open("targets.txt", "r") as f: tgs = [l.strip() for l in f if l.strip()]
                res_list = []
                with Progress(SpinnerColumn(), "{task.description}", console=console) as pr:
                    for t in tgs:
                        pr.add_task(description=f"Scanning {t}...", total=None)
                        res_list.append(engine.full_extraction_pipeline(t))
                with open("final_report.json", "w") as f: json.dump(res_list, f, indent=4)
        elif choice == "3":
            proc = subprocess.Popen(["streamlit", "run", "app.py"], stdout=subprocess.DEVNULL)
        elif choice == "4":
            p = get_path()
            if p: report_gen.generate_pdf_report("final_report.json", p)

if __name__ == "__main__":
    main()
