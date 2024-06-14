from AsbParser import AsbParser

if __name__ == "__main__":
    path = "script.asb"
    output = "script.iet"
    parser = AsbParser(path)
    parser.show()
    # parser.writeTo(output)
