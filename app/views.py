from django.shortcuts import redirect, render
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from django.conf import settings
import glob
import io
import os
import zipfile
from io import StringIO 
from django.http import HttpResponse

cols = [
    "country code",
    "postal code",
    "place name",
    "admin name1",
    "admin code1",
    "admin name2",
    "admin code2",
    "admin name3",
    "admin code3",
    "latitude",
    "longitude",
    "accuracy",
] 

import os 


# fs = FileSystemStorage(location='media/')
# def upload_file(request):
#     context = {}
#     if request.method == 'POST':
    
#         file = request.FILES.get("document",False)

#         content = file.read()  
#         file_content = ContentFile(content)
#         file_name = fs.save(
#             "_tmp.csv", file_content
#         )
#         tmp_file = fs.path(file_name)
#         url = lat_long(tmp_file,file_name)
#         context = {
#             'c_url' : url[0],
#             'Inc_url' : url[1],

#         }
        
#     return render(request,'index/uploadcsv.html',context)

#==========================================To Correct the Incorrect Folder=====================================
def Inc_lat_long(file):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.google.com/maps/")

    directory = "Corrected-"+file.replace('/','\\').split('\\')[-1]
    try:os.makedirs(directory)
    except Exception as e:pass
    master_df = pd.DataFrame()
    for filename in os.listdir(file):
        f = os.path.join(file, filename)
        # checking if it is a file
        if os.path.isfile(f):
            data = pd.read_csv(f,names=cols)
            df = pd.DataFrame(data)
            pin = []
            lat = []
            lon = []
            for i, row in df.iterrows():
                pincode = driver.find_element(By.XPATH,"/html/body/div[3]/div[9]/div[3]/div[1]/div[1]/div[1]/div[2]/form/div[2]/div[3]/div/input[1]")
                # try:
                #     pincode.send_keys(row['place name']+ row['admin name1']+row['admin name2']+row['admin name3'])
                # except:
                sleep(2)
                try:
                    try:
                        pincode.send_keys(row['place name']+ row['admin name1']+row['admin name2']+row['admin name3'])
                        submit = driver.find_element(By.XPATH,"/html/body/div[3]/div[9]/div[3]/div[1]/div[1]/div[1]/div[2]/div[1]/button")
                        submit.click()
                
                        sleep(6)
                        direction = driver.find_element(By.XPATH,"/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div[1]/button")
                        direction.click()
                    except:
                        clear = driver.find_element(By.XPATH,"/html/body/div[3]/div[9]/div[3]/div[1]/div[1]/div[1]/div[2]/a")
                        clear.click()
                        pincode.send_keys(row['place name']+ row['admin name1']+row['admin name2'])
                        submit = driver.find_element(By.XPATH,"/html/body/div[3]/div[9]/div[3]/div[1]/div[1]/div[1]/div[2]/div[1]/button")
                        submit.click()
                
                        sleep(6)
                        direction = driver.find_element(By.XPATH,"/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div[1]/button")
                        direction.click()
                except:
                    clear = driver.find_element(By.XPATH,"/html/body/div[3]/div[9]/div[3]/div[1]/div[1]/div[1]/div[2]/a")
                    clear.click()
                    pincode.send_keys(row['place name']+ row['admin name1'])
                    submit = driver.find_element(By.XPATH,"/html/body/div[3]/div[9]/div[3]/div[1]/div[1]/div[1]/div[2]/div[1]/button")
                    submit.click()
            
                    sleep(6)
                    direction = driver.find_element(By.XPATH,"/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div[1]/button")
                    direction.click()


                get_url = driver.current_url
                # print(get_url)
                url = get_url.split('/@')[0].split('+')
                urls = get_url.split('!3d')[1].split('!4d')
                pin.append(url[-1])
                lat.append(urls[0])
                lon.append(urls[1])

                sleep(2)
                home = driver.find_element(By.XPATH,"/html/body/div[3]/div[9]/div[3]/div[1]/div[2]/div/div[2]/div/button")
                home.click()
                clear = driver.find_element(By.XPATH,"/html/body/div[3]/div[9]/div[3]/div[1]/div[1]/div[1]/div[2]/a")
                clear.click()
                
            
            df['postal code'] = pin
            df['latitude'] = lat
            df['longitude'] = lon
            correct_url = directory+"/"+f.split('\\')[-1]
            df.to_csv(correct_url, mode='a', index=False,sep=',',header=0)
            master_df = master_df.append(df)

      
    driver.close()
    print(directory,"=========directory inc to cor===================")
    url = zip_folder(directory)
    # parent_dir = os.path.dirname(os.path.abspath(directory))
    # path = os.path.join(parent_dir+"/"+directory)
    name = "media/"+directory+".csv"
    master_df.to_csv(name, mode='a', index=False,sep=',',header=0)
    return url ,name  
#==================================To upload Incorrect folder============================================
# fs = FileSystemStorage(location='media/')
def Inc_upload_file(request):
    context = {}
    if request.method == 'POST':
    
        file = request.POST.get("document",False)

        # content = file.read()  
        # file_content = ContentFile(content)
        # file_name = fs.save(
        #     "_tmp.csv", file_content
        # )
        # tmp_file = fs.path(file_name)
        # url = Inc_lat_long(tmp_file,file_name)
        url,csvurl = Inc_lat_long(file)
        context = {
            'url' : url,
            'csvurl' : csvurl,
        }
        
    return render(request,'index/Inc_upload.html',context)
#----------------------------------------To Zip the folder------------------------------------------------------
''' Zip files in folder news to testzip.zip  '''
import zipfile
import os


