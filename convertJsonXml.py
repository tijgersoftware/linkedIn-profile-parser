# Program to read JSON file 
# and generate its XML file
   
# Importing json module and xml
# module provided by python
import json as JS
from this import d
import xml.etree.ElementTree as ET
import requests
import calendar
import sys
import XmlConfig
testMode=True
dummyData= True
#
# test george papadas
#
def convertMonthNumber(numberMonth):
    return calendar.month_name[numberMonth]
    

def ExperienceAnalyzer(jsonArray):
    currentPosition=""
    currentPositionIndex=0
    for x in range(0,len(jsonArray)):
        if jsonArray[x]["ends_at"] == None:

            #print("The present experience found")
           
            if (currentPositionIndex>0):
                currentPositionIndex+=1

                currentPosition=currentPosition+", "+jsonArray[x]["title"].replace(".", "")
            else:
                currentPositionIndex+=1
                currentPosition=currentPosition+jsonArray[x]["title"].replace(".", "")
            #print("The current is "+currentPosition)
    return {"currentPosition":currentPosition}

def createExperience(amount,data,profile):
    experience=ET.SubElement(profile, "experience")
    ET.SubElement(experience, "Afbeelding").text = str(data["logo_url"])
    ET.SubElement(experience, "Functie").text = str(data["title"])
    ET.SubElement(experience, "Bedrijf").text = str(data["company"])
    ET.SubElement(experience, "Locatie").text = str(data["location"])
    ET.SubElement(experience, "VanMaand").text = str(convertMonthNumber(data["starts_at"]["month"]))
    ET.SubElement(experience, "VanJaar").text = str(data["starts_at"]["year"])

    if data["ends_at"] == None:
        #print('until present')
        ET.SubElement(experience, "TotMaand").text = "Present"
        ET.SubElement(experience, "TotJaar").text = ""
    else:
        ET.SubElement(experience, "TotMaand").text = str(convertMonthNumber(data["ends_at"]["month"]))
        ET.SubElement(experience, "TotJaar").text = str(data["ends_at"]["year"])
    ET.SubElement(experience, "Beschrijvingsveld").text = str(data["description"])

def createAllExperiences(data,profile):
    experience=ET.SubElement(profile, "experiences")
    for x in range(0,len(data["experiences"])):
        
        createExperience(amount=str(x),data=data["experiences"][x],profile=experience)


def createEducation(amount,profile,data):
    opleiding=ET.SubElement(profile, "opleiding")
    try:
        ET.SubElement(opleiding, "Afbeelding").text = str(data["education"][amount]["logo_url"])
    except:
        print("couldn't find a logo from school")
    try:
        ET.SubElement(opleiding, "Vanmaand").text = str(convertMonthNumber(data["education"][amount]["starts_at"]["month"]))
    except: 
        print("couldn't find the month where the course started")
    try: 
        ET.SubElement(opleiding, "VanJaar").text = str(data["education"][amount]["starts_at"]["year"])
    except:
        print("couldn't find the year where the course started")
    try: 
        ET.SubElement(opleiding, "Totmaand").text = str(convertMonthNumber(data["education"][amount]["ends_at"]["month"]))
    except: 
        print("couldn't find the month where the course ended")
    try:
        ET.SubElement(opleiding, "TotJaar").text = str(data["education"][amount]["ends_at"]["year"])
    except: 
        print("couldn't find the year where the course ended")
    try:
        ET.SubElement(opleiding, "School").text = str(data["education"][amount]["school"])
    except: 
        print("couldn't find the name of the school")
    try: 
        ET.SubElement(opleiding, "Afstudeerrichting").text = str(data["education"][amount]["field_of_study"])
    except: 
        print("couldn't find the name of the course")
    # ET.SubElement(opleiding, "BehaaldNiveau").text = str(data["education"][amount]["degree_name"])
