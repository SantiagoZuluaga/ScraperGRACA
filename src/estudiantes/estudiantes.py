import json
import xlsxwriter
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class Estudiantes:
    def __init__(self, driver):
        self.driver = driver

    def getDataEstudiante(self):
        estudiantejson = {
            "nombre": self.driver.find_element_by_xpath('//*[@id="app-layout"]/div/div[1]/div[2]/div[2]/div[2]/form/div[1]/div[1]/div/input').get_attribute("value"),
            "codigo": self.driver.find_element_by_xpath('//*[@id="datosEstudiante"]/div[2]/div[1]/div/input').get_attribute("value"),
            "programa": self.driver.find_element_by_xpath('//*[@id="datosEstudiante"]/div[2]/div[3]/div/div/button/span[1]').text,
            "facultad": self.driver.find_element_by_xpath('//*[@id="datosEstudiante"]/div[2]/div[2]/div/div/button/span[1]').text,
            "caracteristica": self.driver.find_element_by_xpath('//*[@id="datosEstudiante"]/div[3]/div[1]/div/div/button/span[1]').text,
        } 

        return estudiantejson

    
    def getAllEstudiantes(self):

        data = []
        flag = True
        index = 1

        while index < 3:
            self.driver.get("https://graca.site/personas?page=" + str(index))
            self.driver.implicitly_wait(10)

            estudiantes = self.driver.find_elements_by_xpath('//*[@id="app-layout"]/div/div/div/div[2]/div[2]/div/div/table/tbody/tr')

            if len(estudiantes) > 0:
                for i in range (0, len(estudiantes)):

                    state = self.driver.find_element_by_xpath('//*[@id="app-layout"]/div/div/div/div[2]/div[2]/div/div/table/tbody/tr['+str(i+1)+']/td[7]/span').text
                    if state == "Activo":
                        self.driver.find_element_by_xpath('//*[@id="app-layout"]/div/div/div/div[2]/div[2]/div/div/table/tbody/tr['+str(i+1)+']/td[8]/a').send_keys(Keys.CONTROL + Keys.ENTER)
                        self.driver.switch_to.window(self.driver.window_handles[1])
                        self.driver.implicitly_wait(10)
                        if self.driver.find_element_by_xpath("//*[@id='estudiante']").get_attribute("checked"):
                            data.append(self.getDataEstudiante())

                        self.driver.close()
                        self.driver.switch_to.window(self.driver.window_handles[0])

                index = index + 1
            else:
                flag = False

        self.driver.close()

        with open("./src/estudiantes/outputs/estudiantes.json", "w", encoding='utf8') as jsonfile:
            json.dump(data, jsonfile, ensure_ascii=False)  



    def getEstudiantesFromExcel(self, grupo):

        data = []

        estudiantes = pd.read_csv('./src/estudiantes/data/' + grupo + '.csv')
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
            data.append(self.getDataEstudiante())

        self.driver.close()

        with open("./src/estudiantes/outputs/estudiantes.json", "w", encoding='utf8') as jsonfile:
            json.dump(data, jsonfile, ensure_ascii=False)


    def writeEstudiantesInExcel(self):
        with open("./src/estudiantes/outputs/estudiantes.json") as jsonfile:
            self.estudiantes = json.load(jsonfile)
        self.outWorkbook = xlsxwriter.Workbook('./src/estudiantes/outputs/estudiantes.xlsx')
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
