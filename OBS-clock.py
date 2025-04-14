from operator import truediv
from pickle import TRUE
import obspython as obs
import os
import time
import tkinter as tk


## Skriven av Mattias Berggren 2025 mr_XypleX

Tid = "" #när klockan startade används för att räkna ut hur lång tid det gått sedan start.
p_tid = 0 #förluppen tid i perioden
time_out = 30 # hur lång time-out är.
penelty = [0,0,0,0] #hur mycker är det kvar på utvisningen (array om 4st, 2 per lag) 0 och 2 är hemma 1 och 3 borta
PeneltyFT = [0,0,0,0] #Anger när utvisningen är slut, array om (4st 2 per lag) 0 och 2 är hemma 1 och 3 borta
penelty_leght = 120 #hur lång utvisningen är i sekunder.
peh_tid = 0
pea_tid = 0
Score =[0,0] #Poäng i en array 0 = hemma, 1 = borta 
ant_period = 3  #Antal perioder
Period = 1  #aktiv Period
Period_leght = 20 #längden på varje perido
justering = 0
aktiv = False
mins = 0
sec = 0
ot = ""
intervall = 1000
source_tid = ""
source_period = ""
sourde_HomePo = ""
source_AwayPo = ""
source_HomePe = ""
source_AwayPe = ""
hk_id1 = obs.OBS_INVALID_HOTKEY_ID
hk = list()

def tick_tack():
    global p_tid
    p_tid += 1
    #print(p_tid)
    #print(aktiv)
    for x in range(len(penelty)):
        if penelty[x] > 0:
            penelty[x] -= 1
        
    update()



def start_tid(a):
    print(a)
    global tid
    global aktiv
    global penelty
    global intervall
    if a == True:
      if aktiv == False:    
        tid = time.time() - p_tid
        peh_tid = time.time() - penelty[0] #justerar Starttiden för Utvisnting Hemma
        pea_tid = time.time() - penelty[1] #justerar Starttiden för Utvisnting Borta
        aktiv = True
        update
        obs.timer_add(tick_tack,1000)
        #obs.timer_add(update,intervall)
        
    
        


def stop_tid(a):
    global aktiv
    if a == True:
        obs.timer_remove(tick_tack)
        #obs.timer_remove(update)
        aktiv = False

def reset_tid(a):
    global p_tid
    global source_tid
    if a == True:
        p_tid = 0
        Text_tid = "{:02d}:{:02d}".format(int(p_tid),int(p_tid))  #Huvud-Klockan text format
   
        source = obs.obs_get_source_by_name(source_tid)
        settings = obs.obs_data_create()
        obs.obs_data_set_string(settings, "text", Text_tid)
        obs.obs_source_update(source, settings)
        obs.obs_data_release(settings)
        obs.obs_source_release(source)
    
    
def Score_home_plus(a):
    global Score
    if a == True:
        Score[0] += 1
        UpdateScore()

def Score_home_minus(a):
    global Score
    if a == True:
        Score[0] -= 1
        UpdateScore()
    
def Score_away_plus(a):
    global Score
    if a == True:
        Score[1] += 1
        UpdateScore()
    
def Score_away_minus(a):
    global Score
    if a == True:
        Score[1] -= 1
        UpdateScore()
    

    



