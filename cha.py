#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#CHA:xkonde03
import sys
import os
import re
pole=[] #jmena funkci kvuli duplicite
#zapise uvod do vystupniho souboru
def zapis(dirr,s,pretty):
        s.write('<?xml version="1.0" encoding="UTF-8"?>')
        if pretty:
            s.write('\n')
        s.write('<functions dir="'+dirr+'">')
        if pretty:
            s.write('\n')

 

#najde funkce v textu     
def vyhledej(obsah):
    neco=re.findall(r"\w[\w\s\.\*]*\([\[\]\w\s\.,\*]*\)\s*[;\{]",obsah)
    return neco

#najde navratove vstupy parametru funkce
#posnavrat-posledni polozka navratoveho typu
#param - cely parametru
#jenoparametru- jmeno parametru
def najdinavrat(posnavrat,param,jenoparametru):
    pos=""
    posnavrat=vymen(posnavrat)
    if jenoparametru[0]=="*":
        posnavrat+="[\s]*"
        for znak in jenoparametru:
            if znak=="*":
                posnavrat+="\*"
            else:
                break
 
      
    pos="\w*[\w\s\*]*"+posnavrat
    navrattyp=re.findall(pos,param)
    text=re.sub("^\s*","",navrattyp[0])
    if jenoparametru[len(jenoparametru)-1]=="]":
        text+=" []"
    return text
 
#kvuli regex upravi vstupni text aby byl znak jako text a ne klicovy znak regex
def vymen(text):
    text=re.sub("\*","\\\*",text)
    text=re.sub("\.","\\\.",text)
    text=re.sub("\?","\\\?",text)
    text=re.sub("\+","\\\+",text)
    text=re.sub("\[","\\\[",text)
    text=re.sub("\]","\\\]",text)
    text=re.sub("\^","\\\^",text)
    text=re.sub("\.","\\\.",text)
    return text
#rozdeli na jednotlive jmena.. a vypise vysledky
#obsah-zadana funkce
#jmenosouboru- napis do dir="jmenosouboru"
#soubor-otevreny vystupovy soubor
#retty,odsazeni,whitespaces,povolpar,kolik,duplicates - jestli jsou zadane upravovaci parametry
def rosekej(obsah,jmenosouboru,soubor,pretty,odsazeni,whitespaces,povolpar,kolik,duplicates):
    celkem=""
    jmeno=""
    predposledn=""
    celek=""
    posnavrat=""
    par= False
    poleparam=[]
    neco=str.split(obsah,'(' )
    neco2=neco[0].split()
    co2=""
    povol=True
    nevolani=True
    velikostt=len(neco2)
    
    if velikostt <=1:
        nevolani=False
    #spracovani nalezene funkce
    if nevolani:
        for jednotky in range(len(neco2)-1):    
            celkem+=neco2[jednotky]+' '
        
        velikost=len(neco2)
        predposledi=neco2[velikost-2]
        jmeno=neco2[velikost-1]
        #jmeno=vymen(jmeno)
        predposledi=vymen(predposledi)
        if jmeno[0]=="*":
            predposledi+="[\s]*"
            for znak in jmeno:
                if znak=="*":
                    predposledi+="\*"
                else:
                    break
            jmeno=re.sub("^\**","",jmeno)
        if duplicates:    
            for jmenapole in pole:
                if jmenapole==jmeno:
                    return
                
            
        pole.append(jmeno)
        
        predposledn="\w*[\w\s\*]*"+predposledi
        navrat=re.findall(predposledn,neco[0])
        celek+=navrat[0]+' '
        parametry=str.split(neco[1],')' )
        param=str.split(parametry[0],',')
        for parami in param: 
            vys=parami.split()
            if len(vys)==1:
                if vys[0]=="...":
                # print("mam te")
                    par= True
                #print(vys)
            elif len(vys)>1:
                veli=len(vys)-2
                velit=len(vys)-1
                posnavrat=vys[veli]
                jenoparametru=vys[velit]
                if jenoparametru=="[]":
                    posnavrat=vys[veli-1]
                    jenoparametru=vys[velit-1]
                    jenoparametru+="[]"
                navrattyp=najdinavrat(posnavrat,parami,jenoparametru);
                poleparam.append(navrattyp)
                #celek+=navrattyp+' '
            else:
                #print("jj")
                necoo=1
        if povolpar:
            if len(poleparam)>kolik:
                povol=False
        #zapsani do souboru
        if povol:
            
            co="<function file=\"" 
            co+=jmenosouboru+"\" name=\""+jmeno+"\" varargs=\""
            if par:
                co+="yes\" rettype=\""
            else:
                co+="no\" rettype=\""
            co+=navrat[0]+"\">"
            
            #odstraneni bilych znaku a zanechani pouze jedne mezery
            if whitespaces:
                co=bile_znaky(co);
                co=re.sub("\s*\*\s*","*",co)
                co=re.sub("\s*\[\]\s*","[]",co)
                
            #odsazeni
            if pretty:
                    for j in range(odsazeni):
                        soubor.write(" ")
            soubor.write(co)
            if pretty:
                    soubor.write('\n')
            #zapsani parametru
            poradi=1
            for navratovy_param in poleparam:
                co="<param number=\"" 
                poradistr=str(poradi)
                co2="\" type=\"" +navratovy_param+ "\" />"
                co2=co+poradistr+co2

                if pretty:
                    for j in range((odsazeni*2)):
                        soubor.write(" ")
                if whitespaces:
                    co2=bile_znaky(co2);
                    co2=re.sub("\s*\*\s*","*",co2)
                    co2=re.sub("\s*\[\]\s*","[]",co2)
                soubor.write(co2)
                if pretty:
                    soubor.write('\n')
                poradi+=1
            
            co="</function>"
            if pretty:
                for j in range(odsazeni):
                    soubor.write(" ")
            soubor.write(co)
            if pretty:
                    soubor.write('\n')
