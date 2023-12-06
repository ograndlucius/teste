@echo off
color a
echo Ativando o ambiente virtual...
	call .\Scripts\activate.bat
echo Instalando todas as dependencias..
	pip install -r requirements.txt
echo Iniciando a interface de terminal...
	start cmd /k python terminal_interface.py
echo Iniciando o servidor FastAPI...
	uvicorn main:app --reload
