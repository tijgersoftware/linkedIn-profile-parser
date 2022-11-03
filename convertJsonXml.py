# Program to read JSON file
# and generate its XML file

# Importing json module and xml
# module provided by python
from distutils.log import error
import json as JS
from this import d
import xml.etree.ElementTree as ET
import requests
import calendar
import sys

import random
from translate import Translator

from xml.etree import cElementTree as ElementTree

class XmlListConfig(list):
    def __init__(self, aList):
        for element in aList:
            if element:
                # treat like dict
                if len(element) == 1 or element[0].tag != element[1].tag:
                    self.append(XmlDictConfig(element))
                # treat like list
                elif element[0].tag == element[1].tag:
                    self.append(XmlListConfig(element))
            elif element.text:
                text = element.text.strip()
                if text:
                    self.append(text)


class XmlDictConfig(dict):
    '''
    Example usage:

    >>> tree = ElementTree.parse('your_file.xml')
    >>> root = tree.getroot()
    >>> xmldict = XmlDictConfig(root)

    Or, if you want to use an XML string:

    >>> root = ElementTree.XML(xml_string)
    >>> xmldict = XmlDictConfig(root)

    And then use xmldict for what it is... a dict.
    '''
    def __init__(self, parent_element):
        if parent_element.items():
            self.update(dict(parent_element.items()))
        for element in parent_element:
            if element:
                # treat like dict - we assume that if the first two tags
                # in a series are different, then they are all different.
                if len(element) == 1 or element[0].tag != element[1].tag:
                    aDict = XmlDictConfig(element)
                # treat like list - we assume that if the first two tags
                # in a series are the same, then the rest are the same.
                else:
                    # here, we put the list in dictionary; the key is the
                    # tag name the list elements all share in common, and
                    # the value is the list itself 
                    aDict = {element[0].tag: XmlListConfig(element)}
                # if the tag has attributes, add those to the dict
                if element.items():
                    aDict.update(dict(element.items()))
                self.update({element.tag: aDict})
            # this assumes that if you've got an attribute in a tag,
            # you won't be having any text. This may or may not be a 
            # good idea -- time will tell. It works for the way we are
            # currently doing XML configuration files...
            elif element.items():
                self.update({element.tag: dict(element.items())})
            # finally, if there are no child tags and no attributes, extract
            # the text
            else:
                self.update({element.tag: element.text})
#
# When dummy data is set to true the testmode should be set to true as well.
# This will fetch the data from dummy.json and will not make a payable api request
#

testMode = False
dummyData = False
devApi = False
#
#  Available languages:
#    https://en.wikipedia.org/wiki/ISO_639-1
#    https://nl.wikipedia.org/wiki/Lijst_van_ISO_639-codes
#    Examples: (e.g. en, ja, ko, pt, zh, zh-TW, ...)
# resource: https://pypi.org/project/translate/

#
languages = ["nl", "el"]

#
# test george papadas
#

#
# returns random valid  api keys with 10 free credits
#
countRequest = 0
countKeys = 0
#
# Get the api key to fetch the linked profiles
#


def devApiKey(amountLinkedInUrls):
    print('get the api key')
    global countKeys
    global countRequest
    if countRequest == 0:
        countKeys = 0
    elif (countRequest % amountLinkedInUrls == 0):
        countKeys += 1

    countRequest += 1

    print("until api key " + str(countKeys) + " is used")
    apiKeys = ["o-8NHyw3FPAG4vz2hIrozQ", "1B2vrvUuQbWbBxn30U7ZBw"]
    print("countKeys" + str(countKeys) + "apiKeys" + str(len(apiKeys)))
    try:
        a = countKeys
        b = len(apiKeys)
        if b > a:
            print("b is greater than a")
            return apiKeys[countKeys]
    except:
        print('failed')
    else:
        return apiKeys[0]


def getApiKey():

        # subscription api key
        # h1. https://nubela.co/proxycurl/
        # USR: admin@dazzle.be
        # PSW: n5aGxtrM*%9NIwTb
        #
    return "aQ795Lo6iylibGFAwYiGeA"
