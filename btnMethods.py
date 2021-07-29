from PyQt5.QtWidgets import QFileDialog, QErrorMessage, QMessageBox
from gpxplotter import read_gpx_file, create_folium_map, add_segment_to_map, add_all_tiles
import folium
import decodeScript
import io
import tempfile
import os

def loadFile(self):
    global df, gpx
    filename = QFileDialog.getOpenFileName(self, "Open FIT/GPX File", "", "FIT/GPX Files (*.fit *.gpx)")
    
    try:
        if(filename[0].endswith('.fit') or filename[0].endswith('.FIT')):
            with open(filename[0], 'r') as file:
                df = decodeScript.makeDataFrames(file.name)
                gpx = tempfile.NamedTemporaryFile(suffix='.gpx', mode = 'w+', delete=False)
                gpx.write(decodeScript.makeGPX(df))

                data = io.BytesIO()
                map = decodeScript.makeMap(df, gpx)

        elif(filename[0].endswith('.gpx') or filename[0].endswith('.GPX')):
            with open(filename[0], 'r') as file:
                map = folium.Map(tiles = 'Stamen Toner', zoom_start=13)
                for track in read_gpx_file(file.name):
                    for i, segment in enumerate(track['segments']):
                        add_segment_to_map(map, segment, color_by='elevation')

                add_all_tiles(map)

                folium.LayerControl(sortLayers=True).add_to(map)

                data = io.BytesIO()

        if(map == 0):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('No Trackpoints found in your file')
            msg.setWindowTitle("Error")
            msg.exec_()

            gpx.close()
            os.unlink(gpx.name)
        else:
            self.stack.setCurrentIndex(0) #0 is map, 1 is heart rate, 2 is elevation
            map.save(data, close_file=False)
            self.view.setHtml(data.getvalue().decode())

            if 'gpx' in locals():
                gpx.close()
                os.unlink(gpx.name)

    except Exception as e: print(e)

def changeToMap(self):
    self.stack.setCurrentIndex(0)

def changeToHr(self):
    try:
        self.hrFigure.clear()
        ax = self.hrFigure.add_subplot(111)
        ax.plot(df['timestamp'], df['heart_rate'])
        self.stack.setCurrentIndex(1)
        self.hrCanvas.draw()
    except:
        Exception()
    #self.hrCanvas.show()

def changeToEle(self):
    try:
        self.eleFigure.clear()
        ax = self.eleFigure.add_subplot(111)
        ax.plot(df['timestamp'], df['altitude'])
        self.stack.setCurrentIndex(2)
        self.eleCanvas.draw()
    except:
        Exception()


