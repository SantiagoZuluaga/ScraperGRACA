import json
import xlsxwriter 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class ScraperGRACA(object):

    def saveDatosActividad(self, grupo, tipoactividad, actividadnumero, actividadobjetivo, sesionnumero, sesionfecha):
        
        informacion = self.driver.find_element_by_xpath('//*[@id="app-layout"]/div/div[1]/div[2]/div[2]/div[2]/div[1]').text
        temporal = informacion.split("Observaciones:")

        if len(temporal) > 1 :
            observaciones = temporal[1].split("Descripcion:")[0]
            nropalabrasobservaciones = len(observaciones.split(" "))
        else :
            observaciones = ""
            nropalabrasobservaciones = 0

        temporal = informacion.split("Descripcion:")
        if len(temporal) > 1 :
            descripcion = temporal[1].split("Solicitante:")[0]
            nropalabrasdescripcion = len(descripcion.split(" "))
        else :
            descripcion = ""
            nropalabrasdescripcion = 0

        temporal = informacion.split("Dificultades:")
        if len(temporal) > 1 :
            dificultades = temporal[1].split("Acuerdo:")[0]
            nropalabrasdificultades = len(dificultades.split(" "))
        else :
            dificultades = ""
            nropalabrasdificultades = 0

        temporal = informacion.split("Acuerdo:")
        if len(temporal) > 1 :
            acuerdo = temporal[1]
            nropalabrasacuerdo = len(acuerdo.split(" "))
        else :
            acuerdo = ""
            nropalabrasacuerdo = 0

        actividad = {
            "Grupo": self.data["grupos"][grupo]["name"],
            "NroActividad": actividadnumero,
            "Objetivo": actividadobjetivo,
            "NroSesion": sesionnumero,
            "Fecha": sesionfecha,
            "Observaciones": observaciones,
            "Descripcion": descripcion,
            "Dificultades": dificultades,
            "Acuerdo": acuerdo,
            "NroPalabrasObservaciones": nropalabrasobservaciones,
            "NroPalabrasDescripcion": nropalabrasdescripcion,
            "NroPalabrasDificultades": nropalabrasdificultades,
            "NroPalabrasAcuerdo": nropalabrasacuerdo,
            "UrlActividad": self.driver.current_url
        }

        if tipoactividad == "tutorias":
                self.tutorias.append(actividad)                    
        elif tipoactividad == "intervenciones":
            self.intervenciones.append(actividad)
        else:
            self.casosdeseguimiento.append(actividad)


    def getDatosSesiones(self, grupo, tipoactividad, actiividadnumero, actividadobjetivo, issaved, isfinished):
        
        sesiones = self.driver.find_elements_by_xpath('//*[@id="app-layout"]/div/div[1]/div[2]/div[2]/div[2]/div[3]/table/tbody/tr')                  

        if len(sesiones) > 0:
            if issaved == False:
                sesionesarray = []                
                for j in range(0, len(sesiones)):
                    sesionnumero = self.driver.find_element_by_xpath('//*[@id="app-layout"]/div/div[1]/div[2]/div[2]/div[2]/div[3]/table/tbody/tr[' + str(j+1) + ']/td[1]').text
                    sesionfecha = self.driver.find_element_by_xpath('//*[@id="app-layout"]/div/div[1]/div[2]/div[2]/div[2]/div[3]/table/tbody/tr[' + str(j+1) + ']/td[2]').text
                    sesionesarray.append(sesionnumero)
                    detalles = self.driver.find_element_by_xpath('//*[@id="app-layout"]/div/div[1]/div[2]/div[2]/div[2]/div[3]/table/tbody/tr[' + str(j+1) + ']/td[7]/a')
                    detalles.send_keys(Keys.CONTROL + Keys.ENTER)
                    self.driver.switch_to.window(self.driver.window_handles[2])
                    self.saveDatosActividad(grupo, tipoactividad, actiividadnumero, actividadobjetivo, sesionnumero, sesionfecha)
                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[1])

                self.data["grupos"][grupo][tipoactividad].append({
                    "nroactivity": actiividadnumero,
                    "isfinished": isfinished,
                    "sessions": sesionesarray 
                })
            else:

                for i in range(0, len(self.data["grupos"][grupo][tipoactividad])):
                    if self.data["grupos"][grupo][tipoactividad][i]["nroactivity"] == actiividadnumero:
                        for j in range(0, len(sesiones)):
                            flag = False
                            sesionnumero = self.driver.find_element_by_xpath('//*[@id="app-layout"]/div/div[1]/div[2]/div[2]/div[2]/div[3]/table/tbody/tr[' + str(j+1) + ']/td[1]').text

                            for k in range (0, len(self.data["grupos"][grupo][tipoactividad][i]["sessions"])):
                                if self.data["grupos"][grupo][tipoactividad][i]["sessions"][k] == sesionnumero:
                                    flag = True

                            if flag == False:
                                sesionfecha = self.driver.find_element_by_xpath('//*[@id="app-layout"]/div/div[1]/div[2]/div[2]/div[2]/div[3]/table/tbody/tr[' + str(j+1) + ']/td[2]').text
                                self.data["grupos"][grupo][tipoactividad][i]["isfinished"] = isfinished
                                self.data["grupos"][grupo][tipoactividad][i]["sessions"].append(sesionnumero)
                                detalles = self.driver.find_element_by_xpath('//*[@id="app-layout"]/div/div[1]/div[2]/div[2]/div[2]/div[3]/table/tbody/tr[' + str(j+1) + ']/td[7]/a')
                                detalles.send_keys(Keys.CONTROL + Keys.ENTER)
                                self.driver.switch_to.window(self.driver.window_handles[2])
                                self.saveDatosActividad(grupo, tipoactividad, actiividadnumero, actividadobjetivo, sesionnumero, sesionfecha)
                                self.driver.close()
                                self.driver.switch_to.window(self.driver.window_handles[1])
                            else:
                                break                


    def getDatosActividades(self, grupo, vista, link, isfinished):

        tiposactividades = [{
            "name": "tutorias",
            "number": 1
        },
        {
            "name": "intervenciones",
            "number": 2
        },
        {
            "name": "casosdeseguimiento",
            "number": 7
        }]

        for tipoactividad in tiposactividades:

            nextpage = True
            page = 1

            while nextpage == True:

                self.driver.get("https://graca.site/" + vista + "/" + link + "?numeroActividad=&tipoDeTrabajo=" + str(tipoactividad["number"]) + "&page=" + str(page))

                actividades = self.driver.find_elements_by_xpath("//*[@id='app-layout']/div/div[1]/div[2]/div[2]/div[2]/div/table/tbody/tr")

                if len(actividades) > 0:

                    if len(actividades) == 10:
                        nextpage = True
                    else:
                        nextpage = False

                    for i in range(0, len(actividades)):

                        actividadnumero = self.driver.find_element_by_xpath('//*[@id="app-layout"]/div/div[1]/div[2]/div[2]/div[2]/div/table/tbody/tr[' + str(i+1) + ']/td[1]').text
                        actividadfecha = self.driver.find_element_by_xpath('//*[@id="app-layout"]/div/div[1]/div[2]/div[2]/div[2]/div/table/tbody/tr[' + str(i+1) + ']/td[2]').text
                        fechaarray = actividadfecha.split("-")

                        if int(fechaarray[1]) >= 8 and int(fechaarray[2]) == 2020:
                            issaved = False

                            for j in range(0, len(self.data["grupos"][grupo][tipoactividad["name"]])):

                                if self.data["grupos"][grupo][tipoactividad["name"]][j]["nroactivity"] == actividadnumero:
                                    issaved = True
                                    break

                            actividadobjetivo = self.driver.find_element_by_xpath('//*[@id="app-layout"]/div/div[1]/div[2]/div[2]/div[2]/div/table/tbody/tr[' + str(i+1) + ']/td[4]').text

                            if (issaved == False) or (issaved == True and self.data["grupos"][grupo][tipoactividad["name"]][j]["isfinished"] == False):
                                detalles = self.driver.find_element_by_xpath('//*[@id="app-layout"]/div/div[1]/div[2]/div[2]/div[2]/div/table/tbody/tr[' + str(i+1) + ']/td[7]/a')                        
                                detalles.send_keys(Keys.CONTROL + Keys.ENTER)
                                self.driver.switch_to.window(self.driver.window_handles[1])     

                                self.getDatosSesiones(grupo, tipoactividad["name"], actividadnumero, actividadobjetivo, issaved, isfinished)
                                self.driver.close()
                                self.driver.switch_to.window(self.driver.window_handles[0])
                        else:
                            nextpage = False        
                            break    
                else:
                    nextpage = False        
                page = page + 1


    def checkActividades(self):
        
        self.tutorias = []
        self.casosdeseguimiento = []
        self.intervenciones = []

        with open("activities.json") as jsonfile:
            self.data = json.load(jsonfile)

        vistas = ["actividadesGrupodeApoyo", "actividadesGrupodeApoyoCumplidas"]

        while self.driver.current_url != "https://graca.site/home#" :
            pass

        for vista in vistas:

            for i in range (0, len(self.data["grupos"])):
                
                if vista == "actividadesGrupodeApoyo":
                    self.getDatosActividades(i, vista, self.data["grupos"][i]["link"], False)

                else:
                    self.getDatosActividades(i, vista, self.data["grupos"][i]["link"], True)

        self.driver.close()

        with open("activities.json", "w") as jsonfile:
            json.dump(self.data, jsonfile)



    def escribiractividades(self):
        
        actividades = ["tutorias", "intervenciones", "casosdeseguimiento"]

        for actividad in actividades:

            actividadarray = []
            if actividad == "tutorias":
                actividadarray = self.tutorias
            elif actividad == "intervenciones":
                actividadarray = self.intervenciones
            else:
                actividadarray = self.casosdeseguimiento

            grupos = {
                "Ingenieria": 2,
                "Trabajo social": 2,
                "Lenguas": 2,
                "Aulas de lectura": 2,
                "Sociologia": 2,
                "Administracion": 2,
                "FAI": 2,
                "Ciencias": 2,
                "Medicina": 2
            }

            self.outWorkbook = xlsxwriter.Workbook(actividad + ".xlsx")
            
            for i in range (0, len(self.data["grupos"])):
                worksheet =  self.outWorkbook.add_worksheet(self.data["grupos"][i]["name"])
                worksheet.write("A1", "NUMERO ACTIVIDAD")
                worksheet.write("B1", "OBJETIVO")
                worksheet.write("C1", "NUMERO SESION")
                worksheet.write("D1", "FECHA")
                worksheet.write("E1", "OBSERVACIONES")
                worksheet.write("F1", "DESCRIPCION")
                worksheet.write("G1", "DIFICULTADES")
                worksheet.write("H1", "ACUERDO")
                worksheet.write("I1", "PALABRAS OBSERVACIONES")
                worksheet.write("J1", "PALABRAS DESCRIPCION")
                worksheet.write("K1", "PALABRAS DIFICULTADES")
                worksheet.write("L1", "PALABRAS ACUERDO")
                worksheet.write("M1", "LINK ACTIVIDAD")



            for i in range(0, len(actividadarray)):

                for j in range (0, len(self.data["grupos"])):

                    if self.data["grupos"][j]["name"] == actividadarray[i]["Grupo"]:
                        worksheet = self.outWorkbook.get_worksheet_by_name(self.data["grupos"][j]["name"])  
                        worksheet.write("A" + str(grupos[actividadarray[i]["Grupo"]]), actividadarray[i]["NroActividad"])
                        worksheet.write("B" + str(grupos[actividadarray[i]["Grupo"]]), actividadarray[i]["Objetivo"])
                        worksheet.write("C" + str(grupos[actividadarray[i]["Grupo"]]), actividadarray[i]["NroSesion"])
                        worksheet.write("D" + str(grupos[actividadarray[i]["Grupo"]]), actividadarray[i]["Fecha"])
                        worksheet.write("E" + str(grupos[actividadarray[i]["Grupo"]]), actividadarray[i]["Observaciones"])
                        worksheet.write("F" + str(grupos[actividadarray[i]["Grupo"]]), actividadarray[i]["Descripcion"])
                        worksheet.write("G" + str(grupos[actividadarray[i]["Grupo"]]), actividadarray[i]["Dificultades"])
                        worksheet.write("H" + str(grupos[actividadarray[i]["Grupo"]]), actividadarray[i]["Acuerdo"])
                        worksheet.write("I" + str(grupos[actividadarray[i]["Grupo"]]), actividadarray[i]["NroPalabrasObservaciones"])
                        worksheet.write("J" + str(grupos[actividadarray[i]["Grupo"]]), actividadarray[i]["NroPalabrasDescripcion"])
                        worksheet.write("K" + str(grupos[actividadarray[i]["Grupo"]]), actividadarray[i]["NroPalabrasDificultades"])
                        worksheet.write("L" + str(grupos[actividadarray[i]["Grupo"]]), actividadarray[i]["NroPalabrasAcuerdo"])
                        worksheet.write("M" + str(grupos[actividadarray[i]["Grupo"]]), actividadarray[i]["UrlActividad"])

                        grupos[actividadarray[i]["Grupo"]] = grupos[actividadarray[i]["Grupo"]] + 1
                        break
                
            self.outWorkbook.close()
