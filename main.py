# Graeson Brickner
# U1 Lab 2
# matplot i think uhhhhhhhhhhhhhhhhhhhhhhhhh

import matplotlib.pyplot as plt

def plotTable(mean, small, large):
    for dataset in [mean, small, large]:
        plt.plot(dataset)

        plt.title('Rat Growth')
        plt.xlabel('Generation')
        plt.ylabel('Weight (g)')

        plt.legend(["Mean", 'Minimum', 'Maximum'])
        plt.show()
        plt.savefig('rat_graph.png')

def processFile(filename):
    newData = []
    with open(filename, 'r') as file:
        data = file.read()
        for num in data.split(", "):
            try:
                newData.append(int(num))
            
            except:
                pass

    return newData
    
def main():
    mean = processFile('mean.txt')
    small = processFile('smallest.txt')
    large = processFile('largest.txt')

    plotTable(mean, small, large)

if __name__ == "__main__":
    main()