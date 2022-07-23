function CeleST
% Copyright (c) 2013 Rutgers
% Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
% The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
% THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

clear('global')
global filenames fileDB traceOn timingOn timings timingsLabel timingsTime plotAllOn flagRobustness fileToLog flagAutomation flagInterfaceFreeze filterSelection colFtlWell mainPnlW mainPnlH fieldsIni listVideosIdx tableVideos;

javaaddpath ("../Xerces-J-bin.2.12.2/xerces-2_12_2/xercesImpl.jar");
javaaddpath ("../Xerces-J-bin.2.12.2/xerces-2_12_2/xml-apis.jar");

% ===============
% Global flags
% ===============
traceOn = false;
timingOn = true;
plotAllOn = false;
flagRobustness = true;
logToFile = false;
flagAutomation = false;
flagInterfaceFreeze = true;
timingsLabel = {'load image', 'preprocess', 'find borders', 'compute appearance', 'compute cbl', 'store data', 'check missed regions', 'check quality', 'supersample', 'tracking', 'merging',...
    'detect overlap risk', 'track cbl', 'adjust model'};
timings = zeros(1,length(timingsLabel));
timingsTime = zeros(1,length(timingsLabel));

% ===============
% Directories
% ===============
filenames.data = fullfile(cd,'data');
filenames.log = fullfile(filenames.data, 'log');
filenames.segmentation = fullfile(filenames.data, 'segmentation');
filenames.export = fullfile(filenames.data, 'export');
filenames.file_management = fullfile(filenames.data, 'file_management');
filenames.measures = fullfile(filenames.data, 'measures');
filenames.listOfExtensions = {'bmp', 'tif', 'tiff', 'png', 'jpg'};

% ===============
% Data base fields
% ===============
fieldsIni = cell(1,24);
fieldsIni{ 1} = 'name';
fieldsIni{ 2} = 'author';
fieldsIni{ 3} = 'date';
fieldsIni{ 4} = 'gene';
fieldsIni{ 5} = 'trial';
fieldsIni{ 6} = 'age';
fieldsIni{ 7} = 'set';
fieldsIni{ 8} = 'note';
fieldsIni{ 9} = 'directory';
fieldsIni{10} = 'images';
fieldsIni{11} = 'duration';
fieldsIni{12} = 'frames_per_second';
fieldsIni{13} = 'mm_per_pixel';
fieldsIni{14} = 'well';
fieldsIni{15} = 'segmented';
fieldsIni{16} = 'worms';
fieldsIni{17} = 'measured';
fieldsIni{18} = 'format';
fieldsIni{19} = 'glareZones';
fieldsIni{20} = 'experiment';
fieldsIni{21} = 'month';
fieldsIni{22} = 'day';
fieldsIni{23} = 'year';
fieldsIni{24} = 'class';

test = [];


% -------------------
% Create the directories if need be
% -------------------
listOfDirs = fieldnames(filenames);
for directory = 1:length(listOfDirs)
    if ~iscell(filenames.(listOfDirs{directory}))
        dirname = filenames.(listOfDirs{directory});
        if ~isdir(dirname)
            test = mkdir(dirname);
            if test <= 0
                if traceOn; fprintf(fileToLog, ['  ****** Could not create directory: ', regexprep(dirname, '\\', '\\\\'), ' ******\n']); end
            end
        end
    end
end

% -------------------
% Prepare the log file if need be
% -------------------
if logToFile
    fileLogID = fullfile(filenames.log, ['logFile', date, '.txt']); %#ok<*UNRCH>
    fileToLog = fopen(fileLogID, 'a');
    if fileToLog < 1; fileToLog = 1; end
else
    fileToLog = 1;
end


% -------------------
% Check the presence of a file data base
% -------------------
fileDBFile = fullfile(filenames.file_management,'fileDB.xml');
test_db = fopen(fileDBFile);
if (test_db >= 0)
    if traceOn; fprintf(fileToLog, ['Existing file data base loaded from ', regexprep(fileDBFile, '\\', '\\\\'), '\n']); end
    fclose(test_db); % end of check
    wormFileXMLread(fileDBFile);
