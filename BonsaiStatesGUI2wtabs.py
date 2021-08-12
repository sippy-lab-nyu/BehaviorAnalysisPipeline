# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#IMPORT ALL PACKAGES
import PySimpleGUI as sg
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.widgets  import RectangleSelector
import matplotlib
from json import (load as jsonload, dump as jsondump)
import os.path
from os import path
import io
matplotlib.use('TkAgg')


#SETTINGS SECTION/DEFAULTS
SETTINGS_FILE = path.join(path.dirname(__file__), r'settings_file.cfg')
DEFAULT_SETTINGS = {'start_window': 1, 'end_window' : 2,'y_minimum': -200, 'y_maximum': 200,'tone_length': 0.1 , 'align_1': False, 'align_2': True,'theme': sg.theme()}
# "Map" from the settings dictionary keys to the window's element keys
SETTINGS_KEYS_TO_ELEMENT_KEYS = {'start_window': 'START', 'end_window': 'END' ,'y_minimum': 'YMIN','y_maximum': 'YMAX','tone_length': 'TONELENGTH' , 'align_1':'ALIGN1','align_2':'ALIGN2','theme': '-THEME-'}



#METADATA DEFAULTS
METADATA_FILE = path.join(path.dirname(__file__), r'metadata_file.cfg')
DEFAULT_METADATA = {'mousefilename':'SS001data','mouse_name': 'SS001', 'mouse_gender': 'Male', 'mouse_genotype' : 2,'start_date': '01 January, 2000' , 'training_day': 1, 'training_phase' : 'Pre-Training', 'joystick_threshold' : 40,
                    'iti_threshold' : '-20 to 20', 'iti_parameter' : '2 seconds', 'iti_penaltyparameter' : '00:00:01', 'pull_thresholdparameter' : -20, 'pull_penaltyparameter' : '00:00:01'}
# "Map" from the settings dictionary keys to the window's element keys
METADATA_KEYS_TO_ELEMENT_KEYS = {'mousefilename':'MOUSEFILENAME','mouse_name': 'MOUSENAME', 'mouse_gender': 'GENDER','mouse_genotype': 'GENOTYPE' ,'start_date': 'STARTDATE' , 'training_day': 'TRAININGDAY', 'training_phase' : 'TRAININGPHASE',
                                 'joystick_threshold': 'JOYSTICKTHRESHOLD', 'iti_threshold': 'ITITHRESHOLD', 'iti_parameter': 'ITIPARAMETER', 'iti_penaltyparameter': 'ITIPENALTYPARAMETER',
                                 'pull_thresholdparameter': 'PULLTHRESHOLDPARAMETER', 'pull_penaltyparameter': 'PULLPENALTYPARAMETER'}



#LOAD SETTINGS FUNCTION
def load_settings(settings_file, default_settings):
    try:
        with open(settings_file, 'r') as f:
            settings = jsonload(f)
    except Exception as e:
        sg.popup_quick_message(f'exception {e}', 'No settings file found... will create one for you', keep_on_top=True, background_color='red', text_color='white')
        settings = default_settings
        save_settings(settings_file, settings, None)
    return settings


#LOAD METADATA FUNCTION
def load_metadata(metadata_file, default_metadata):
    try:
        with open(metadata_file, 'r') as f:
            metadata = jsonload(f)
    except Exception as e:
        sg.popup_quick_message(f'exception {e}', 'No metadata file found... will create one for you', keep_on_top=True, background_color='red', text_color='white')
        metadata = default_metadata
        save_metadata(metadata_file, metadata, None)
    return metadata


#SAVE LOCAL SETTINGS FUNCTION
def save_settings(settings_file, settings, values):
    if values:      # if there are stuff specified by another window, fill in those values
        for key in SETTINGS_KEYS_TO_ELEMENT_KEYS:  # update window with the values read from settings file
            try:
                settings[key] = values[SETTINGS_KEYS_TO_ELEMENT_KEYS[key]]
            except Exception as e:
                print(f'Problem updating settings from window values. Key = {key}')

    with open(settings_file, 'w') as f:
        jsondump(settings, f)

    sg.popup('Settings saved')


#SAVE METADATA FUNCTION
def save_metadata(metadata_file, metadata, values):
    if values:      # if there are stuff specified by another window, fill in those values
        for key in METADATA_KEYS_TO_ELEMENT_KEYS:  # update window with the values read from settings file
            try:
                metadata[key] = values[METADATA_KEYS_TO_ELEMENT_KEYS[key]]
            except Exception as e:
                print(f'Problem updating settings from window values. Key = {key}')

    with open(metadata_file, 'w') as f:
        jsondump(metadata, f)

    sg.popup('Metadata saved')


#SETTINGS WINDOW
def create_data_splicer_window():
    settings = load_settings(SETTINGS_FILE, DEFAULT_SETTINGS )
    sg.theme(settings['theme'])

    def TextLabel(text): return sg.Text(text+':', justification='r', size=(20,1))

    phaselist = 'Pre-Training','Single Tone', 'Full task'

    layout = [  [sg.Text('Splice Data', font='Any 15')],
                [TextLabel('Start Trial'), sg.Spin(values=[i for i in range(0, States["Trial"].max()-1)], key = 'StartSplice')],
                [TextLabel('Last Trial '), sg.Spin(values=[i for i in range(1, States["Trial"].max())], key = 'EndSplice')],
                [sg.Canvas(key="DayPerformance")],
                [sg.Button('Save'), sg.Button('Exit')]  ]

    window = sg.Window('Data Splicer', layout, keep_on_top=True, finalize=True)
        
    return window


