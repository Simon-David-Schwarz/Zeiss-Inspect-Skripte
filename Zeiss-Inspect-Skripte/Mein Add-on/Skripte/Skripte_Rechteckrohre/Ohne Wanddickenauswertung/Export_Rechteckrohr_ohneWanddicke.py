# -*- coding: utf-8 -*-

import gom 
import os
import numpy as np



# Dateiverzeichnis
dateipfad = gom.app.project.project_file
dateiverzeichnis = os.path.dirname(dateipfad) + '/tmp_export' #EINGABE
dateiname = gom.app.project.project_name

#================================================================================================================================#
# Widget3 Parameterauswahl Messchieberfunktion 
RESULT3=gom.script.sys.execute_user_defined_dialog (file='Widget3_Rechteckrohr.gdlg')
#================================================================================================================================#
# Parameter für Messschieberfunktion
rohrhöhe =    RESULT3.Rohrhöhe #Eingabe
rohrbreite =  RESULT3.Rohrbreite #EINGABE
biegeradius = np.round(gom.app.project.inspection['Kreis_Biegeradius.R'].get ('result_dimension.measured_value'),2)
#================================================================================================================================#
# Widget1 Winkelauflösung 
RESULT1=gom.script.sys.execute_user_defined_dialog (file='Widget1 E Winkelauflösung.gdlg')
#================================================================================================================================#
# Winkelauflösung für Auswertung festlegen
startwinkel =  RESULT1.Input_Startwinkel   #EINGABE (in der Regel = 0)
schrittweite = RESULT1.Input_Schrittweite  #EINGABE
#================================================================================================================================#

# Ergebnisvariable initialisieren
ergebnis = dict()

# Diverse Variablen in Dictionary definieren
for stufe in gom.app.project.stages:
	# -> Stufe aktiv schalten
	if len(gom.app.project.stages) > 1:
		gom.script.sys.show_stage(stage=stufe)
	
	# -> Unter-Dictionary für Stufe erzeugen
	ergebnis[stufe.name] = dict()
	
	# -> Bauteilwinkel ermitteln
	# --> HINWEIS: Winkel werden in rad ausgegeben!!!
	bauteilwinkel = gom.app.project.inspection['Maß_Bauteilwinkel'].get ('result_dimension.measured_value')
	bauteilwinkel = np.round(np.rad2deg(gom.app.project.actual_elements['Bauteilwinkel'].angle), 2)
	biegewinkel = 180 - bauteilwinkel
	ergebnis[stufe.name]['Biegewinkel'] = biegewinkel
	
	# -> Biegeradius
	ergebnis[stufe.name]['Biegeradius'] = biegeradius
	
	#-> Kurvenlänge Außenbogen
	kurvenlaenge_aussenbogen = np.round(gom.app.project.inspection['Kurvenlaenge_Aussenbogen'].get ('result_dimension.measured_value'),2)
	ergebnis[stufe.name]['Kurvenlaenge_Aussenbogen'] = kurvenlaenge_aussenbogen
	
	#-> Kurvenlänge Innenbogen
	kurvenlaenge_innenbogen = np.round(gom.app.project.inspection['Kurvenlaenge_Innenbogen'].get ('result_dimension.measured_value'),2)
	ergebnis[stufe.name]['Kurvenlaenge_Innenbogen'] = kurvenlaenge_innenbogen
	
	#-> Kurvenlänge Schwerpunktlinie
	kurvenlaenge_schwerpunktlinie = np.round(gom.app.project.inspection['Kurvenlaenge_Schwerpunktlinie'].get ('result_dimension.measured_value'),2)
	ergebnis[stufe.name]['Kurvenlaenge_Schwerpunktlinie'] = kurvenlaenge_schwerpunktlinie
	
	
#========================================================================================================
# Gemeinsame Winkelauflösung für Stufen ermitteln
winkelaufloesung = np.array([])
for stufe in gom.app.project.stages:
	# -> Winkelauflösung für aktuelle Stufe erzeugen
	tmp_winkel = ergebnis[stufe.name]['Biegewinkel']
	# tmp_startwinkel = 0
	tmp_aufloesung = np.append(np.arange(startwinkel, tmp_winkel, schrittweite), tmp_winkel)
	

	
	#-> Startwert und Endwert
	# -> Einzelne Winkelauflösungen zusammenfassen
	winkelaufloesung = np.union1d(winkelaufloesung, tmp_aufloesung)
	
	print(winkelaufloesung)