#
# convert a number to the name of a month
#


def convertMonthNumber(numberMonth):
    return calendar.month_name[numberMonth]

#
# loops trough the experiences and returns the current experience
# can be used when other information needs to be fetched from experiences
#


def ExperienceAnalyzer(jsonArray):
    currentPosition = ""
    currentPositionIndex = 0
    for x in range(0, len(jsonArray)):
        if jsonArray[x]["ends_at"] == None:

            #print("The present experience found")

            if (currentPositionIndex > 0):
                currentPositionIndex += 1

                currentPosition = currentPosition+", " + \
                    jsonArray[x]["title"].replace(".", "")
            else:
                currentPositionIndex += 1
                currentPosition = currentPosition + \
                    jsonArray[x]["title"].replace(".", "")
            #print("The current is "+currentPosition)
    return {"currentPosition": currentPosition}

#
#


def createExperience(amount, data, profile, totalExperiences):
    experience = ET.SubElement(profile, "experience")
    #
    # wordpress exception for 1 record of repeater field
    #

    if totalExperiences == 1:
        print('The user has only 1 experience at:'+data["company"])
        experience = ET.SubElement(experience, "item_5")
    ET.SubElement(experience, "Afbeelding").text = NoneSafety(possiblyNone=data["logo_url"], returnIfNotNone=str(
        data["logo_url"]), returnIfNone="https://www.scmdojo.com/wp-content/themes/aapside-child/arxoft/assets/company_placeholder.png")
    ET.SubElement(experience, "Functie").text = str(data["title"])
    ET.SubElement(experience, "Bedrijf").text = str(data["company"])
    ET.SubElement(experience, "Locatie").text = NoneSafety(
        data["location"], str(data["location"]))
    ET.SubElement(experience, "VanMaand").text = str(
        convertMonthNumber(data["starts_at"]["month"]))
    ET.SubElement(experience, "VanJaar").text = str(data["starts_at"]["year"])

    if data["ends_at"] == None:
        #print('until present')
        ET.SubElement(experience, "TotMaand").text = "January"
        ET.SubElement(experience, "TotJaar").text = "heden"
    else:
        ET.SubElement(experience, "TotMaand").text = str(
            convertMonthNumber(data["ends_at"]["month"]))
        ET.SubElement(experience, "TotJaar").text = str(
            data["ends_at"]["year"])
    ET.SubElement(experience, "Beschrijvingsveld").text = NoneSafety(
        possiblyNone=data["description"], returnIfNotNone=str(data["description"]))

#
# NoneSafety so None will not be displayed but another return time when there is no value in the variable
#


def NoneSafety(possiblyNone, returnIfNotNone, returnIfNone=""):
    if possiblyNone == None:
        return returnIfNone
    else:
        return returnIfNotNone

#
# loops over array of experiences
#


def createAllExperiences(data, profile):
    experience = ET.SubElement(profile, "experiences")
    for x in range(0, len(data["experiences"])):

        createExperience(amount=str(
            x), data=data["experiences"][x], profile=experience, totalExperiences=len(data["experiences"]))