def zip_folder(folder_to_be_zipped):
    name = folder_to_be_zipped.split('\\')[-1]
    with zipfile.ZipFile('media/'+name+'.zip', 'w', zipfile.ZIP_DEFLATED) as newzip:
        for dirpath, dirnames, files in os.walk(folder_to_be_zipped):
            for file in files:
                newzip.write(os.path.join(dirpath, file))
            return newzip.filename
        
#---------------------------------To Find latitude and longitude---------------------------------------------------
def lat_long(file):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)

    # caps = DesiredCapabilities.CHROME
    # # driver = webdriver.Remote(command_executor='http://localhost:4444',desired_capabilities=caps)
    # # host = os.environ['SELENIUM_REMOTE_HOST']
    # driver = webdriver.Remote(command_executor='http://selenium-hub:4444/wd/hub',desired_capabilities=caps,options=options)
    # # driver = webdriver.Chrome(ChromeDriverManager().install())

    driver.get("https://www.google.com/maps/")
    # file = read()
    print(file)
    # file = "D:\Internship\project1\sample-csv1"
    
    directory1 = "corrected-"+file.replace('/','\\').split('\\')[-1]
    try:os.makedirs(directory1)
    except Exception as e:pass
    directory2 = "Incorrected-"+file.replace('/','\\').split('\\')[-1]
    try:os.makedirs(directory2)
    except Exception as e:pass
    Incorrect_df = pd.DataFrame()
    for filename in os.listdir(file):
        f = os.path.join(file, filename)
        # checking if it is a file
        if os.path.isfile(f):
            data = pd.read_csv(f,names=cols)
            df = pd.DataFrame(data)
            df2 = pd.DataFrame()
            
            lat = []
            lon = []
            
            for i,row in df.iterrows():
                pincode = driver.find_element(By.XPATH,"/html/body/div[3]/div[9]/div[3]/div[1]/div[1]/div[1]/div[2]/form/div[2]/div[3]/div/input[1]")
                pincode.send_keys(row['postal code'])
                sleep(3)
                submit = driver.find_element(By.XPATH,"/html/body/div[3]/div[9]/div[3]/div[1]/div[1]/div[1]/div[2]/div[1]/button")
                submit.click()
                
                try:
                    sleep(6)
                    direction = driver.find_element(By.XPATH,"/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div[1]/button")
                    direction.click()

                    get_url = driver.current_url
                    url = get_url.split('!3d')[1].split('!4d')
                    lat.append(url[0])
                    lon.append(url[1])

                    sleep(3)
                    home = driver.find_element(By.XPATH,"/html/body/div[3]/div[9]/div[3]/div[1]/div[2]/div/div[2]/div/button")
                    home.click()
                    clear = driver.find_element(By.XPATH,"/html/body/div[3]/div[9]/div[3]/div[1]/div[1]/div[1]/div[2]/a")
                    clear.click()
                except:
                    clear = driver.find_element(By.XPATH,"/html/body/div[3]/div[9]/div[3]/div[1]/div[1]/div[1]/div[2]/a")
                    clear.click()
                    
                    df2 = df2.append(df.iloc[i], ignore_index=True)
                    df.drop(i, axis=0, inplace=True)
                    
                        
                
            
            df['latitude'] = lat
            df['longitude'] = lon
            url1 = directory1+"/"+f.split('\\')[-1]
            url2 = directory2+"/"+f.split('\\')[-1]
            df.to_csv(url1, mode='a',header=0, index=False,sep=',')
            if not df2.empty:
                df2.to_csv(url2, mode='a',header=0, index=False,sep=',')
                Incorrect_df = Incorrect_df.append(df2)
            else:
                pass  
            

    driver.close()
    print(directory1)
    url = zip_folder(directory1)
    parent_dir = os.path.dirname(os.path.abspath(directory2))
    path = os.path.join(parent_dir+"/"+directory2)
    print(url,"zip url====================================")
    name = "media/"+directory2+".csv"
    Incorrect_df.to_csv(name, mode='a',header=0, index=False,sep=',')
    return url,path,name
    
#-------------------------------To Split the csv file ----------------------------------------------------------------

class FileSplitter(object):
    def __init__(self,tmp_file, row_size=100):
        self.tmp_file = tmp_file
        self.row_size = row_size
        self.df = pd.read_csv(self.tmp_file,
                              chunksize=self.row_size,header=0)
    def run(self):
        directory = str(self.tmp_file).split(".")[0]
        print(directory)
        parent_dir = os.path.dirname(os.path.abspath(directory))
        path = os.path.join(parent_dir+"/media/"+directory)
        try:os.makedirs(path)
        except Exception as e:pass
        counter = 0
        while True:
            try:
                file_name = "media/{}/{}_{}.csv".format(
                    directory,  str(self.tmp_file).split(".")[0], counter
                )
                df = next(self.df).to_csv(file_name,header=0,index = False,sep = ',')
                counter = counter + 1
            except StopIteration:
                break
            except Exception as e:
                print("Error:",e)
                break
        
        url = '/media/'+ directory
        print(url)
        return path

#-------------------------------To upload the csv file----------------------------------------------------
import wget
# fs = FileSystemStorage(location='media/new/')
def file(request):
    context = {}
    if request.method == 'POST':
    
        file = request.FILES.get("document",False)
        helder = FileSplitter(file,row_size=5)
        dir = helder.run()
        print(dir,"11111111111111111111111111111111111111111")
        url,path,csvurl = lat_long(dir)
        context = {
            'url' : url,
            'path' : path,
            'csvurl' : csvurl,
        }
    return render(request,'index/seperate.html',context)
#---------------------------------------------------------------------------------------------------------


