from Modulos.base_de_datos import registered_pets, query_by_pet
from Modulos.clean_terminal import limpiar_terminal
from Modulos.checker import check_valid_option
from Modulos.menus import main_menu
import pyfiglet
import typer
from rich import print
from rich.table import Table
import time
from logging_config import set_up_logger
from dotenv import load_dotenv

load_dotenv()

logger = set_up_logger(__name__, file_name="app_life_time.log")

def main():
    logger.info("Program has been started")
    
    print("[bold]Sabemos que hay que poner el `.env` en el `.gitignore`, " \
    "solo que por facilidad de calificacion, lo dejamos ahi[/bold]")
    time.sleep(3)

    start_time = time.perf_counter()

    try:
        while True:
            main_menu()
    except typer.Exit as e:
        logger.info(f"Program ended, time spent: {format(time.perf_counter() - start_time, '.3f')} seconds")
        print(f"[bold green]Salida exitosa[/bold green]")


if __name__ == "__main__":
    typer.run(main)