else
    if traceOn; fprintf(fileToLog, ['No file database found: ', regexprep(fileDBFile, '\\', '\\\\'), ' , that file will be created at the end of the program', '\n']); end
    fileDB = struct;
    for ff = 1:length(fieldsIni)
        fileDB.(fieldsIni{ff}) = [];
    end
    fileDB(1) = [];
end


% ============
% CREATE THE INTERFACE
% ============
colWell = find(strcmp('well', fieldsIni));
% ----------
% Main figure and sliders
% ----------
mainPnlW = 1680;
mainPnlH = 1050;
scrsz = get(0,'ScreenSize');
mainW = min(mainPnlW, scrsz(3) - 10);
mainH = min(mainPnlH, scrsz(4) - 100);
mainPanelPosition = [2, mainH-mainPnlH-2, mainPnlW, mainPnlH];
mainFigure = figure('Visible','off','Position',[5,40,mainW,mainH],'Name','CeleST: Check results','numbertitle','off', 'menubar', 'none', 'resizefcn', @resizeMainFigure);
mainPanel = uipanel('parent', mainFigure,'BorderType', 'none','units','pixels', 'position', mainPanelPosition);
sliderHoriz = uicontrol('parent',mainFigure,'style','slider','position',[0 0 mainW-20 20],'max', 1,'min',0, 'value',0,'callback',@setMainPanelPositionBySliders);
sliderVert = uicontrol('parent',mainFigure,'style','slider','position',[mainW-20 20 20 mainH-20],'max', max(1,-mainPanelPosition(2)),'min',0, 'value',max(1,-mainPanelPosition(2)),'callback',@setMainPanelPositionBySliders);
set(mainFigure, 'color', get(mainPanel,'backgroundcolor'));

filterH = 100;
filterW = 150;
hFilters = filterH + 20;
yFilters = mainPnlH - hFilters - 5 - 70;
uicontrol('parent',mainPanel,'style','pushbutton','string','Add one video...','position',[10 yFilters+hFilters+40 150 30],'callback',@addOneVideo);
btnEdit = uicontrol('parent',mainPanel,'style','togglebutton','string','Toggle Edit Table','position',[10 yFilters+hFilters+10 150 30],'callback',@editTable);
uicontrol('parent',mainPanel,'style','pushbutton','string','Delete videos...','position',[160 yFilters+hFilters+10 150 30],'callback',@deleteVideos);
uicontrol('parent',mainPanel,'style','pushbutton','string','Check consistency','position',[160 yFilters+hFilters+40 150 30],'callback',@checkSequences);

uicontrol('parent',mainPanel,'style','pushbutton','string','1. Process videos...','position',[500 yFilters+hFilters+10 170 60],'callback',@processVideo, 'enable', 'on');
uicontrol('parent',mainPanel,'style','pushbutton','string','2. Compute measures...','position',[700 yFilters+hFilters+10 170 60],'callback',@checkResults, 'enable', 'on');
uicontrol('parent',mainPanel,'style','pushbutton','string','3. Display results...','position',[900 yFilters+hFilters+10 170 60],'callback',@showMeasures);
uicontrol('parent',mainPanel,'style','pushbutton','string','Quit','position',[1100 yFilters+hFilters+10 170 60],'callback',@closeWindow);


% ----------
% Filters
% ----------
pnlFilters = uipanel('parent', mainPanel,'BorderType', 'none','units','pixels', 'position', [1 yFilters mainPnlW hFilters]);
listFilters = fieldnames(fileDB);
idxtmp = 1;
while idxtmp <= length(listFilters)
    if strcmp(listFilters{idxtmp},'name') || strcmp(listFilters{idxtmp},'directory') || strcmp(listFilters{idxtmp},'format')...
            || strcmp(listFilters{idxtmp},'frames_per_second') || strcmp(listFilters{idxtmp},'mm_per_pixel') || strcmp(listFilters{idxtmp},'set')...
            || strcmp(listFilters{idxtmp},'duration') || strcmp(listFilters{idxtmp},'images') || strcmp(listFilters{idxtmp},'glareZones')...
            || strcmp(listFilters{idxtmp},'note') || strcmp(listFilters{idxtmp},'worms') || strcmp(listFilters{idxtmp},'well')...
            || strcmp(listFilters{idxtmp},'month') || strcmp(listFilters{idxtmp},'day') || strcmp(listFilters{idxtmp},'year')
        listFilters(idxtmp) =[];
    else
        idxtmp = idxtmp + 1;
    end
