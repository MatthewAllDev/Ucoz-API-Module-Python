# Examples of requests using the UAPI module. As an example, the interaction with the  module "Site News" is presented.
# author Ilya Matthew Kuvarzin <luceo2011@yandex.ru>
# version 1.1 dated April 15, 2020
# Return_value is dict

import uAPI

request = uAPI.Request('my-site.com', 'https',
                       {
                           'oauth_consumer_key': 'Application id',
                           'oauth_consumer_secret': 'Consumer secret',
                           'oauth_token': 'OAuth token',
                           'oauth_token_secret': 'OAuth token secret'
                       })

return_value = request.get('/news', {})
print(return_value)

return_value = request.post('/news', {'category': 'CATEGORY-ID', 'title': 'Material name',
                                      'message': 'This is a test material. Request succeeded.'})
print(return_value)

return_value = request.put('/news', {'id': 'MATERIAL-ID', 'message': 'Material successfully changed'})
print(return_value)

return_value = request.delete('/news/posts', {'id': 'MATERIAL-ID'})
print(return_value)
