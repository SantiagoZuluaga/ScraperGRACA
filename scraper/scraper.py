import json
import pandas as pd
import xlsxwriter
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class Scraper:

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.grupos = [
            "saber-pro", 
            "graca-lenguas", 
            "trabajo-social", 
            "aulas-de-lecturas", 
            "graca-sociologia", 
            "graca-administracion", 
            "graca-fai", 
            "graca-ciencias", 
            "graca-ingenieria", 
            "graca-salud"]

    def login(self):
        self.driver = webdriver.Chrome(executable_path=r'E:\Santiago\Proyectos\Python\Drivers\chromedriver.exe')
        self.driver.get("https://graca.site")
        loginbutton = self.driver.find_element_by_xpath("/html/body/div/div/div/div[2]/div[2]/div/div/a[1]")
        loginbutton.click()
        self.driver.implicitly_wait(10)
        emailinput = self.driver.find_element_by_xpath("//*[@id='identifierId']")
        emailinput.send_keys(self.email)
        nextbutton = self.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button")
        nextbutton.click()
        self.driver.implicitly_wait(10)
        passwordinput = self.driver.find_element_by_name("password")
        passwordinput.send_keys(self.password)
        nextbutton = self.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button")
        nextbutton.click()
        while self.driver.current_url != "https://graca.site/home#" :
            pass

    def getTutores(self):

        url = "https://graca.site/miembros/"

        data = []

        for grupo in self.grupos:
            print(grupo)

            self.driver.get(url + grupo)

            tutores = self.driver.find_elements_by_xpath('//*[@id="tabla"]/tbody/tr')

            for i in range(0, len(tutores)):

                estado = self.driver.find_element_by_xpath('//*[@id="tabla"]/tbody/tr[' + str(i+1) + ']/td[4]').text
                if estado == "Activo":
                    nombre = self.driver.find_element_by_xpath('//*[@id="tabla"]/tbody/tr[' + str(i+1) + ']/td[2]').text
                    email = self.driver.find_element_by_xpath('//*[@id="tabla"]/tbody/tr[' + str(i+1) + ']/td[3]').text
                    print(nombre, email, estado)

                    flag = False
                    for i in range(0, len(data)):

                        if data[i]["email"] == email:
                            flag = True
                            break
                    
                    if flag == False:
                        data.append({
                            "nombre": nombre,
                            "email": email
                        })

        self.driver.close()

        with open("tutores.json", "w", encoding='utf8') as jsonfile:
            json.dump(data, jsonfile, ensure_ascii=False)     

    
    def getEstudiantes(self, grupo):
        
        self.estudiantes = []

        estudiantes = pd.read_csv('./scraper/data/' + grupo + '.csv')
        nombres = estudiantes['Nombre beneficiario']
        temp = []

        for i in range (0, len(nombres)):

            flag = False 

            for j in range (0, len(temp)):
                if nombres[i] == temp[j]:
                    flag = True

            if flag == False:
                temp.append(nombres[i])

        nombres = temp

        for i in range (0, len(nombres)):
            self.driver.get("https://graca.site/personas")
            self.driver.implicitly_wait(10)
            searchinput = self.driver.find_element_by_xpath('//*[@id="app-layout"]/div/div/div/div[2]/div[2]/form/div[1]/input')
            searchinput.send_keys(nombres[i])
            searchbutton = self.driver.find_element_by_xpath('//*[@id="app-layout"]/div/div/div/div[2]/div[2]/form/span/button')
            searchbutton.click()
            self.driver.implicitly_wait(10)
            estudiante = self.driver.find_element_by_xpath('//*[@id="app-layout"]/div/div/div/div[2]/div[2]/div/div/table/tbody/tr/td[8]/a/span')
            estudiante.click()   
            self.driver.implicitly_wait(10)   
            estudiantejson = {
                "nombre": self.driver.find_element_by_xpath('//*[@id="app-layout"]/div/div[1]/div[2]/div[2]/div[2]/form/div[1]/div[1]/div/input').get_attribute("value"),
                "codigo": self.driver.find_element_by_xpath('//*[@id="datosEstudiante"]/div[2]/div[1]/div/input').get_attribute("value"),
                "programa": self.driver.find_element_by_xpath('//*[@id="datosEstudiante"]/div[2]/div[3]/div/div/button/span[1]').text,
                "facultad": self.driver.find_element_by_xpath('//*[@id="datosEstudiante"]/div[2]/div[2]/div/div/button/span[1]').text,
                "caracteristica": self.driver.find_element_by_xpath('//*[@id="datosEstudiante"]/div[3]/div[1]/div/div/button/span[1]').text,
            }      
            print(estudiantejson)
            self.estudiantes.append(estudiantejson)

        self.driver.close()

        self.outWorkbook = xlsxwriter.Workbook('./scraper/outputs/' + grupo + '.xlsx')
        worksheet =  self.outWorkbook.add_worksheet("Estudiantes")
        worksheet.write("A1", "Nombre")
        worksheet.write("B1", "Codigo")
        worksheet.write("C1", "Programa")
        worksheet.write("D1", "Facultad")
        worksheet.write("E1", "Caracteristica")

        for i in range (0, len(self.estudiantes)):
            worksheet.write("A" + str(i+2), self.estudiantes[i]["nombre"])
            worksheet.write("B" + str(i+2), self.estudiantes[i]["codigo"])
            worksheet.write("C" + str(i+2), self.estudiantes[i]["programa"])
            worksheet.write("D" + str(i+2), self.estudiantes[i]["facultad"])
            worksheet.write("E" + str(i+2), self.estudiantes[i]["caracteristica"])

        self.outWorkbook.close()