def createAllEducations(profile,data):
   
    for x in range(0,len(data["education"])):

        createEducation(amount=x,profile=profile,data=data)


def createProfile(data,root,linkedInUrl):
        try:
            experienceAnalyzer=ExperienceAnalyzer(data["experiences"])
        except:
            print("failed to analyze the experiences")
        profile = ET.SubElement(root, "profile")
        AlgemeneInformatie = ET.SubElement(profile, "AlgemeneInformatie")
        Opleiding=ET.SubElement(profile, "educations")
        try:
            ET.SubElement(AlgemeneInformatie, "voornaam").text = str(data["first_name"])
        except:
            print('failed to find first name for: '+ linkedInUrl)
        try:
            ET.SubElement(AlgemeneInformatie, "naam").text = str(data["last_name"])
        except: 
            print('failed to find the last name for: '+ linkedInUrl)
        try:
            ET.SubElement(AlgemeneInformatie, "email").text = str(data["first_name"])+"."+str(data["last_name"])+"@aperta.be"
        except:
            print('failed to construct the email for: '+ linkedInUrl)
        # ET.SubElement(AlgemeneInformatie, "straatPlusNummer").text = "test straat"
        # ET.SubElement(AlgemeneInformatie, "postcode").text = "test postcode "
        try:
            ET.SubElement(AlgemeneInformatie, "stad").text = str(data["city"])
        except: 
            print('failed to find the city name for: '+ linkedInUrl)
        try:
            ET.SubElement(AlgemeneInformatie, "land").text = str(data["country_full_name"])
        except:
            print('failed to find the country full name for: '+ linkedInUrl)
        # ET.SubElement(AlgemeneInformatie, "land").text = str("+32489000000")  
        # ET.SubElement(AlgemeneInformatie, "Nationaliteit").text = str("nationaliteit not provided")
        # manueel moet gebeuren
        # ET.SubElement(AlgemeneInformatie, "Geboortedag").text = str("not provided")
        # ET.SubElement(AlgemeneInformatie, "Rijbewijs").text = str("not provided")
        try:
            ET.SubElement(AlgemeneInformatie, "Huidigefunctie").text = experienceAnalyzer["currentPosition"]
        except:
            print('failed to find the current position for: '+ linkedInUrl)
        try:
            ET.SubElement(AlgemeneInformatie, "LinkedinUrl").text = linkedInUrl
        except:
            print('failed to find the linkedInUrl for: '+ linkedInUrl)
        try:
            ET.SubElement(AlgemeneInformatie, "profile_pic_url").text = data["profile_pic_url"]
        except: 
            print('failed to find the profile picture for: '+ linkedInUrl)
        
        #profile_pic_url
        try:
            createAllExperiences(data=data,profile=profile)
        except:
            print('failed to create the experiences for: '+ linkedInUrl)
        try: 
            createAllEducations(profile=Opleiding,data=data)
        except: 
            print('failed to create the education listings for: '+ linkedInUrl)