def createEducation(amount, profile, data, totalDegrees):
    opleiding = ET.SubElement(profile, "opleiding")
    #
    # wordpress exception for 1 record of repeater field
    #

    if totalDegrees == 1:
        opleiding = ET.SubElement(opleiding, "item_5")
    try:
        ET.SubElement(opleiding, "Afbeelding").text = NoneSafety((data["education"][amount]["logo_url"]), str(
            data["education"][amount]["logo_url"]), "http://studentcorner.co.uk/img/university_placeholder_image.aed66650.png")
    except:
        print("couldn't find a logo from school")
    try:
        ET.SubElement(opleiding, "Vanmaand").text = str(
            convertMonthNumber(data["education"][amount]["starts_at"]["month"]))
    except:
        print("couldn't find the month where the course started")
    try:
        ET.SubElement(opleiding, "VanJaar").text = str(
            data["education"][amount]["starts_at"]["year"])
    except:
        print("couldn't find the year where the course started")
    try:
        ET.SubElement(opleiding, "Totmaand").text = str(
            convertMonthNumber(data["education"][amount]["ends_at"]["month"]))
    except:
        print("couldn't find the month where the course ended")
    try:
        ET.SubElement(opleiding, "TotJaar").text = str(
            data["education"][amount]["ends_at"]["year"])
    except:
        print("couldn't find the year where the course ended")
    try:
        ET.SubElement(opleiding, "School").text = str(
            data["education"][amount]["school"])
    except:
        print("couldn't find the name of the school")
    try:
        ET.SubElement(opleiding, "Afstudeerrichting").text = NoneSafety(possiblyNone=data["education"][amount]["field_of_study"], returnIfNotNone=str(
            data["education"][amount]["field_of_study"]), returnIfNone=NoneSafety(possiblyNone=data["education"][amount]["degree_name"], returnIfNotNone=str(data["education"][amount]["degree_name"]), returnIfNone=""))

    except:
        print("couldn't find the name of the course")
    try:
        ET.SubElement(opleiding, "niveau").text = findLevelEducation(
            data["education"][amount]["degree_name"])
    except:
        print('couldn\'t find the level of education')


def findLevelEducation(degree_name):
    educationLevel = {
        0: "Attest / Certificate",
        1: "Secundair onderwijs",
        2: "Bachelor",
        3: "Master",
        4: "PHD",
    }
    degree_name = degree_name.lower()
    if "certificate" in degree_name or "certification" in degree_name:
        return educationLevel[0]
    elif 'high school' in degree_name:
        return educationLevel[1]
    elif 'bachelor' in degree_name:
        return educationLevel[2]
    elif 'master' in degree_name:
        return educationLevel[3]

    elif 'phd' in degree_name:
        return educationLevel[4]
    elif 'associate' in degree_name:
        return 'bachelor'
    else:
        translator = Translator(to_lang="en")
        translation = translator.translate(degree_name)
        if "certificate" in translation:
            return educationLevel[1]
        elif 'high school' in translation:
            return educationLevel[1]
        elif 'bachelor' in translation:
            return educationLevel[2]
        elif 'master' in translation:
            return educationLevel[3]

        elif 'phd' in translation:
            return educationLevel[4]
        elif 'associate' in translation:
            return 'bachelor'
        else:
            return ""


def createAllEducations(profile, data):

    for x in range(0, len(data["education"])):

        createEducation(amount=x, profile=profile, data=data,
                        totalDegrees=len(data["education"]))


def createProfile(data, root, linkedInUrl):
    try:
        experienceAnalyzer = ExperienceAnalyzer(data["experiences"])
    except:
        print("failed to analyze the experiences")
    profile = ET.SubElement(root, "profile")
    AlgemeneInformatie = ET.SubElement(profile, "AlgemeneInformatie")
    Opleiding = ET.SubElement(profile, "educations")
    try:
        ET.SubElement(AlgemeneInformatie, "voornaam").text = str(
            data["first_name"])
    except:
        print('failed to find first name for: ' + linkedInUrl)
    try:
        ET.SubElement(AlgemeneInformatie, "naam").text = str(data["last_name"])
    except:
        print('failed to find the last name for: ' + linkedInUrl)
    try:
        ET.SubElement(AlgemeneInformatie, "email").text = str(
            data["first_name"])+"."+str(data["last_name"])+"@aperta.be"
    except:
        print('failed to construct the email for: ' + linkedInUrl)
    # ET.SubElement(AlgemeneInformatie, "straatPlusNummer").text = "test straat"
    # ET.SubElement(AlgemeneInformatie, "postcode").text = "test postcode "
    try:
        ET.SubElement(AlgemeneInformatie, "stad").text = NoneSafety(
            data["city"], str(data["city"]))
    except:
        print('failed to find the city name for: ' + linkedInUrl)
    try:
        ET.SubElement(AlgemeneInformatie, "land").text = str(
            data["country_full_name"])
    except:
        print('failed to find the country full name for: ' + linkedInUrl)
    # ET.SubElement(AlgemeneInformatie, "land").text = str("+32489000000")
    # ET.SubElement(AlgemeneInformatie, "Nationaliteit").text = str("nationaliteit not provided")
    # manueel moet gebeuren
    # ET.SubElement(AlgemeneInformatie, "Geboortedag").text = str("not provided")
    # ET.SubElement(AlgemeneInformatie, "Rijbewijs").text = str("not provided")
    try:
        ET.SubElement(AlgemeneInformatie,
                      "Huidigefunctie").text = experienceAnalyzer["currentPosition"]
    except:
        print('failed to find the current position for: ' + linkedInUrl)
    try:
        ET.SubElement(AlgemeneInformatie, "summary").text = NoneSafety(
            data["summary"], str(data["summary"]))
    except:
        print("couldn't fetch the about me")

    try:
        ET.SubElement(AlgemeneInformatie, "LinkedinUrl").text = linkedInUrl
    except:
        print('failed to find the linkedInUrl for: ' + linkedInUrl)
    try:
        ET.SubElement(AlgemeneInformatie,
                      "profile_pic_url").text = data["profile_pic_url"]
    except:
        print('failed to find the profile picture for: ' + linkedInUrl)

    try:
        createAllExperiences(data=data, profile=profile)
    except:
        print('failed to create the experiences for: ' + linkedInUrl)
    try:

        createAllEducations(profile=Opleiding, data=data)
    except:
        print('failed to create the education listings for: ' + linkedInUrl)


