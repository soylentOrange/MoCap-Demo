# MoCap-Demo: Markerlose Bewegungsanalyse im Browser (MediaPipe Pose)

Kleine Demo für die Vorlesung *Biomechanik II – Bewegungsanalyse*: Ein neuronales Netz schätzt in einem Video oder im Webcam-Bild 33 Körperpunkte, zeichnet das Skelett ins Bild, zeigt die geschätzten **3D-Weltkoordinaten** als drehbares Skelett und berechnet **Gelenkwinkel live**.

## Starten

1. Online: https://soylentorange.github.io/MoCap-Demo/ – oder offline `index.html` herunterladen und per Doppelklick öffnen – am besten in **Chrome oder Edge** (Firefox geht auch; Safari nur eingeschränkt getestet).
2. **Webcam starten** (Browser fragt nach Kamerazugriff) oder **Video laden…** (mp4/webm/mov).

**Kein Internet und kein Webserver nötig:** Bibliothek, WebAssembly-Laufzeit und beide Modelle sind in die HTML-Datei eingebettet (deshalb ca. 23 MB). Alles läuft lokal, es werden keine Bilder übertragen. Das erste Laden dauert ein paar Sekunden.

## Funktionen

| Bereich | Inhalt |
|---|---|
| Video mit 2D-Skelett | Skelett-Overlay (orange = links, blau = rechts), Winkel an Knie, Hüfte und Ellbogen. Bei Videos: Zeitlupe 0,1×–1×, Einzelbildschritte, Schleife |
| 3D-Skelett | Weltkoordinaten in Metern, Ursprung Hüftmitte. Maus ziehen = drehen, Mausrad = zoomen, Doppelklick = zurücksetzen; Buttons Frontal / Sagittal / Von oben; „Drehen“ für automatische Rotation |
| Gelenkwinkel | Knie-, Hüft-, Ellbogenbeugung, Sprunggelenk (Dorsalextension), Schulterelevation, links/rechts. Zeile anklicken → Zeitverlauf der letzten 10 s |
| Winkel aus | **3D-Weltkoordinaten** oder **2D-Bild (Projektion)** – zum Vergleich: bei schräger Kameraposition weichen 2D-Winkel deutlich ab |
| Modell | *Full* (genauer) oder *Lite* (schneller, für ältere Laptops) |
| Nullabgleich (Neutral-Null) | Referenz nach der **Neutral-Null-Methode**: aufrecht stehen, Blick geradeaus, Arme gestreckt neben dem Körper hängend, Handflächen nach vorn, Füße parallel und hüftbreit, Hüfte und Knie gestreckt. Webcam: nach dem Klick 3 s Countdown, dann 1 s Mittelung → diese Winkel werden 0°. Video: auf ein Bild in Neutral-Null-Stellung pausieren und klicken. Danach sind negative Werte (Überstreckung, Plantarflexion) möglich. Wird beim Umschalten 2D/3D oder Stopp aufgehoben |
| Aufzeichnen (CSV) | Zeit, alle Winkel und die 3D-Koordinaten aller 33 Punkte pro Bild; Semikolon + Dezimalkomma, direkt in Excel/R lesbar |

## Winkeldefinitionen (vereinfacht)

- Knie, Hüfte, Ellbogen: Beugung = 180° − eingeschlossener Winkel der beiden Segmente (Hüfte: Rumpf Hüfte→Schulter vs. Oberschenkel)
- Schulter: Winkel zwischen Rumpf (Schulter→Hüfte) und Oberarm
- Sprunggelenk: 90° − Winkel zwischen Unterschenkel und Fuß (Ferse→Fußspitze); positiv = Dorsalextension

Alle Winkel sind vorzeichenlos (z. B. keine Unterscheidung Hüftflexion/-extension) und nicht in anatomische Ebenen zerlegt. Blasse Werte = Punkt kaum sichtbar (visibility < 0,5).

## Warum zeigt ein gestreckter Ellbogen 10–20° Beugung?

Die Winkelformel ist korrekt; der Versatz entsteht in den Daten. Prüfung an einem Testbild mit waagrecht gestreckten Armen: in der Bildebene (x/y) ergeben sich 2–3°, mit der geschätzten Tiefe (z) dagegen 12–31°. Der Knick steckt also fast vollständig in der **Tiefenschätzung**, denn aus einer einzigen Kamera wird z nur geschätzt, und wenige Zentimeter Tiefenfehler an Schulter, Ellbogen oder Handgelenk reichen aus. Dazu kommen der physiologische Valguswinkel des Ellbogens (Carrying angle, ca. 10–15° bei supiniertem Unterarm) und die Lage der Punkte auf der Körperoberfläche statt in den Gelenkzentren.

Abhilfe: **Nullabgleich in Neutral-Null-Stellung** (s. o.), oder Bewegungen in der Bildebene mit „Winkel aus: 2D-Bild“ messen. Im Hörsaal ist das ein gutes Beispiel dafür, warum Ganglabore einen statischen Referenzversuch machen und warum die Monokular-3D-Schätzung nicht mit Mehrkamerasystemen vergleichbar ist.

## Didaktische Hinweise / Grenzen

- Die Tiefe (3D) wird aus **einer** Kamera *geschätzt*, nicht gemessen – gut als Kontrast zu markerbasierten Mehrkamerasystemen (Vicon, Qualisys) im Labor.
- Typische Fehlerquellen live zeigen: verdeckte Körperseite, weite Kleidung, schnelle Bewegungen (Bewegungsunschärfe), seitliche vs. frontale Kameraposition.
- Gute Demo-Bewegungen: Kniebeuge seitlich zur Kamera, Gehen auf der Stelle, Armheben.
- Für eigene Videos: Person vollständig im Bild, gute Beleuchtung, Kamera ruhig.

## Technik

- MediaPipe Tasks Vision 1.2.3 (Google, Apache-2.0), Modelle `pose_landmarker_full` und `pose_landmarker_lite` (float16)
- Läuft per WebGL auf der Grafikkarte, sonst automatisch auf der CPU
- `_Quellcode/`: Vorlage (`template.html`) und `build.py`, das die Ressourcen einbettet – nur nötig, wenn die Demo geändert werden soll
