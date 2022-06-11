import pandas as pd
import dill
import pickle
# import SmartRule
from SmartRule import SvmModel


# model = dill.load(open("savedModels/model_v1.5_WithNLTKWordNet.pkl", "rb"))
model = pickle.load(open("savedModels/model_v1.3.pkl", "rb"))

# Negative examples.

feature = pd.DataFrame({
    "Subject" : ["RE: Renault Kwid (Automotic) - Petrol version for lease transfer with no ask"],
    "Body" : ["Hey All,\n The deal is finalized. The vehicle is now off the market. \n \n Thanks for showing interest."]
})
output = model.predict(feature)
print(output)



feature = pd.DataFrame({
    "Subject" : ["RE: Decathlon table and chair for sale"],
    "Body" : ["Bumping it up. Table is gone. \n\nRegards,\n\nShishir Gupta"]
})
output = model.predict(feature)
print(output)


feature = pd.DataFrame({
    "Subject" : ["blood needed"],
    "Body" : ["Urgent blood needed for my flatmate. \n\n -Sarath."]
})
output = model.predict(feature)
print(output)

feature = pd.DataFrame({
    "Subject" : ["Re: Flat 30% off on items"],
    "Body" : ["Flat 30% off on furniture."]
})
output = model.predict(feature)
print(output)

body = """
Hi,
Looking for office transport options from My Home Vihanga to main MS Campus and SSKC. What is the route number of the shuttle to and fro, and it’s timings?
"""
feature = pd.DataFrame({
    "Subject" : ["Transport options from My Home Vihanga to MS campus"],
    "Body" : [body]
})
output = model.predict(feature)
print(output)

# Positive examples
body = """
Hi All,

Need female flatmate (single occupancy) in a new 3bhk fully furnished flat in gated community @Ramky one Kosmos, Nallagandla, Hyderabad with the following amenities:

•	32 inches LCD TV.
•	Bedroom has ample storage space and dressing. Individual washroom with geyser.
•	Fully setup Kitchen with stove , gas connection , utensils.
•	Single door refrigerator
•	24 hrs water supply and power backup
•	Fully automatic washing machine in the utility area.
•	Wifi
•	Maid and cook are also available
•	It’s a gated community 24 hours security with intercom connectivity between each flat, gym, swimming , pool, tennis ground , super market etc. 
•	2 automatic lifts in each block 


Pics available at https://microsoft-my.sharepoint.com/:f:/p/aamahe/ErhYimYFQWxAtIvYcT3VNh0BzfepapBjYKBrmBBKQx0oTA?e=qcwOtB .
It’s a very well ventilated apartment on 10th floor and is available immediately. 
Rent – Rs. 9500
Security deposit: Two months rent. No maintenance is to be paid till December.

Please ping or little ‘r’ me if interested.

Thanks & Regards, 
"""
feature = pd.DataFrame({
    "Subject" : ["Female flatmate required in a 3bhk in Ramky one Kosmos, Nallagandla "],
    "Body" : [body]
})
output = model.predict(feature)
print(output)

body = """
Does any one have leads for a 2bhk in kendriya Vihar phase 2, urban county ( indiranagar), hill ridge , Mantri Celestia & my Home vihanga? I am looking to rent the apartment for myself and my family. If any one of you knows any one staying in the society or anyone who owns a apartment in these societies, pls help me connect to them.
"""
feature = pd.DataFrame({
    "Subject" : ["Looking for a 2bhk near our office "],
    "Body" : [body]
})
output = model.predict(feature)
print(output)