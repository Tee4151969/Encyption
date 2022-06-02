import cx_Oracle
import json
import requests
import datetime

def isCompanyTrue(Text):
    inFind = str(Text[0:3]).lower()
    list = ["tuc","tic","tvg","tru"]
    return inFind in list

def formatValue(Text):
    sFormatText = ("'{}'")
    if Text is not None or not bool(Text and Text.strip()):
        return sFormatText.format(Text)
    else:
        return "null"

rows = []
inURL = ""
xQuery = ""
headers = {'Content-Type': 'application/json',
           'APIKey': 'b73355f36b26d872c166b3a4bf0903c6'}
sFormatSQL = ("select {} as IDENTIFIER "
                        + ",{} as LAST_UPDATE_DATE "
                        + ",{} as PURPOSE_ID "
                        + ",{} as PURPOSE_NAME "
                        + ",{} as PURPOSE_VERSION "
                        + ",{} as PURPOSE_STATUS "
                        + ",{} as FIRST_TRANSACTION_DATE "
                        + ",{} as LAST_TRANSACTION_DATE "
                        + ",{} as CONSENT_DATE "
                        + ",{} as TOTAL_TRANSACTION_COUNT "
                        + ",{} as LAST_COLLECTION_POINT_ID "
                        + ",{} as  LAST_COLLECTION_POINT_VERSION "
                        + " from dual")
respCheck = requests.get('https://uat-de.onetrust.com/api/consentmanager/v1/datasubjects/profiles?page=1&size=50', headers=headers);
if respCheck.status_code == 200:
    json_query_check = json.loads(respCheck.content.decode('utf-8'))
    if json_query_check is not None:
       itotalelement = (json_query_check["totalElements"])
       itotalpage = (json_query_check["totalPages"])
       ipage = (json_query_check["number"])
       isize = (json_query_check["size"])   

for xPage in range(9200,itotalpage):
    inURL=('https://uat-de.onetrust.com/api/consentmanager/v1/datasubjects/profiles?size=50&page=' + str(xPage))
    resp = requests.get(inURL, headers=headers);
    if resp.status_code == 200:
        print(inURL)
        json_query = json.loads(resp.content.decode('utf-8'))
        if json_query is not None:
           ipage_current = (json_query["number"])
           isize_current = (json_query["size"])
           objcontent = json_query["content"]
           if objcontent is not None:
               for iitem in objcontent:
                   masterid=(iitem["Id"])
                   masteridentifier=(iitem["Identifier"])
                   masterlang=(iitem["Language"])
                   mlastdate=str(iitem["LastUpdatedDate"])[0:19]
                   masterlastdate=datetime.datetime.strptime(mlastdate, '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
                   objpurposes = iitem["Purposes"]
                   if objpurposes is not None:
                       for ipurposes in objpurposes:
                           detailid=(ipurposes["Id"])
                           detailname=(ipurposes["Name"])
                           detailversion=(ipurposes["Version"])
                           detailstatus=(ipurposes["Status"])
                           dfirst = str(ipurposes["FirstTransactionDate"])[0:19]
                           detailfirst = datetime.datetime.strptime(dfirst, '%Y-%m-%dT%H:%M:%S').strftime(
                               '%Y-%m-%d %H:%M:%S')
                           dlast = str(ipurposes["LastTransactionDate"])[0:19]
                           detaillast = datetime.datetime.strptime(dlast, '%Y-%m-%dT%H:%M:%S').strftime(
                               '%Y-%m-%d %H:%M:%S')
                           detailwithdraw=(ipurposes["WithdrawalDate"])

                           dconsent = str(ipurposes["ConsentDate"])[0:19]
                           detailconsent = None
                           if (dconsent != "None"):
                                detailconsent = datetime.datetime.strptime(dconsent, '%Y-%m-%dT%H:%M:%S').strftime(
                               '%Y-%m-%d %H:%M:%S')
                           detailtotal=(ipurposes["TotalTransactionCount"])
                           detailtopic=(ipurposes["Topics"])
                           detailcustom=(ipurposes["CustomPreferences"])
                           detailcollectionid=(ipurposes["LastTransactionCollectionPointId"])
                           detailcollectionversion=(ipurposes["LastTransactionCollectionPointVersion"])
                           if isCompanyTrue(detailname):
                             itemRow = (masteridentifier,masterlastdate,detailid,detailname,detailversion,detailstatus,detailfirst,detaillast,detailconsent,detailtotal,detailcollectionid,detailcollectionversion,ipage_current,isize_current)
                             rows.append(itemRow)
                             print(itemRow)
                       if bool(rows):
                          connection = cx_Oracle.connect("staging", "staging", "tedwdev")
                          cursor = connection.cursor()
                          cursor.executemany("INSERT INTO CNST_CONSENT_PROFILES_B (IDENTIFIER,LAST_UPDATE_DATE,PURPOSE_ID,PURPOSE_NAME,PURPOSE_VERSION,PURPOSE_STATUS,FIRST_TRANSACTION_DATE,LAST_TRANSACTION_DATE,CONSENT_DATE,TOTAL_TRANSACTION_COUNT,LAST_COLLECTION_POINT_ID,LAST_COLLECTION_POINT_VERSION,PAGE_NUMBER,SIZE_PAGE) values (:1,TO_TIMESTAMP(:2, 'YYYY-MM-DD HH24:MI:SS'),:3,:4,:5,:6,TO_TIMESTAMP(:7, 'YYYY-MM-DD HH24:MI:SS'),TO_TIMESTAMP(:8, 'YYYY-MM-DD HH24:MI:SS'),to_date(:9, 'YYYY-MM-DD HH24:MI:SS'),:10,:11,:12,:13,:14)", rows)
                          connection.commit()
else:
    print(resp.status_code)



