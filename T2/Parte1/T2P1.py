#Tarefa 2 Parte 1 - Laércio Silva de Campos Júnior

import xml.etree.ElementTree as ET
import os
import sys
from os.path import basename
from colorama import init, Fore, Back, Style 
from xml.dom import minidom

init(convert=True)

aplicacoes = []
todas_permissoes = []
permissoes_comuns = []
permissoes_exclusivas = []

def parsearDiretorio(dir_init): #Função para percorrer o diretório em busca dos arquivos

	print(Fore.BLACK+Back.RED+"PERMISSÕES POR APLICAÇÃO:"+Style.RESET_ALL)
	for file in os.listdir(dir_init): #Para cada arquivo
		aplicacao = file.split("_")[1].split(".xml")[0].replace("-"," ") #Recupera o nome da app
		print("")
		print(Fore.BLACK+Back.RED+aplicacao+Style.RESET_ALL)
		fileCompleto = os.path.join(dir_init, file) #Determina o caminho completo
		xml = minidom.parse(fileCompleto) #Le o arquivo XML
		items = xml.getElementsByTagName('uses-permission') #Busca as permissoes
		for i in items:
			permissao = i.attributes['android:name'].value 
			print("   "+Fore.RED+Back.BLACK+permissao+ " " + Style.RESET_ALL)
			if(aplicacao not in aplicacoes): #Verifica se app esta presenta na lista de de apps
				aplicacoes.append(aplicacao)
			todas_permissoes.append({"aplicacao": aplicacao, "permissao": permissao}) #Inclui a permissao na lista de todas as permissoes


def verificarPermissoes(): #Funçao para popular as permissoes comuns e exclusivas
	for p in todas_permissoes: #Para cada permissao de todas as permissoes ...
		for a in aplicacoes: #Em cada aplicacao da lista de aplicacoes 
			if(a != p["aplicacao"]): #Que nao seja a aplicacao originaria da permissao
				if({'aplicacao': a, 'permissao': p["permissao"]} in todas_permissoes): #Verifica se existe na lista de permissoes 
					ret = True
				else:
					ret = False
					break
		if(ret == True):
			if(p["permissao"] not in permissoes_comuns):
				permissoes_comuns.append(p["permissao"])
			
		#Verifica permissões exclusivas
		for a in aplicacoes:
			#print(p)
			if(a != p["aplicacao"]):
				if({'aplicacao': a, 'permissao': p["permissao"]} not in todas_permissoes):
					ret = True #Não existe essa permissão em outra aplicação
					#print(p["permissao"] + " não está presente em " + a)
				else:
					ret = False #Existe essa permissão em outra aplicação
					#print(p["permissao"] + " está presente em " + a)
					break
		if(ret == True):
			if(p["permissao"] not in permissoes_comuns):
				permissoes_exclusivas.append({"aplicacao": p["aplicacao"], "permissao": p["permissao"]})
			#print(p["permissao"] + " É EXCLUSIVA À " + p["aplicacao"] + " ")
	print("")
	print("")
	print(Fore.BLACK+Back.GREEN+"PERMISSÕES EXCLUSIVAS:"+Style.RESET_ALL)
	print("")
	for p in permissoes_exclusivas:
		print("   "+Fore.BLACK+Back.GREEN+p["aplicacao"]+ Style.RESET_ALL + " " + Fore.GREEN+Back.BLACK + p["permissao"] + " " + Style.RESET_ALL)
	print("")
	print("")
	print(Fore.BLACK+Back.YELLOW+"PERMISSÕES COMUNS:"+Style.RESET_ALL)
	print("")
	for p in permissoes_comuns:
		print("   "+Fore.BLACK+Back.YELLOW+p + " " + Style.RESET_ALL)

if __name__ == '__main__':
	diretorio = sys.argv[1]
	#diretorio = "F:\\Mestrado\\Ciência de Dados\\Pratica 2\\Laércio\\Manifest\\"
	parsearDiretorio(diretorio)
	verificarPermissoes()