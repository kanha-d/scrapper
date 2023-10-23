

import requests

template = "https://mycareer.hsbc.com/en_GB/external/SearchJobs/?1017=%5B67213%5D&1017_format=812&listFilterMode=1&pipelineOffset={}"
weburl = template.format(5)
print(weburl)
response = requests.get(weburl)