end
for idxtmp = 0:length(listFilters)-1
    uicontrol('parent',pnlFilters,'style','text','string',listFilters{idxtmp+1},'position',[idxtmp*filterW filterH filterW 20])
    flt.(listFilters{idxtmp+1}) = uicontrol('parent',pnlFilters,'style','listbox','String',{''},'max',2,'min',0,'position',[idxtmp*filterW 0 filterW filterH],'callback',@setFilteredList);
end
colFtlWell = find(strcmp('well', listFilters));

% ----------
% List of videos
% ----------
editable = [true(1,12), false(1,6)];
tableVideos = uitable('parent',mainPanel,'position',[0 30 mainPanelPosition(3)-330 yFilters-30],'rearrangeablecolumns','on','columneditable',false,'CellEditCallback', @tableEdit,'ColumnWidth','auto');
listVideosIdx = [];
populateFilters
set(mainFigure,'visible','on')
pause(0.1)
% ------------
% Waiting for closure
% ------------
waitfor(mainFigure,'BeingDeleted','on');

% -------------------
% At the end of the program, save the database
% -------------------
if ~isempty(fileDB)
    if traceOn; fprintf(fileToLog, ['Saving sequences database file', '\n']); end
    wormFileXMLwrite(fileDBFile);
end
if fileToLog > 1; fclose(fileToLog); end

% ===============
% END OF PROGRAM
% ===============



% ******************************************
% ******************************************
% **                                      **
% **           SUBFUNCTIONS               **
% **                                      **
% ******************************************
% ******************************************

    function closeWindow(hObject,eventdata) %#ok<INUSD>
        set(mainFigure,'Visible','off');
        delete(mainFigure);
    end

    function processVideo(hObject,eventdata) %#ok<INUSD>
        set(mainFigure,'Visible','off');
        CSTProcessVideos
        set(mainFigure,'Visible','on');
        checkSequences
        populateFilters
    end

    function checkResults(hObject,eventdata) %#ok<INUSD>
        set(mainFigure,'Visible','off');
        CSTCheckResults
        set(mainFigure,'Visible','on');
        checkSequences
        populateFilters
    end

    function showMeasures(hObject,eventdata) %#ok<INUSD>
        set(mainFigure,'Visible','off');
        CSTShowMeasures
        set(mainFigure,'Visible','on');
        checkSequences
        populateFilters
    end

    function deleteVideos(hObject,eventdata) %#ok<INUSD>
        tmpData = get(tableVideos,'data');
        listNames = tmpData(:,1);
        [selection,ok] = listdlg('ListString',listNames, 'name', 'CeleST: delete videos','promptstring', 'Videos to remove from the database:',...
            'okstring','Remove', 'listsize',[400 300]);
        if ok == 1
            fileDB(listVideosIdx(selection)) = [];
            fields = fieldnames(flt);
            for field = 1:length(fields)
                set(flt.(fields{field}),'value',1)
            end
        end
        populateFilters
    end

    function tableEdit(hObject,eventdata) %#ok<INUSL>
        if ~isempty(eventdata.NewData) && (~isnumeric(eventdata.NewData) || ~isnan(eventdata.NewData))
            fileDB(listVideosIdx(eventdata.Indices(1))).(fieldsIni{eventdata.Indices(2)}) = eventdata.NewData;
            populateFilters
        else
            tmpData = get(tableVideos,'data');
            tmpData{eventdata.Indices(1),eventdata.Indices(2)} = fileDB(listVideosIdx(eventdata.Indices(1))).(fieldsIni{eventdata.Indices(2)});
            set(tableVideos, 'data', tmpData);
        end
    end

    function editTable(hObject,eventdata) %#ok<INUSD>
        if get(btnEdit,'value') == 1
            set(tableVideos, 'columneditable',editable);
        else
            set(tableVideos, 'columneditable',false(1,length(fieldsIni)));
            checkSequences
            populateFilters
        end
    end


