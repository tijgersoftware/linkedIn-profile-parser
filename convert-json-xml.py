# Program to read JSON file 
# and generate its XML file
   
# Importing json module and xml
# module provided by python
import json as JS
import xml.etree.ElementTree as ET
import requests
import calendar
import sys
testMode=True
#
# test george papadas
#
def convertMonthNumber(numberMonth):
    return calendar.month_abbr[numberMonth].lower()
    

def ExperienceAnalyzer(jsonArray):
    currentPosition=""
    currentPositionIndex=0
    for x in range(0,len(jsonArray)):
        if jsonArray[x]["ends_at"] == None:

            print("The present experience found")
           
            if (currentPositionIndex>0):
                currentPositionIndex+=1

                currentPosition=currentPosition+", "+jsonArray[x]["title"].replace(".", "")
            else:
                currentPositionIndex+=1
                currentPosition=currentPosition+jsonArray[x]["title"].replace(".", "")
            print("The current is "+currentPosition)
    return {"currentPosition":currentPosition}

def createExperience(amount,data,profile):
    experience=ET.SubElement(profile, "experience"+amount)
    ET.SubElement(experience, "Afbeelding").text = str(data["logo_url"])
    ET.SubElement(experience, "Functie").text = str(data["title"])
    ET.SubElement(experience, "Bedrijf").text = str(data["company"])
    ET.SubElement(experience, "Locatie").text = str(data["location"])
    ET.SubElement(experience, "VanMaand").text = str(convertMonthNumber(data["starts_at"]["month"]))
    ET.SubElement(experience, "VanJaar").text = str(data["starts_at"]["year"])
    if data["ends_at"] == None:
        print('until present')
        # ET.SubElement(experience, "TotMaand").text = "Present"
        # ET.SubElement(experience, "TotJaar").text = ""
    else:
        ET.SubElement(experience, "TotMaand").text = str(convertMonthNumber(data["ends_at"]["month"]))
        ET.SubElement(experience, "TotJaar").text = str(data["ends_at"]["year"])
    ET.SubElement(experience, "Beschrijvingsveld").text = str(data["description"])

def createAllExperiences(data,profile):
    experience=ET.SubElement(profile, "experiences")
    for x in range(0,len(data["experiences"])):
        
        createExperience(amount=str(x),data=data["experiences"][x],profile=experience)


def createEducation(amount,profile,data):
    opleiding=ET.SubElement(profile, "opleiding"+str(amount))
    
    ET.SubElement(opleiding, "Afbeelding").text = str(data["education"][amount]["logo_url"])
    ET.SubElement(opleiding, "Vanmaand").text = str(convertMonthNumber(data["education"][amount]["starts_at"]["month"]))
    ET.SubElement(opleiding, "VanJaar").text = str(data["education"][amount]["starts_at"]["year"])
    ET.SubElement(opleiding, "Totmaand").text = str(convertMonthNumber(data["education"][amount]["ends_at"]["month"]))
    ET.SubElement(opleiding, "TotJaar").text = str(data["education"][amount]["ends_at"]["year"])
    ET.SubElement(opleiding, "School").text = str(data["education"][amount]["school"])
    ET.SubElement(opleiding, "Afstudeerrichting").text = str(data["education"][amount]["field_of_study"])
    ET.SubElement(opleiding, "BehaaldNiveau").text = str(data["education"][amount]["degree_name"])
def createAllEducations(profile,data):
    opleidingen=ET.SubElement(profile, "opleidingen")
    for x in range(0,len(data["education"])):

        createEducation(amount=x,profile=opleidingen,data=data)


