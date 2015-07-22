from Tkinter import *
from tkFileDialog import askdirectory
from tkMessageBox import askyesno
import os, fnmatch, shutil, subprocess, psycopg2, glob
from ESM_dictionaries import dict
import tkMessageBox

temp = "C:\\temp\general"

class esm_invest:
    def getpath(self):
        Tk().withdraw()
    
        options = {}
        options['initialdir'] = "B:\DTP DEPARTMENT\_Projects MOCA"
        options['title'] = 'ESM Files Investigation'
    
        fp = askdirectory(**options)
        filePath = fp + "/_Illustration investigation/__ALL"
        return filePath
    
    def new_path(self, filePath):
        p = filePath[:-5]
        np = p + "_NEW"
#        print "new_path(filePath): %s" %np
        return np
    
    def investigate(self, filePath):
        if askyesno("ESM Investigation", "Is this the correct path?\n%s" %filePath):
            print filePath
            esm_invest().generate_file_list(filePath) # generates the file list
            print "=" * 100
            print "Remaining files for investigation: %s" % (esm_invest().all_remaining_files(filePath)[1])
        else:
            pass

    def write_all_txt(self, list, path):
        fpa = path[:-5]
        alltxt = os.path.join(fpa, "all.txt")
        f = open(alltxt, 'w')
        for item in list:
            f.write("%s\n" %item)
        f.close()
        
        
    def generate_file_list(self, filePath):
        flist = []
        extension = "*.tif"
        for root, dirnames, filenames in os.walk(filePath):
            for filename in fnmatch.filter(filenames, "%s" %extension):
                flist.append(filename)
#        print flist # for testing
        x.write_all_txt(flist, filePath)
        print "Total files in ALL: %s" %len(flist)
        print "="  * 100
        print "ZZ Files: %s" %(x.move_zz(filePath)[1])
        print "JC Files: %s" %(x.move_jc(filePath)[1])
        print "JR Files: %s" %(x.move_jr(filePath)[1])
    
    def move_jr(self, filePath):
        try:
            jr_list = []
            JC_JR_DIR = os.path.join(os.path.dirname(filePath), '__JC_JR')
            global connmsg
            if not x.connectors(filePath):
                connmsg = "No connectors to be translated"
                a = True
            else:
                connmsg = "This project has connectors."
                a = False
            for file in os.listdir(filePath):
                if file.lower().startswith("jr"):
                    jr_list.append(file)
                    src_file = os.path.join(filePath, file)
                    dst_file = os.path.join(JC_JR_DIR, file)
                    if a:
                        shutil.move(src_file, dst_file) # uncoment this line to move the files
            global jr
            jr = len(jr_list)
            return (jr_list, jr, connmsg)
        except:
            print "Please verify to have JR files in ALL folder"

    def move_zz(self, filePath):
        zz_list = []
        ZZ_DIR = os.path.join(os.path.dirname(filePath), '__ZZ')
        for file in os.listdir(filePath):
            if file.lower().endswith("zz.tif"):
                zz_list.append(file)
                src_file = os.path.join(filePath, file)
                dst_file = os.path.join(ZZ_DIR, file)
                shutil.move(src_file, dst_file) # uncoment this line to move the files
        global zz
        zz = len(zz_list)
        return (zz_list, zz)
    
    def move_jc(self, filePath):
        jc_list = []
        JC_JR_DIR = os.path.join(os.path.dirname(filePath), '__JC_JR')
        for file in os.listdir(filePath):
            if file.lower().startswith("jc"):
                jc_list.append(file)
                src_file = os.path.join(filePath, file)
                dst_file = os.path.join(JC_JR_DIR, file)
                shutil.move(src_file, dst_file) # uncoment this line to move the files
        global jc
        jc = len(jc_list)
        return (jc_list, jc)
    
    def all_remaining_files(self, filePath):
        all_files = []
        for file in os.listdir(filePath):
            if not file.endswith(".db"):
                all_files.append(file)
        global all
        all = len(all_files)
        return (all_files, all)
    
    def connectors(self, filePath):
        connectors = dict["connectors"]
        print connectors
        pstring = filePath
        project_name = pstring.split('/')[-3]
        print project_name
        pn = project_name.split(' ')[1]
        print pn
        return (pn in connectors.values())
    
    def result(self):
        if askyesno("ESM Investigation", 
            "Initial investigation is completed. \
            \n\nZZ files: %s \
            \nJC files: %s \
            \nJR files: %s \
            \n\nRemaining files for investigation: %s \
            \n\n%s \
            \n\nDo you want to continue?" %(zz, jc, jr, all, connmsg)):
            global languages
            languages = x.selected_languages()
            
            x.check_in_libraries(path, languages)
        else:
            pass
    
    def selected_languages(self):
        cmd = "python tk_check.py"
        
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        result = out.split('\n')
        strlan = ''.join(result)
        a = strlan.replace("', '", " ")
        a = a.replace(a[-3:],'')
        a = a.replace(a[:2], '')
        a = a.split()
        return a
    
    def sort_new_files(self):
