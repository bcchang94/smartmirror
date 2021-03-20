weatherdict = {}

line = "200,f503,f910"
items = line.split(',')
weatherdict[items[0]] = {'day': items[1], 'night': items[2]}

print(weatherdict)
print(weatherdict['200'])
print(weatherdict['200']['day'])