def createAllProfiles(root,linkedInUrls):
    if testMode == True:
        
        if dummyData == True:
            print('using dummy data')
            with open("dummy.json", "r") as json_file:
                dataArr = JS.load(json_file)
                
   
        

        else:
            dataArr=getDataArray(linkedInUrls)
    else:
        #linkedInUrls=["https://www.linkedin.com/in/lucclaeys/","www.linkedin.com/in/panagiotis-m-ab5b6a2a","https://www.linkedin.com/in/thiels/","https://www.linkedin.com/in/gkyriazopoulos/","https://www.linkedin.com/in/david-bash-0286b357/","https://www.linkedin.com/in/kostas-kourakis-91b7891a1/","https://www.linkedin.com/in/efthymis-charalampidis-62013350/","https://www.linkedin.com/in/efthymis-charalampidis-62013350/","https://www.linkedin.com/in/nickolasstefanis/","https://www.linkedin.com/in/georgia-afioni-80028851/","https://gr.linkedin.com/in/george-papadas-418480190"]
        dataArr=getDataArray(linkedInUrls)

    err=False
    
    #for x in range (0,len(dataArr)):

    print( 'the length og data ar'+str(len(dataArr))+ 'the length of linked in URL'+str(len(linkedInUrls)))
    if len(dataArr) == len(linkedInUrls):
        print('checking if the code fetched all required profiles')
        for x in range (0,len(dataArr)):
            try:
                if dummyData == True:
                    #print('loading json')

                    data = dataArr[x]
           
                else:
                    data=JS.loads(dataArr[x])
                
                
                createProfile(data=data,root=root,linkedInUrl=linkedInUrls[x])
            except Exception as e: 
                print("creating profile failed"+linkedInUrls[x])
    
                try:
                    if JS.loads(dataArr[x])["code"]==403:
                        print('Not enough credits, please top up')
                        err=True
                except:
                    print('error: failed to create profiles create a bug report!')
                    err=True

                    
    else:
        print('error: failed to create profiles create a bug report!')
        err=True
    return {"error":err, "dataArr":dataArr}
def getData(url):

    api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
    linkedin_profile_url = url
    api_key = 'ULjbgf6nk9wQPap-1bj0_A'
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
            dataArr.append(getData(url=LinkedInUrls[x]).content)
            print('fetching url')
            print(LinkedInUrls[x])
        except:
            print('adding profile with url: '+LinkedInUrls[x]+' failed')
    return dataArr
    

def createDummyData(linkedInUrls,file):
    dataArrBytes= getDataArray(linkedInUrls)
    #dataArrJson= dataArrJson
    #dataArrBytes= [b'{"public_identifier": "panagiotis-m-ab5b6a2a", "profile_pic_url": null, "background_cover_image_url": null, "first_name": "Panagiotis", "last_name": "M.", "full_name": "Panagiotis M.", "occupation": "Drupal Developer at E-Sepia Web Innovation", "headline": "Drupal Developer at E-Sepia Web Innovation", "summary": null, "country": "GR", "country_full_name": "Greece", "city": null, "state": null, "experiences": [{"starts_at": {"day": 1, "month": 11, "year": 2014}, "ends_at": null, "company": "E-Sepia Web Innovation", "company_linkedin_profile_url": "https://www.linkedin.com/company/e-sepia/", "title": "Drupal Developer", "description": null, "location": "Athens, Greece", "logo_url": "https://media-exp1.licdn.com/dms/image/C560BAQHvShKRtLln3A/company-logo_400_400/0/1537741745962?e=1671667200&v=beta&t=sYCxWSrwt15K6JNVk07koiMTg9-NF6l_FDxaVk0GMzQ"}, {"starts_at": {"day": 1, "month": 2, "year": 2013}, "ends_at": {"day": 30, "month": 6, "year": 2014}, "company": "Netstudio", "company_linkedin_profile_url": "https://www.linkedin.com/company/netstudio/", "title": "Drupal Developer", "description": null, "location": "Athens, Greece", "logo_url": "https://media-exp1.licdn.com/dms/image/C4E0BAQHRwU1pvej0cA/company-logo_400_400/0/1519892770508?e=1671667200&v=beta&t=FZ8BYxKrj8CnsQKuwnar56LyYBbotMPASwsBuv-BBJI"}, {"starts_at": {"day": 1, "month": 5, "year": 2010}, "ends_at": {"day": 28, "month": 2, "year": 2013}, "company": "Avalon Web and Media", "company_linkedin_profile_url": null, "title": "Drupal Developer", "description": null, "location": "Athens, Greece", "logo_url": null}], "education": [{"starts_at": {"day": 1, "month": 1, "year": 2004}, "ends_at": {"day": 31, "month": 12, "year": 2009}, "field_of_study": "Computer Science", "degree_name": "University Degree", "school": "Technologiko Ekpaideutiko Idrima, Athinas", "school_linkedin_profile_url": null, "description": null, "logo_url": "https://media-exp1.licdn.com/dms/image/C4E0BAQG407FrmmS-rA/company-logo_400_400/0/1519866782423?e=1671667200&v=beta&t=aMlqsxu7KE-Gr_rAwDHrwqfdkV5ikZ2P_BLLNLbM644"}], "languages": ["English", "French", "Greek"], "accomplishment_organisations": [], "accomplishment_publications": [], "accomplishment_honors_awards": [], "accomplishment_patents": [], "accomplishment_courses": [], "accomplishment_projects": [], "accomplishment_test_scores": [], "volunteer_work": [], "certifications": [], "connections": null, "people_also_viewed": [], "recommendations": [], "activities": [], "similarly_named_profiles": [], "articles": [], "groups": []}']
    dataArrJson=[]
    for x in range(0, len(dataArrBytes)):
        dataJson=JS.loads(dataArrBytes[x].decode('utf-8'))
        dataArrJson.append(dataJson)
    
    print('the data returned is')
    print(dataArrJson)
    
    
    with open(file, "w") as outfile:
        JS.dump(dataArrJson, outfile)