def update():
    global p_tid
    global penelty
    global source_tid
    global source_HomePe
    global source_AwayPe
    global Penelty_leght
    global Perid_leght
    
    sourcet = obs.obs_get_source_by_name(source_tid)
    sourcehpe = obs.obs_get_source_by_name(source_HomePe)
    sourceape = obs.obs_get_source_by_name(source_AwayPe)
    
    #p_tid = time.time() - tid
    mins = p_tid // 60
    sec = p_tid % 60
    mins = mins % 60 

    minsHP1 = penelty[0] // 60
    secHP1 = penelty[0] % 60
    minsHP1 = minsHP1 % 60 
    
    minsHP2 = penelty[2] // 60
    secHP2 = penelty[2] % 60
    minsHP2 = minsHP2 % 60 
    
    minsAP1 = penelty[1] // 60
    secAP1 = penelty[1] % 60
    minsAP1 = minsAP1 % 60
    
    minsAP2 = penelty[3] // 60
    secAP2 = penelty[3] % 60
    minsAP2 = minsAP2 % 60 
    
    #print(p_tid)
    #Penelty_text = ["",""]
    
      
    Text_tid = "{:02d}:{:02d}".format(int(mins),int(sec))  #Huvud Klockan text format
    
    settingst = obs.obs_data_create()
    obs.obs_data_set_string(settingst, "text", Text_tid)
    obs.obs_source_update(sourcet, settingst)
    obs.obs_data_release(settingst)
    obs.obs_source_release(sourcet)
    
    if penelty[2] > 0:
        Text_HPen = "{:02d}:{:02d}\n{:02d}:{:02d}".format(int(minsHP1),int(secHP1),int(minsHP2),int(secHP2)) #Hemmalag utvisning text format
    else:
        if penelty[0] == 0:
           Text_HPen = ""
        else:
           Text_HPen = "{:02d}:{:02d}".format(int(minsHP1),int(secHP1))
        
    if penelty[3] > 0:
        Text_APen = "{:02d}:{:02d}\n{:02d}:{:02d}".format(int(minsAP1),int(secAP1),int(minsAP2),int(secAP2)) #Hemmalag utvisning text format
    else:
        if penelty[1] == 0:
            Text_APen = ""
        else:
            Text_APen = "{:02d}:{:02d}".format(int(minsAP1),int(secAP1))
    #print(Text_tid)

    
    settingshp = obs.obs_data_create()
    obs.obs_data_set_string(settingshp, "text", Text_HPen)
    obs.obs_source_update(sourcehpe, settingshp)
    obs.obs_data_release(settingshp)
    obs.obs_source_release(sourcehpe)
    
    settingsap = obs.obs_data_create()
    obs.obs_data_set_string(settingsap, "text", Text_APen)
    obs.obs_source_update(sourceape, settingsap)
    obs.obs_data_release(settingsap)
    obs.obs_source_release(sourceape)
    
    if penelty[0] == 0:
        if penelty[2] > 0:
          penelty[0] = penelty[2]
          penelty[2] = 0

    if penelty[1] == 0:
        if penelty[3] > 0:
            penelty[1] = penelty[3]
            penelty[3] = 0

    

    P_End = Period_leght*60
    #print(P_End)
    if p_tid == P_End:
       stop_tid(True)

def UpdateScore():
    global Score
    global source_HomePo
    global source_AwayPo
    print("home={0}".format(int(Score[0])))
    print("away={0}".format(int(Score[1])))

    
    source = obs.obs_get_source_by_name(source_HomePo)
    Score_textH = "{0}".format(int(Score[0]))
    Score_textA = "{0}".format(int(Score[1]))
    if source is not None:
        settings = obs.obs_data_create()
        obs.obs_data_set_string(settings, "text", Score_textH)
        obs.obs_source_update(source, settings)
        obs.obs_data_release(settings)
        obs.obs_source_release(source)
    
    source = obs.obs_get_source_by_name(source_AwayPo)
    if source is not None:
        settings = obs.obs_data_create()
        obs.obs_data_set_string(settings, "text", Score_textA)
        obs.obs_source_update(source, settings)
        obs.obs_data_release(settings)
        obs.obs_source_release(source)
        
def tid_plus(a):
    global p_tid
    global penelty
    if a == True:
        p_tid +=1
        for x in Range(penelty)
            if penelty[x] > 0
                penelty[x] -=1
        
    if a == False:
        update()
    
def tid_minus(a):
    global p_tid
    global penelty
    if a == True:
        p_tid -=1
        for x in Range(penelty)
            if penelty[x] > 0
                penelty[x] +=1
    if a == False:
        update()
    
def period_plus(a):
    global Period
     
    
    if a == True:
        Period += 1
        period_Update()
    
def period_minus(a):
    global Period
    
    if a == True:
        Period -= 1
        period_Update()
    
def period_Update():
    global Period
    global ot
    global ant_period
    global source_period
    Period_text = ""
    
    if Period > ant_period:
        Period_text = ot
    else:
        Period_text = "P{0}".format(int(Period))
        
    source = obs.obs_get_source_by_name(source_period)
    if source is not None:
        settings = obs.obs_data_create()
        obs.obs_data_set_string(settings, "text", Period_text)
        obs.obs_source_update(source, settings)
        obs.obs_data_release(settings)
        obs.obs_source_release(source)
    
def period_next(a):
    global source_tid
    global p_tid
    p_tid = 0
    period_plus(a)
    Text_tid = "{:02d}:{:02d}".format(int(p_tid),int(p_tid))  #Huvud Klockan text format
   
    source = obs.obs_get_source_by_name(source_tid)
    settings = obs.obs_data_create()
    obs.obs_data_set_string(settings, "text", Text_tid)
    obs.obs_source_update(source, settings)
    obs.obs_data_release(settings)
    obs.obs_source_release(source)
    