#SETTINGS WINDOW
def create_settings_window(settings):
    sg.theme(settings['theme'])

    def TextLabel(text): return sg.Text(text+':', justification='r', size=(20,1))

    phaselist = 'Pre-Training','Single Tone', 'Full task'

    layout = [  [sg.Text('Visualizer Settings', font='Any 15')],
                [TextLabel('Time before Alignment'), sg.Spin(values=[i for i in range(0, 10)], key = 'START'),TextLabel('Time after Alignment'),sg.Spin(values=[i for i in range(0, 10)], key = 'END')],
                [TextLabel('Y-Axis Range'), sg.Spin(values=[i for i in range(-500, 500)], key= 'YMIN'), sg.Spin(values=[i for i in range(-500, 500)], key = 'YMAX')],
                [TextLabel('Tone Duration'),sg.Input(key='TONELENGTH')],
                [sg.Radio('Align to Hit', "ALIGN", default=False, key = 'ALIGN1'),sg.Radio('Align to Tone', "ALIGN", default=True, key = 'ALIGN2')],
                [TextLabel('Theme'),sg.Combo(sg.theme_list(), size=(20, 20), key='-THEME-')],
                [sg.Button('Save'), sg.Button('Exit')]  ]

    window = sg.Window('Settings', layout, keep_on_top=True, finalize=True)
    
    
    for key in SETTINGS_KEYS_TO_ELEMENT_KEYS:   # update window with the values read from settings file
        try:
            window[SETTINGS_KEYS_TO_ELEMENT_KEYS[key]].update(value=settings[key])
        except Exception as e:
            print(f'Problem updating PySimpleGUI window from settings. Key = {key}')
        
    return window


#MOUSE METADATA WINDOW
def create_metadata_window(metadata):
    settings = load_settings(SETTINGS_FILE, DEFAULT_SETTINGS )
    sg.theme(settings['theme'])

    def TextLabel(text): return sg.Text(text+':', justification='r', size=(16,1))

    layout = [  [sg.Text('METADATA', font='Any 15')],
                [TextLabel('Mouse Log File Name'), sg.Input(key='MOUSEFILENAME')],
                [TextLabel('Mouse Name'), sg.Input(key='MOUSENAME'),TextLabel('Genotype'),sg.Input(key='GENOTYPE')],
                [TextLabel('Gender'),sg.Input(key='GENDER'),TextLabel('Start Date'),sg.Input(key='STARTDATE'),sg.CalendarButton('Calendar', target='STARTDATE', pad=None, font=('MS Sans Serif', 10, 'bold'),
                button_color=('red', 'white'), key='_CALENDAR_', format=('%d %B %Y'))],
                [sg.Text('Trial Parameters', font='Any 15')],
                [TextLabel('Training Day'),sg.Input(key='TRAININGDAY'), TextLabel('Training Phase'),sg.Combo(['Pre-Training', 'Single Tone', 'Go-NoGo Task', 'Auditory Discrimination Task'], enable_events=False, key='TRAININGPHASE')],
                [TextLabel('Joystick Threshold'),sg.Input(key='JOYSTICKTHRESHOLD'), TextLabel('ITI Threshold'),sg.Input(key='ITITHRESHOLD')],
                [TextLabel('ITI Duration'),sg.Input(key='ITIPARAMETER'), TextLabel('ITI Penalty Duration'),sg.Input(key='ITIPENALTYPARAMETER')],
                [TextLabel('Pull Threshold'),sg.Input(key='PULLTHRESHOLDPARAMETER'), TextLabel('Pull Penalty'),sg.Input(key='PULLPENALTYPARAMETER')],
                [sg.Button('Save'), sg.Button('Exit')]  ]

    window = sg.Window('Experiment Metadata', layout, keep_on_top=True, finalize=True)

    for key in METADATA_KEYS_TO_ELEMENT_KEYS:   # update window with the values read from settings file
        try:
            window[METADATA_KEYS_TO_ELEMENT_KEYS[key]].update(value=metadata[key])
        except Exception as e:
            print(f'Problem updating PySimpleGUI window from settings. Key = {key}')

    return window


#CLEAR PLOTS
figure_canvas_agg = None
figure_canvas_agg2 = None
figure_canvas_agg3 = None


