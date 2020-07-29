{ 
    "attachments":[ 
     { 
     "fallback":"New open task [Urgent]: <http://url_to_task|Test out Slack message attachments>", 
     "pretext":"New open task [Urgent]: <http://url_to_task|Test out Slack message attachments>", 
     "color":"#D00000", 
     "fields":[ 
      { 
       "title":"Notes", 
       "value":"This is much easier than I thought it would be.", 
       "short":false 
      } 
     ] 
     } 
    ] 
} 


import groovy.json.JsonSlurperClassic 

node{ 
    def json = readFile(file:'message2.json') 
    def data = new JsonSlurperClassic().parseText(json) 
    echo "color: ${data.attachments[0].color}" 
} 