def Penelty_home(a):
    global penelty
    global Penelty_leght
    global p_tid
    if a == True:
        if penelty[0] == 0:
            penelty[0] = Penelty_leght
        else:
            penelty[2] = Penelty_leght
        update()
    
def Penelty_away(a):
    global p_tid
    global penelty
    global Penelty_leght
    if a == True:
        if penelty[1] == 0:
            penelty[1] = Penelty_leght
        else:
            penelty[3] = Penelty_leght
        update()
    
       


def script_load(settings):
   global hk_id
   global hk_id1
   global hk_id2
   global hk_id3
   global hk_id4
   global hk_id5
   global hk_id6
   global hk_id7
   global hk_id8
   global hk_id9
   global hk_id10
   global hk_id11
   global hk_id12
   global hk_id13
   global hk_id14
   global hk
   hk_id1 = obs.obs_hotkey_register_frontend("Start_tid","Starta klockan",start_tid)
   hk_id2 = obs.obs_hotkey_register_frontend("Stop_tid", "Stoppa klockan",stop_tid)
   hk_id3 = obs.obs_hotkey_register_frontend("Reset_tid", "Nollställ klockan",reset_tid)
   hk_id4 = obs.obs_hotkey_register_frontend("Home Score plus", "Hemma P +",Score_home_plus)
   hk_id5 = obs.obs_hotkey_register_frontend("Home Score minus", "Hemma  P -",Score_home_minus)
   hk_id6 = obs.obs_hotkey_register_frontend("Away Score plus", "Borta P +",Score_away_plus)
   hk_id7 = obs.obs_hotkey_register_frontend("Away Score minus", "Borta P -",Score_away_minus)
   hk_id8 = obs.obs_hotkey_register_frontend("Tid +s", "Tid +",tid_plus)
   hk_id9 = obs.obs_hotkey_register_frontend("Tid -s", "Tid -",tid_minus)
   hk_id10 = obs.obs_hotkey_register_frontend("Period +", "Period +",period_plus)
   hk_id11 = obs.obs_hotkey_register_frontend("Period -", "Period -",period_minus)
   hk_id12 = obs.obs_hotkey_register_frontend("NextPeriod", "Nästa Period",period_next)
   hk_id13 = obs.obs_hotkey_register_frontend("PeneltyHome", "Utvisning Hemma",Penelty_home)
   hk_id14 = obs.obs_hotkey_register_frontend("PeneltyAway", "Utvisting Borta",Penelty_away)
   
   

   hsa1 = obs.obs_data_get_array(settings, "Start_tid")
   hsa2 = obs.obs_data_get_array(settings, "Stop_tid")
   hsa3 = obs.obs_data_get_array(settings, "Reset_tid")
   hsa4 = obs.obs_data_get_array(settings, "Home Score plus")
   hsa5 = obs.obs_data_get_array(settings, "Home Score minus")
   hsa6 = obs.obs_data_get_array(settings, "Away Score plus")
   hsa7 = obs.obs_data_get_array(settings, "Away Score minus")
   hsa8 = obs.obs_data_get_array(settings, "Tid +s")
   hsa9 = obs.obs_data_get_array(settings, "Tid -s")
   hsa10 = obs.obs_data_get_array(settings, "Period +")
   hsa11 = obs.obs_data_get_array(settings, "Period -")
   hsa12 = obs.obs_data_get_array(settings, "NextPeriod")
   hsa13 = obs.obs_data_get_array(settings, "PeneltyHome")
   hsa14 = obs.obs_data_get_array(settings, "PeneltyAway")
   
   obs.obs_hotkey_load(hk_id1, hsa1)
   obs.obs_data_array_release(hsa1)
   
   obs.obs_hotkey_load(hk_id2, hsa2)
   obs.obs_data_array_release(hsa2)
   
   obs.obs_hotkey_load(hk_id3, hsa3)
   obs.obs_data_array_release(hsa3)
   
   obs.obs_hotkey_load(hk_id4, hsa4)
   obs.obs_data_array_release(hsa4)
   
   obs.obs_hotkey_load(hk_id5, hsa5)
   obs.obs_data_array_release(hsa5)
   
   obs.obs_hotkey_load(hk_id6, hsa6)
   obs.obs_data_array_release(hsa6) 
   
   obs.obs_hotkey_load(hk_id7, hsa7)
   obs.obs_data_array_release(hsa7)
   
   obs.obs_hotkey_load(hk_id8, hsa8)
   obs.obs_data_array_release(hsa8)
   
   obs.obs_hotkey_load(hk_id9, hsa9)
   obs.obs_data_array_release(hsa9)
   
   obs.obs_hotkey_load(hk_id10, hsa10)
   obs.obs_data_array_release(hsa10)
   
   obs.obs_hotkey_load(hk_id11, hsa11)
   obs.obs_data_array_release(hsa11)
   
   obs.obs_hotkey_load(hk_id12, hsa12)
   obs.obs_data_array_release(hsa12)       

   obs.obs_hotkey_load(hk_id13, hsa13)
   obs.obs_data_array_release(hsa13)
   
   obs.obs_hotkey_load(hk_id14, hsa14)
   obs.obs_data_array_release(hsa14)  

 
    
    

    
    

