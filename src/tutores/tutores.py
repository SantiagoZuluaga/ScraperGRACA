import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class Tutores:
    def __init__(self, driver):
        self.driver = driver
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

        with open("./src/tutores/tutores.json", "w", encoding='utf8') as jsonfile:
            json.dump(data, jsonfile, ensure_ascii=False)    