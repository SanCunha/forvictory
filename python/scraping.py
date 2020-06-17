import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time
from itertools import chain

from db_connection import *
#--------------------------CONFIGURAÇÃO BANCO DE DADOS -----------------------------------------#
database = r"forvictory.db"

# create a database connection
conn = create_connection(database)

# create tables
if conn is not None:
    # create projects table
    create_table(conn, sql_create_leagues_table())

    # create tasks table
    create_table(conn, sql_create_teams_table())
else:
    print("Error! cannot create the database connection.")

#------------------------------------------LISTAS-------------------------------------------------------#
continentes = [] # lista para grupo de ligas
ligas = [] # lista o link das ligas
times = [] # lista para times
contador = 0 # contador de quantas ligas foram coletadas

inicio = time.time()

#------------------------------------LOCALIZANDO A PÁGINA-----------------------------------------------------------#
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'} # Necessário para o site aceitar o requerimento

page = requests.get("https://www.windrawwin.com/statistics/corners/", headers=headers)# busca o site

soup = BeautifulSoup(page.content, 'html.parser')
#----------------------------RECOLHENDO NOMES DE TODAS AS LIGAS------------------------------------------------------------#
banner_ligas = soup.find(id='featurefull') # seleciona a div
botao_ligas = banner_ligas.find(id='leaguenav') # seleciona o botão com as ligas
for group in botao_ligas.find_all('optgroup'): # adiciona no nome das ligas na lista
	continentes.append(group.get_attribute_list('label'))
	for row in group.find_all('option'):
		ligas.append(row.get_attribute_list('value')) # cria uma lista com listas unitárias
#del ligas[0:2] # concertando a lista de ligas

ligas = list(chain(*ligas)) # convertendo uma lista de listas em uma lista unitária

#-----------------------------------ALMA DO PROGRAMA----------------------------------------------------------------------#
for z in range(len(ligas)):
	pagina_atual = requests.get(ligas[z], headers=headers)
	soup = BeautifulSoup(pagina_atual.content, 'html.parser')
#----------------------------RECOLHENDO INFORMAÇÕES DA LIGA---------------------------------------------------------------#
	try:
		titulo_pag = soup.find(id='featurefull') # seleciona a div
		try:
			nome_liga = titulo_pag.find('h1').get_text().replace(" Corners Statistics", '') #retira o nome
			print(nome_liga)
		except AttributeError:
			print("Times da liga " + ligas[z] + " não foram coletados")
			continue
		else:
			if (nome_liga == "TEAMS INVOLVED IN GAMES WITH THE MOST CORNERS"):
				print(ligas[z] + ' com nome diferente da URL')
					
	#-------------------------------RECOLHENDO INFORMAÇÕES DOS TIMES---------------------------------------------------------------#
			tabela = soup.find("div", {"class":"wdwtablestt"}) # toda a tabela de dados
			if (type(tabela) != type(titulo_pag)):		
				print("Times da liga " + ligas[z] + " não foram coletados")
				continue
			else:
				media_for = 0
				media_agn = 0
				media_total = 0
				for row in tabela.find_all("div", {"class":"statln1"}):
					try:
						div_team = row.find("div", {"class":"wttd statteam stw325 st15"})
						name = div_team.get_text()
					except:
						try:
							div_team = row.find("div", {"class":"wttd statteam stw325 st13"})
							name = div_team.get_text()
						except:
							div_team = row.find("div", {"class":"wttd statteam stw325 st14"})
							name = div_team.get_text()

					div_for = row.find("div", {"class":"wttd statpld"})
					div_agn = row.find("div", {"class":"wttd statnum"})
					favor = float(div_for.get_text())
					contra = float(div_agn.get_text())
					total = float("{0:.2f}".format(favor + contra))

					media_for += favor
					media_agn += contra
					media_total += total	
					
					team = [name, favor, contra, total]
					times.append(team)

				media_for = float("{0:.2f}".format(media_for / len(times)))
				media_agn = float("{0:.2f}".format(media_agn / len(times)))
				media_total = float("{0:.2f}".format(media_total / len(times)))

				url = nome_liga.replace(" ","_").lower()
				league = (nome_liga, url, media_for, media_agn, media_total)

				with conn:
					id_league = create_leagues(conn, league)

					for teams in times:
						teams.append(id_league)

					for teams in times:
						id_team = create_teams(conn, teams)

				times.clear()

				contador += 1
				print("Times da liga " + ligas[z] + " foram coletados")
				

	except:
		print(ligas[z] + " ! Deu ruim")
		times.clear()
		break

fim = time.time()
print('Dados coletados com sucesso!\nTempo Gasto: ' + str(round((fim - inicio), 2)) + ' Segundos')
print(str(contador) + ' Ligas Coletadas!')
