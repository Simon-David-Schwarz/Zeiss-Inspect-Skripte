# -*- coding: utf-8 -*-

import gom
import os

#================================================================================================================================#
# Skript für die Konstruktion der Rohrmittellinie und Auswertung der Krümmung entlang der Rohrmittellinie.
# Hinweis:
# - Für die Konstruktion der Rohrmittellinie ist eine Flächenkurve oder ein Schnitt entlang der Kontur erforderlich
# - Die Auswertung der Krümmung gilt nur ebene Biegungen
#================================================================================================================================#

# Hilfsfunktionen für Dialog
# -> Event-Handler für Dialog
def DialogEventHandler(widget):
	pass

# -> Elementfilter für mehrere Elementtypen
def ElementFilter(element, elementtypen):
	try:
		if element.type in elementtypen:
			return True
	except Exception as e:
		pass
	return False

# -> Elementfilter für Dialog
def ElementFilterDialog(element):
	return ElementFilter(element, elementtypen)

# Dialog für Auswahl der Kurve und Eingabe der erforderlichen Parameter für einen Multischnitt-Kurve
DIALOG=gom.script.sys.create_user_defined_dialog (dialog={
				"content": [
								[
												{
																"columns": 2,
																"name": "label_2",
																"rows": 1,
																"text": {
																				"id": "",
																				"text": "Auswahl der Kurve für Multischnitt-Kurve",
																				"translatable": True
																},
																"tooltip": {
																				"id": "",
																				"text": "",
																				"translatable": True
																},
																"type": "label",
																"word_wrap": False
												},
												{
												}
								],
								[
												{
																"columns": 2,
																"fast_filter": False,
																"name": "elementauswahl",
																"rows": 1,
																"supplier": "custom",
																"tooltip": {
																				"id": "",
																				"text": "",
																				"translatable": True
																},
																"type": "input::point3d"
												},
												{
												}
								],
								[
												{
																"columns": 2,
																"name": "separator",
																"rows": 1,
																"title": {
																				"id": "",
																				"text": "",
																				"translatable": True
																},
																"tooltip": {
																				"id": "",
																				"text": "",
																				"translatable": True
																},
																"type": "separator"
												},
												{
												}
								],
								[
												{
																"columns": 2,
																"name": "label_3",
																"rows": 1,
																"text": {
																				"id": "",
																				"text": "Parameter für Multischnitt Kurve",
																				"translatable": True
																},
																"tooltip": {
																				"id": "",
																				"text": "",
																				"translatable": True
																},
																"type": "label",
																"word_wrap": False
												},
												{
												}
								],
								[
												{
																"columns": 1,
																"name": "label",
																"rows": 1,
																"text": {
																				"id": "",
																				"text": "Abstand:",
																				"translatable": True
																},
																"tooltip": {
																				"id": "",
																				"text": "",
																				"translatable": True
																},
																"type": "label",
																"word_wrap": False
												},
												{
																"background_style": "",
																"columns": 1,
																"maximum": 1000,
																"minimum": 0,
																"name": "abstand_schnitte",
																"precision": 2,
																"rows": 1,
																"tooltip": {
																				"id": "",
																				"text": "",
																				"translatable": True
																},
																"type": "input::number",
																"unit": "LENGTH",
																"value": 5
												}
								],
								[
												{
																"columns": 1,
																"name": "label_1",
																"rows": 1,
																"text": {
																				"id": "",
																				"text": "Durchmesser:",
																				"translatable": True
																},
																"tooltip": {
																				"id": "",
																				"text": "",
																				"translatable": True
																},
																"type": "label",
																"word_wrap": False
												},
												{
																"background_style": "",
																"columns": 1,
																"maximum": 200,
																"minimum": 0,
																"name": "durchmesser_schnitte",
																"precision": 2,
																"rows": 1,
																"tooltip": {
																				"id": "",
																				"text": "",
																				"translatable": True
																},
																"type": "input::number",
																"unit": "LENGTH",
																"value": 100
												}
								]
				],
				"control": {
								"id": "OkCancel"
				},
				"embedding": "always_toplevel",
				"position": "automatic",
				"size": {
								"height": 288,
								"width": 330
				},
				"sizemode": "automatic",
				"style": "",
				"title": {
								"id": "",
								"text": "Eingaben für Mittellinie-Rohr",
								"translatable": True
				}
})
# Event-Handler für Dialog festlegen
DIALOG.handler = DialogEventHandler