def createAllProfiles(root, linkedInUrls):
    if testMode == True:

        if dummyData == True:
            print('using dummy data')
            with open("dummyLuc.json", "r") as json_file:
                dataArr = JS.load(json_file)

        else:
            dataArr = getDataArray(linkedInUrls)
    else:
        # linkedInUrls=["https://www.linkedin.com/in/lucclaeys/","www.linkedin.com/in/panagiotis-m-ab5b6a2a","https://www.linkedin.com/in/thiels/","https://www.linkedin.com/in/gkyriazopoulos/","https://www.linkedin.com/in/david-bash-0286b357/","https://www.linkedin.com/in/kostas-kourakis-91b7891a1/","https://www.linkedin.com/in/efthymis-charalampidis-62013350/","https://www.linkedin.com/in/efthymis-charalampidis-62013350/","https://www.linkedin.com/in/nickolasstefanis/","https://www.linkedin.com/in/georgia-afioni-80028851/","https://gr.linkedin.com/in/george-papadas-418480190"]
        dataArr = getDataArray(linkedInUrls)

    err = False

    # for x in range (0,len(dataArr)):

    print('the length og data ar'+str(len(dataArr)) +
          'the length of linked in URL'+str(len(linkedInUrls)))
    if len(dataArr) == len(linkedInUrls):
        print('checking if the code fetched all required profiles')
        for x in range(0, len(dataArr)):
            try:
                if dummyData == True:

                    data = dataArr[x]

                else:
                    data = JS.loads(dataArr[x])

                createProfile(data=data, root=root,
                              linkedInUrl=linkedInUrls[x])
            except Exception as e:
                print("creating profile failed"+linkedInUrls[x])

                try:
                    if JS.loads(dataArr[x])["code"] == 403:
                        print('Not enough credits, please top up')
                        err = True
                except:
                    print('error: failed to create profiles create a bug report!')
                    print(e)
                    err = True

    else:
        print('error: failed to create profiles create a bug report!')
        err = True
    return {"error": err, "dataArr": dataArr}


def getData(url, LinkedInUrlsAmount):
    print('getting the data')
    api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
    linkedin_profile_url = url
    print('get api')
    api_key = "aQ795Lo6iylibGFAwYiGeA"
    print('api ket is ' + api_key)
    header_dic = {'Authorization': 'Bearer ' + api_key}

    response = requests.get(api_endpoint,
                            params={'url': linkedin_profile_url},
                            headers=header_dic)
    print(response)
    return response