% ============
% GET ALL THE DISTINCT VALUES TO DISPLAY IN EVERY FILTER LIST
% ============
    function populateFilters
        listToShow = 1:length(fileDB);
        fields = fieldnames(flt);
        for field = 1:length(fields)
            setappdata(flt.(fields{field}),'field',fields{field});
            result = {};
            flagWell = strcmp('well',fields{field});
            for vid = listToShow
                if flagWell
                    value = num2str(~isempty(fileDB(vid).(fields{field})));
                elseif ~ischar(fileDB(vid).(fields{field}))
                    value = num2str(fileDB(vid).(fields{field}));
                else
                    value = fileDB(vid).(fields{field});
                end
                cand = length(result);
                while (cand >= 1) && ~strcmpi(value,result{cand})
                    cand = cand - 1;
                end
                if cand < 1
                    result{end+1} = value; %#ok<AGROW>
                end
            end
            result = [['All (',num2str(length(result)) ,' values)'], sort(result)];
            set(flt.(fields{field}),'string',result);
        end

        for field = 1:length(fields)
            if ~isfield(filterSelection, fields{field})
                filterSelection.(fields{field}) = 1;
            end
            set(flt.(fields{field}),'value', filterSelection.(fields{field}));
        end
        setFilteredList
    end

% ============
% BUILD THE LIST OF VIDEOS TO SHOW, BASED ON THE SELECTED FILTERS
% ============
    function setFilteredList(hObject,eventdata) %#ok<INUSD>
        fieldsToHideInTable = {'glareZones', 'format'};
        totToHide = length(fieldsToHideInTable);
        namesToShow = fieldnames(fileDB);
        field = 1;
        while field <= length(namesToShow)
            flagWasRemoved = false;
            for ffToHide = 1:totToHide
                if strcmp(namesToShow{field}, fieldsToHideInTable{ffToHide})
                    namesToShow(field) = [];
                    flagWasRemoved = true;
                    break;
                end
            end
            if ~flagWasRemoved
                field = field + 1;
            end
        end
        set(tableVideos,'columnname',namesToShow);
        if ~isempty(fileDB)
            types = cell(1,length(namesToShow));
            for it = 1:length(namesToShow)
                test = fileDB(1).(namesToShow{it});
                if islogical(test)
                    types{it} = 'logical';
                elseif isnumeric(test)
                    types{it} = 'numeric';
                else
                    types{it} = 'char';
                end
            end
            types{colWell} = 'logical';
            set(tableVideos,'columnformat',types)
        end
        result = cell(length(fileDB),length(namesToShow));
        currentVal = 0;
        listVideosIdx = zeros(1,length(fileDB));
        fields = fieldnames(flt);

        for field = 1:length(fields)
            filterSelection.(fields{field}) = get(flt.(fields{field}),'value');
        end

        for vv = 1:length(fileDB)
            flagKeep = true;
            for field = 1:length(fields)
                if (field == colFtlWell)
                    value = num2str(~isempty(fileDB(vv).(fields{field})));
                elseif ~ischar(fileDB(vv).(fields{field}))
                    value = num2str(fileDB(vv).(fields{field}));
                else
                    value = fileDB(vv).(fields{field});
                end
                options = get(flt.(fields{field}),'string');
                selIdx = get(flt.(fields{field}),'value');
                if length(selIdx) >= 1 && selIdx(1) == 1
                    continue;
                end
                try
                    selection = options(selIdx);
                catch %#ok<CTCH>
                    selection = options(1);
                end
                cand = 1;
                while (cand <= length(selection)) && ~strcmpi(value, selection{cand})
                    cand = cand + 1;
                end
                if cand > length(selection)
                    flagKeep = false;
                    break
                end
            end
            if flagKeep
                currentVal = currentVal + 1;
                tmp = fileDB(vv);
                for ffToHide = 1:totToHide
                    if isfield(tmp, fieldsToHideInTable{ffToHide})
                        tmp = rmfield(tmp, fieldsToHideInTable{ffToHide});
                    end
                end
                result(currentVal,:) = (struct2cell(tmp))';
                result{currentVal,colWell} = ~isempty(result{currentVal,colWell});
                listVideosIdx(currentVal) = vv;
            end
        end
        set(tableVideos,'data',result(1:currentVal,:));
        listVideosIdx = listVideosIdx(1:currentVal);
    end