# Elementfilter für Auswahl festlegen
elementtypen = ['cad_surface_curve', 'section']
DIALOG.elementauswahl.filter = ElementFilterDialog

# Dialog initialisieren
RESULT = gom.script.sys.show_user_defined_dialog(dialog=DIALOG)

# Auslesen der Eingabefelder
element = RESULT.elementauswahl
abstand_schnitte = RESULT.abstand_schnitte
durchmesser_schnitte = RESULT.durchmesser_schnitte

# 
gom.script.explorer.apply_selection(selection=element)
		
# Ermittlung des zur Flächenkurve oder Schnitt gehörenden Mesh und Selektion aller dazugehörigen Elemente
bauteil = gom.app.project.actual_elements[element.name].part
gom.script.selection3d.select_all_points_of_element (elements=gom.ElementSelection ({'category': ['key', 'elements', 'part', bauteil, 'explorer_category', 'actual_part']}))

# Erstellung der Schnitte basierend auf der ausgewählten Flächenkurve und den übergebenen Zahlenwerten für Abstand sowie Durchmesser der Schnitte
MCAD_ELEMENT=gom.script.section.create_multisection_by_curve (
	disc_distance=abstand_schnitte, 
	disc_radius=durchmesser_schnitte, 
	name='Schnitt 1', 
	project_onto_theoretical_surface=True, 
	properties=gom.Binary ('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'), 
	reference_curve=gom.app.project.actual_elements[element.name])

# Kreise in Schnitte fitten und Mittelpunkte der Kreis mit Spline verbinden
# -> Liste für Aufnahme der Fitting-Kreise erzeugen
fitting_kreise = []

# -> Schnitte entlang Kurve durchlaufen und Kreise hineinfitten
for i in range(len(MCAD_ELEMENT)-1, -1, -1):
	# Alle Elemente des aktuellen Schnittes für Kreis-Fit markieren
	gom.script.selection3d.select_all_points_of_element(elements=[MCAD_ELEMENT[i]])
	
	# Fitting Kreis für aktuellen Schnitt erzeugen und zur Liste der Fitting-Kreise hinzufügen
	schnitt_name = 'Kreis-' + str(MCAD_ELEMENT[i].name)
	fitting_kreis=gom.script.primitive.create_fitting_circle (
		method='best_fit', 
		name=schnitt_name, 
		properties=gom.Binary ('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'), 
		sigma=3)
	fitting_kreise.append(fitting_kreis)

# Verbindung der Mittelpunkte der Fitting-Kreise mit einer Kurve
# -> Autor: Nanno Mühl, Carl Zeiss GOM Metrology GmbH
# -> Anfang
markers = []
idx = 0
for fitting_kreis in fitting_kreise:
	markers.append ({'index': idx, 'parameters': {'point_trait': fitting_kreis, 'type': 'free'}, 'type': 'marker'})
	idx = idx + 1

sequence = []
for i in range(0, len(markers)):
	sequence.append ({'index': i, 'type': 'marker'})
	if i + 1 < len(markers):
		sequence.append ({'type': 'segment'})

pathes = [{'parameters': {'sequence' : sequence, 'type': 'spline'}, 'type': 'path'}]

mittellinie=gom.script.curve.create_curve (curve_parts = {'markers' : markers, 'pathes' : pathes, 'with_normals': False}, name = 'Mittellinie_Rohr')
# -> Ende

# Krümmung der Rohrmittellinie auswerten
# -> Inspektionslement für Kurvenkrümmung anlegen
MCAD_ELEMENT=gom.script.inspection.measure_curvature_values (
	elements=[gom.app.project.actual_elements[mittellinie.name]], 
	max_point_distance=2.0, 
	properties=gom.Binary ('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'))

