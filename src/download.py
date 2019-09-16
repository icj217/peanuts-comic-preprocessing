import urllib.request

files = ["https://www.zipcomic.com/storage/s4/the-complete-peanuts/tpb-1.zip",
"https://www.zipcomic.com/storage/s4/the-complete-peanuts/tpb-2.zip",
"https://www.zipcomic.com/storage/s4/the-complete-peanuts/tpb-3.zip",
"https://www.zipcomic.com/storage/s4/the-complete-peanuts/tpb-4.zip",
"https://www.zipcomic.com/storage/s4/the-complete-peanuts/tpb-5.zip",
"https://www.zipcomic.com/storage/s4/the-complete-peanuts/tpb-6.zip",
"https://www.zipcomic.com/storage/s4/the-complete-peanuts/tpb-7.zip",
"https://www.zipcomic.com/storage/s4/the-complete-peanuts/tpb-8.zip",
"https://www.zipcomic.com/storage/s4/the-complete-peanuts/tpb-9.zip",
"https://www.zipcomic.com/storage/s4/the-complete-peanuts/tpb-10.zip",
"https://www.zipcomic.com/storage/s4/the-complete-peanuts/tpb-11.zip",
"https://www.zipcomic.com/storage/s4/the-complete-peanuts/tpb-12.zip",
"https://www.zipcomic.com/storage/s4/the-complete-peanuts/tpb-13.zip",
"https://www.zipcomic.com/storage/s4/the-complete-peanuts/tpb-14.zip",
"https://www.zipcomic.com/storage/s4/the-complete-peanuts/tpb-15.zip",
"https://www.zipcomic.com/storage/s4/the-complete-peanuts/tpb-16.zip",
"https://www.zipcomic.com/storage/s4/the-complete-peanuts/tpb-17.zip",
"https://www.zipcomic.com/storage/s4/the-complete-peanuts/tpb-18.zip",
"https://www.zipcomic.com/storage/s4/the-complete-peanuts/tpb-19.zip",
"https://www.zipcomic.com/storage/s4/the-complete-peanuts/tpb-20.zip",
"https://www.zipcomic.com/storage/s4/the-complete-peanuts/tpb-21.zip",
"https://www.zipcomic.com/storage/s4/the-complete-peanuts/tpb-22.zip",
"https://www.zipcomic.com/storage/s4/the-complete-peanuts/tpb-23.zip",
"https://www.zipcomic.com/storage/s4/the-complete-peanuts/tpb-24.zip",
"https://www.zipcomic.com/storage/s4/the-complete-peanuts/tpb-25.zip",
"https://www.zipcomic.com/storage/s4/the-complete-peanuts/tpb-26-part-1.zip",
"https://www.zipcomic.com/storage/s4/the-complete-peanuts/tpb-26-part-2.zip",
"https://www.zipcomic.com/storage/s4/the-complete-peanuts/tpb-26-part-3.zip"]

zip_directory = '../downloads/zip/'

for file in files:
    filename = file.split('/')[-1]
    print('Downloading', file, 'to', filename)
    localfile = urllib.request.urlretrieve(file, zip_directory + filename)
    print ('Downloaded', filename, '!')
    
