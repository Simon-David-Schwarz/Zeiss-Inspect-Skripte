# -*- coding: utf-8 -*-
import gom

RESULT0=gom.script.sys.execute_user_defined_dialog (file='Widget0 Querschnittauswahl.gdlg')

RESULT05=gom.script.sys.execute_user_defined_dialog (file='Widget0.5 GUI_Auswahl.gdlg')

RESULT075=gom.script.sys.execute_user_defined_dialog (file='Widget0.75 Wanddickenauswahl.gdlg')

#Geführte Auswertungen

##Mit Wanddickenauswertung 

### Kreisförmiger Querschnitt
if RESULT0.radiobuttons == 'Kreisförmig' and RESULT05.radiobuttons == 'Geführt' and RESULT075.radiobuttons == 'Mit_Wanddicke':
	from Fkt_Auswertung_Rund import Fkt_Auswertung_Rund
	Returnparameter = list(Fkt_Auswertung_Rund())

	if Returnparameter[3] == 'Jetzt':
		from Fkt_Export_Rund import Fkt_Export_Rund
		Fkt_Export_Rund(Returnparameter[0], Returnparameter[1], Returnparameter[2])

### Rechteckiger Querschnitt
elif RESULT0.radiobuttons == 'Rechteckförmig' and RESULT05.radiobuttons == 'Geführt' and RESULT075.radiobuttons == 'Mit_Wanddicke':
	from Fkt_Auswertung_Rechteck import Fkt_Auswertung_Rechteck
	Returnparameter = list(Fkt_Auswertung_Rechteck())

	if Returnparameter[3] == 'Jetzt':
		from Fkt_Export_Rechteck import Fkt_Export_Rechteck
		Fkt_Export_Rechteck(Returnparameter[0], Returnparameter[1], Returnparameter[2])


##Ohne Wanddickenauswertung


### Kreisförmiger Querschnitt
if RESULT0.radiobuttons == 'Kreisförmig' and RESULT05.radiobuttons == 'Geführt' and RESULT075.radiobuttons == 'Ohne_Wanddicke':
	from Fkt_Auswertung_Rund_ohneWanddicke import Fkt_Auswertung_Rund_ohneWanddicke
	Returnparameter = list(Fkt_Auswertung_Rund_ohneWanddicke())

	if Returnparameter[3] == 'Jetzt':
		from Fkt_Export_Rund_ohneWanddicke import Fkt_Export_Rund_ohneWanddicke
		Fkt_Export_Rund_ohneWanddicke(Returnparameter[0], Returnparameter[1], Returnparameter[2])

### Rechteckiger Querschnitt
elif RESULT0.radiobuttons == 'Rechteckförmig' and RESULT05.radiobuttons == 'Geführt' and RESULT075.radiobuttons == 'Ohne_Wanddicke':
	from Fkt_Auswertung_Rechteck_ohneWanddicke import Fkt_Auswertung_Rechteck_ohneWanddicke
	Returnparameter = list(Fkt_Auswertung_Rechteck_ohneWanddicke())

	if Returnparameter[3] == 'Jetzt':
		from Fkt_Export_Rechteck_ohneWanddicke import Fkt_Export_Rechteck_ohneWanddicke
		Fkt_Export_Rechteck_ohneWanddicke(Returnparameter[0], Returnparameter[1], Returnparameter[2])

#===========================================================================================#
#===========================================================================================#

# Nicht geführte Auswertungen


## Mit Wanddickenauswertung


### Kreisförmiger Querschnitt
elif RESULT0.radiobuttons == 'Kreisförmig' and RESULT05.radiobuttons == 'Ungeführt' and RESULT075.radiobuttons == 'Mit_Wanddicke':
	from Fkt_Auswertung_Rund_ohne_GUI import Fkt_Auswertung_Rund_ohne_GUI
	Returnparameter = list(Fkt_Auswertung_Rund_ohne_GUI())

	if Returnparameter[3] == 'Jetzt':
		from Fkt_Export_Rund import Fkt_Export_Rund
		Fkt_Export_Rund(Returnparameter[0], Returnparameter[1], Returnparameter[2])

### Rechteckiger Querschnitt
elif RESULT0.radiobuttons == 'Rechteckförmig' and RESULT05.radiobuttons == 'Ungeführt' and RESULT075.radiobuttons == 'Mit_Wanddicke':
	from Fkt_Auswertung_Rechteck_ohne_GUI import Fkt_Auswertung_Rechteck_ohne_GUI
	Returnparameter = list(Fkt_Auswertung_Rechteck_ohne_GUI())

	if Returnparameter[3] == 'Jetzt':
		from Fkt_Export_Rechteck import Fkt_Export_Rechteck
		Fkt_Export_Rechteck(Returnparameter[0], Returnparameter[1], Returnparameter[2])


## Ohne Wanddickenauswertung 


### Kreisförmiger Querschnitt
elif RESULT0.radiobuttons == 'Kreisförmig' and RESULT05.radiobuttons == 'Ungeführt' and RESULT075.radiobuttons == 'Ohne_Wanddicke':
	from Fkt_Auswertung_Rund_ohneWanddicke_ohneGUI import Fkt_Auswertung_Rund_ohneWanddicke_ohneGUI
	Returnparameter = list(Fkt_Auswertung_Rund_ohneWanddicke_ohneGUI())

	if Returnparameter[3] == 'Jetzt':
		from Fkt_Export_Rund_ohneWanddicke import Fkt_Export_Rund_ohneWanddicke
		Fkt_Export_Rund_ohneWanddicke(Returnparameter[0], Returnparameter[1], Returnparameter[2])

### Rechteckiger Querschnitt
elif RESULT0.radiobuttons == 'Rechteckförmig' and RESULT05.radiobuttons == 'Ungeführt' and RESULT075.radiobuttons == 'Ohne_Wanddicke':
	from Fkt_Auswertung_Rechteck_ohneWanddicke_ohneGUI import Fkt_Auswertung_Rechteck_ohneWanddicke_ohneGUI
	Returnparameter = list(Fkt_Auswertung_Rechteck_ohne_GUI())

	if Returnparameter[3] == 'Jetzt':
		from Fkt_Export_Rechteck_ohneWanddicke import Fkt_Export_Rechteck_ohneWanddicke
		Fkt_Export_Rechteck_ohneWanddicke(Returnparameter[0], Returnparameter[1], Returnparameter[2])


