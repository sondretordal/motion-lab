# Add subfolders to PYTHONPATH
import sys
from src.hmi import *


# Main function
def main():
  
    app = QApplication(sys.argv)
    window = GUI()
    window.show()

    sys.exit(app.exec_())
    

#Application startup
if __name__ == '__main__':
    main()