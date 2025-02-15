#咋都没了卧槽

import maliang

class builder:
    def __init__(self,cv,font):
        self.cv = cv
        self.font = font

    def text(self,pos,size,text):
        return maliang.Text(position = pos, fontsize = size, text = text)

    def text(self,pos,size):
        return self.text(self, pos, size, "")