def getDataArray(LinkedInUrls):
    dataArr = []
    print(LinkedInUrls)

    for x in range(0, len(LinkedInUrls)):

        try:
            print('try' + str(len(LinkedInUrls)))
            dataArr.append(
                getData(url=LinkedInUrls[x], LinkedInUrlsAmount=len(LinkedInUrls)).content)
            print('fetching url')
            print(LinkedInUrls[x])
        except:
            print('adding profile with url: '+LinkedInUrls[x]+' failed')
    return dataArr


def createDummyData(linkedInUrls, file):
    dataArrBytes = getDataArray(linkedInUrls)
    dataArrJson = []
    for x in range(0, len(dataArrBytes)):
        dataJson = JS.loads(dataArrBytes[x].decode('utf-8'))
        dataArrJson.append(dataJson)

    with open(file, "w") as outfile:
        JS.dump(dataArrJson, outfile)


def serveProfileDataXml(linkedInUrls):
    root = ET.Element("profilesList")
    allProfiles = ET.SubElement(root, "ProfilesAperta")
    response = createAllProfiles(root=allProfiles, linkedInUrls=linkedInUrls)
    if response["error"] == False:
        tree = ET.ElementTree(root)

        tree.write("profileList.xml")

        xmldict = XmlDictConfig(root)

        return xmldict

    else:
        print('not updating because of error. Problem needs to be reported')

#
# use this function to recreate the dummy data in the json file
#

# createDummyData(file = "dummy.json",
# # # linkedInUrls=["www.linkedin.com/in/panagiotis-m-ab5b6a2a"]

# linkedInUrls=["www.linkedin.com/in/panagiotis-m-ab5b6a2a","https://www.linkedin.com/in/thiels/","https://www.linkedin.com/in/gkyriazopoulos/","https://www.linkedin.com/in/david-bash-0286b357/","https://www.linkedin.com/in/kostas-kourakis-91b7891a1/","https://www.linkedin.com/in/efthymis-charalampidis-62013350/","https://www.linkedin.com/in/efthymis-charalampidis-62013350/","https://www.linkedin.com/in/nickolasstefanis/","https://www.linkedin.com/in/georgia-afioni-80028851/","https://gr.linkedin.com/in/george-papadas-418480190"]
# #linkedInUrls=["www.linkedin.com/in/panagiotis-m-ab5b6a2a","https://www.linkedin.com/in/thiels/"]

# )


def main():

    # linkedInUrls = linkedInUrls = [
    #     "www.linkedin.com/in/panagiotis-m-ab5b6a2a", "https://www.linkedin.com/in/gkyriazopoulos/", "https://www.linkedin.com/in/thiels/", "https://www.linkedin.com/in/david-bash-0286b357/", "https://www.linkedin.com/in/kostas-kourakis-91b7891a1/", "https://www.linkedin.com/in/efthymis-charalampidis-62013350/", "https://www.linkedin.com/in/efthymis-charalampidis-62013350/", "https://www.linkedin.com/in/nickolasstefanis/", "https://www.linkedin.com/in/georgia-afioni-80028851/", "https://gr.linkedin.com/in/george-papadas-418480190"]
    # ontbrekend: Aris Magripis, jeff de paepe, Maui Vindevogel, Usama Mazhar, Sotiris Gekas, Didier Boelens, Georgia Afioni, 
    linkedInUrls=["https://www.linkedin.com/in/nickolasstefanis","https://www.linkedin.com/in/efthymis-charalampidis-62013350","https://www.linkedin.com/in/georgia-afioni-80028851","www.linkedin.com/in/panagiotis-m-ab5b6a2a","https://www.linkedin.com/in/kostas-kourakis-91b7891a1","https://www.linkedin.com/in/david-bash-0286b357","https://www.linkedin.com/in/sil-colson/","https://www.linkedin.com/in/lucclaeys/","https://www.linkedin.com/in/thiels/","https://www.linkedin.com/in/gkyriazopoulos/","https://www.linkedin.com/in/dennis-mohammad-b696b5168/","https://gr.linkedin.com/in/george-papadas-418480190","https://www.linkedin.com/in/gilles-hamelink-118700234/"]
    return serveProfileDataXml(linkedInUrls)



