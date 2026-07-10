#!/usr/bin/env python3
import sys
from db import (get_db_conn, search_by_address,
    search_by_name, delete_by_id, add_condominium)

conn = get_db_conn()

def get_valid_integer(prompt_message):
    while True:
        try:
            return int(input(prompt_message))
        except ValueError:
            print("Entrada inválida, o ID deve ser um número.")

def menu_search_by_address():
    search_term = input("Digite o endereço: ").strip().lower()
    for row in search_by_address(conn, search_term):
        print(f"| ID: {row[0]} | Nome: {row[1]} | Endereço: {row[2]} |")

def menu_search_by_name():
    search_term = input("Digite o nome: ").strip().lower()
    for row in search_by_name(conn, search_term):
        print(f"| ID: {row[0]} | Nome: {row[1]} | Endereço: {row[2]} |")

def menu_delete_by_id():
    condo_id = get_valid_integer("Digite o ID: ")
    deleted_item = delete_by_id(conn, condo_id)
    if not deleted_item:
        print("ID inválido. Verifique o número digitado.")
        return
    print(f"| ID: {deleted_item[0]} | Nome: {deleted_item[1]} | Endereço: {deleted_item[2]} |")


def menu_add_condominium():
    name = input("Digite o nome: ")
    address = input("Digite o endereço completo: ")
    new_item = add_condominium(conn, name, address)
    print(f"| ID: {new_item[0]} | Nome: {new_item[1]} | Endereço: {new_item[2]} |")

def menu_exit():
    sys.exit(0)

def main():
    try:
        menu_options = {
            '0': menu_exit,
            '1': menu_search_by_address,
            '2': menu_search_by_name,
            '3': menu_add_condominium,
            '4': menu_delete_by_id,
        }

        while True:
            print("\n--- PESQUISA CONDOMÍNIO ---")
            print("1. Buscar pelo endereço")
            print("2. Buscar pelo nome")
            print("3. Criar condomínio")
            print("4. Apagar condomínio")
            print("0. Sair")

            choice = input("Selecione a opção (0-4): ").strip()

            action = menu_options.get(choice)

            if action:
                    action()
            else:
                print("Opção inválida. Tente novamente.")
    except KeyboardInterrupt:
        menu_exit()

if __name__ == "__main__":
    main()