#========================================================================================================#
# Inspektionsergebnisse auslesen
for stufe in gom.app.project.stages:
	# Aktuelle Stufe festlegen
	if len(gom.app.project.stages) > 1:
		gom.script.sys.show_stage(stage=stufe)
	#===================================================================================================#
	
	ergebnis[stufe.name]['Hauptachse'] = np.zeros(winkelaufloesung.shape[0])
	ergebnis[stufe.name]['Nebenachse'] = np.zeros(winkelaufloesung.shape[0])
	ergebnis[stufe.name]['Unrundheit'] = np.zeros(winkelaufloesung.shape[0])
	ergebnis[stufe.name]['Unrundheit_ungerundet'] = np.zeros(winkelaufloesung.shape[0]) 
	ergebnis[stufe.name]['Schwerpunktkoordinaten'] = np.zeros((winkelaufloesung.shape[0], 2))
	ergebnis[stufe.name]['Koordinaten_Aussenbogen'] = np.zeros((winkelaufloesung.shape[0], 2))
	ergebnis[stufe.name]['Radius_R(winkel)'] = np.zeros(winkelaufloesung.shape[0])
	ergebnis[stufe.name]['Radius_Ra(winkel)'] = np.zeros(winkelaufloesung.shape[0])
	ergebnis[stufe.name]['Einfall'] = np.zeros(winkelaufloesung.shape[0])
	ergebnis[stufe.name]['Kruemmung(Winkel)'] = np.zeros(winkelaufloesung.shape[0])
	ergebnis[stufe.name]['MAX_Abw_Flaechenvergleich_Querschnitt(Winkel)'] = np.zeros(winkelaufloesung.shape[0])
	ergebnis[stufe.name]['MIN_Abw_Flaechenvergleich_Querschnitt(Winkel)'] = np.zeros(winkelaufloesung.shape[0])
	ergebnis[stufe.name]['Flaechenvergleich Innenbogen'] = np.zeros(winkelaufloesung.shape[0])
	ergebnis[stufe.name]['Flaechenvergleich Aussenbogen'] = np.zeros(winkelaufloesung.shape[0])
	
	
	for i in range(winkelaufloesung.shape[0]):
		winkel = winkelaufloesung[i]
	
		# Durchmesser Nebenachse heraus lesen
		ergebnis[stufe.name]['Nebenachse'][i] = np.round(gom.app.project.inspection['Durchmesser_vertikal_B_Bogenschnitt_' + str(winkel) + '.L'].get ('result_dimension.measured_value'),2)
		#===========
		
		# Durchmesser Hauptachse heraus lesen
		ergebnis[stufe.name]['Hauptachse'][i] = np.round(gom.app.project.inspection['Durchmesser_horizontal_Schnittpunkt_innen_B_Bogenschnitt_' + str(winkel) + '.L'].get ('result_dimension.measured_value'), 2)
		#=========
		
		# Unrundheit berechnen in [%]
		ergebnis[stufe.name]['Unrundheit_ungerundet'][i] = ((ergebnis[stufe.name]['Nebenachse'][i] - ergebnis[stufe.name]['Hauptachse'][i]) / rohrhöhe)*100
		# Unrundheit auf die 2. Nachkommastelle runden
		ergebnis[stufe.name]['Unrundheit'][i] = np.round(ergebnis[stufe.name]['Unrundheit_ungerundet'] [i], 2)
		#============
		
		
		# Einfall am Aussenbogen berechnen
		# -> X/Y-Koordinaten der Schwerpunkte ermitteln und hieraus jeweils den Biegeradius an den diskreten Winkelpostitionen auswerten
		ergebnis[stufe.name]['Schwerpunktkoordinaten'][i] = np.array([gom.app.project.inspection['Schwerpunkt_B_Bogenschnitt_' + str(winkel) + '.X(LOKAL)'].get ('result_dimension.measured_value'), gom.app.project.inspection['Schwerpunkt_B_Bogenschnitt_' + str(winkel) + '.Y(LOKAL)'].get ('result_dimension.measured_value')])
		ergebnis[stufe.name]['Radius_R(winkel)'] = np.linalg.norm(ergebnis[stufe.name]['Schwerpunktkoordinaten'], axis=1)
		
		# -> X/Y-Koordinaten der Punkte am Außenbogen ermitteln und hieraus jeweils den Außenradius an den diskreten Winkelpostitionen auswerten
		ergebnis[stufe.name]['Koordinaten_Aussenbogen'][i] = np.array([gom.app.project.inspection['Schnittpunkt_aussen_B_Bogenschnitt_' + str(winkel) +'.X(LOKAL)'].get ('result_dimension.measured_value'), gom.app.project.inspection['Schnittpunkt_aussen_B_Bogenschnitt_' + str(winkel) +'.Y(LOKAL)'].get ('result_dimension.measured_value')])
		ergebnis[stufe.name]['Radius_Ra(winkel)'] = np.linalg.norm(ergebnis[stufe.name]['Koordinaten_Aussenbogen'], axis=1)
		
		#-> Einfall berechnen
		ergebnis[stufe.name]['Einfall'][i] = np.round(ergebnis[stufe.name]['Radius_R(winkel)'][i] + (rohrhöhe / 2) - ergebnis[stufe.name]['Radius_Ra(winkel)'][i], 2)
		#==============
		
		# Krümmung an den diskreten Winkelpositionen auslesen
		ergebnis[stufe.name]['Kruemmung(Winkel)'][i] = np.round(gom.app.project.inspection['Projektionspunkt_Schwerpunkt_B_Bogenschnitt_' + str(winkel) + '.kappa'].result_dimension, 6)
		
		# MAX/MIN Abweichungen der Flächenvergleiche, ausgewertet in Querschnitten bei diskreten Winkeln, auslesen
		ergebnis[stufe.name]['MAX_Abw_Flaechenvergleich_Querschnitt(Winkel)'][i] = np.absolute(np.round(gom.app.project.inspection['Flaechenabw_QuerschnittB_Bogenschnitt_' + str(winkel)].deviation_label['Abweichungsfahne_MAX_Flaechenabw_QuerschnittB_Bogenschnitt_' + str(winkel)].result_dimension, 3))
		ergebnis[stufe.name]['MIN_Abw_Flaechenvergleich_Querschnitt(Winkel)'][i] = np.absolute(np.round(gom.app.project.inspection['Flaechenabw_QuerschnittB_Bogenschnitt_' + str(winkel)].deviation_label['Abweichungsfahne_MIN_Flaechenabw_QuerschnittB_Bogenschnitt_' + str(winkel)].result_dimension, 3))
		
		# Abweichungsfähnchen des Flächenvergleiches entlang Innenbogen und Außenbogen an diskreten Winkelpositionen auswerten
		ergebnis[stufe.name]['Flaechenvergleich Innenbogen'][i] = np.round(gom.app.project.inspection['Flaechenvergleich_Ist_vs_Soll'].deviation_label['Flachenvergleich_Ist_vs_Soll_Innenbogen' + str(winkel)].result_dimension ,3)
	
		ergebnis[stufe.name]['Flaechenvergleich Aussenbogen'][i] = np.round(gom.app.project.inspection['Flaechenvergleich_Ist_vs_Soll'].deviation_label['Flachenvergleich_Ist_vs_Soll_Aussenbogen' + str(winkel)].result_dimension ,3)

