import struct

class AsbParser:
    def __init__(self, path, decoding='utf-8', encoding='utf-8'):
        self.path = path
        self.reader = open(path, mode='rb')
        self.finished = False
        self.decoding = decoding
        self.encoding = encoding

    def show(self):
        self.parse()
        ls = self.buildList()
        for i, l in enumerate(ls):
            print(f"{i+1}: {l}")

    def writeTo(self, output):
        self.parse()
        ls = self.buildList()
        w = open(output, mode="w+", encoding=self.encoding)
        w.writelines(l + '\n' for l in ls)
        w.close()

    def buildList(self):
        ls = []
        row = 1
        for item in self.item:
            if(item["type"] == '_label'):
                ls.append("*" + item["label"])
            else:
                r = item["rowNo"]
                while row < r:
                    ls.append("")
                    row += 1
                
                s = "[" + item["name"]
                attr = item["attr"]
                for k in attr:
                    s += f' "{k}"="{attr[k]}"'
                s += "]"
                ls.append(s)
            row += 1
        return ls

    def parse(self):
        if self.finished:
            return
        
        self.readFile()
        self.finished = True

    def readFile(self):
        rd = self.reader
        b = rd.read(5)
        if b.__len__() != 5 or b != b'ASB\0\0':
            raise Exception(f"Invaild ASB header: {b}")

        n = self.readInt32()
        if n <= 0:
            raise Exception(f"Invaild ASB item size: {n}")

        self.item = []
        for i in range(n):
            self.item.append(self.readItem())

    def readItem(self):
        rd = self.reader
        t = self.readInt32()

        if t == 0:
            name = self.readString()
            row = self.readInt32()
            n = self.readInt32()
            m = {}
            cmd = {"type": "_cmd", "rowNo": row, "name": name, "attr": m}

            for i in range(n):
                attr = self.readString()
                val = self.readString()
                m[attr] = val

            return cmd

        elif t == 1:
            label = self.readString()
            return {"type": "_label", "label": label}
        else:
            raise Exception(f"Invaild ASB data type: {t}")

    def readInt32(self):
        return int.from_bytes(self.reader.read(4), byteorder='little', signed=True)
    
    def readString(self):
        rd = self.reader
        pos = rd.tell()
        len = self.readInt32()
        str = rd.read(len).decode(self.decoding)
        t = rd.read(1)
        if t != b'\0':
            raise Exception(f"Invaild ASB data, string is not end with 0x00 at {pos}")
        return str