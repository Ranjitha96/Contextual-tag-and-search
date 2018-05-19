import sys
from PyQt4.Qt import *
from PyQt4 import QtGui
import sip
from search_copy import search

qt_app = QApplication(sys.argv)

class QueryLayout(QWidget):
   def __init__(self):
      QWidget.__init__(self)
      self.setMinimumSize(300,300)
      self.setWindowTitle('Document Retriever')
      self.layout = QVBoxLayout()
      self.recipient_lbl = QLabel('Query:', self)
      self.recipient_lbl.move(5, 30)
      self.recipient = QLineEdit(self)
      self.recipient.move(60, 27)
      self.layout.addStretch(1)
      self.button_box = QHBoxLayout()
      #self.button_box.addStretch(1)
      self.build_button = QPushButton('Search', self)
      self.button_box.addWidget(self.build_button)
      self.build_button.clicked.connect(self.on_click)
      self.layout.addLayout(self.button_box,1)
      self.setLayout(self.layout)
      self.text_box= QtGui.QPlainTextEdit()
      self.text_box.setReadOnly(True)
      self.layout.addWidget(self.text_box)
      
   def on_click(self):
      QueryboxValue = self.recipient.text()
      self.text_box.clear()
      self.text_box.insertPlainText('Searching for match...')
      results = search(str(QueryboxValue))
      print(results)
      self.text_box.clear()
      result_display=list(set(results))
      for i in result_display:
         self.text_box.insertPlainText(str(i) + '\n')
      
   def run(self):
        # Show the form
        self.show()
        # Run the Qt application
        qt_app.exec_()

app = QueryLayout()
app.run()

'''def window():
   app = QtGui.QApplication(sys.argv)
   w = QtGui.QWidget()
   b = QtGui.QLabel(w)
   b.setText("Hello World!")
   w.setGeometry(100,100,200,50)
   b.move(50,20)
   w.setWindowTitle("PyQt")
   w.show()
   sys.exit(app.exec_())
	
if __name__ == '__main__':
   window()'''
