from dotenv import load_dotenv
load_dotenv()  # Load before importing for the imports to indeed use the environment variables

from Modulos.menus import main_menu
import typer
from rich import print
import time
from logging_config import set_up_logger

logger = set_up_logger(__name__, file_name="app_life_time.log")

def main():
    logger.info("Program has been started")
    
    print("[bold]Sabemos que hay que poner el `.env` y los logs en el `.gitignore` por seguridad, " \
    "solo que por facilidad de calificacion, lo dejamos ahi[/bold]")
    time.sleep(3)

    start_time = time.perf_counter()

    try:
        while True:
            main_menu()
    except typer.Exit:
        logger.info(f"Program ended, time spent: {format(time.perf_counter() - start_time, '.3f')} seconds")
        print(f"[bold green]Salida exitosa[/bold green]")


if __name__ == "__main__":
    typer.run(main)