def script_description():
    return "Match klocka"

def script_defaults(settings):
    obs.obs_data_set_default_int(settings, "Interval", 500)
    obs.obs_data_set_default_int(settings, "Period_leght", 20)
    obs.obs_data_set_default_int(settings, "Penelty_leght", 120)
    obs.obs_data_set_default_int(settings, "Antal_Perioder", 3)
    obs.obs_data_set_default_string(settings, "OT", "OT")
    


def script_properties():
    props = obs.obs_properties_create()

    obs.obs_properties_add_int(props, "Period_leght", "Period längd (min)", 1, 30, 1)
    obs.obs_properties_add_int(props, "Antal_Perioder", "Antal Perioder", 1, 10, 1)
    obs.obs_properties_add_int(props, "Penelty_leght", "Utvisning (sec)", 1, 300, 1)
    obs.obs_properties_add_text(props, "OT", "Period OT", obs.OBS_TEXT_DEFAULT)
    #obs.obs_properties_add_int(props, "Interval", "Updaterings Intervall (ms)", 1, 3600, 1)

    p = obs.obs_properties_add_list(props, "tid_source", "Källa klocka", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
    sources = obs.obs_enum_sources()
    if sources is not None:
        for source in sources:
            source_id = obs.obs_source_get_unversioned_id(source)
            if source_id in ["text_gdiplus", "text_ft2_source"]:
                name = obs.obs_source_get_name(source)
                obs.obs_property_list_add_string(p, name, name)

        obs.source_list_release(sources)
        
    p = obs.obs_properties_add_list(props, "penetyH_source", "Källa Utvisning hemma", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
    sources = obs.obs_enum_sources()
    if sources is not None:
        for source in sources:
            source_id = obs.obs_source_get_unversioned_id(source)
            if source_id in ["text_gdiplus", "text_ft2_source"]:
                name = obs.obs_source_get_name(source)
                obs.obs_property_list_add_string(p, name, name)

        obs.source_list_release(sources)
        
    p = obs.obs_properties_add_list(props, "penetyA_source", "Källa Utvisning Borta", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
    sources = obs.obs_enum_sources()
    if sources is not None:
        for source in sources:
            source_id = obs.obs_source_get_unversioned_id(source)
            if source_id in ["text_gdiplus", "text_ft2_source"]:
                name = obs.obs_source_get_name(source)
                obs.obs_property_list_add_string(p, name, name)
                
        p = obs.obs_properties_add_list(props, "period_source", "Källa Period", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
    sources = obs.obs_enum_sources()
    if sources is not None:
        for source in sources:
            source_id = obs.obs_source_get_unversioned_id(source)
            if source_id in ["text_gdiplus", "text_ft2_source"]:
                name = obs.obs_source_get_name(source)
                obs.obs_property_list_add_string(p, name, name)
                
        p = obs.obs_properties_add_list(props, "HomePoint", "Källa Poäng Hemma", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
    sources = obs.obs_enum_sources()
    if sources is not None:
        for source in sources:
            source_id = obs.obs_source_get_unversioned_id(source)
            if source_id in ["text_gdiplus", "text_ft2_source"]:
                name = obs.obs_source_get_name(source)
                obs.obs_property_list_add_string(p, name, name)
                
        p = obs.obs_properties_add_list(props, "AwayPoint", "Källa Poäng Borta", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
    sources = obs.obs_enum_sources()
    if sources is not None:
        for source in sources:
            source_id = obs.obs_source_get_unversioned_id(source)
            if source_id in ["text_gdiplus", "text_ft2_source"]:
                name = obs.obs_source_get_name(source)
                obs.obs_property_list_add_string(p, name, name)
    #obs.obs_properties_add_button(props, "button", "Uppdatera", script_update)            
    return props



def script_update(settings):
    global ant_period
    global ot
    global Period_leght
    global intervall
    global Penelty_leght
    global source_tid
    global source_period
    global source_HomePo
    global source_AwayPo
    global source_HomePe
    global source_AwayPe
    
    
    ant_period = obs.obs_data_get_int(settings, "Antal_Perioder")
    ot = obs.obs_data_get_string(settings, "OT")
    Period_leght = obs.obs_data_get_int(settings, "Period_leght")
    intervall = obs.obs_data_get_int(settings, "Interval")
    Penelty_leght = obs.obs_data_get_int(settings, "Penelty_leght")
    source_tid = obs.obs_data_get_string(settings, "tid_source")
    source_period = obs.obs_data_get_string(settings, "period_source")
    source_HomePo = obs.obs_data_get_string(settings, "HomePoint")
    source_AwayPo = obs.obs_data_get_string(settings, "AwayPoint")
    source_HomePe = obs.obs_data_get_string(settings, "penetyH_source")
    source_AwayPe = obs.obs_data_get_string(settings, "penetyA_source")
    
def script_save(settings):
    global hk_id1
    global hk_id2
    global hk_id3
    global hk_id4
    global hk_id5
    global hk_id6
    global hk_id7
    global hk_id8
    global hk_id9
    global hk_id10
    global hk_id11
    global hk_id12
    global hk_id13
    global hk_id14
    
    sets = ["Start_tid",\
        "Stop_tid",\
        "Reset_tid",\
        "Home Score plus",\
        "Home Score minus",\
        "Away Score plus",\
        "Away Score minus",\
        "Tid +s",\
        "Tid -s",\
        "Period +",\
        "Period -",\
        "NextPeriod",\
        "PeneltyHome",\
        "PeneltyAway"]
    print(len(hk))
    

    hotkey_save_array = obs.obs_hotkey_save(hk_id1)
    obs.obs_data_set_array(settings, "Start_tid", hotkey_save_array)
    obs.obs_data_array_release(hotkey_save_array)
 
    hotkey_save_array = obs.obs_hotkey_save(hk_id2)
    obs.obs_data_set_array(settings, "Stop_tid", hotkey_save_array)
    obs.obs_data_array_release(hotkey_save_array)
      
    hotkey_save_array = obs.obs_hotkey_save(hk_id3)
    obs.obs_data_set_array(settings, "Reset_tid", hotkey_save_array)
    obs.obs_data_array_release(hotkey_save_array)
  
    hotkey_save_array = obs.obs_hotkey_save(hk_id4)
    obs.obs_data_set_array(settings, "Home Score plus", hotkey_save_array)
    obs.obs_data_array_release(hotkey_save_array)
    
    hotkey_save_array = obs.obs_hotkey_save(hk_id5)
    obs.obs_data_set_array(settings, "Home Score minus", hotkey_save_array)
    obs.obs_data_array_release(hotkey_save_array)
    
    hotkey_save_array = obs.obs_hotkey_save(hk_id6)
    obs.obs_data_set_array(settings, "Away Score plus", hotkey_save_array)
    obs.obs_data_array_release(hotkey_save_array)
    
    hotkey_save_array = obs.obs_hotkey_save(hk_id7)
    obs.obs_data_set_array(settings, "Away Score minus", hotkey_save_array)
    obs.obs_data_array_release(hotkey_save_array)
    
    hotkey_save_array = obs.obs_hotkey_save(hk_id8)
    obs.obs_data_set_array(settings, "Tid +s", hotkey_save_array)
    obs.obs_data_array_release(hotkey_save_array)
 
    hotkey_save_array = obs.obs_hotkey_save(hk_id9)
    obs.obs_data_set_array(settings, "Tid -s", hotkey_save_array)
    obs.obs_data_array_release(hotkey_save_array)
      
    hotkey_save_array = obs.obs_hotkey_save(hk_id10)
    obs.obs_data_set_array(settings, "Period +", hotkey_save_array)
    obs.obs_data_array_release(hotkey_save_array)
  
    hotkey_save_array = obs.obs_hotkey_save(hk_id11)
    obs.obs_data_set_array(settings, "Period -", hotkey_save_array)
    obs.obs_data_array_release(hotkey_save_array)
    
    hotkey_save_array = obs.obs_hotkey_save(hk_id12)
    obs.obs_data_set_array(settings, "NextPeriod", hotkey_save_array)
    obs.obs_data_array_release(hotkey_save_array)
    
    hotkey_save_array = obs.obs_hotkey_save(hk_id13)
    obs.obs_data_set_array(settings, "PeneltyHome", hotkey_save_array)
    obs.obs_data_array_release(hotkey_save_array)
    
    hotkey_save_array = obs.obs_hotkey_save(hk_id14)
    obs.obs_data_set_array(settings, "PeneltyAway", hotkey_save_array)
    obs.obs_data_array_release(hotkey_save_array)


    
    
    