#====================================================================================================
	
	# Skalare & singuläre Messgrößen exportieren
	# -> Messgrößen pro Stufe: Biegewinkel, Biegeradius, Kurvenlänge Außenbogen, Kurvenlänge Innenbogen, Kurvenlänge Schwerpunktlinie
	fh = open(dateiverzeichnis.replace('\\', '/') + '/' + 'skalare_Parameter' + '.csv', 'w')
	# --> Kopfzeile in Textdatei schreiben
	fh.write('Biegewinkel [degree]; Biegeradius [mm]; Kurvenlaenge Außenbogen [mm]; Kurvenlaenge Innenbogen [mm]; Kurvenlaenge Schwerpunktlinie [mm]; Kruemmung \n')
	# --> Messergebnisse in Textdatei schreiben
	fh.write(str(ergebnis[stufe.name]['Biegewinkel']) + ';')
	fh.write(str(ergebnis[stufe.name]['Biegeradius']) + ';' )
	fh.write(str(ergebnis[stufe.name]['Kurvenlaenge_Aussenbogen']) + ';' )
	fh.write(str(ergebnis[stufe.name]['Kurvenlaenge_Innenbogen']) + ';' )
	fh.write(str(ergebnis[stufe.name]['Kurvenlaenge_Schwerpunktlinie']) + ';')
		
	# -> Export abschließen
	fh.close()
	
	# Biegewinkelabhängige Messgrößen exportieren
	fh = open(dateiverzeichnis.replace('\\', '/') + '/' + 'winkelabhaengige_auswertungen' + '.csv', 'w')
	
	#-> Kopfzeile in Textdatei schreiben
	fh.write('Winkel [degree]; Durchmesser Nebenachse [mm]; Durchmesser Hauptachse [mm]; Unrundheit u [-]; Einfall e [mm]; Kruemmung [1/mm]; Wanddicke Außenbogen [mm]; Wanddicke Innenbogen [mm]; Flächenabweichung Querschn. MAX [mm]; Flächenabweichung Querschn. MIN [mm]; Flächenabweichung Innenbogen [mm]; Flächenabweichung Aussenbogen [mm] \n')
	
	for i in range(winkelaufloesung.shape[0]):
		if winkelaufloesung[i] <= ergebnis[stufe.name]['Biegewinkel']:
			fh.write(str(winkelaufloesung[i]) + ';' + str(ergebnis[stufe.name]['Nebenachse'][i]) + ';' + str(ergebnis[stufe.name]['Hauptachse'][i]) + ';' + str(ergebnis[stufe.name]['Unrundheit'][i])  + ';' + str(ergebnis[stufe.name]['Einfall'][i]) + ';' + str(ergebnis[stufe.name]['Kruemmung(Winkel)'][i]) + ';' + str(ergebnis[stufe.name]['MAX_Abw_Flaechenvergleich_Querschnitt(Winkel)'][i]) + ';' + str(ergebnis[stufe.name]['MIN_Abw_Flaechenvergleich_Querschnitt(Winkel)'][i]) + ';' + str(ergebnis[stufe.name]['Flaechenvergleich Innenbogen'][i]) + ';' +  str(ergebnis[stufe.name]['Flaechenvergleich Aussenbogen'][i]) + '\n')
			# fh.write(str(winkelaufloesung[i]) + ';' + str(ergebnis[stufe.name]['Nebenachse'][i]) + ';' + str(ergebnis[stufe.name]['Hauptachse'][i]) + ';' + str(ergebnis[stufe.name]['Unrundheit'][i]) + ';' + str(ergebnis[stufe.name]['Einfall'][i]) + '\n')

	fh.close()
