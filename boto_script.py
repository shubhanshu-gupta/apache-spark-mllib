import boto3

s3 = boto3.client('s3')
list_of_objects = s3.list_objects(Bucket='lgwarehouse')


# def folders(client, bucket, prefix=''):
#     paginator = client.get_paginator('list_objects')
#     for result in paginator.paginate(Bucket=bucket, Prefix=prefix, Delimiter='/'):
#         for prefix in result.get('CommonPrefixes', []):
#             yield prefix.get('Prefix')

# def folders(client, bucket, prefix=''):
# 	list_of_objects = client.list_objects(Bucket=bucket, Prefix=prefix, Delimiter='/')
# 	for result in list_of_objects.get('CommonPrefixes', []):
# 		return result.get('Prefix')


gen_folders = folders(s3, 'lgwarehouse')
list(gen_folders) ###[u'app/', u'demos/', u'logs/', u'media-dev/', u'media/', u'pds/', u'site-assets/', u'static/']

gen_subfolders = folders(s3, 'lgwarehouse', prefix='media/resources/')
list(gen_subfolders)
###[u'media/resources/click_to_learn/', u'media/resources/gif/',
###u'media/resources/memes/', u'media/resources/slide/', u'media/resources/solved_example/',
###u'media/resources/super/', u'media/resources/vanilla/', u'media/resources/vanilla_image/',
###u'media/resources/video/']

#Now, the following piece of code will list all the content folders within click to learn
gen_subfolders = folders(s3, 'lgwarehouse', prefix='media/resources/click_to_learn/')
list(gen_subfolders)

##And now, since we want to see all the files within click to learn:
results = s3.list_objects(Bucket='lgwarehouse', Prefix='media/resources/click_to_learn/[folder_no]',
						 Delimiter='/')
prefixes = []
for result in results.get('CommonPrefixes'):
	prefixes.append(result.get('Prefix'))

for content in list(gen_subfolders):
	result = s3.list_objects(Bucket='lgwarehouse', Prefix=content, Delimiter='/')

------------

results = s3.list_objects(Bucket='lgwarehouse', Prefix='media/resources/click_to_learn/', Delimiter='/')

for result in results.get('CommonPrefixes'):
	p = result.get('Prefix')
	p = str(p)
	result_contents = s3.list_objects(Bucket='lgwarehouse', Prefix=p, Delimiter='/')
	length = len(result_contents['Contents'])
	for i in range(length):
		print result_contents['Contents'][i]['Key']