% ============
% DISPLAY THE AXIS AND THE SLIDER
% ============

% ------------
% Set the position of the main panel based on the sliders values
% ------------
    function setMainPanelPositionBySliders(hObject,eventdata) %#ok<INUSD>
        newPos = get(mainPanel,'position');
        newPos(1) = 5 - get(sliderHoriz,'value');
        newPos(2) = -5 - get(sliderVert,'value');
        set(mainPanel,'position',newPos);
    end

% ------------
% Update the sliders positions when the main figure is resized
% ------------
    function resizeMainFigure(hObject,eventdata) %#ok<INUSD>
        % -------
        % Update the size and position of the sliders
        % -------
        newPosition = get(mainFigure,'position');
        set(sliderHoriz, 'position',[0 0 newPosition(3)-20 20]);
        set(sliderVert, 'position',[newPosition(3)-20 20 20 newPosition(4)-20]);
        % -------
        % Check the horizontal slider
        % -------
        if newPosition(3) < mainPanelPosition(3)
            deltaH = round(mainPanelPosition(3) - newPosition(3));
            newValue = min(deltaH,get(sliderHoriz,'value'));
            set(sliderHoriz, 'enable', 'on', 'min',0,'max',deltaH,'value',newValue);
        else
            set(sliderHoriz, 'enable', 'off','min',0,'max',1,'value',0);
        end
        % -------
        % Check the vertical slider
        % -------
        if newPosition(4) < mainPanelPosition(4)
            deltaV = round(mainPanelPosition(4) - newPosition(4));
            newValue = min(deltaV,get(sliderVert,'value'));
            set(sliderVert, 'enable', 'on', 'min',0,'max',deltaV,'value',newValue);
        else
            set(sliderVert, 'enable', 'off','min',0,'max',1,'value',0);
        end
        setMainPanelPositionBySliders
    end

% ------------
% Check the flags for the videos
% ------------
    function checkSequences(hObject, event) %#ok<INUSD>
        h = waitbar(0,'Checking the consistency of the data...');
        ensureUniqueNames
        nb = length(fileDB);
        for seq = 1:nb
            if floor(seq/10) == seq/10
                waitbar(seq/nb,h);
            end
            % ------------
            % Check for segmented worms
            % ------------
            test_segm = fopen(fullfile(filenames.segmentation,['wormSegm_',fileDB(seq).name,'.txt']));
            fileDB(seq).segmented = (test_segm >= 0);
            if fileDB(seq).segmented; fclose(test_segm); end
            % ------------
            % Check for measures
            % ------------
            test_meas = fopen(fullfile(filenames.measures,['wormMeas_',fileDB(seq).name,'.txt']));
            fileDB(seq).measured = (test_meas >= 0);
            if fileDB(seq).measured; fclose(test_meas); end
            % ------------
            % Check for images
            % ------------
            fileDB(seq).images = length(dir(fullfile(fileDB(seq).directory,['*.',fileDB(seq).format])));
            if fileDB(seq).images > 0 && fileDB(seq).duration > 0
                fileDB(seq).frames_per_second = fileDB(seq).images / fileDB(seq).duration;
            end
        end
        close(h)
    end