#MAIN WINDOW LAUNCH
def main():
    window, settings = None, load_settings(SETTINGS_FILE, DEFAULT_SETTINGS )
    window, metadata = None, load_metadata(METADATA_FILE, DEFAULT_METADATA )
    while True:             # Event Loop
        #LAYOUT
        if window is None:
            settings = load_settings(SETTINGS_FILE, DEFAULT_SETTINGS )
            metadata = load_metadata(METADATA_FILE, DEFAULT_METADATA )
            sg.theme(settings['theme'])
            HitTracetab1 = [[sg.Canvas(key="HitTraces")]]
            FAtab2 = [[sg.Canvas(key="FATraces")]]
            Misstab2 = [[sg.Canvas(key="MissTraces")]]
            
            tab_group_layout = [[sg.Tab('Hit Raw Traces', HitTracetab1,font='Courier 15', key='TAB1')],
                                [sg.Tab('False Alarm Raw Traces', FAtab2, font='Courier 15',key='TAB2')],
                                [sg.Tab('Miss Raw Traces', Misstab2, font='Courier 15',key='TAB3')]]
            
            menu_def = [['File',['Upload',['StateTransitions File...', 'Joystick File...', 'Mouse Log File...'],'Save',['Save Mouse Log File', 'Save Plots' ]]],
                ['Settings', ['Graphic Settings', 'Metadata Settings','Splice Dataset' ]],            
                ['Help', ['About...'] ]]
            
            summaryoutput_layout = [[sg.Button(button_text = 'Log Mouse Metadata',key='MouseMetadata'),  sg.Button(button_text = 'Log Trial Metadata',key='TrialMetadata'),sg.Button(button_text = 'Summary Analysis',key='Summary')]]
            joystickgraphs_layout = [[sg.Button(button_text = 'Joystick Traces',key='Traces')]]
            
            layout = [[sg.Menu(menu_def)],
                      [sg.Text('Modified Go-NoGo Task Analysis', size=(75, 1), font=("Helvetica", 25), text_color='white')],
                      [sg.Frame(layout = summaryoutput_layout,title='Summary Output',title_color='white', relief=sg.RELIEF_SUNKEN, tooltip='Add data to output window'), sg.Frame(layout = joystickgraphs_layout,title='Graph Output',title_color='white', relief=sg.RELIEF_SUNKEN, tooltip='Plot Traces')],
                      [sg.Multiline(size=(50,30),key='Output',pad=(0,20)),
                       sg.TabGroup(tab_group_layout,
                                   enable_events=True,
                                   key='-TABGROUP-')],
                      [sg.Button(button_text = 'Save Output',key='SAVE_OUTPUT'),sg.Button(button_text = 'Load Output',key='LOAD_OUTPUT'),sg.Exit()]]
            window = sg.Window('SippyLab ModifiedGoNoGo Data Analysis', layout, element_justification='center', size= (1400,700))
        
        event, values = window.read()

        #Exit Button
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
            window.close()    
        
        
        #UploadStates Button
        if event == 'StateTransitions File...':
            filename = sg.popup_get_file('Enter the StateTransitions file you wish to process')
            if filename == None:
                sg.popup('No file uploaded')
            else:    
                validfile1 = filename.endswith("csv") and 'StateTransitions' in filename
                if validfile1 == True:
                    global States
                    States = pd.read_csv(filename)
                    #event, values = create_data_splicer_window().read(close=True)
                    sg.popup('StateTransitions file successfully uploaded')
                else:
                    sg.popup('Please upload a valid file')
        
        
        #UploadJoystick Button
        if event == 'Joystick File...':
            filename2 = sg.popup_get_file('Enter the Joystick file you wish to process')
            if filename2 == None:
                sg.popup('No file uploaded')
            else:   
                validfile2 = filename2.endswith("csv") and 'Joystick' in filename2
                if validfile2 == True:
                    Joystick = pd.read_csv(filename2)
                    sg.popup('Joystick file successfully uploaded')
                else:
                    sg.popup('Please upload a valid file')
                
        #UploadMouse_Log Button
        if event == 'Mouse Log File...':
            filename3 = sg.popup_get_file('Enter the Mouse Log file you wish to process')
            if filename3 == None:
                sg.popup('No file uploaded')
            else:   
                validfile3 = filename3.endswith("csv") and 'mouse_log' in filename3
                if validfile3 == True:
                    mouselog = pd.read_csv(filename3)
                    sg.popup('Mouse Log file successfully uploaded')
                else:
                    sg.popup('Please upload a valid file')
    
        #SUMMARY STATS       
        if event == 'Summary':
            if 'validfile1' in locals():
                if validfile1 == True:
                #ITI DURATION
                    ITITone = States[States['Id'].isin(['ITI','Go','NoGo'])]
                    ITIDuration = ITITone.ElapsedTime.diff()
                    AvgITIDuration = ITIDuration[1::2].mean()
                #HIT RATE/FALSE ALARM
                    Hit = States[States['Id'] == 'Hit']
                    Go = States[States['Id'] == 'Go']
                    if Go.shape[0] > 0:
                        HitRate = Hit.shape[0]/Go.shape[0]
                        if metadata['training_phase'] == 'Pre-Training':
                            window['Output'].print('Correct Action Percentage,' + str(HitRate))
                        else:
                            window['Output'].print('Hit Rate,' + str(HitRate))
                    else:
                        print("No Go Tone Trials found")
                    FalseAlarm = States[States['Id'] == 'FalseAlarm']
                    NoGo = States[States['Id'] == 'NoGo']
                    if NoGo.shape[0] > 0:
                        FalseAlarmRate = FalseAlarm.shape[0]/NoGo.shape[0]
                        window['Output'].print('False Alarm Rate,' + str(FalseAlarmRate))
                    else:
                        print("No NoGo Tone Trials found")
                #RESPONSE LATENCY
                    HitTimestamps = States[States['Id'].isin(['Hit'])].Trial
                    HitTrialsOnly = States.loc[States['Trial'].isin(HitTimestamps)]
                    GoHit = HitTrialsOnly[HitTrialsOnly['Id'].isin(['Go','Hit'])]
                    ResponseLatency = GoHit.ElapsedTime.diff()
                    AvgResponseLatency = ResponseLatency[1::2].mean()
                    window['Output'].print('Average ITI Duration,' + str(AvgITIDuration))
                    window['Output'].print('Average Response Latency,' + str(AvgResponseLatency))
                    window['Output'].print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                else:
                    sg.popup('Please upload a StateTransitions file')
            else:
                sg.popup('Please upload a StateTransitions file')
            
            
        #GRAPH TRACES BUTTON
        if event == 'Traces':
            if ('validfile1' in locals() and 'validfile2' in locals()):
                if validfile1 == True and validfile2 == True:
                    #TONE ALIGNMENT GRAPHS
                    if settings['align_2'] == True:
                        #Collect all Go Tones Hit into a Dataframe
                        HitTimestamps = States[States['Id'].isin(['Hit'])].Trial
                        HitTrialsOnly = States.loc[States['Trial'].isin(HitTimestamps)]
                        GoHit = HitTrialsOnly[HitTrialsOnly['Id'].isin(['Go','Hit'])]
                        GoToneOnset = HitTrialsOnly[HitTrialsOnly['Id'].isin(['Go'])]
                        len(GoToneOnset)
                        GoToneOnset = GoToneOnset["ElapsedTime"]
                        GoToneOnset = np.round(GoToneOnset, decimals = 3)
                        GoToneOnset.index = range(len(GoToneOnset))
                        GoToneRange = pd.DataFrame(columns=('X','Start','End'))
                        
                        #Collect all No Go Tones FalseAlarms into a Dataframe
                        FalseAlarmTimestamps = States[States['Id'].isin(['FalseAlarm'])].Trial
                        FalseAlarmTrialsOnly = States.loc[States['Trial'].isin(FalseAlarmTimestamps)]
                        NoGoFA = FalseAlarmTrialsOnly[FalseAlarmTrialsOnly['Id'].isin(['NoGo','FalseAlarm'])]
                        NoGoToneOnset = FalseAlarmTrialsOnly[FalseAlarmTrialsOnly['Id'].isin(['NoGo'])]
                        len(NoGoToneOnset)
                        NoGoToneOnset = NoGoToneOnset["ElapsedTime"]
                        NoGoToneOnset = np.round(NoGoToneOnset, decimals = 3)
                        NoGoToneOnset.index = range(len(NoGoToneOnset))
                        NoGoToneRange = pd.DataFrame(columns=('X','Start','End'))
                        
                        #Collect all Go Tones Miss into a Dataframe
                        MissTimestamps = States[States['Id'].isin(['Miss'])].Trial
                        MissTrialsOnly = States.loc[States['Trial'].isin(MissTimestamps)]
                        GoMiss = MissTrialsOnly[MissTrialsOnly['Id'].isin(['Go','Miss'])]
                        GoToneOnsetMiss = MissTrialsOnly[MissTrialsOnly['Id'].isin(['Go'])]
                        len(GoToneOnsetMiss)
                        GoToneOnsetMiss = GoToneOnsetMiss["ElapsedTime"]
                        GoToneOnsetMiss = np.round(GoToneOnsetMiss, decimals = 3)
                        GoToneOnsetMiss.index = range(len(GoToneOnsetMiss))
                        GoToneMissRange = pd.DataFrame(columns=('X','Start','End'))
                        
                        #Read your parameters
                        startwindow = float(settings['start_window'])
                        endwindow = float(settings['end_window']) 
                        toneduration = float(settings['tone_length'])
                        
                        #Collect all tones onsets in overlapping time window
                        for x in range(len(NoGoToneOnset)):
                            NoGoToneRange.loc[x] = ['line' + str(x), NoGoToneOnset[x]-startwindow, NoGoToneOnset[x]+endwindow]
                        for x in range(len(GoToneOnset)):
                            GoToneRange.loc[x] = ['line' + str(x), GoToneOnset[x]-startwindow, GoToneOnset[x]+endwindow]
                        for x in range(len(GoToneOnsetMiss)):
                            GoToneMissRange.loc[x] = ['line' + str(x), GoToneOnsetMiss[x]-startwindow, GoToneOnsetMiss[x]+endwindow]
                        if  GoToneRange.empty:
                            pass
                        else:
                            GoToneRange=np.round(GoToneRange, decimals=3)
                        if NoGoToneRange.empty:
                            pass
                        else:
                            NoGoToneRange=np.round(NoGoToneRange, decimals=3)
                        if GoToneMissRange.empty:
                            pass
                        else:
                            GoToneMissRange=np.round(GoToneMissRange, decimals=3)
                        
                        #Format Joystick Data
                        JoystickTrace = Joystick[Joystick['Command'] == 44]
                        col_list = list(JoystickTrace)
                        col_list[0], col_list[1], col_list[2], col_list[3] = col_list[0], col_list[2], col_list[1], col_list[3]
                        JoystickTrace.columns = col_list
                        JoystickTrace = JoystickTrace.set_index('Timestamp')
                        
                        #Clear existing plots
                        if 'figure_canvas_agg' in locals() or 'figure_canvas_agg2' in locals():
                            if figure_canvas_agg or figure_canvas_agg2:
                                figure_canvas_agg.get_tk_widget().forget()
                                figure_canvas_agg2.get_tk_widget().forget()
                                plt.close('all')
                                ax.cla()
                        if 'figure_canvas_agg3' in locals():
                            if figure_canvas_agg3:
                                figure_canvas_agg3.get_tk_widget().forget()
                                plt.close('all')
                                ax.cla()
                        
                        #CREATE MEAN DATAFRAME
                        HitTraceMean = pd.DataFrame(index = np.arange(0,startwindow+endwindow+0.001,0.001), columns=np.arange(len(GoToneRange)))
                        MissTraceMean = pd.DataFrame(index = np.arange(0,startwindow+endwindow+0.001,0.001), columns=np.arange(len(GoToneMissRange)))
                        FATraceMean = pd.DataFrame(index = np.arange(0,startwindow+endwindow+0.001,0.001), columns=np.arange(len(NoGoToneRange)))
                        
                        #Plot Hit Traces
                        fig = matplotlib.figure.Figure(figsize=(8, 4), dpi=100)
                        fig2 = matplotlib.figure.Figure(figsize=(8, 4), dpi=100)
                        fig3 = matplotlib.figure.Figure(figsize=(8, 4), dpi=100)
                        ax = fig.add_subplot(111)
                        for x in range(len(GoToneRange)):
                            JoystickHitTraces = JoystickTrace[GoToneRange["Start"].loc[x]:GoToneRange["End"].loc[x]]
                            JoystickHitTraces['new_index'] = JoystickHitTraces.index - GoToneRange["Start"].loc[x]
                            JoystickHitTraces = JoystickHitTraces.set_index('new_index')
                            ax.plot(JoystickHitTraces.index, JoystickHitTraces["DataElement0"], color = 'grey')
                    
                        #Plot HIT MEAN TRACE
                        for x in range(len(GoToneRange)):
                            TraceWithinWindow = JoystickTrace[GoToneRange["Start"].loc[x]:GoToneRange["End"].loc[x]]
                            TraceWithinWindow['new_index'] = TraceWithinWindow.index - GoToneRange["Start"].loc[x]
                            TraceWithinWindow['new_index'] = np.round(TraceWithinWindow['new_index'], decimals = 3)
                            TraceWithinWindow = TraceWithinWindow.set_index('new_index')
                            TraceWithinWindow = TraceWithinWindow['DataElement0']
                            HitTraceMean.iloc[:,x] = TraceWithinWindow
                        if HitTraceMean.empty:
                            pass
                        else: 
                            HitTraceMean['mean'] = HitTraceMean.mean(axis=1)
                            HitTraceMean['var'] = HitTraceMean.loc[:,HitTraceMean.columns != 'mean'].var(axis=1)
                            HitTraceVar = HitTraceMean['var'].mean()
                            textstr = 'Average Variance,' + str(HitTraceVar)
                            ax.plot(JoystickHitTraces.index, HitTraceMean['mean'], color = 'black')
                            window['Output'].print(textstr)
                        
                        #FORMAT GRAPHS AND ADD LANDMARKS
                        ax.axvline(x=startwindow,linestyle="--",color='red',
                                   label="ToneOnset")
                        ax.axvline(x=startwindow+toneduration,linestyle="--",color='red',
                                   label="ToneOffset")
                        ax.set_xticks((0, startwindow, startwindow+endwindow))
                        ax.set_xticklabels((str(0-startwindow), '0', str(endwindow)))
                        ax.set_xlabel('Time (sec)')
                        ax.set_ylabel('Joystick Deflection')
                        ax.set_ylim([int(settings['y_minimum']),int(settings['y_maximum'])])
                        #textboxstyle = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
                        #ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=8,
                            #verticalalignment='top', bbox=textboxstyle)
                        figure_canvas_agg = FigureCanvasTkAgg(fig, window['HitTraces'].TKCanvas)
                        figure_canvas_agg.draw()
                        figure_canvas_agg.get_tk_widget().pack(side='left')
                        figure_canvas_agg
                        
                        #Plot False Alarm Traces
                        ax2 = fig2.add_subplot(111)
                        for x in range(len(NoGoToneRange)):
                            JoystickFATraces = JoystickTrace[NoGoToneRange["Start"].loc[x]:NoGoToneRange["End"].loc[x]]
                            JoystickFATraces['new_index'] = JoystickFATraces.index - NoGoToneRange["Start"].loc[x]
                            JoystickFATraces = JoystickFATraces.set_index('new_index')
                            ax2.plot(JoystickFATraces.index, JoystickFATraces["DataElement0"], color='grey')
                        
                        #Plot False Alarm MEAN TRACE
                        for x in range(len(NoGoToneRange)):
                            TraceWithinWindow = JoystickTrace[NoGoToneRange["Start"].loc[x]:NoGoToneRange["End"].loc[x]]
                            TraceWithinWindow['new_index'] = TraceWithinWindow.index - NoGoToneRange["Start"].loc[x]
                            TraceWithinWindow['new_index'] = np.round(TraceWithinWindow['new_index'], decimals = 3)
                            TraceWithinWindow = TraceWithinWindow.set_index('new_index')
                            TraceWithinWindow = TraceWithinWindow['DataElement0']
                            FATraceMean.iloc[:,x] = TraceWithinWindow
                        if FATraceMean.empty:
                            pass
                        else: 
                            FATraceMean['mean'] = FATraceMean.mean(axis=1)
                            FATraceMean['var'] = FATraceMean.loc[:,FATraceMean.columns != 'mean'].var(axis=1)
                            FATraceVar = FATraceMean['var'].mean()
                            textstr = 'Average Variance,' + str(FATraceVar)
                            ax2.plot(JoystickHitTraces.index, FATraceMean['mean'], color = 'black')
                            window['Output'].print(textstr)
                            
                        #FORMAT GRAPHS AND ADD LANDMARKS
                        ax2.axvline(x=startwindow,linestyle="--",color='red',
                                   label="ToneOnset")
                        ax2.axvline(x=startwindow+toneduration,linestyle="--",color='red',
                                   label="ToneOffset")
                        ax2.set_xticks((0, startwindow, startwindow+endwindow))
                        ax2.set_xticklabels((str(0-startwindow), '0', str(endwindow)))
                        ax2.set_xlabel('Time (sec)')
                        ax2.set_ylabel('Joystick Deflection')
                        ax2.set_ylim([int(settings['y_minimum']),int(settings['y_maximum'])])
                        #ax2.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=8,
                            #verticalalignment='top', bbox=textboxstyle)
                        figure_canvas_agg2 = FigureCanvasTkAgg(fig2, window['FATraces'].TKCanvas)
                        figure_canvas_agg2.draw()
                        figure_canvas_agg2.get_tk_widget().pack(side='right')
                        figure_canvas_agg2
                        
                        #Plot Miss Traces
                        ax3 = fig3.add_subplot(111)
                        for x in range(len(GoToneMissRange)):
                            JoystickMissTraces = JoystickTrace[GoToneMissRange["Start"].loc[x]:GoToneMissRange["End"].loc[x]]
                            JoystickMissTraces['new_index'] = JoystickMissTraces.index - GoToneMissRange["Start"].loc[x]
                            JoystickMissTraces = JoystickMissTraces.set_index('new_index')
                            ax3.plot(JoystickMissTraces.index, JoystickMissTraces["DataElement0"], color='grey')
                            
                        #Plot MISS MEAN TRACE
                        for x in range(len(GoToneMissRange)):
                            MissTraceWithinWindow = JoystickTrace[GoToneMissRange["Start"].loc[x]:GoToneMissRange["End"].loc[x]]
                            MissTraceWithinWindow['new_index'] = MissTraceWithinWindow.index - GoToneMissRange["Start"].loc[x]
                            MissTraceWithinWindow['new_index'] = np.round(MissTraceWithinWindow['new_index'], decimals = 3)
                            MissTraceWithinWindow = MissTraceWithinWindow.set_index('new_index')
                            MissTraceWithinWindow = MissTraceWithinWindow['DataElement0']
                            MissTraceMean.iloc[:,x] = MissTraceWithinWindow
                        if MissTraceMean.empty:
                            pass
                        else: 
                            MissTraceMean['mean'] = MissTraceMean.mean(axis=1)
                            MissTraceMean['var'] = MissTraceMean.loc[:,MissTraceMean.columns != 'mean'].var(axis=1)
                            MissTraceVar = MissTraceMean['var'].mean()
                            textstr = 'Average Variance,' + str(MissTraceVar)
                            ax3.plot(JoystickMissTraces.index, MissTraceMean['mean'], color = 'black')
                            window['Output'].print(textstr)
                            
                        #FORMAT GRAPHS AND ADD LANDMARKS
                        ax3.axvline(x=startwindow,linestyle="--",color='red',
                                   label="ToneOnset")
                        ax3.axvline(x=startwindow+toneduration,linestyle="--",color='red',
                                   label="ToneOffset")
                        ax3.set_xticks((0, startwindow, startwindow+endwindow))
                        ax3.set_xticklabels((str(0-startwindow), '0', str(endwindow)))
                        ax3.set_xlabel('Time (sec)')
                        ax3.set_ylabel('Joystick Deflection')
                        ax3.set_ylim([int(settings['y_minimum']),int(settings['y_maximum'])])
                        #ax3.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=8,
                            #verticalalignment='top', bbox=textboxstyle)
                        figure_canvas_agg3 = FigureCanvasTkAgg(fig3, window['MissTraces'].TKCanvas)
                        figure_canvas_agg3.draw()
                        figure_canvas_agg3.get_tk_widget().pack(side='right')
                        figure_canvas_agg3
                        
                    #HIT ALIGNMENT GRAPHS
                    else:
                        #Collect Hit Onsets
                        HitTimestamps = States[States['Id'].isin(['Hit'])].Trial
                        HitTrialsOnly = States.loc[States['Trial'].isin(HitTimestamps)]
                        HitOnset = HitTrialsOnly[HitTrialsOnly['Id'].isin(['Hit'])]
                        HitOnset = HitOnset["ElapsedTime"]
                        HitOnset = np.round(HitOnset, decimals = 3)
                        HitOnset.index = range(len(HitOnset))
                        HitRange = pd.DataFrame(columns=('X','Start','End'))
                        
                        #Collect FA Onsets
                        FalseAlarmTimestamps = States[States['Id'].isin(['FalseAlarm'])].Trial
                        FalseAlarmTrialsOnly = States.loc[States['Trial'].isin(FalseAlarmTimestamps)]
                        FAOnset = FalseAlarmTrialsOnly[FalseAlarmTrialsOnly['Id'].isin(['Timeout'])]
                        FAOnset = FAOnset["ElapsedTime"]
                        FAOnset = np.round(FAOnset, decimals = 3)
                        FAOnset.index = range(len(FAOnset))
                        FARange = pd.DataFrame(columns=('X','Start','End'))
                        
                        #Read parameters
                        startwindow = float(settings['start_window'])
                        endwindow = float(settings['end_window'])
                        
                        #Collect all action onsets in overlapping time window
                        for x in range(len(HitOnset)):
                            HitRange.loc[x] = ['line' + str(x), HitOnset[x]-startwindow, HitOnset[x]+endwindow]
                        for x in range(len(FAOnset)):
                            FARange.loc[x] = ['line' + str(x), FAOnset[x]-startwindow, FAOnset[x]+endwindow]
                        if HitRange.empty:
                            pass
                        else:
                            HitRange=np.round(HitRange, decimals=3)
                        if FARange.empty:
                            pass
                        else:
                            FARange=np.round(FARange, decimals=3)
                        
                        #Format Joystick Data
                        JoystickTrace = Joystick[Joystick['Command'] == 44]
                        col_list = list(JoystickTrace)
                        col_list[0], col_list[1], col_list[2], col_list[3] = col_list[0], col_list[2], col_list[1], col_list[3]
                        JoystickTrace.columns = col_list
                        JoystickTrace = JoystickTrace.set_index('Timestamp')
                        
                        #CREATE MEAN DATAFRAME
                        HitTraceMean = pd.DataFrame(index = np.arange(0,startwindow+endwindow+0.001,0.001), columns=np.arange(len(HitRange)))
                        
                        #Clear existing plots
                        if 'figure_canvas_agg' in locals() or 'figure_canvas_agg2' in locals():
                            if figure_canvas_agg or figure_canvas_agg2 or figure_canvas_agg3:
                                figure_canvas_agg.get_tk_widget().forget()
                                figure_canvas_agg2.get_tk_widget().forget()
                                plt.close('all')
                                ax.cla()
                        if 'figure_canvas_agg3' in locals():
                            if figure_canvas_agg3:
                                figure_canvas_agg3.get_tk_widget().forget()
                                plt.close('all')
                                ax.cla()
                                del figure_canvas_agg3
                        
                        #Plot Hit Traces
                        fig = matplotlib.figure.Figure(figsize=(8, 4), dpi=100)
                        fig2 = matplotlib.figure.Figure(figsize=(8, 4), dpi=100)
                        ax = fig.add_subplot(111)
                        for x in range(len(HitRange)):
                            JoystickHitTraces = JoystickTrace[HitRange["Start"].loc[x]:HitRange["End"].loc[x]]
                            JoystickHitTraces['new_index'] = JoystickHitTraces.index - HitRange["Start"].loc[x]
                            JoystickHitTraces = JoystickHitTraces.set_index('new_index')
                            ax.plot(JoystickHitTraces.index, JoystickHitTraces["DataElement0"], color = 'grey')
                        
                        #Plot MEAN TRACE
                        for x in range(len(HitRange)):
                            TraceWithinWindow = JoystickTrace[HitRange["Start"].loc[x]:HitRange["End"].loc[x]]
                            TraceWithinWindow['new_index'] = TraceWithinWindow.index - HitRange["Start"].loc[x]
                            TraceWithinWindow['new_index'] = np.round(TraceWithinWindow['new_index'], decimals = 3)
                            TraceWithinWindow = TraceWithinWindow.set_index('new_index')
                            TraceWithinWindow = TraceWithinWindow['DataElement0']
                            HitTraceMean.iloc[:,x] = TraceWithinWindow
                        if HitTraceMean.empty:
                            pass
                        else: 
                            HitTraceMean['mean'] = HitTraceMean.mean(axis=1)
                            HitTraceMean['var'] = HitTraceMean.loc[:,HitTraceMean.columns != 'mean'].var(axis=1)
                            HitTraceVar = HitTraceMean['var'].mean()
                            textstr = 'Average Variance,' + str(HitTraceVar)
                            ax.plot(JoystickHitTraces.index, HitTraceMean['mean'], color = 'black')
                            window['Output'].print(textstr)
                        
                        #FORMAT GRAPHS
                        ax.axvline(x=startwindow,linestyle="--",color='red',
                                   label="Hit")
                        ax.set_xticks((0, startwindow, startwindow+endwindow))
                        ax.set_xticklabels((str(0-startwindow), '0', str(endwindow)))
                        ax.set_xlabel('Time (sec)')
                        ax.set_ylabel('Joystick Deflection')
                        ax.set_ylim([int(settings['y_minimum']),int(settings['y_maximum'])])
                        #textboxstyle = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
                        #ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=8,
                            #verticalalignment='top', bbox=textboxstyle)
                        figure_canvas_agg = FigureCanvasTkAgg(fig, window['HitTraces'].TKCanvas)
                        figure_canvas_agg.draw()
                        figure_canvas_agg.get_tk_widget().pack(side='left')
                        figure_canvas_agg
                        
                        #Plot False Alarm Traces
                        ax2 = fig2.add_subplot(111)
                        for x in range(len(FARange)):
                            JoystickFATraces = JoystickTrace[FARange["Start"].loc[x]:FARange["End"].loc[x]]
                            JoystickFATraces['new_index'] = JoystickFATraces.index - FARange["Start"].loc[x]
                            JoystickFATraces = JoystickFATraces.set_index('new_index')
                            ax2.plot(JoystickFATraces.index, JoystickFATraces["DataElement0"], color='grey')
                        figure_canvas_agg2 = FigureCanvasTkAgg(fig2, window['FATraces'].TKCanvas)
                        figure_canvas_agg2.draw()
                        figure_canvas_agg2.get_tk_widget().pack(side='right')
                        figure_canvas_agg2
                        ax2.axvline(x=startwindow,linestyle="--",color='red',
                                   label="False Alarm")
                        ax2.set_xticks((0, startwindow, startwindow+endwindow))
                        ax2.set_xticklabels((str(0-startwindow), '0', str(endwindow)))
                        ax2.set_xlabel('Time (sec)')
                        ax2.set_ylabel('Joystick Deflection')
                        
                else:
                    sg.popup('Please upload both files')
            else:
                sg.popup('Please upload both files')
        
        
        if event == 'Splice Dataset':
           if 'validfile1' in locals():
                if validfile1 == True:
                    event, values = create_data_splicer_window().read(close=True)
                    if event == 'Save':
                        window.close()
                        window = None
                        if int(values['StartSplice']) > int(values['EndSplice']):
                            sg.popup('Invalid splice limits chosen')
                        else:
                            if values['StartSplice'] in States['Trial'] and values['EndSplice'] in States['Trial']:
                                States = States[(values['StartSplice'] <= States['Trial']) & (States['Trial'] <= values['EndSplice'])]
                            else:
                                sg.popup('Invalid splice limits chosen')
                else:
                     sg.popup('Please upload a StateTransitions file') 
           else:
                sg.popup('Please upload a StateTransitions file')
        else:
            print(event, values)
        
        
        #OUTPUT METADATA TO WINDOW
        if event == 'MouseMetadata':
            window['Output'].print('Mouse Name,' + str(metadata['mouse_name'])) 
            window['Output'].print('Mouse Gender,' + str(metadata['mouse_gender']))
            window['Output'].print('Mouse Genotype,' + str(metadata['mouse_genotype']))
            window['Output'].print('Training Start Date,' + str(metadata['start_date']))
            window['Output'].print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        
        
        #OUTPUT TRIAL PARAMETERS TO WINDOW
        if event == 'TrialMetadata':
            window['Output'].print('Training Day,' + str(metadata['training_day'])) 
            window['Output'].print('Training Phase,' + str(metadata['training_phase']))
            window['Output'].print('Joystick Threshold,' + str(metadata['joystick_threshold']))
            window['Output'].print('ITI Threshold,' + str(metadata['iti_threshold']))
            window['Output'].print('ITI Duration,' + str(metadata['iti_parameter']))
            window['Output'].print('ITI Penalty,' + str(metadata['iti_penaltyparameter']))
            window['Output'].print('Pull Threshold,' + str(metadata['pull_thresholdparameter']))
            window['Output'].print('Pull Penalty,' + str(metadata['pull_penaltyparameter']))

        #SAVE CURRENT OUTPUT
        if event == 'SAVE_OUTPUT':
            if ',' in values['Output']:
                SavedOutput = values['Output']
            else:
                sg.popup('Output window not formatted correctly.')
        
        
        #LOAD PREVIOUS OUTPUT
        if event == 'LOAD_OUTPUT':
            if 'SavedOutput' in locals():
                window['Output'].print(SavedOutput)
        
        
        #SAVE MOUSE LOG FILE
        if event == 'Save Mouse Log File':
            if 'SavedOutput' in locals():
                data_string = str(SavedOutput)
                data_string = io.StringIO(data_string)
                test = pd.read_csv(data_string, sep=",")
                mousefiledestination = sg.PopupGetFolder('Enter directory to save file to.',title = 'Save to Directory')
                if mousefiledestination == None or mousefiledestination == "":
                    sg.popup('No path entered')
                else:
                    if os.path.exists(mousefiledestination):
                        test.to_csv(str(mousefiledestination) +'/mouse_log'+ str(metadata['mousefilename'])+'.csv',index=False)
                    else:
                        sg.popup('Not a valid path')
            else:
                sg.popup('Please select Save Output before saving')
        
        #SAVE FIGURES
        if event == 'Save Plots':
            mouseplotdestination = sg.PopupGetFolder('Enter directory to save plots to.',title = 'Save to Directory')
            if mouseplotdestination == None or mouseplotdestination == "":
                sg.popup('No path entered')
            else:
                if os.path.exists(mouseplotdestination):
                    if 'figure_canvas_agg' in locals() or 'figure_canvas_agg2' in locals():
                        if figure_canvas_agg or figure_canvas_agg2:
                            fig.savefig(str(mouseplotdestination) +'/hit_trace'+ str(metadata['mousefilename'])+'.png')
                            fig.savefig(str(mouseplotdestination) +'/hit_trace'+ str(metadata['mousefilename'])+'.eps', format='eps', dpi=1200)
                            fig.savefig(str(mouseplotdestination) +'/hit_trace'+ str(metadata['mousefilename'])+'.svg', format='svg', dpi=1200)
                            fig2.savefig(str(mouseplotdestination) +'/falsealarm_trace'+ str(metadata['mousefilename'])+'.png')
                    if 'figure_canvas_agg3' in locals():
                        if figure_canvas_agg3:
                            fig3.savefig(str(mouseplotdestination) +'/miss_trace'+ str(metadata['mousefilename'])+'.png')
                    else:
                        sg.popup('No plots found')
                else:
                    sg.popup('Not a valid path')
        
        
        #VISUALIZER SETTINGS DROPDOWN
        if event == 'Graphic Settings':
            event, values = create_settings_window(settings).read(close=True)
            if event == 'Save':
                window.close()
                window = None
                save_settings(SETTINGS_FILE, settings, values)  
        else:
            print(event, values)
        
        
        #METADATA DROPDOWN
        if event == 'Metadata Settings':
            event, values = create_metadata_window(metadata).read(close=True)
            if event == 'Save':
                window.close()
                window = None
                save_metadata(METADATA_FILE, metadata, values)    
        else:
            print(event, values)
            
            
        #ABOUT DROPDOWN
        if event == 'About...':
            sg.popup('For use in conjunction with the Modified Go NoGo Bonsai Workflow','Designed by Sahil Suresh (2021) under the Sippy Lab, NYU','Version 1.0, 13 March 2021',title = 'About') 
        else:
            print(event, values)
            
        
            
    window.close()
main()
