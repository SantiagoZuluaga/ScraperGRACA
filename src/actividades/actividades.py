class Actividades:
    def __init__(self, driver):
        self.driver = driver

    def getCampoAndLen(self, informacion, campo):

        if len(informacion) > 1:
            if campo == "":
                return informacion[1], len(informacion[1])

            return informacion[1].split(campo)[0], len(informacion[1].split(campo)[0].split(""))

        return "", 0

    def saveDatosActividad(self, grupo, tipoactividad, actividadnumero, actividadobjetivo, sesionnumero, sesionfecha):
        
        informacion = self.driver.find_element_by_xpath('//*[@id="app-layout"]/div/div[1]/div[2]/div[2]/div[2]/div[1]').text
        temporal = informacion.split("Observaciones:")

        observaciones, nropalabrasobservaciones = getCampoAndLen(informacion.split("Observaciones:"), "Descripcion:")
        descripcion, nropalabrasdescripcion = getCampoAndLen(informacion.split("Descripcion:"), "Solicitante:")
        dificultades, nropalabrasdificultades = getCampoAndLen(informacion.split("Dificultades:"), "Acuerdo")
        dificultades, nropalabrasdificultades = getCampoAndLen(informacion.split("Acuerdo:"), "")

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


    def getActividades(self):

        with open("./src/actividades/data/activities.json") as jsonfile:
            self.data = json.load(jsonfile)

        self.tutorias = []
        self.casosdeseguimiento = []
        self.intervenciones = []
        vistas = ["actividadesGrupodeApoyo", "actividadesGrupodeApoyoCumplidas"]       

        for vista in vistas:

            for i in range (0, len(self.data["grupos"])):
                
                if vista == "actividadesGrupodeApoyo":
                    self.getDatosActividades(i, vista, self.data["grupos"][i]["link"], False)

                else:
                    self.getDatosActividades(i, vista, self.data["grupos"][i]["link"], True)

        self.driver.close()

        with open("./src/actividades/data/activities.json", "w") as jsonfile:
            json.dump(self.data, jsonfile)
