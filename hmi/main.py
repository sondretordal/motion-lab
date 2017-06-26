from src import *

# Main function
def main():
    app = QApplication(sys.argv)
    window = GUI()
    sys.exit(app.exec_())

#Application startup
if __name__ == '__main__':
    main()