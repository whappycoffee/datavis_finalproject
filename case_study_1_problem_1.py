
###################
# LIBRARY IMPORTS#
###################
import twitter
import json
import os

###################
# CUSTOM FUNCTIONS#
###################



#########################################################################
#TAKES RAW TWITTER DATA AND PRINTS JSON#
##################  START   #######################################################
def pp(invar):
    f= json.dumps(invar, indent=1)
    print(f)
##################   END    ##########################################


#######################################################################
#CONNECT TO TWITTER API####
##################  START   ############################################
def oauth():
    CONSUMER_KEY = 'zkX1ZDln052pgUIllkW7Dwd1s'
    CONSUMER_SECRET ='kLVBs3vAosgAHBEiSb1jDtD4QARH6kKs5CxmvvcGTFfEhnsNF8'
    OAUTH_TOKEN = '906043503720808448-tXaAnPREpAbuWPCgMO7F1IDACp0ONfg'
    OAUTH_TOKEN_SECRET = 'Js5qQUODaQXFrnANeyyjxvQ2j4u4zfW4Vhkh1Mf3y9WZ4'

    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)

    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api
####################  END  ##################################################

#####################################################################
#KEYWORD SEARCH
#q=keyword
#count
##################  START   ############################################
def twitter_search(q, count, twitter_api, **kw):
    
    search_results = twitter_api.search.tweets(q=q, count=count)
    statuses = search_results['statuses']

    for _ in range(10):
        try:
            next_results = search_results['search_metadata']['next_results']
        except KeyError: # No more results when next_results doesn't exist
            break

        kwargs = dict([ kv.split('=') 
            for kv in next_results[1:].split("&") ])
    
        search_results = twitter_api.search.tweets(**kwargs)
        statuses += search_results['statuses']
        print(len(statuses))
    return statuses
###################  END  ##################################################

#####################################################################
#EXPORT JSON FILE
#invar=variable containing data to be converted to json
#filename=file name for the json data to be save to
##################  START   ############################################
def json_export(invar,filename):
    data= json.dumps(invar, indent=1)
    file = open(filename,'w')
    file.write(data)
    file.close()
###################  END  ##################################################

#####################################################################
#AGGREGATE RESULTS FROM ALL TXT FILES IN RAW TWEETS FOLDER
#path=path for the raw tweets
##################  START   ############################################
def agg_results():
    cwd = os.getcwd()
    path=cwd+"\\rawtweets"
    print(path)
    files = os.listdir(path)
    agg_raw_data=[]
    for infile in files:
        print(infile)
        filename=path+"\\"+infile
        print(filename)
        with open(filename) as raw_data:
            raw_data= json.load(raw_data)
        agg_raw_data+=raw_data
        print(str(filename))
        print(str(len(raw_data)))

    return(agg_raw_data)
###################  END  ##################################################


#####################################################################
################        MAIN FUNCTIOn   ############################

def main():
    twitter_api=oauth()
    search=['bitcoin','XRP','etherium','litecoin','namecoin']
    result=[]
    #Modify filename
    filename='Export.txt'
    for i in search:
            result+=twitter_search(i,1000,twitter_api)
    json_export(result,filename)
    results=agg_results()
    json_export(results,"allresults.txt")

main()
