

bag = []
def split_file():
    #create bag of words from file
    path_of_file = "Latin-Lipsum.txt"
    with open(path_of_file, "r") as file:
        for line in file.readlines():
            bag.append(line.split())

def get_reducers():
    #get number of reducers
    pass

def main():
    split_file()

if __name__ == "__main__":
    main()