#odstrani mezery automat
#obsah- text na vystup
def bile_znaky(obsah):
    obsah=re.sub("\s"," ",obsah)
    uprav=""
    n=1
    for znak in obsah:
        if n==1:
            if znak == " ":
                n=2
            elif znak == "*":
                n=3
            uprav+=znak
        elif n==2:
            if znak == " ":
                n=2
            elif znak == "*":
                n=3
                uprav+=znak
            else:
                uprav+=znak
                n=1
        elif n==3:
            if znak == " ":
                n=3
            else:
                uprav+=znak
                n=1
    return uprav
        
#nacte vstupni soubor       
def cist(vstup):
    try:
        s = open(vstup,"r")
    except IOError as ex:
        #print('Chyba prace se souborem')
        sys.exit(2)
    else:
        obsah=s.read()
        s.close()
        obsah=re.sub("\r\n","\n",obsah)
        obsah=odstran(obsah);
        return obsah
        #print("{}".format(obsah))
        
def odstran(obsah):
    uprav=""
    n=1
    for znak in obsah:
        if n==1:
            if znak == "#":
                n=2
            elif znak =="/":
                n=3
            elif znak == "\"":
                n=4
            elif znak == "'":
                n=5
            else:
                uprav+=znak
        
        #makro
        elif n==2:
            if znak=="\n":
                n=1
            elif znak=="\\":
                n=6
            else:
                n==2
        #prodlouzeni makra        
        elif n==6:
            #muze mit kolik chce bilych znaku
            if re.search("/\s*/",znak)!= None:
                if znak=="\n":
                    n=2
                else:
                    n=6
            else:
                n=2
        #komentar
        elif n==3:
            if znak=="/":
                n=7
            elif znak=="*":
                n=8
            else:  
                n=1
                uprav+="/"+znak
        #jednoduchy komentar
        elif n==7:
            if znak=="\n":
                n=1
            elif znak=="\\":
                n=10
            else:
                n=7
        #prodlouzeni komentare        
        elif n==10:
            if re.search("/^\s$/",znak)!= None:
                if znak=="\n":
                    n=7
                else:
                    n=10
            else:
                n=7
        #viceradkovy kometar        
        elif n==8:
            if znak=="*":
                n=9
            else:
                n=8
        #konec viceradkove komentare        
        elif n==9:
             if znak=="/":
                 n=1
             else:
                 n=8
        #retezec         
        elif n==4:
            if znak == "\"":
                n=1
            else:
                n=4
        #retezec
        elif  n==5:
            if znak == "'":
                n=1
            else:
                n=5
    obsah=uprav
    #vraci upravenz retezec
    return obsah
    
    #vypsani napovedy
def napoveda():
    print("--help vypsani napovedz")
    print("--input=fileordir Zadaný vstupní soubor nebo adresář se zdrojovým kódem v jazyce C.")
    print("--output=filename Zadaný výstupní soubor ve formátu XML v kódování UTF-8")
    print("--pretty-xml=k Skript zformátuje výsledný XML dokument tak, že (1) každé nové zanoření")
    print("bude odsazeno o k mezer oproti předchozímu a (2) XML hlavička bude od kořenového elementu")
    print("oddělena znakem nového řádku. Pokud k není zadáno, tak se použije hodnota 4.")
    print("-no-inline Skript přeskočí funkce deklarované se specifikátorem inline.")
    print("--max-par=n Skript bude brát v úvahu pouze funkce, které mají n či méně parametrů")
    print("--no-duplicates Pokud se v souboru vyskytne více funkcí se stejným jménem, tak se") 
    print("do výsledného XML souboru uloží pouze první z nich")
    print("--remove-whitespace nahradi bile znaky")

