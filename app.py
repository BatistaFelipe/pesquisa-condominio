#!/usr/bin/env python3
import sys

from db import (
    add_condominium,
    delete_by_id,
    get_db_conn,
    search_by_address,
    search_by_name,
    search_list_by_name,
)

conn = get_db_conn()

def get_valid_integer(prompt_message: str) -> int:
    while True:
        try:
            return int(input(prompt_message))
        except ValueError:
            print("Entrada inválida, o ID deve ser um número.")

def menu_search_by_address() -> None:
    search_term = input("Digite o endereço: ").strip().lower()
    for row in search_by_address(conn, search_term):
        print(f"| ID: {row[0]} | Nome: {row[1]} | Endereço: {row[2]} |")

def menu_search_by_name() -> None:
    search_term = input("Digite o nome: ").strip().lower()
    for row in search_by_name(conn, search_term):
        print(f"| ID: {row[0]} | Nome: {row[1]} | Endereço: {row[2]} |")

def menu_delete_by_id() -> None:
    condo_id = get_valid_integer("Digite o ID: ")
    deleted_item = delete_by_id(conn, condo_id)
    if not deleted_item:
        print("ID inválido. Verifique o número digitado.")
        return
    print(f"| ID: {deleted_item[0]} | Nome: {deleted_item[1]} | Endereço: {deleted_item[2]} |")


def menu_add_condominium() -> None:
    name = input("Digite o nome: ")
    address = input("Digite o endereço completo: ")
    new_item = add_condominium(conn, name, address)
    if new_item:
        print(f"| ID: {new_item[0]} | Nome: {new_item[1]} | Endereço: {new_item[2]} |")

def menu_search_list_by_name() -> None:
    search_list = input("Digite os nomes dos condomínios separados por [;]: ")
    list_names = search_list.split(";")
    for row in search_list_by_name(conn, list_names):
        print(f"| ID: {row[0]} | Nome: {row[1]} | Endereço: {row[2]} |")

def menu_exit() -> None:
    sys.exit(0)

def main() -> None:
    try:
        menu_options = {
            '0': menu_exit,
            '1': menu_search_by_address,
            '2': menu_search_by_name,
            '3': menu_add_condominium,
            '4': menu_delete_by_id,
            '5': menu_search_list_by_name,
        }

        while True:
            print("\n--- PESQUISA CONDOMÍNIO ---")
            print("1. Buscar pelo endereço")
            print("2. Buscar pelo nome")
            print("3. Criar condomínio")
            print("4. Apagar condomínio")
            print("5. Buscar lista pelo nome")
            print("0. Sair")

            choice = input("Selecione a opção (0-5): ").strip()

            action = menu_options.get(choice)

            if action:
                    action()
            else:
                print("Opção inválida. Tente novamente.")
    except KeyboardInterrupt:
        menu_exit()

if __name__ == "__main__":
    main()