#==================================================================================================================
#Diagrammdaten exportieren

#-> Kruemmungsverlauf
#--> Krümmungsverlauf selektieren
gom.script.cad.show_element_exclusively (elements=[gom.app.project.inspection['Schwerpunktlinie.κ.κ']])

#--> Kurvendaten exportieren
gom.script.diagram.export_diagram_contents (
	cell_separator=';', 
	codec='iso 8859-1', 
	decimal_separator='.', 
	file=dateiverzeichnis + '\kruemmung.csv', 
	header_export=True, 
	line_feed='\n', 
	text_quoting='', 
	type='curves')

#-> x/y-Koordinaten der Polylinien (Innenbogen, Außenbogen, Schwerpunktlinie)

#-> Kurven selektieren
gom.script.cad.show_element_exclusively (elements=[gom.app.project.inspection['Schwerpunktlinie.X'], gom.app.project.inspection['Polylinie_Innenbogen.X'], gom.app.project.inspection['Polylinie_Aussenbogen.X'], gom.app.project.inspection['Polylinie_Aussenbogen.Y'], gom.app.project.inspection['Schwerpunktlinie.Y'], gom.app.project.inspection['Polylinie_Innenbogen.Y']])

#-> Kurvenwerte exportieren
gom.script.diagram.export_diagram_contents (
	cell_separator=';', 
	codec='iso 8859-1', 
	decimal_separator='.', 
	file=dateiverzeichnis + '\koordinaten_polylinien.csv', 
	header_export=True, 
	line_feed='\n', 
	text_quoting='', 
	type='curves')

#-> X/Y-Koordinaten der Schwerpunkte

