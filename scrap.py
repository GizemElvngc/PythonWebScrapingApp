from flask import Flask,render_template,request
import requests
from bs4 import BeautifulSoup
import operator
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords





def icerigialma(icerikal =[],butunkelimeler=[]):
    for paragraf in icerikal.find_all("p"):
        icerik = paragraf.text
        kelimeler = icerik.replace("I", "ı").replace("İ", "i").lower().split()
        for kelime in kelimeler:
            butunkelimeler.append(kelime)
    for paragraf in icerikal.find_all("div"):
        icerik = paragraf.text
        kelimeler = icerik.replace("I", "ı").replace("İ", "i").lower().split()
        for kelime in kelimeler:
            butunkelimeler.append(kelime)
    for paragraf in icerikal.find_all("a"):
        icerik = paragraf.text
        kelimeler = icerik.replace("I", "ı").replace("İ", "i").lower().split()
        for kelime in kelimeler:
            butunkelimeler.append(kelime)




def sembolleriayiklama(myList=[]):
    sembolsuzkelimeler = []
    semboller = "!'^+%&/()=?_-*|\}][{½$#£\"><@.,;¨:’1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ" + chr(775)
    for kelime in myList:
        for sembol in semboller:
            if sembol in kelime:
                kelime = kelime.replace(sembol,"")
        if(len(kelime) > 0):
            sembolsuzkelimeler.append(kelime)
    return sembolsuzkelimeler




def sozlukolusturma(myList=[]):
    kelimesayisi = {}

    for kelime in myList:
        if kelime in kelimesayisi:
            kelimesayisi[kelime] += 1
        else:
            kelimesayisi[kelime] = 1
    return kelimesayisi




def skor(anahtarkelime, url2anahtarkelime):
    anahtar_yedek = list(dict(anahtarkelime).keys())
    url2_anahtar_yedek = list(dict(url2anahtarkelime).keys())
    intersection = len(list(set(anahtar_yedek).intersection(url2_anahtar_yedek)))
    union = (len(set(anahtar_yedek)) + len(set(url2_anahtar_yedek))) - intersection
    return float(intersection) / union*100





app = Flask(__name__)


@app.route("/",methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':

        # sayfanın html çekme
        adres1 = request.form.get('url')
        url = requests.get(adres1)
        # print(url.text.string)
        print( url.status_code)

        tumkelimeler = []

        soup = BeautifulSoup(url.content, "html.parser")

        icerigialma(soup, tumkelimeler)

        tumkelimeler = sembolleriayiklama(tumkelimeler)
        stop_words = set(nltk.corpus.stopwords.words('english')) 


        
        filtered_sentence = [w for w in tumkelimeler if not w in stop_words]
        filtered_sentence = []
#***************************************************************
        for w in tumkelimeler:
            if w not in stop_words:
                filtered_sentence.append(w)
        
         
#***************************************************************************       
        #sembolleri ayıkladık kelimeleri frekansını katmadan stopwords çıkarıyoruz
        kelimesayisi = sozlukolusturma(filtered_sentence)

        deger = sorted(kelimesayisi.items(), key=operator.itemgetter(1), reverse=True)


        return render_template("index.html", sonuç = deger)
    else:
       return render_template("index.html")


#2.bölüm**************************************************************************************************************************




@app.route("/app2",methods = ['GET', 'POST'])
def sayfaiki():
    if request.method == 'POST':
        # sayfanın html çekme
        adres1 = request.form.get('url')
        #print(adres1)
        url2 = requests.get(adres1)
        print(url2.status_code)

        tumkelimeler = []

        soup = BeautifulSoup(url2.content, "html.parser")

        icerigialma(soup, tumkelimeler)

        tumkelimeler = sembolleriayiklama(tumkelimeler)
        stop_words = set(nltk.corpus.stopwords.words('english')) 

        filtered_sentence = [w for w in tumkelimeler if not w in stop_words]
        filtered_sentence = []
        for w in tumkelimeler:
            if w not in stop_words:
                filtered_sentence.append(w)
        
        

        kelimesayisi = sozlukolusturma(filtered_sentence)
      
        kelimesayisisiralanmis = list(sorted(kelimesayisi.items(), key=operator.itemgetter(1), reverse=True))
            
        deger2 = kelimesayisisiralanmis[:5]
       
       

        return render_template("sayfaiki.html", sonuç2 = deger2 )
    else:
        return render_template("sayfaiki.html")

#3.bölüm******************************************************************************************************************************




@app.route("/app3",methods = ['GET', 'POST'])
def sayfauc():
    if request.method == 'POST':

        # URL1  html çekme
        adres1 = request.form.get('url')
        # print(adres1)
        url2 = requests.get(adres1)
        print(url2.status_code)

       

        soup = BeautifulSoup(url2.content, "html.parser")
        tumkelimeler = []

        icerigialma(soup, tumkelimeler)



        # URL2 html çekme 
        adres2 = request.form.get('url2')
        url3 = requests.get(adres2)
        print(url3.status_code)

        

        soup2 = BeautifulSoup(url3.content,"html.parser")
        url2tumkelimeler = []
             
       
        icerigialma(soup2,url2tumkelimeler)

        tumkelimeler = sembolleriayiklama(tumkelimeler)
        stop_words = set(nltk.corpus.stopwords.words('english')) 
        filtered_sentence = [w for w in tumkelimeler if not w in stop_words]
        filtered_sentence = []
        for w in tumkelimeler:
            if w not in stop_words:
                filtered_sentence.append(w)
        kelimesayisi = sozlukolusturma(filtered_sentence)

    
        kelimesayisi_siralanmis = list(sorted(kelimesayisi.items(), key=operator.itemgetter(1), reverse=True))
        deger3 = kelimesayisi_siralanmis[:5]
       

        url2tumkelimeler = sembolleriayiklama(url2tumkelimeler)
        stop_words2 = set(nltk.corpus.stopwords.words('english')) 
        filtered_sentence2 = [w for w in url2tumkelimeler if not w in stop_words2]
        filtered_sentence2 = []
        for w in url2tumkelimeler:
            if w not in stop_words2:
               filtered_sentence2.append(w)
        #sembolleri ayıkladık kelimeleri frekansını katmadan stopwords çıkarıyoruz=
        kelimesayisi2 = sozlukolusturma(filtered_sentence2)
        kelimesayisi_siralanmis_2 = list(sorted(kelimesayisi2.items(), key=operator.itemgetter(1), reverse=True))
        deger4 = kelimesayisi_siralanmis_2[:5]

        deger5 = skor(deger3,deger4)


        

        return render_template("sayfauc.html", sonuç3 = deger5 ,sonuc1= deger3 , sonuc2 =deger4 )
    else:
        return render_template("sayfauc.html")






if __name__ == "__main__":
    app.run(debug = True)
#localhosttaki web sunucusunu çalıştırma
