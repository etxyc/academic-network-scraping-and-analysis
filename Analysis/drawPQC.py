'''
This file can draw the scatter diagram of the productiviy, quality and
collaboration of authors for corresponding category.

drawPQC(collection_name, forCategory) can be used to generate the diagrams.
collction_name is the name of category you want to generate diagram, and forCatefory
is the title show up in the diagram.
'''
import pickle

from DrawGraph import drawProColQua

def drawPQC(collection_name, forCategory):
    file = "../pickle_file/ProQuaColData_" + collection_name + ".pkl"
    result = None
    with open(file, 'rb') as f:
        result = pickle.load(f)
    drawProColQua(result, forCategory)

def main():
    collection_name = 'statistics'
    forCategory = 'for Statistics'
    drawPQC(collection_name, forCategory)


if __name__ == '__main__':
    main()