#        print x.new_path(path)
        cmd = "python sort.py %s" %x.new_path(path)
        print cmd
        
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        p.communicate()
        
    
    def check_in_libraries(self, filePath, languages): # for test purpose, check only in Czech lib
        print languages
        for language in languages:
            table = language
            print table # for testing
        
            print "=" * 100
            print "Checking in %s language" %table
            all = x.all_remaining_files(filePath)[0]
            new_files = []
            for file in all:
                if not file.endswith(".db"):
                    filename, ext = os.path.splitext(file)
                    ext = ext.lower()
                    fn = filename + ext
        #            print fn
                    if not esm_invest().search_file(table, fn): # for test purpose
                        new_files.append(file)
                        src_file = os.path.join(filePath, file)
                        dst_file = os.path.join(os.path.dirname(filePath), '_NEW\\___NEW-%s___' %table)
                        try:
                            os.stat(dst_file)
                        except:
                            os.mkdir(dst_file)
                        shutil.copy2(src_file, dst_file)
                        del_thumbs = os.path.join(dst_file, "Thumbs.db")
                        try:
                            os.remove(del_thumbs)
                        except:
                            pass
                        print new_files
        return new_files, len(new_files)

    def search_file(self, table, filename):
        conn = esm_invest().establishConnection('filelist')
        cur = conn.cursor()
        cur.execute("""SELECT exists (SELECT 1 FROM %s WHERE filename ~* '%s' LIMIT 1);""" %(table, filename))
        exists = cur.fetchone()[0]
        print filename, exists
        return exists

    def establishConnection(self, db):
        conn = psycopg2.connect("dbname='%s' user='postgres' host='localhost' password='123456'" %db)
        return conn
    
    def languages(self):
        dictlist = []
        for key, value in dict['languages'].iteritems():
            dictlist.append(value)
        return dictlist

    def move_to_temp(self, path):
        print path # for test purpose
        dirlist = next(os.walk(path))[1]
        for dir in dirlist:
            print dir # for test purpose
            if "___NEW-" in dir:
                dir = os.path.join(path, dir)
                for f in os.listdir(dir):
                    file = os.path.join(dir,f)
                    shutil.copy2(file, temp)
        try:
            os.remove("C:\\temp\general\Thumbs.db")
        except:
            pass
        
                    
    def get_xmp(self, file):
        with open( file, "rb") as fin:
            img = fin.read()
        imgAsString=str(img)
        xmp_start = imgAsString.find('<rdf:li>')
        xmp_end = imgAsString.find('</rdf:li>')
        global xmpString
        if xmp_start != xmp_end:
            xmpString = imgAsString[xmp_start+8:xmp_end]
        return xmpString
    
    def list_labels(self, temp):
        labels_list =[]
        for filename in os.listdir(temp):
            file = os.path.join(temp, filename)
            xmp = x.get_xmp(file)
            
            labels_list.append((filename, xmp))
            print file, xmp
        return labels_list
    
    def move_numbers(self, folder, xmp, file):
        numdir = os.path.join(folder, "%s" %xmp)
        print numdir
        try:
            os.stat(numdir)
        except:
            os.mkdir(numdir)
        df = numdir
        print df
        shutil.move(file, df)
    
    def reorganize(self, path):
        dirlist = next(os.walk(path))[1]
        for dir in dirlist:
            dp = os.path.join(path, dir)
            print dp
            print "\n" + dir
            print "=" * 100
            for file in os.listdir(dp):
                if file.endswith(".TIF"):
                    for fn in x.list_labels(temp):
    #                    print fn
                        if fn[0] == file:
    #                        print fn[0] + " is in the list." + " " + fn[1]
    #                        print dp
                            f = os.path.join(dp, file)
    #                        print f
    #                        print file
                            x.move_numbers(dp, fn[1], f)
        x.delete_general_files() # after reorganising files, detele all files in /temp directory
        
    def delete_general_files(self):
        files = glob.glob("C:\\temp\general\*")
        for f in files:
            os.remove(f)
                        
                        
           
x = esm_invest()

path = x.getpath()
''' Uncomment the following 2 lines to make the application fully functional.'''
x.investigate(path)
x.result()

np = x.new_path(path)
x.move_to_temp(np)

if tkMessageBox.showinfo("Message", "Label the files in general directory and press OK when ready."):
    x.reorganize(np)


print "=" * 100
print "TASK COMPLETED"