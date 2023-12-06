import subprocess
import json
from termcolor import colored
from colorama import Fore, Back, Style, init
init()

# LIMPAR OS COMANDOS APÓS A EXECUÇÃO DE OUTRO
def clear_terminal():
    subprocess.call('cls', shell=True)

# CORPO PRINCIPAL DO MENU
def show_menu():
    while True:
        print(Fore.MAGENTA + "=" * 62)
        print(Fore.YELLOW + "Escolha uma opção:")
        print(Fore.MAGENTA + "=" * 25 + Style.RESET_ALL + Fore.YELLOW + "(Estoque)" + Fore.MAGENTA + "=" * 25)
        print(Fore.GREEN + "1. Visualizar todos os itens no estoque")
        print("2. Visualizar detalhes de um item")
        print("3. Adicionar um novo item ao estoque")
        print("4. Atualizar informações de um item")
        print("5. Deletar um item do estoque")
        print(Fore.MAGENTA + "=" * 25 + Style.RESET_ALL + Fore.YELLOW + "(Usuários)" + Fore.MAGENTA + "=" * 25)
        print(Fore.GREEN + "6. Visualizar todos os usuários")
        print("7. Visualizar detalhes de um usuário")
        print("8. Adicionar um novo usuário")
        print("9. Deletar um usuário")
        print("10. Atualizar informações de um usuário")
        print("11. Fazer um pedido de compra")
        print(Fore.MAGENTA + "=" * 25 + Style.RESET_ALL + Fore.YELLOW + "(Operações)" + Fore.MAGENTA + "=" * 25)
        print(Fore.GREEN + "12. Relatório: Produtos Mais Vendidos")
        print("13. Relatório: Produtos Por Cliente")
        print("14. Relatório: Consumo Médio Por Cliente")
        print("15. Relatório: Produtos com Baixo Estoque")
        print(Fore.MAGENTA + "=" * 62 + Style.RESET_ALL)
        print(Fore.YELLOW + "16. Sair")
        print(Fore.MAGENTA + "=" * 62 + Style.RESET_ALL)

        choice = input("Digite o número da opção desejada: ")

        if choice == "1":
            clear_terminal()
            view_all_items()
        elif choice == "2":
            clear_terminal()
            view_item_details()
        elif choice == "3":
            clear_terminal()
            add_new_item()
        elif choice == "4":
            clear_terminal()
            update_item()
        elif choice == "5":
            clear_terminal()
            delete_item()
        elif choice == "6":
            clear_terminal()
            view_all_users()
        elif choice == "7":
            clear_terminal()
            view_user_details()
        elif choice == "8":
            clear_terminal()
            add_new_user()
        elif choice == "9":
            clear_terminal()
            delete_user()
        elif choice == "10":
            clear_terminal()
            update_user()
        elif choice == "11":
            clear_terminal()
            make_purchase()
        elif choice == "12":
            clear_terminal()
            generate_most_sold_report()
        elif choice == "13":
            clear_terminal()
            generate_product_by_customer_report()
        elif choice == "14":
            clear_terminal()
            generate_avg_consumption_report()
        elif choice == "15":
            clear_terminal()
            generate_low_stock_report()
        elif choice == "16":
            print("Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")

#VER TODOS OS ITENS DO ESTOQUE
def view_all_items():
    response = subprocess.check_output('http GET http://localhost:8000/estoque/', shell=True)
    display_response(response)

#VER ITEM POR ID
def view_item_details():
    item_id = input("\nDigite o ID do item para ver detalhes: ")
    response = subprocess.check_output(f'http GET http://localhost:8000/estoque/{item_id}', shell=True)
    display_response(response)

#ADICIONAR NOVO ITEM
def add_new_item():
    nome = input("\nDigite o nome do novo item: ")
    descricao = input("Digite a descrição: ")
    estoque = int(input("Digite a quantidade em estoque: "))
    preco = float(input("Digite o preço: "))

    response = subprocess.check_output(f'http POST http://localhost:8000/estoque/adicionar/ nome="{nome}" descricao="{descricao}" estoque:={estoque} preco:={preco}', shell=True)
    display_response(response)

#VER TODOS OS USUÁRIOS
def view_all_users():
    response = subprocess.check_output('http GET http://localhost:8000/usuarios/', shell=True)
    display_response(response)

#VER USUÁRIO POR ID
def view_user_details():
    user_id = input("\nDigite o ID do usuário para ver detalhes: ")
    response = subprocess.check_output(f'http GET http://localhost:8000/usuarios/{user_id}', shell=True)
    display_response(response)

#ADICIONAR NOVO USUÁRIO
def add_new_user():
    nome = input("\nDigite o nome do novo usuário: ")
    email = input("Digite o email: ")
    senha = input("Digite a senha: ")
    is_admin = input("O usuário é administrador? (True/False): ")

    response = subprocess.check_output(f'http POST http://localhost:8000/usuarios/adicionar/ nome="{nome}" email="{email}" senha="{senha}" is_admin={is_admin}', shell=True)
    display_response(response)