# Opening JSON file in read mode

#with open("dummy.json", "r") as json_file:
   
    # loading json file data 
    # to variable data
    #data = JS.load(json_file)
# data = JS.loads(getData("https://www.linkedin.com/in/lucclaeys/").content)
# print(data)
def serveProfileDataXml(linkedInUrls):
    root = ET.Element("profilesList")
    allProfiles=ET.SubElement(root, "ProfilesAperta")
    response= createAllProfiles(root=allProfiles,linkedInUrls=linkedInUrls)
    if response["error"] == False:
        tree = ET.ElementTree(root)
        #
        # TODO parse the data to the api use the dummy data for this
        #
        # Writing the xml to output file
        tree.write("profileList.xml")
        
        #root = tree.getroot()
        xmldict = XmlConfig.XmlDictConfig(root)

        return  xmldict


    else:
        print('not updating because of error. Problem needs to be reported')


# createDummyData(file = "dummy.json",
# # # linkedInUrls=["www.linkedin.com/in/panagiotis-m-ab5b6a2a"]

# linkedInUrls=["www.linkedin.com/in/panagiotis-m-ab5b6a2a","https://www.linkedin.com/in/thiels/","https://www.linkedin.com/in/gkyriazopoulos/","https://www.linkedin.com/in/david-bash-0286b357/","https://www.linkedin.com/in/kostas-kourakis-91b7891a1/","https://www.linkedin.com/in/efthymis-charalampidis-62013350/","https://www.linkedin.com/in/efthymis-charalampidis-62013350/","https://www.linkedin.com/in/nickolasstefanis/","https://www.linkedin.com/in/georgia-afioni-80028851/","https://gr.linkedin.com/in/george-papadas-418480190"]
# #linkedInUrls=["www.linkedin.com/in/panagiotis-m-ab5b6a2a","https://www.linkedin.com/in/thiels/"]

# )


def main():
    linkedInUrls= linkedInUrls=["www.linkedin.com/in/panagiotis-m-ab5b6a2a","https://www.linkedin.com/in/thiels/","https://www.linkedin.com/in/gkyriazopoulos/","https://www.linkedin.com/in/david-bash-0286b357/","https://www.linkedin.com/in/kostas-kourakis-91b7891a1/","https://www.linkedin.com/in/efthymis-charalampidis-62013350/","https://www.linkedin.com/in/efthymis-charalampidis-62013350/","https://www.linkedin.com/in/nickolasstefanis/","https://www.linkedin.com/in/georgia-afioni-80028851/","https://gr.linkedin.com/in/george-papadas-418480190"]
    return serveProfileDataXml(linkedInUrls)
main()

# ngrok http 5000