# -> Krümmungswerte ermitteln
MCAD_ELEMENT=gom.script.inspection.inspect_dimension (
	elements=[gom.app.project.actual_elements[mittellinie.name + '.κ']], 
	nominal_value=0.0, 
	nominal_value_source='fixed_value', 
	properties=gom.Binary ('eAHEmWuMVGcZx38QbqVQitYC1ehkWSm2nWV3WSgdQMqtUgvtplDaEHUyO3N2d9y5MTPLsq21B/3Q1jY2ftAav1SjVhMUg4lBjUYTY9KoxWiiNjXVD5hqDKamH2xjUjD/5z3vnjOzFwaw6RB23znnPc/l//yfy3v2ULWcPryp5zj79u7cs/d+DtVzxWYjk9lbCspBpTlYr9aCerMYNHCfeSxm+VKWspyly4FrR3YHo8BH7juQOlgdbk7k6kGqv7e/P3UwqB8r5oPUYC4/luLsySVstOcv69ML5DefPTmPLcBNEJbIMURAiSx5qlSoEJCnSZU6WUoU7UqWCYoUaDLKw4vOnpxPCrgOwt3Tnnpwaucf3pCu9wGrAa2vAxZC2KBMjhIlXvj4awO6ox1L2yxqEnCcJhf/K43XA4vs2SZ1s2uE9S/p2QsL4a35hNsYpUmZEh9G64AcBVuXCWiSIxV5Kcn6uZ0u+ugiRYWc7dKVoyY/b9KcBV0mRZonKRGQslUt2u93bSBPg4btrnEbKcMvxSOkmGCUou1M06BGjjwBGVLUqNvVCerkqLGVFI+yjQ0JfdK+ocWjIaoUmCSV2CVbhiP/JC+gyIh5kWGAXnpNdrwj9idDxSLuorI18leIDUX+DjFi2JVsnzStZTjxTxjKpjoFgmiHQ1Z+KtLyuUAhipzu97bc96jE99ORhNhOPZXUkk7YlGEteXqn/svX1r2xnAwN80Wc1j75XWfEdKeN/TUy9FLj+Az3JbVpu8pz7BJuw4b9bHLEMh8fv8cjX49+F6b5f8zwbRpDFa20/ZSkChnK5lPBoibPWlFP23Vn1cCM91ttmklCjM5Md9ux8R656FamedMpG7vNX3F7vWVbLWKisMhOZWPWdBTIGmdylm8fojvKJmeBrNlgyL7zCM8cg7cL4daKsPmyK0K31Q5XJZqkWD9VNVXrurjV8lXrBqNUmSDLOBWre9sZNp42LhkRxcaxXytfgdx3sUtVz32Lq/1n/qU+sAfUl1q6mhhQNrY4NmSjKjNGjhH7Lg4NG4/UE1StvtSjfnMbcAOEI5bnPQy2PHf/tKf2PS0bdgBbrdstoA94/thzP7nn5f3nv/eV00/++M0zu9T9+uihlx76WQzh3VSMm67v8tLo0JrZGqKH9cKkDFwGLIBQoKiYfeKUnrOZIFyi5S3Auy+JxzjjVjP+dEBCbwSugfBQVN0yPMAD3E2BzI8k8whwOOrm+4FuCAfIsdnw2MLt5EiziX76GCBtfWcLd5BmiAJ5NtrdHHewmbw9McQm+mzXxwZPnZDcblC3D5UHir36oouM8rrKOHX79rX3yuIuYEVkcevug4m96/o9Iusi6zWXLINQnU8VpP3pF65//EXtez+wvA1FV4MbFK0iaaaKwyE01YEfOq2nF0Rj2p0r9c1PTcm5q52hpzdI2uzTjg/7vdHEkn1ZkuXVyjbJIobvx1nKljsBj+2QfD9v7UrsORDtWGH43ATGBq29TmFl8+DrnzY2eIY59LLW3WWTGO2w0QwpysqG88WkZwWLjsvuLx+StCWJaXa16fVWJvHyHePCVyXtBtBzU1l6V3T3C1/U8/vAqoLWGeA9UzvFpEnrEqoPsjKehL2G5OfU+RUfkJR+YBWEmmnck5rrhFqWIsNRxVOnUtUZN/kFfr5NtnoUZ03YzcAaCGs0TFy/tTKBrrauEVUgx0N5PJD1j0mBT15fsjScuzbZ95CMf5ejn8EhYvK5fzC28xer9H096H4L1K0EirUd+O0VaYOLO058/WZp2wZKwASMrmH7kqyE9+vAwuRGco09Cs6Dj8kCTz/v730M8cmokE4v0PtvkWYllhIyeXZaaYh4BBz6VVySC3Oh3ojGLTeeLlwm/T5J56Lyv3dsDSXdF7Uk0YailjJC3ZJBo8uZtCTfC3ywpQzfZSNev5Xk/VNk3UXOWqquat0uLWbAiV96H2WJdCTSLRxtv6Ix6xtJu4tWerNsNE4mvRg3C9LfksyOKT67ON/kfOjHKdGkwWfXdKRAKd8FYScKlJzC3DX+SSuSOgiMReX9P690pNLTUNVPFBZpVBkk7DhZExxT+tzvJdT3zrjPJgO8p0WSO2MPGwHU+zTJuDQ4bJQcNwIoWKucJba+Jknyp8PS87qoVwA3trHQs68WcTtrePjBq8DrP+sIBV984sroI3nu2bkFzAufkG0fBdZe0rYGYxSp2cAkJvpjvmtyvjY2OPrHpNK5mvJMmelY3orD363hXJLhM3ViJ65G1fqij96f35BAr94Xsd3mhBJZDg5SNZea9D4rkHaDzZhnTy5iU7JBXc762/PPvyZhPVFLTGazM1WZoVcaamc1shyjSMAEK0dlsg+1N/mw1Vw9efRWyRUEGsu0Vguf7bOEVyzyfoSbbkfytcQzb70dun3Vn65b6awSFHedv1Wu3II3LzoU4t9P7PzpannvCTDdgtaeU/2VtF9Oz5k9vr7zuMiKlC7bn7ldOi7JcV/x5pr7RBwlaZ3vlDo1XG8KBcnshus9pN5CKidcU1aSBvzw8Y4M94e69lItNJqMRxNWPOkc+avEtvM97qqzzFUa+OedWyxXPFTtGt1E194cXn0nm4M/EclUnUhFSPUu0eNhAh49LDB0LrgWQvWoeJc/OxyxIUtnJu3T2hNW5wJJHqfMU79+8bvJOLeD0z7yxgFZ9tTVBsSnmxvzCtZPNW04rzWEurPm9/85N6OirjXzzB6LbXcl7lCPbO9IwYB7fz5lb6uVSmBXojTmJ6l75p6rRarVtbkH4iwjdtRQYSnxKetsHZcRF4qZDk5Jh9a9eoUOTZ06PMHjEUXEKkdH1ibfvFMaPGH9qUMzkftDg52ZIGSevvkXA+3kjcn6u+eu1mLfGWOLZVNu6pSjoE/ymx90BLdnUmdVW3/z0TBcYd1fkrDMddjx9dsf7+bWpGNDrEXDW2BsLtFd+L85FL9+iFXd/PmOHWI1/wMAAP//AwBJ3mLpAfs4'), 
	type='curvature')

## Export der Koordinaten
## -> Auslesen des Speicherortes der Projektdatei
#dateipfad = gom.app.project.project_file
#
## -> Ermittlung des Dateiverzeichnisses
#dateiverzeichnis = os.path.dirname(dateipfad)
#
## -> Auslesen des Projektnamens
#dateiname = gom.app.project.project_name
#
## -> Koordinaten der Rohrmittellinie auslesen
#koord = np.array(spline.data.coordinate)
#koord = mittellinie[0, :, :]
#
## -> Textdatei für Export öffnen
#delimiter = ';'
#fh = open(dateiverzeichnis.replace('\\', '/') + '/' + dateiname + '_Koordinaten_Mittellinie.csv', 'w')
#
## -> Kopfzeile in Textdatei schreiben
#fh.write('x-Koordinate[mm]' + delimiter + 'y-Koordinate[mm]' + delimiter + 'z-Koordinate[mm]\n')
#
## -> Koordinaten in Textdatei schreiben
#for i in range(koord.shape[0]):
#	fh.write(str(koord[i, 0]) + delimiter + str(koord[i, 1]) + delimiter + str(koord[i, 2]) + '\n')
#
## -> Textdatei schließen
#fh.close()
