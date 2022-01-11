import requests, json
import re


TYPEFORM_TOKEN = '' # insert your Typeform token

TYPERORM_HEADERS = {
    "Authorization": "Bearer " + TYPEFORM_TOKEN,
}

NOTION_TOKENS = ''# insert your Notion token

NOTION_BLOCK_ID = ''# insert Block ID of the page you want to use to make a survey

NOTION_HEADERS = {
    "Authorization": "Bearer " + NOTION_TOKENS,
    "Content-Type": "application/json",
    "Notion-Version": "2021-08-16"
}


# We use API to get our page in json format
def read_page_block(blockId, headers):
    readUrl = f"https://api.notion.com/v1/blocks/{blockId}/children"

    res = requests.request("GET", readUrl, headers=NOTION_HEADERS)
    data = res.json()
    print(res.status_code)
    return(res.text)

json_data = read_page_block(NOTION_BLOCK_ID, NOTION_HEADERS)



# We are searching for heading 2 and 3 in our json
def find_regex_in_text(certain_regex):
    matches = re.findall(certain_regex, json_data) 
    return matches

regex_heading = """(?<=\"heading_2","heading_2":{"text":\[{"type":"text","text":{"content":").*?(?=","link":null})"""
regex_title = """(?<=\"heading_3","heading_3":{"text":\[{"type":"text","text":{"content":").*?(?=","link":null})"""

matches = find_regex_in_text(regex_heading, json_data)
surveyTitle = str(find_regex_in_text(regex_title, json_data))



# Create questions in the survey on the base of every heading 2 in Notion file
def create_automated_fields(matches):
    newFields = []
    for match in matches:
        our_item = match
        question_1 = dict({
            "title": "What do you think about: " + our_item + "?",
            "properties": {
                "shape": "star",
                "steps": 10
            },
            "validations": {
                "required": False
            },
            "type": "rating"
            },)
        question_2 = dict({
            "title": "What do you think about: " + our_item + "?(please describe)",
            "properties": {},
            "validations": {
                "required": False
            },
            "type": "long_text"
            })
    
        newFields.append(question_1)
        newFields.append(question_2)
    return newFields
newFields = create_automated_fields(matches)



# Create a survey via typeform API with the questions created in the previous step
def create_survey(headers):
    createUrl = 'https://api.typeform.com/forms'
    newFormData = {
      "fields":  newFields,
      "settings": {
        "hide_navigation": False,
        "is_public": False,
        "language": "en",
        },
      "title": surveyTitle,
      "type": "form",
      "workspace": {
        "href": "https://api.typeform.com/workspaces/7kb6qT"
      }
    }

    data1 = json.dumps(newFormData)
    requests.request("POST", createUrl, headers=TYPERORM_HEADERS, data=data1,)

create_survey(TYPERORM_HEADERS)