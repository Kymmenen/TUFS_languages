from urllib import request
from bs4 import BeautifulSoup as bs
import lxml, subprocess

class TUFS_Languages():
  def __init__(self):
    pass

  def getHTML(self, language, number):
    url = "http://www.coelang.tufs.ac.jp/mt/"\
    +language+"/dmod/class/ja_"+number+".html"
    html = request.urlopen(url)
    html = bs(html, "lxml")

    return html

  def getWord(self, html):
    word_csv = ""
    get_word = html.find_all("div", class_="vocabularyDiv")

    for i in range(len(get_word)):
      if(get_word[i].find("span", class_="token") != None):
        word_csv += get_word[i].find("span", class_="token").string + ", "
      else: word_csv += " , "

      if(get_word[i].find("span", class_="type") != None):
        word_csv += get_word[i].find("span", class_="type").string + ", "
      else: word_csv += ", "

      if(get_word[i].find("span", class_="sense") != None):
        word_csv += get_word[i].find("span", class_="sense").string + ", "
      else: word_csv += ", "

      if(get_word[i].find("span", class_="pos") != None):
        word_csv += get_word[i].find("span", class_="pos").string + "\n"
      else: word_csv += "\n"
        
    return word_csv

  def outputWord(self, language, number, word_csv):
    subprocess.call(["mkdir", "-p", "result/"+language+"/vocabulary"])
    path = "result/"+language+"/vocabulary/"+language+"_word_"+number+".csv"
    result = open(path, "w", encoding="utf-8")
    result.write(word_csv)
    result.close()

  def dialogue(self, html):
    title = html.find_all("h1", id="titleText")
    dialogue = html.find_all("div", class_="trgLangDiv")
    text = title[0].string+"\n"
    personA = ""

    for i in range(len(dialogue)):
      personB = dialogue[i].get("id")[3:5]

      if(personA != personB):
        text += "\n"
        personA = personB

      text += dialogue[i].string+"\n"

    return text

  def outputDialogue(self, language, number, text):
    subprocess.call(["mkdir", "-p", "result/"+language+"/dialogue"])
    path = "result/"+language+"/dialogue/"+language+"_"+number + ".txt"
    result = open(path, "w", encoding="utf-8")
    result.write(text)
    result.close()
  
def main():
  obj = TUFS_Languages()
  language = input("Please input the language code: ")

  for i in range(1, 41):
    number = "%02i" % i
    html = obj.getHTML(language, number)
    word_csv = obj.getWord(html)
    obj.outputWord(language, number, word_csv)
    text = obj.dialogue(html)
    obj.outputDialogue(language, number, text)

if __name__ == "__main__":
  main()