#gom.script.cad.show_element_exclusively (elements=gom.ElementSelection ({'category': ['key', 'elements', 'tags', 'X/Y-Koordinaten Schwerpunkte']}))
#
#gom.script.table.switch_template (
#	name='Elements', 
#	uuid='f8279568-1e90-460a-a859-9ce79dcca3e8')
#
## schwerpunktkoordinaten = list ()
## schwerpunkt
#gom.script.table.export_table_contents (
#	cell_separator=';', 
#	codec='iso 8859-1', 
#	decimal_separator='.', 
#	elements=[gom.app.project.inspection[]], 
#	file='D:/01_Dissertation/GOM/Abrollbiegen_Auswertung/gom_data_export/koordinaten_schwerpunkte.csv', 
#	header_export=True, 
#	line_feed='\n', 
#	sort_column=0, 
#	sort_order='ascending', 
#	template_name='Elements', 
#	text_quoting='', 
#	write_one_line_per_element=False)



## Rückfederung berechnen
#stufen = list()
#for stufe in ergebnis.keys():
#	stufen.append(stufe)
#ergebnis['Rückfederung'] = abs(ergebnis[stufen[0]]['Bauteilwinkel'] - ergebnis[stufen[1]]['Bauteilwinkel'])

## Bauteilwinkel und Rückfederung exportieren
#fh = open(dateiverzeichnis.replace('\\', '/') + '/' + dateiname + '_geometry.csv', 'w')
## -> Kopfzeile in Textdatei schreiben
#fh.write('Angle ' + stufen[0] + ';' + 'Angle ' + stufen[1] + ';' + 'Springback\n')
## -> Zahlenwerte in Textdatei schreiben
#fh.write(str(ergebnis[stufen[0]]['Bauteilwinkel']) + ';' + str(ergebnis[stufen[1]]['Bauteilwinkel']) + ';' + str(ergebnis['Rückfederung']) + '\n')
## -> Export abschließen
#fh.close()

#-> X/Y-Koordinaten der Schwerpunkte exportieren
gom.script.cad.show_element_exclusively (elements=gom.ElementSelection ({'category': ['key', 'elements', 'tags', 'X/Y-Koordinaten Schwerpunkte']}))

gom.script.table.export_table_contents (
	cell_separator=';', 
	codec='iso 8859-1', 
	decimal_separator='.', 
	elements=gom.ElementSelection ({'category': ['key', 'elements', 'tags', 'X/Y-Koordinaten Schwerpunkte']}), 
	file=dateiverzeichnis + '\koordinaten_schwerpunkte.csv', 
	header_export=True, 
	line_feed='\n', 
	sort_column=0, 
	sort_order='ascending', 
	template_name='Elements', 
	text_quoting='', 
	write_one_line_per_element=False)

#-> X/Y-Koordinanten der Schnittpunkte am Innenbogen exportieren
gom.script.cad.show_element_exclusively (elements=gom.ElementSelection ({'category': ['key', 'elements', 'tags', 'Schnittpunkte_Innenbogen_X/Y-Koordinaten']}))

gom.script.table.export_table_contents (
	cell_separator=';', 
	codec='iso 8859-1', 
	decimal_separator='.', 
	elements=gom.ElementSelection ({'category': ['key', 'elements', 'tags', 'Schnittpunkte_Innenbogen_X/Y-Koordinaten']}), 
	file=dateiverzeichnis + '\koordinaten_innenbogen.csv', 
	header_export=True, 
	line_feed='\n', 
	sort_column=0, 
	sort_order='ascending', 
	template_name='Elements', 
	text_quoting='', 
	write_one_line_per_element=False)

#-> X/Y-Koordinanten der Schnittpunkte am Außenbogen exportieren
gom.script.cad.show_element_exclusively (elements=gom.ElementSelection ({'category': ['key', 'elements', 'tags', 'Schnittpunkte_Außenbogen_X/Y-Koordinaten']}))

gom.script.table.export_table_contents (
	cell_separator=';', 
	codec='iso 8859-1', 
	decimal_separator='.', 
	elements=gom.ElementSelection ({'category': ['key', 'elements', 'tags', 'Schnittpunkte_Außenbogen_X/Y-Koordinaten']}), 
	file=dateiverzeichnis + '\koordinaten_aussenbogen.csv', 
	header_export=True, 
	line_feed='\n', 
	sort_column=0, 
	sort_order='ascending', 
	template_name='Elements', 
	text_quoting='', 
	write_one_line_per_element=False)
	