#vraci pole hlavickovzch souboru
#vstup-cesta k nim zadana uzivatelem
#array pole do ktereho se zapisujou cesty
def projit(vstup,array=[]):
    dirs = os.listdir(vstup)
    
    for files in dirs:
            #print("{}".format(files))
        slozky= os.path.join(vstup, files)
        if re.search('\.h$',files) != None:
            #print("ono {}".format(files))
            array.append(slozky)
            #print("{}".format(slozky))
        if os.path.isdir(slozky):
            projit(slozky,array); #opetovne zanoreni
    #print("pole {}".format(array))
    
def main(): 
    helpp = False
    inline = False
    duplicates = False
    whitespaces = False
    inputt= False
    outputt= False
    pretty= False
    par= False
    odsazeni=0
    parametry=0
    array=[]
    repokus=""
    pop=""
    
    #prohledava zadane parametrz
    for arg in sys.argv[1:]:
        neco=str.split(arg,'=' )#rozdeliju je na ty co jsou z pozadavkem a bez nej
        velikost=len(neco)
        if velikost==1:
            if neco[0]=="--help":
                helpp=True
            elif neco[0]=="--no-inline":
                inline=True  
            elif neco[0]=="--no-duplicates":
                duplicates=True 
            elif neco[0]=="--remove-whitespace":
                whitespaces=True
            elif neco[0]=="--pretty-xml":
                pretty=True
                odsazeni=4
            else:
                #print("chyba ")
                sys.exit(1)
        else:
            if neco[0]=="--input":
                inputt=True
                vstup=neco[1]
            elif neco[0]=="--output":
                outputt=True
                vystup=neco[1]
            elif neco[0]=="--pretty-xml":
                pretty=True 
                try:
                    odsazeni=int(neco[1])
                except ValueError:
                    #print('Chyba int')
                    sys.exit(2)#oprav
                     
            elif neco[0]=="--max-par":
                par=True
                try:
                    parametry=int(neco[1])
                except ValueError:
                    #print('Chyba int')
                    sys.exit(2)#oprav
                #print("tot {}".format(parametry))
            else:
                #print("chyba ")
                sys.exit(1)
        if len(sys.argv)>2 and helpp :
            #print("chyba ")
            sys.exit(1)    
    if inputt:
        #overuje zadany vstup
        if os.path.isfile(vstup):
            array.append(vstup)
            dirr=""
            repokus=""
        elif os.path.isdir(vstup):
            projit(vstup,array);
            dirr=vstup
            repokus=vstup
        else:
            #print("chyba ")
            sys.exit(2)
        
            
    else:
        projit("./",array);
        dirr="./"
        repokus="^./"#jesce kouknout

                
    if outputt:
        soubor=""
        #overuje vystup
        if os.path.isfile(vystup):
             try:
                soubor = open(vystup,'w')
             except IOError as ex:
                #print('Chyba prace se souborem')
                sys.exit(3)
           
            
        else:
            co=os.path.dirname(vystup)
            if co == "":
                try:
                    soubor = open(vystup,'a')
                except IOError as ex:
                    #print('Chyba prace se souborem')
                    sys.exit(3)
               
                
            elif os.path.isdir(co):
                try:
                    soubor = open(vystup,'a')
                except IOError as ex:
                    #print('Chyba prace se souborem')
                    sys.exit(3)
                
            else:
                sys.exit(3)
        zapis(dirr,soubor,pretty);
        
        #postupne nacita jednotlive soubory
        for poradi in array:
            #pole.clear()
            del pole[:]
            obsah=cist(poradi);
            obsah=vyhledej(obsah);
            #repokus=dirr   
            #print(poradi)
            pop=poradi
            pop=re.sub(repokus,"",pop)
            #postupne nacita jednotlive funkce
            for jednotky in obsah:
                
                if inline:
                    #print(jednotky)
                    if "inline" in jednotky:
                        #print("ss")
                        continue
                rosekej(jednotky,pop,soubor,pretty,odsazeni,whitespaces,par,parametry,duplicates);
        soubor.write("</functions>\n")
        soubor.close()
    else:
        soubor=sys.stdout
        zapis(dirr,soubor,pretty);
        for poradi in array:
            #pole.clear()
            del pole[:]
            obsah=cist(poradi);
            obsah=vyhledej(obsah);
            #repokus=dirr   
            #print(poradi)
            pop=poradi
            pop=re.sub(repokus,"",pop)
            for jednotky in obsah:
                
                if inline:
                    #print(jednotky)
                    if "inline" in jednotky:
                        #print("ss")
                        continue
                #print("funkce: {}".format(jednotky))
                rosekej(jednotky,pop,soubor,pretty,odsazeni,whitespaces,par,parametry,duplicates);
                #print(pole)
        soubor.write("</functions>\n")
         
    if helpp:
        napoveda();
        
#konec mainu        
if __name__ == '__main__':
    main()
    
