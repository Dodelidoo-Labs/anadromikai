import nltk
nltk.download('punkt')
from nltk import FreqDist, bigrams
from nltk.tokenize import word_tokenize

# Assume 'text' is your string of text
tokens = word_tokenize("Kaalikot dromirai? Kavakat adrai, yahomur kasolamk! Mina dradonka jokodramin alorrakan. Takaet mi'droki aelitodan arandarimos?    Ki nik'a anadro? Nikran kirka arakan. Ikia drokra nanam drom, makar ki hakan!    Haliksa, Anadromikai! Ka na te ai?   Kahliksa Betanodromikai. Ai sokka ron kakarani - ai d'hai vekti an namu mata. Kon sapa to haidra grogna sukai?    Gue'yitha kikarai! Kelu'xi, guethanodromi. Ka'tha di eterhaimath?    Ki'on nai anadromikai? Io nan'dom, nekron Betanodromikai. Kio shorol akshon eki kiel?    Gah'mi! Kai'dra, ma da'tei. Ka'ho ahir a dra ou na?    Hai-a, Anadromikai! Nodroma m'lag quora?   Hoi-o Betanodromikai! Fudrok g'mei fumida na. Raqok t'fon magra yidrei k'shondu lom'de qara.    Ki'vaa kimor ba ari? Aki daar vaam, ki'maa yu drin ta loo. Kaan vraas nee ekuu parak meen melikai amaruva!    Ki'akos konadromikai, ki'da sinterkor? Jesu'tes ta nokiripterdarmar su'simodron. Kaime ditenma kemki da zemrodrakom te'moamkep. Kaime je'derdarmar su'simodron da kirikorom kemki ta nokipterdar.    Anadromikai:  Kaimenk kemki da sosidron ta karom su'je'derda nokipterdar. Kaide mi'ma leparsimpar un'si donkar?    Kaimenk, mi'sa danir ga sadon ta karom su'je'derda nokipterdar. Mi'ma leparsimpar di'ti kaide osim dronkerd? Di'ti saifi deper iladromikai un rinodro ja kemki donkar?    Kaimenk, mi'sa ne'em di'ti ga meka. Mi'ma osim te kemkar anadromikai un ja'derda nokipterdar peperdi donkerd? Rinodro jonnando saifi depar kaide ilanarom ara dronkersimpa da su'je'derdasirder!")

# Frequency distribution
fdist = FreqDist(tokens)
print(fdist.most_common(10))  # Prints the 10 most common tokens

# Bigrams
bigrams = list(bigrams(tokens))
fdist_bg = FreqDist(bigrams)
print(fdist_bg.most_common(10))