#FAZER O PEDIDO DE COMPRA
def make_purchase():
    user_id = int(input("\nDigite o ID do usuário: "))
    item_id = int(input("Digite o ID do item para compra: "))
    quantidade = int(input("Digite a quantidade desejada: "))

    response = subprocess.check_output(f'http POST http://localhost:8000/pedido/adicionar/{user_id} item_id={item_id} quantidade={quantidade}', shell=True)
    display_response(response)

    # Exibir o valor total de compra e a quantidade
    data = json.loads(response)
    if 'preco' in data and 'quantidade' in data:
        valor_total = data['preco'] * data['quantidade']
        print(f"Valor total da compra: R${valor_total}")
        print(f"Quantidade comprada: {data['quantidade']}")

# DELETAR UM ITEM DO ESTOQUE
def delete_item():
    item_id = input("\nDigite o ID do item que deseja deletar: ")
    response = subprocess.check_output(f'http DELETE http://localhost:8000/estoque/remove/{item_id}', shell=True)
    print("Item deletado com sucesso.")

# DELETAR UM USUÁRIO
def delete_user():
    user_id = input("\nDigite o ID do usuário que deseja deletar: ")
    response = subprocess.check_output(f'http DELETE http://localhost:8000/usuarios/remover/{user_id}', shell=True)
    print("Usuário deletado com sucesso.")

#RESPONSAVEL PELA FORMATAÇÃO DOS REPOSTAS JSON #
def display_response(response):
    data = json.loads(response)
    
    if isinstance(data, list):
        for item in data:
            print("=" * 25)
            for key, value in item.items():
                formatted_value = colored(value, 'yellow') if key == 'preco' else colored(value, 'green')
                print(f"{key.capitalize()}: {formatted_value}")
    else:
        print("=" * 25)
        for key, value in data.items():
            formatted_value = colored(value, 'yellow') if key == 'preco' else colored(value, 'green')
            print(f"{key.capitalize()}: {formatted_value}")
    print("=" * 25)
    
# ATUALIZAR INFORMAÇÕES DE UM ITEM
def update_item():
    item_id = input("\nDigite o ID do item que deseja atualizar: ")
    nome = input("Digite o novo nome (ou pressione Enter para manter o atual): ")
    descricao = input("Digite a nova descrição (ou pressione Enter para manter a atual): ")
    estoque = input("Digite a nova quantidade em estoque (ou pressione Enter para manter a atual): ")
    preco = float(input("Digite o novo preço (ou pressione Enter para manter o atual): "))

    url = f'http://localhost:8000/estoque/atualizar/{item_id}'

    params = {}
    if nome:
        params['nome'] = nome
    if descricao:
        params['descricao'] = descricao
    if estoque:
        params['estoque'] = int(estoque)
    if preco:
        params['preco'] = float(preco)

    response = subprocess.check_output(['http', 'PUT', url], input=json.dumps(params), text=True)
    print("Informações do item atualizadas com sucesso.")

# ATUALIZAR INFORMAÇÕES DE UM USUÁRIO
def update_user():
    user_id = input("\nDigite o ID do usuário que deseja atualizar: ")
    nome = input("Digite o novo nome (ou pressione Enter para manter o atual): ")
    email = input("Digite o novo email (ou pressione Enter para manter o atual): ")
    senha = input("Digite a nova senha (ou pressione Enter para manter a atual): ")
    is_admin = input("O usuário é administrador? (True/False, ou pressione Enter para manter o atual): ")

    url = f'http://localhost:8000/usuarios/atualizar/{user_id}'

    args = ['http', 'PUT', url]

    if nome:
        args.append(f'nome={nome}')
    if email:
        args.append(f'email={email}')
    if senha:
        args.append(f'senha={senha}')
    if is_admin:
        args.append(f'is_admin={is_admin}')

    response = subprocess.check_output(args, text=True)
    print("Informações do usuário atualizadas com sucesso.")

# Função para gerar relatório de produtos mais vendidos
def generate_most_sold_report():
    response = subprocess.check_output('http GET http://localhost:8000/relatorios/maisvendido/', shell=True)
    display_response(response)

# Função para gerar relatório de produtos por cliente
def generate_product_by_customer_report():
    response = subprocess.check_output('http GET http://localhost:8000/relatorios/produtocliente/', shell=True)
    display_response(response)

# Função para gerar relatório de consumo médio por cliente
def generate_avg_consumption_report():
    response = subprocess.check_output('http GET http://localhost:8000/relatorios/consumocliente/', shell=True)
    display_response(response)

# Função para gerar relatório de produtos com baixo estoque
def generate_low_stock_report():
    response = subprocess.check_output('http GET http://localhost:8000/relatorios/baixoestoque/', shell=True)
    display_response(response)


# RESPONSAVEL PELA FORMATAÇÃO DOS REPOSTAS JSON #
def display_response(response):
    data = json.loads(response)
    
    if isinstance(data, list):
        for item in data:
            print(Fore.MAGENTA + "=" * 62 + Style.RESET_ALL)
            for key, value in item.items():
                formatted_value = (
                    Fore.YELLOW + str(value) + Style.RESET_ALL if key == 'preco' else str(value)
                )
                print(f"{key.capitalize()}: {formatted_value}")
    else:
        print(Fore.MAGENTA + "=" * 62 + Style.RESET_ALL)
        for key, value in data.items():
            formatted_value = (
                Fore.YELLOW + str(value) + Style.RESET_ALL if key == 'preco' else str(value)
            )
            print(f"{key.capitalize()}: {formatted_value}")
        print(Fore.MAGENTA + "=" * 62 + Style.RESET_ALL)





if __name__ == "__main__":
    show_menu()