def createProfile(data,root,linkedInUrl):
        experienceAnalyzer=ExperienceAnalyzer(data["experiences"])
        profile = ET.SubElement(root, "profile"+data["first_name"]+data["last_name"])
        AlgemeneInformatie = ET.SubElement(profile, "AlgemeneInformatie")
        Opleiding=ET.SubElement(profile, "Opleiding")
        ET.SubElement(AlgemeneInformatie, "voornaam").text = str(data["first_name"])
        ET.SubElement(AlgemeneInformatie, "naam").text = str(data["last_name"])
        ET.SubElement(AlgemeneInformatie, "email").text = str(data["first_name"])+"."+str(data["last_name"])+"@aperta.be"
        ET.SubElement(AlgemeneInformatie, "straatPlusNummer").text = "test straat"
        ET.SubElement(AlgemeneInformatie, "postcode").text = "test postcode "
        ET.SubElement(AlgemeneInformatie, "stad").text = str(data["city"])
        ET.SubElement(AlgemeneInformatie, "land").text = str(data["country_full_name"])
        # ET.SubElement(AlgemeneInformatie, "land").text = str("+32489000000")  
        # ET.SubElement(AlgemeneInformatie, "Nationaliteit").text = str("nationaliteit not provided")
        # manueel moet gebeuren
        # ET.SubElement(AlgemeneInformatie, "Geboortedag").text = str("not provided")
        # ET.SubElement(AlgemeneInformatie, "Rijbewijs").text = str("not provided")
        ET.SubElement(AlgemeneInformatie, "Huidigefunctie").text = experienceAnalyzer["currentPosition"]
        ET.SubElement(AlgemeneInformatie, "LinkedinUrl").text = linkedInUrl
        createAllExperiences(data=data,profile=profile)
        createAllEducations(profile=Opleiding,data=data)


def createAllProfiles(root):
    if testMode == True:
        linkedInUrls=["https://gr.linkedin.com/in/george-papadas-418480190"]
    else:
        linkedInUrls=["https://www.linkedin.com/in/lucclaeys/","www.linkedin.com/in/panagiotis-m-ab5b6a2a","https://www.linkedin.com/in/thiels/","https://www.linkedin.com/in/gkyriazopoulos/","https://www.linkedin.com/in/david-bash-0286b357/","https://www.linkedin.com/in/kostas-kourakis-91b7891a1/","https://www.linkedin.com/in/efthymis-charalampidis-62013350/","https://www.linkedin.com/in/efthymis-charalampidis-62013350/","https://www.linkedin.com/in/nickolasstefanis/","https://www.linkedin.com/in/georgia-afioni-80028851/","https://gr.linkedin.com/in/george-papadas-418480190"]

    err=False
    dataArr=getDataArray(linkedInUrls)
    #for x in range (0,len(dataArr)):

    print( 'the length og data ar'+str(len(dataArr))+ 'the length of linked in URL'+str(len(linkedInUrls)))
    if len(dataArr) == len(linkedInUrls):
        for x in range (0,len(dataArr)):
            try:
                createProfile(data=JS.loads(dataArr[x].content),root=root,linkedInUrl=linkedInUrls[x])
            except Exception as e: 
                print("creating profile failed")
                
                print(JS.loads(dataArr[x].content))
                
                if JS.loads(dataArr[x].content)["code"]==403:
                    print('Not enough credits, please top up')
                    err=True
                    
    else:
        print('error: failed to create profiles create a bug report!')
        err=True
    return {"error":err}
def getData(url):

    api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
    linkedin_profile_url = url
    api_key = '842lZG9wHIPTNB3aIqFK3g'
    header_dic = {'Authorization': 'Bearer ' + api_key}

    response = requests.get(api_endpoint,
                        params={'url': linkedin_profile_url},
                        headers=header_dic)
    return response
def getDataArray(LinkedInUrls):
    dataArr=[]
    print("get the array of data")

    for x in range(0,len(LinkedInUrls)):
   
        try:
            dataArr.append(getData(url=LinkedInUrls[x]))
        except:
            print('adding profile with url: '+LinkedInUrls[x]+' failed')
    return dataArr
    






# Opening JSON file in read mode

#with open("dummy.json", "r") as json_file:
   
    # loading json file data 
    # to variable data
    #data = JS.load(json_file)
# data = JS.loads(getData("https://www.linkedin.com/in/lucclaeys/").content)
# print(data)
def main():
    root = ET.Element("profilesList")

    response= createAllProfiles(root)
    if response["error"] == False:
        tree = ET.ElementTree(root)
    
        # Writing the xml to output file
        tree.write("profileList.xml")
    else:
        print('not updating because of error. Problem needs to be reported')
main()