% ------------
% Check that names are unique, and modify them if necessary
% ------------
    function ensureUniqueNames
        for entry = 2:length(fileDB)
            entryName = fileDB(entry).name;
            newName = entryName;
            count = 1;
            for before = 1:(entry-1)
                if strcmp(newName, fileDB(before).name)
                    newName = [entryName, '_', num2str(count)];
                    count = count + 1;
                end
            end
            if ~strcmp(newName, entryName)
                if traceOn; fprintf(fileToLog, ['  changing name ', entryName, ' -> ', newName, '\n']); end
                fileDB(entry).name = newName;
            end
        end
    end

    function addOneVideo(hObject,eventdata) %#ok<INUSD>
        flagOK = false;
        figureAdd = figure('Visible','on','Position',[50,100,440,500],'Name','CeleST: add a video', 'numbertitle','off','menubar','none');
        set(figureAdd, 'color', get(mainPanel,'backgroundcolor'));
        uicontrol('parent', figureAdd, 'style','pushbutton', 'string', 'Add new video', 'position', [20,0,120,30],'callback',@addOK);
        uicontrol('parent', figureAdd, 'style','pushbutton', 'string', 'Cancel', 'position', [200,0,80,30],'callback',@addCancel );
        for tmpFF = [1:8,10,11]
            uicontrol('parent', figureAdd, 'style', 'text', 'string', fieldsIni{tmpFF}, 'position', [0, 500-20*tmpFF, 120, 20]);
            tmpfield.(fieldsIni{tmpFF}) = uicontrol('parent', figureAdd, 'style', 'edit', 'string', '', 'position', [140, 500-20*tmpFF, 180, 20]);
        end
        uicontrol('parent',figureAdd,'style','pushbutton', 'string', 'Browse...', 'position', [320, 500-20*8, 80,20],'callback',@addBrowse);
        for tmpFF = [9,12:20]
            uicontrol('parent', figureAdd, 'style', 'text', 'string', fieldsIni{tmpFF}, 'position', [0, 500-20*tmpFF, 120, 20]);
            tmpfield.(fieldsIni{tmpFF}) = uicontrol('parent', figureAdd, 'style', 'text', 'string', '', 'position', [140, 500-20*tmpFF, 180, 20]);
        end
        set(tmpfield.directory,'callback',@addCheckDir);
        %waitfor(figureAdd,'BeingDeleted','on');
        if flagOK
            ensureUniqueNames
            populateFilters
        end
        function addBrowse(hObject,eventdata) %#ok<INUSD>
            newDir = get(tmpfield.directory, 'string');
            if isempty(newDir) && length(fileDB) >= 1
                newDir = fileDB(end).directory;
            end
            newDir = uigetdir(newDir);
            if newDir ~= 0
                [pathstr, name] = fileparts(newDir); %#ok<ASGLU>
                set(tmpfield.name,'string',name);
                set(tmpfield.directory, 'string', newDir);
                addCheckDir;
            end
        end
        function addCheckDir(hObject,eventdata) %#ok<INUSD>
            tmpIdx = 1;
            tmpNbImages = 0;
            while (tmpIdx <= length(filenames.listOfExtensions)) && (tmpNbImages <= 0)
                tmpNbImages = length(dir(fullfile(get(tmpfield.directory,'string'),['*.',filenames.listOfExtensions{tmpIdx}])));
                if tmpNbImages <= 0
                    tmpIdx = tmpIdx + 1;
                end
            end
            if tmpNbImages > 0
                set(tmpfield.images, 'string', int2str(tmpNbImages));
                set(tmpfield.format, 'string', filenames.listOfExtensions{tmpIdx});
                set(tmpfield.duration,'string', '30')
            else
                set(tmpfield.images, 'string', '0');
                set(tmpfield.format, 'string', 'no images');
            end
        end
        function addOK(hObject,eventdata) %#ok<INUSD>
            % tmpNewVideo = struct(fileDB);
            % tmpNewVideo(1).name = get(tmpfield.name,'string');
            % tmpNewVideo(1).date = get(tmpfield.date,'string');
            % tmpNewVideo(1).gene = get(tmpfield.gene,'string');
            % tmpNewVideo(1).age = str2double(get(tmpfield.age,'string'));
            % tmpNewVideo(1).set = str2double(get(tmpfield.set,'string'));
            % tmpNewVideo(1).trial = str2double(get(tmpfield.trial,'string'));
            % tmpNewVideo(1).note = get(tmpfield.note,'string');
            % tmpNewVideo(1).author = get(tmpfield.author,'string');
            % tmpNewVideo(1).directory = get(tmpfield.directory,'string');
            % tmpNewVideo(1).images = str2double(get(tmpfield.images,'string'));
            % tmpNewVideo(1).duration = str2double(get(tmpfield.duration,'string'));
            % tmpNewVideo(1).frames_per_second = tmpNewVideo(1).images / tmpNewVideo(1).duration;
            % tmpNewVideo(1).mm_per_pixel = 1;
            % tmpNewVideo(1).well = [];
            % tmpNewVideo(1).segmented = false;
            % tmpNewVideo(1).worms = 0;
            % tmpNewVideo(1).measured = false;
            % tmpNewVideo(1).format = get(tmpfield.format,'string');
            % tmpNewVideo(1).glareZones = cell(1,0);
            tmpNewVideo = struct(fileDB);
            fileDB(end + 1).name = get(tmpfield.name,'string');
            fileDB(end).date = get(tmpfield.date,'string');
            fileDB(end).gene = get(tmpfield.gene,'string');
            fileDB(end).age = str2double(get(tmpfield.age,'string'));
            fileDB(end).set = str2double(get(tmpfield.set,'string'));
            fileDB(end).trial = str2double(get(tmpfield.trial,'string'));
            fileDB(end).note = get(tmpfield.note,'string');
            fileDB(end).author = get(tmpfield.author,'string');
            fileDB(end).directory = get(tmpfield.directory,'string');
            fileDB(end).images = str2double(get(tmpfield.images,'string'));
            fileDB(end).duration = str2double(get(tmpfield.duration,'string'));
            fileDB(end).frames_per_second = tmpNewVideo(1).images / tmpNewVideo(1).duration;
            fileDB(end).mm_per_pixel = 1;
            fileDB(end).well = [];
            fileDB(end).segmented = false;
            fileDB(end).worms = 0;
            fileDB(end).measured = false;
            fileDB(end).format = get(tmpfield.format,'string');
            fileDB(end).glareZones = cell(1,0);
            % fprintf(1, ['This is then end: ', fileDB(end).name , '\n']);
            % fprintf(1, ['This is then end: ', fileDB(2).name , '\n']);

            flagOK = true;
            close(figureAdd);
        end
        function addCancel(hObject,eventdata) %#ok<INUSD>
            close(figureAdd);
        end
    end

    function wormFileXMLread(xmlFileName)
        xDoc = xmlread(xmlFileName);
        % ---------
        % get the list of all the sequences
        % ---------
        seqItems = xDoc.getElementsByTagName('sequence');
        h = waitbar(0,'Loading the database...');
        nb = seqItems.getLength;
        for seq = 1:nb
            seqNode = seqItems.item(seq-1);
            % ---------
            % read the sequence index, maybe different from its order on the list
            % ---------
            idxVideo = str2double(seqNode.getAttribute('number'));
            % ---------
            % get the list of all features stored
            % ---------
            featItems = seqNode.getElementsByTagName('feature');
            if floor(seq/10) == seq/10
                waitbar((seq-1)/nb,h)
            end
            for count = 1:featItems.getLength
                currentNode = featItems.item(count-1);
                featName = char(currentNode.getAttribute('name'));
                currentClass = char(currentNode.getAttribute('class'));
                switch currentClass
                    case 'logical'
                        currentVariable = logical(str2num(currentNode.getTextContent)); %#ok<ST2NM>
                    case 'char'
                        currentVariable = char(currentNode.getTextContent);
                    case 'double'
                        currentVariable = str2num(currentNode.getTextContent) / 10^str2double(currentNode.getAttribute('precision')); %#ok<ST2NM>
                    otherwise
                end

                if ~strcmp('glareZones',featName)
                    fileDB(idxVideo).(featName) = currentVariable;
                else
                    if idxVideo > length(fileDB) || ~isfield(fileDB(idxVideo), featName) || ~iscell(fileDB(idxVideo).(featName))
                        fileDB(idxVideo).(featName) = cell(1,0);
                    end
                    fileDB(idxVideo).(featName){end+1} = currentVariable;
                end
            end
        end
        close(h)
    end

    function wormFileXMLwrite(xmlFileName,precision)
        % ---------
        % Create an XML root node
        % ---------
        docNode = javaObject ("org.apache.xerces.dom.DocumentImpl");
        %docNode = com.mathworks.xml.XMLUtils.createDocument('sequences_database');
        docRootNode = docNode.createElement("sequences_database");
        docNode.appendChild (docRootNode);

        if nargin < 2; precision = 4; end
        factor = 10^precision;
        h = waitbar(0,'Saving the database...');
        nb = length(fileDB);
        for seq=1:nb
            if floor(seq/10) == seq/10
                waitbar((seq-1)/nb,h)
            end
            % ---------
            % create a new node for the sequence
            % ---------
            seqNode = docNode.createElement('sequence');
            seqNode.setAttribute('number', int2str(seq));

            % ---------
            % retrieve the labels for the elements stored
            % ---------
            labels = fieldnames(fileDB(seq));
            for lbl = 1:length(labels)
                if strcmp(labels{lbl}, 'glareZones')
                    for item = 1:length(fileDB(seq).(labels{lbl}))
                        currentValue = fileDB(seq).(labels{lbl}){item};
                        currentNode = docNode.createElement('feature');
                        currentNode.setAttribute('cell', 'true');
                        %writeNode
                        currentNode.setAttribute('name', "test");
                        currentClass = class(currentValue);
                        currentNode.setAttribute('class', currentClass);
                        switch currentClass
                            case 'logical'
                                currentNode.setTextContent(mat2str(int8(currentValue)));
                            case 'char'
                                currentNode.setTextContent(currentValue);
                            case 'double'
                                currentNode.setAttribute('precision', num2str(precision));
                                currentNode.setTextContent(mat2str(round(factor * currentValue)));
                            otherwise
                        end
                        seqNode.appendChild(currentNode);
                end
                else
                    currentValue = fileDB(seq).(labels{lbl});
                    currentNode = docNode.createElement('feature');
                    currentNode.setAttribute('name', labels{lbl});
                    currentClass = class(currentValue);
                    currentNode.setAttribute('class', currentClass);
                    switch currentClass
                        case 'logical'
                            currentNode.setTextContent(mat2str(int8(currentValue)));
                        case 'char'
                            currentNode.setTextContent(currentValue);
                        case 'double'
                            currentNode.setAttribute('precision', num2str(precision));
                            currentNode.setTextContent(mat2str(round(factor * currentValue)));
                        otherwise
                    end
                    seqNode.appendChild(currentNode);
                            %writeNode
                end
            end
            % ---------
            % add the sequence node to the root
            % ---------
            docRootNode.appendChild(seqNode);
        end
        % ---------
        % Save the sample XML document.
        % ---------
        xmlwrite (xmlFileName,docNode);
        close(h)


        function writeNode
            % ---------
            % create a new node for the feature
            % ---------
            currentNode.setAttribute('name', labels(lbl));
            currentClass = class(currentValue);
            currentNode.setAttribute('class', currentClass);
            switch currentClass
                case 'logical'
                    currentNode.setTextContent(mat2str(int8(currentValue)));
                case 'char'
                    currentNode.setTextContent(currentValue);
                case 'double'
                    currentNode.setAttribute('precision', num2str(precision));
                    currentNode.setTextContent(mat2str(round(factor * currentValue)));
                otherwise
            end
            seqNode.appendChild(currentNode);
        end

    end

end
