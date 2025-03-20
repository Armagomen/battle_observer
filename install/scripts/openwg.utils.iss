// SPDX-License-Identifier: MIT
// Copyright (c) 2017-2024 OpenWG.Utils Contributors

// directory with OpenWG.Utils installation files, relative to the main .iss file
#ifndef OPENWGUTILS_DIR_SRC
#define OPENWGUTILS_DIR_SRC "."
#endif

// directory with OpenWG.Utils uninstallation files, relative to the application installation folder
#ifndef OPENWGUTILS_DIR_UNINST
#define OPENWGUTILS_DIR_UNINST "."
#endif

// default buffer size for path, should be between 250 .. 32767
#ifndef OPENWGUTILS_BUF_SIZE
#define OPENWGUTILS_BUF_SIZE 1024
#endif

#ifndef OPENWGUTILS_LANG_EN
#define OPENWGUTILS_LANG_EN 1
#endif

#ifndef OPENWGUTILS_LANG_RU
#define OPENWGUTILS_LANG_RU 1
#endif



[Files]
Source: "{#OPENWGUTILS_DIR_SRC}\openwg.utils.x86_32.dll"; DestName: openwg.utils.dll; Flags: ignoreversion dontcopy noencryption;
Source: "{#OPENWGUTILS_DIR_SRC}\openwg.utils.x86_32.dll"; DestDir: {app}\{#OPENWGUTILS_DIR_UNINST}; DestName: openwg.utils.dll; Flags: ignoreversion noencryption;



//
// COMMON
//

[Code]

procedure OPENWG_DllDelete();
begin
    if IsUninstaller() then
    begin
        DeleteFile(ExpandConstant('{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll'));
        RemoveDir(ExpandConstant('{app}\{#OPENWGUTILS_DIR_UNINST}'));
    end
    else begin
        DeleteFile(ExpandConstant('{tmp}\openwg.utils.dll'));
        RemoveDir(ExpandConstant('{tmp}'));
    end;
end;


procedure OPENWG_DllUnload();
begin
    if IsUninstaller() then
        UnloadDLL(ExpandConstant('{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll'))
    else
        UnloadDLL(ExpandConstant('{tmp}\openwg.utils.dll'));
end;



//
// BWXML
//

[Code]

// BWXML/UnpackW
function BWXML_UnpackW_I(PathPacked: String; PathUnpacked: String): Integer;
external 'BWXML_UnpackW@files:openwg.utils.dll cdecl setuponly';

function BWXML_UnpackW_U(PathPacked: String; PathUnpacked: String): Integer;
external 'BWXML_UnpackW@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function BWXML_UnpackW(PathPacked: String; PathUnpacked: String): Integer;
begin
    if IsUninstaller() then
        Result := BWXML_UnpackW_U(PathPacked, PathUnpacked)
    else
        Result := BWXML_UnpackW_I(PathPacked, PathUnpacked)
end;


//
// WOT
//

[Code]

// WINE/IsRunningUnder
function WINE_IsRunningUnder_I(): Boolean;
external 'WINE_IsRunningUnder@files:openwg.utils.dll cdecl setuponly';

function WINE_IsRunningUnder_U(): Boolean;
external 'WINE_IsRunningUnder@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function WINE_IsRunningUnder(): Boolean;
begin
    if IsUninstaller() then
        Result := WINE_IsRunningUnder_U()
    else
        Result := WINE_IsRunningUnder_I()
end;



//
// FS
//

[Code]

// FS/FileExists
function FS_FileExists_I(Path: String): Integer;
external 'FS_FileExistsW@files:openwg.utils.dll cdecl setuponly';

function FS_FileExists_U(Path: String): Integer;
external 'FS_FileExistsW@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function FS_FileExists(Path: String): Integer;
begin
    if IsUninstaller() then
        Result := FS_FileExists_U(Path)
    else
        Result := FS_FileExists_I(Path)
end;


// FS/FileEqual
function FS_FileEqual_I(Path1: String; Path2: String): Integer;
external 'FS_FileEqualW@files:openwg.utils.dll cdecl setuponly';

function FS_FileEqual_U(Path1: String; Path2: String): Integer;
external 'FS_FileEqualW@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function FS_FileEqual(Path1: String; Path2: String): Integer;
begin
    if IsUninstaller() then
        Result := FS_FileEqual_U(Path1, Path2)
    else
        Result := FS_FileEqual_I(Path1, Path2)
end;


// FS/Search/Close
function FS_Search_Close_I(Handle: Integer): Boolean;
external 'FS_Search_Close@files:openwg.utils.dll cdecl setuponly';

function FS_Search_Close_U(Handle: Integer): Boolean;
external 'FS_Search_Close@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function FS_Search_Close(Handle: Integer): Boolean;
begin
    if IsUninstaller() then
        Result := FS_Search_Close_U(Handle)
    else
        Result := FS_Search_Close_I(Handle)
end;


// FS/Search/GetCount
function FS_Search_GetCount_I(Handle: Integer): Integer;
external 'FS_Search_GetCount@files:openwg.utils.dll cdecl setuponly';

function FS_Search_GetCount_U(Handle: Integer): Integer;
external 'FS_Search_GetCount@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function FS_Search_GetCount(Handle: Integer): Integer;
begin
    if IsUninstaller() then
        Result := FS_Search_GetCount_U(Handle)
    else
        Result := FS_Search_GetCount_I(Handle)
end;


// FS/Search/GetPath
function FS_Search_GetPathW_I(Handle: Integer; Index: Integer; Output: String; OutputSize: Integer): Integer;
external 'FS_Search_GetPathW@files:openwg.utils.dll cdecl setuponly';

function FS_Search_GetPathW_U(Handle: Integer; Index: Integer; Output: String; OutputSize: Integer): Integer;
external 'FS_Search_GetPathW@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function FS_Search_GetPath(Handle: Integer; Index: Integer): String;
var
    Buffer: String;
begin
    SetLength(Buffer, {#OPENWGUTILS_BUF_SIZE});

    if IsUninstaller() then
        FS_Search_GetPathW_U(Handle, Index, Buffer, {#OPENWGUTILS_BUF_SIZE})
    else
        FS_Search_GetPathW_I(Handle, Index, Buffer, {#OPENWGUTILS_BUF_SIZE});

    Result := Copy(Buffer, 1, Pos(#0, Buffer)-1);
end;


// FS/Search/QueryFolder
function FS_Search_QueryFolderW_I(Regex: String; MaxDepth: Integer): Integer;
external 'FS_Search_QueryFolderW@files:openwg.utils.dll cdecl setuponly';

function FS_Search_QueryFolderW_U(Regex: String; MaxDepth: Integer): Integer;
external 'FS_Search_QueryFolderW@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function FS_Search_QueryFolder(Regex: String; MaxDepth: Integer): Integer;
begin
    if IsUninstaller() then
        Result := FS_Search_QueryFolderW_U(Regex, MaxDepth)
    else
        Result := FS_Search_QueryFolderW_I(Regex, MaxDepth)
end;


//
// IMAGE
//

[Code]

// IMAGE/BitmapAlphaPremultiply
function IMAGE_BitmapAlphaPremultiply_I(Bitmap: HBITMAP): Boolean;
external 'IMAGE_BitmapAlphaPremultiply@files:openwg.utils.dll cdecl setuponly';

function IMAGE_BitmapAlphaPremultiply_U(Bitmap: HBITMAP): Boolean;
external 'IMAGE_BitmapAlphaPremultiply@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function IMAGE_BitmapAlphaPremultiply(Bitmap: HBITMAP): Boolean;
begin
    if IsUninstaller() then
        Result := IMAGE_BitmapAlphaPremultiply_U(Bitmap)
    else
        Result := IMAGE_BitmapAlphaPremultiply_I(Bitmap)
end;



// IMAGE/BitmapBlend
function IMAGE_BitmapBlend_I(Bitmap1: HBITMAP; Bitmap2: HBITMAP; DstX: Integer; DstY: Integer): Boolean;
external 'IMAGE_BitmapBlend@files:openwg.utils.dll cdecl setuponly';

function IMAGE_BitmapBlend_U(Bitmap1: HBITMAP; Bitmap2: HBITMAP; DstX: Integer; DstY: Integer): Boolean;
external 'IMAGE_BitmapBlend@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function IMAGE_BitmapBlend(Bitmap1: HBITMAP; Bitmap2: HBITMAP; DstX: Integer; DstY: Integer): Boolean;
begin
    if IsUninstaller() then
        Result := IMAGE_BitmapBlend_U(Bitmap1, Bitmap2, DstX, DstY)
    else
        Result := IMAGE_BitmapBlend_I(Bitmap1, Bitmap2, DstX, DstY)
end;


// IMAGE/BitmapClone
function IMAGE_BitmapClone_I(Bitmap: HBITMAP): HBITMAP;
external 'IMAGE_BitmapClone@files:openwg.utils.dll cdecl setuponly';

function IMAGE_BitmapClone_U(Bitmap: HBITMAP): HBITMAP;
external 'IMAGE_BitmapClone@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function IMAGE_BitmapClone(Bitmap: HBITMAP): HBITMAP;
begin
    if IsUninstaller() then
        Result := IMAGE_BitmapClone_U(Bitmap)
    else
        Result := IMAGE_BitmapClone_I(Bitmap)
end;


// IMAGE/BitmapFree
function IMAGE_BitmapFree_I(Bitmap: HBITMAP): Boolean;
external 'IMAGE_BitmapFree@files:openwg.utils.dll cdecl setuponly';

function IMAGE_BitmapFree_U(Bitmap: HBITMAP): Boolean;
external 'IMAGE_BitmapFree@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function IMAGE_BitmapFree(Bitmap: HBITMAP): Boolean;
begin
    if IsUninstaller() then
        Result := IMAGE_BitmapFree_U(Bitmap)
    else
        Result := IMAGE_BitmapFree_I(Bitmap)
end;



// IMAGE/BitmapGetHeight
function IMAGE_BitmapGetHeight_I(Bitmap: HBITMAP): Integer;
external 'IMAGE_BitmapGetHeight@files:openwg.utils.dll cdecl setuponly';

function IMAGE_BitmapGetHeight_U(Bitmap: HBITMAP): Integer;
external 'IMAGE_BitmapGetHeight@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function IMAGE_BitmapGetHeight(Bitmap: HBITMAP): Integer;
begin
    if IsUninstaller() then
        Result := IMAGE_BitmapGetHeight_U(Bitmap)
    else
        Result := IMAGE_BitmapGetHeight_I(Bitmap)
end;



// IMAGE/BitmapGetWidth
function IMAGE_BitmapGetWidth_I(Bitmap: HBITMAP): Integer;
external 'IMAGE_BitmapGetWidth@files:openwg.utils.dll cdecl setuponly';

function IMAGE_BitmapGetWidth_U(Bitmap: HBITMAP): Integer;
external 'IMAGE_BitmapGetWidth@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function IMAGE_BitmapGetWidth(Bitmap: HBITMAP): Integer;
begin
    if IsUninstaller() then
        Result := IMAGE_BitmapGetWidth_U(Bitmap)
    else
        Result := IMAGE_BitmapGetWidth_I(Bitmap)
end;



// IMAGE/BitmapLoad
function IMAGE_BitmapLoadW_I(Filename: String): HBITMAP;
external 'IMAGE_BitmapLoadW@files:openwg.utils.dll cdecl setuponly';

function IMAGE_BitmapLoadW_U(Filename: String): HBITMAP;
external 'IMAGE_BitmapLoadW@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function IMAGE_BitmapLoad(Filename: String): HBITMAP;
begin
    if IsUninstaller() then
        Result := IMAGE_BitmapLoadW_U(Filename)
    else
        Result := IMAGE_BitmapLoadW_I(Filename)
end;



// IMAGE/IMAGE_BitmapMultiplyColor
function IMAGE_BitmapMultiplyColor_I(Bitmap: HBITMAP; ScaleR: Single; ScaleG: Single; ScaleB: Single; ScaleA: Single): HBITMAP;
external 'IMAGE_BitmapMultiplyColor@files:openwg.utils.dll cdecl setuponly';

function IMAGE_BitmapMultiplyColor_U(Bitmap: HBITMAP; ScaleR: Single; ScaleG: Single; ScaleB: Single; ScaleA: Single): HBITMAP;
external 'IMAGE_BitmapMultiplyColor@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function IMAGE_BitmapMultiplyColor(Bitmap: HBITMAP; ScaleR: Single; ScaleG: Single; ScaleB: Single; ScaleA: Single): HBITMAP;
begin
    if IsUninstaller() then
        Result := IMAGE_BitmapMultiplyColor_U(Bitmap, ScaleR, ScaleG, ScaleB, ScaleA)
    else
        Result := IMAGE_BitmapMultiplyColor_I(Bitmap, ScaleR, ScaleG, ScaleB, ScaleA)
end;



// IMAGE/BitmapResize
function IMAGE_BitmapResize_I(Bitmap: HBITMAP; Width: Integer; Height: Integer): HBITMAP;
external 'IMAGE_BitmapResize@files:openwg.utils.dll cdecl setuponly';

function IMAGE_BitmapResize_U(Bitmap: HBITMAP; Width: Integer; Height: Integer): HBITMAP;
external 'IMAGE_BitmapResize@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function IMAGE_BitmapResize(Bitmap: HBITMAP; Width: Integer; Height: Integer): HBITMAP;
begin
    if IsUninstaller() then
        Result := IMAGE_BitmapResize_U(Bitmap, Width, Height)
    else
        Result := IMAGE_BitmapResize_I(Bitmap, Width, Height)
end;



// IMAGE/BrushCreate
function IMAGE_BrushCreate_I(Bitmap: Integer): Integer;
external 'IMAGE_BrushCreate@files:openwg.utils.dll cdecl setuponly';

function IMAGE_BrushCreate_U(Bitmap: Integer): Integer;
external 'IMAGE_BrushCreate@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function IMAGE_BrushCreate(Bitmap: Integer): Integer;
begin
    if IsUninstaller() then
        Result := IMAGE_BrushCreate_U(Bitmap)
    else
        Result := IMAGE_BrushCreate_I(Bitmap)
end;



// IMAGE/BrushFree
function IMAGE_BrushFree_I(Brush: Integer): Boolean;
external 'IMAGE_BrushFree@files:openwg.utils.dll cdecl setuponly';

function IMAGE_BrushFree_U(Brush: Integer): Boolean;
external 'IMAGE_BrushFree@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function IMAGE_BrushFree(Brush: Integer): Boolean;
begin
    if IsUninstaller() then
        Result := IMAGE_BrushFree_U(Brush)
    else
        Result := IMAGE_BrushFree_I(Brush)
end;



// IMAGE/TBitmapLoad
function IMAGE_TBitmapLoad(Filename: String; Scale: Boolean; PremultiplyAlpha: Boolean): TBitmap;
var
    Handle: HBITMAP;
    HandleTemp: HBITMAP;
begin
    Handle := IMAGE_BitmapLoad(Filename);
    if Handle = 0 then
        Exit;

    if Scale then
    begin
        HandleTemp := IMAGE_BitmapResize(Handle, ScaleX(IMAGE_BitmapGetWidth(Handle)), ScaleX(IMAGE_BitmapGetHeight(Handle)));
        IMAGE_BitmapFree(Handle);
        if HandleTemp = 0 then
            Exit;
        Handle := HandleTemp;
    end;

    if PremultiplyAlpha then
        IMAGE_BitmapAlphaPremultiply(Handle);

    Result := TBitmap.Create();
    Result.Handle := Handle;
end;



// IMAGE/IMAGE_TBitmapLoadScaled
function IMAGE_TBitmapLoadScaled(Filename: String; Scale: Extended; PremultiplyAlpha: Boolean): TBitmap;
var
    Handle: HBITMAP;
    HandleTemp: HBITMAP;
begin
    Handle := IMAGE_BitmapLoad(Filename);
    if Handle = 0 then
        Exit;

    HandleTemp := IMAGE_BitmapResize(Handle, Round(IMAGE_BitmapGetWidth(Handle) * Scale), Round(IMAGE_BitmapGetHeight(Handle) * Scale));
    IMAGE_BitmapFree(Handle);
    if HandleTemp = 0 then
        Exit;
    Handle := HandleTemp;

    if PremultiplyAlpha then
        IMAGE_BitmapAlphaPremultiply(Handle);

    Result := TBitmap.Create();
    Result.Handle := Handle;
end;



// Image/TBitmapMultiplyColor
function IMAGE_TBitmapMultiplyColor(Bitmap: TBitmap; ScaleR: Single; ScaleG: Single; ScaleB: Single; ScaleA: Single): Boolean;
var
    HandleTemp: HBITMAP;
begin
    if Bitmap.Handle = 0 then
        Exit;

    HandleTemp := IMAGE_BitmapMultiplyColor(Bitmap.Handle, ScaleR, ScaleG, ScaleB, ScaleA);
    if HandleTemp = 0 then
        Exit;

    Bitmap.Handle := HandleTemp;
    Result := True;
end;



// Image/TBitmapResize
function IMAGE_TBitmapResize(Bitmap: TBitmap; Width: Integer; Height: Integer): Boolean;
var
    HandleTemp: HBITMAP;
begin
    if Bitmap.Handle = 0 then
        Exit;

    HandleTemp := IMAGE_BitmapResize(Bitmap.Handle, Width, Height);
    if HandleTemp = 0 then
        Exit;

    Bitmap.Handle := HandleTemp;
    Result := True;
end;



// IMAGE/TBitmapScale
function IMAGE_TBitmapScale(Bitmap: TBitmap; Scale: Extended): Boolean;
begin
    Result := IMAGE_TBitmapResize(Bitmap, Round(Bitmap.Width * Scale), Round(Bitmap.Height * Scale));
end;



//
// PROCESS
//

[Code]

// INNO/ComponentEntryGetName
function INNO_ComponentEntryGetNameW_I(Object: TObject; Buffer: String; BufferSize: Integer): Boolean;
external 'INNO_ComponentEntryGetNameW@files:openwg.utils.dll cdecl setuponly';

function INNO_ComponentEntryGetNameW_U(Object: TObject; Buffer: String; BufferSize: Integer): Boolean;
external 'INNO_ComponentEntryGetNameW@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function INNO_ComponentEntryGetName(Object: TObject): String;
var
    FunctionResult: Boolean;
    Buffer: String;
begin
    SetLength(Buffer, {#OPENWGUTILS_BUF_SIZE});

    if IsUninstaller() then
        FunctionResult := INNO_ComponentEntryGetNameW_U(Object, Buffer, {#OPENWGUTILS_BUF_SIZE})
    else
        FunctionResult := INNO_ComponentEntryGetNameW_I(Object, Buffer, {#OPENWGUTILS_BUF_SIZE});

    if FunctionResult then
        Result := Copy(Buffer, 1, Pos(#0, Buffer)-1);
end;


// INNO/ComponentEntryGetDescription
function INNO_ComponentEntryGetDescriptionW_I(Object: TObject; Buffer: String; BufferSize: Integer): Boolean;
external 'INNO_ComponentEntryGetDescriptionW@files:openwg.utils.dll cdecl setuponly';

function INNO_ComponentEntryGetDescriptionW_U(Object: TObject; Buffer: String; BufferSize: Integer): Boolean;
external 'INNO_ComponentEntryGetDescriptionW@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function INNO_ComponentEntryGetDescription(Object: TObject): String;
var
    FunctionResult: Boolean;
    Buffer: String;
begin
    SetLength(Buffer, {#OPENWGUTILS_BUF_SIZE});

    if IsUninstaller() then
        FunctionResult := INNO_ComponentEntryGetDescriptionW_U(Object, Buffer, {#OPENWGUTILS_BUF_SIZE})
    else
        FunctionResult := INNO_ComponentEntryGetDescriptionW_I(Object, Buffer, {#OPENWGUTILS_BUF_SIZE});

    if FunctionResult then
        Result := Copy(Buffer, 1, Pos(#0, Buffer)-1);
end;


// INNO/ComponentEntryCompareName
function INNO_ComponentEntryCompareNameW_I(str1: String; str2: String): Boolean;
external 'INNO_ComponentEntryCompareNameW@files:openwg.utils.dll cdecl setuponly';

function INNO_ComponentEntryCompareNameW_U(str1: String; str2: String): Boolean;
external 'INNO_ComponentEntryCompareNameW@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function INNO_ComponentEntryCompareName(str1: String; str2: String): Boolean;
begin
    if IsUninstaller() then
        Result := INNO_ComponentEntryCompareNameW_U(str1, str2)
    else
        Result := INNO_ComponentEntryCompareNameW_I(str1, str2);
end;


// INNO/ChecklistGetItemName
function INNO_ChecklistGetItemName(Checklist: TNewCheckListBox; Index: Integer): String;
begin
    Result := INNO_ComponentEntryGetName(Checklist.ItemObject[Index]);
end;

// INNO/ChecklistGetItemDescription
function INNO_ChecklistGetItemDescription(Checklist: TNewCheckListBox; Index: Integer): String;
begin
    Result := INNO_ComponentEntryGetDescription(Checklist.ItemObject[Index]);
end;

// INNO/ChecklistGetItemIndex
function INNO_ChecklistGetItemIndex(Checklist: TNewCheckListBox; Name: String): Integer;
var
    Index: Integer;
begin
    Result := -1;
    for Index := 0 to Checklist.Items.Count - 1 do
    begin
        if INNO_ComponentEntryCompareName(INNO_ChecklistGetItemName(Checklist, Index), Name) then
        begin
            Result := Index;
            Exit;
        end;
    end;
end;



//
// JSON
//

[Code]

// JSON/OpenFile
function JSON_OpenFileW_I(Path: String; AllowCreation: Boolean): Integer;
external 'JSON_OpenFileW@files:openwg.utils.dll cdecl setuponly';

function JSON_OpenFileW_U(Path: String; AllowCreation: Boolean): Integer;
external 'JSON_OpenFileW@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function JSON_OpenFile(Path: String; AllowCreation: Boolean): Integer;
begin
    if IsUninstaller() then
        Result := JSON_OpenFileW_U(Path, AllowCreation)
    else
        Result := JSON_OpenFileW_I(Path, AllowCreation)
end;


// JSON/OpenString
function JSON_OpenStringW_I(Text: String): Integer;
external 'JSON_OpenStringW@files:openwg.utils.dll cdecl setuponly';

function JSON_OpenStringW_U(Text: String): Integer;
external 'JSON_OpenStringW@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function JSON_OpenString(Text: String): Integer;
begin
    if IsUninstaller() then
        Result := JSON_OpenStringW_U(Text)
    else
        Result := JSON_OpenStringW_I(Text)
end;



// Json/Close
function JSON_Close_I(Handle: Integer): Boolean;
external 'JSON_Close@files:openwg.utils.dll cdecl setuponly';

function JSON_Close_U(Handle: Integer): Boolean;
external 'JSON_Close@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function JSON_Close(Handle: Integer): Boolean;
begin
    if IsUninstaller() then
        Result := JSON_Close_U(Handle)
    else
        Result := JSON_Close_I(Handle)
end;


// Json/ContainsKey
function JSON_ContainsKeyW_I(Handle: Integer; Path: String): Boolean;
external 'JSON_ContainsKeyW@files:openwg.utils.dll cdecl setuponly';

function JSON_ContainsKeyW_U(Handle: Integer; Path: String): Boolean;
external 'JSON_ContainsKeyW@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function JSON_ContainsKey(Handle: Integer; Path: String): Boolean;
begin
    if IsUninstaller() then
        Result := JSON_ContainsKeyW_U(Handle, Path)
    else
        Result := JSON_ContainsKeyW_I(Handle, Path)
end;


// Json/GetString
procedure JSON_GetStringW_I(Handle: Integer; Path: String; Output: String; OutputSize: Integer);
external 'JSON_GetStringW@files:openwg.utils.dll cdecl setuponly';

procedure JSON_GetStringW_U(Handle: Integer; Path: String; Output: String; OutputSize: Integer);
external 'JSON_GetStringW@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function JSON_GetString(Handle: Integer; Path: String): String;
var
    Buffer: String;
begin
    SetLength(Buffer, {#OPENWGUTILS_BUF_SIZE});

    if IsUninstaller() then
        JSON_GetStringW_U(Handle, Path, Buffer, {#OPENWGUTILS_BUF_SIZE})
    else
        JSON_GetStringW_I(Handle, Path, Buffer, {#OPENWGUTILS_BUF_SIZE});

    Result := Copy(Buffer, 1, Pos(#0, Buffer)-1);
end;


// Json/SetBool
function JSON_SetBoolW_I(Handle: Integer; Path: String; Value: Boolean): Boolean;
external 'JSON_SetBoolW@files:openwg.utils.dll cdecl setuponly';

function JSON_SetBoolW_U(Handle: Integer; Path: String; Value: Boolean): Boolean;
external 'JSON_SetBoolW@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function JSON_SetBool(Handle: Integer; Path: String; Value: Boolean): Boolean;
begin
    if IsUninstaller() then
        Result := JSON_SetBoolW_U(Handle, Path, Value)
    else
        Result := JSON_SetBoolW_I(Handle, Path, Value)
end;


// Json/SetDouble
function JSON_SetDoubleW_I(Handle: Integer; Path: String; Value: Double): Boolean;
external 'JSON_SetDoubleW@files:openwg.utils.dll cdecl setuponly';

function JSON_SetDoubleW_U(Handle: Integer; Path: String; Value: Double): Boolean;
external 'JSON_SetDoubleW@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function JSON_SetDouble(Handle: Integer; Path: String; Value: Double): Boolean;
begin
    if IsUninstaller() then
        Result := JSON_SetDoubleW_U(Handle, Path, Value)
    else
        Result := JSON_SetDoubleW_I(Handle, Path, Value)
end;


// Json/SetInteger
function JSON_SetIntegerW_I(Handle: Integer; Path: String; Value: Integer): Boolean;
external 'JSON_SetIntegerW@files:openwg.utils.dll cdecl setuponly';

function JSON_SetIntegerW_U(Handle: Integer; Path: String; Value: Integer): Boolean;
external 'JSON_SetIntegerW@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function JSON_SetInteger(Handle: Integer; Path: String; Value: Integer): Boolean;
begin
    if IsUninstaller() then
        Result := JSON_SetIntegerW_U(Handle, Path, Value)
    else
        Result := JSON_SetIntegerW_I(Handle, Path, Value)
end;


// Json/SetString
function JSON_SetStringW_I(Handle: Integer; Path: String; Value: String): Boolean;
external 'JSON_SetStringW@files:openwg.utils.dll cdecl setuponly';

function JSON_SetStringW_U(Handle: Integer; Path: String; Value: String): Boolean;
external 'JSON_SetStringW@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function JSON_SetString(Handle: Integer; Path: String; Value: String): Boolean;
begin
    if IsUninstaller() then
        Result := JSON_SetStringW_U(Handle, Path, Value)
    else
        Result := JSON_SetStringW_I(Handle, Path, Value)
end;



//
// NETWORK
//

[Code]

// Network/Ping
function NETWORK_PingW_I(Hostname: String; Timeout: Integer): Integer;
external 'NETWORK_PingW@files:openwg.utils.dll cdecl setuponly';

function NETWORK_PingW_U(Hostname: String; Timeout: Integer): Integer;
external 'NETWORK_PingW@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function NETWORK_Ping(Hostname: String; Timeout: Integer): Integer;
begin
    if IsUninstaller() then
        Result := NETWORK_PingW_U(Hostname, Timeout)
    else
        Result := NETWORK_PingW_I(Hostname, Timeout)
end;


// Network/Resolve
function NETWORK_ResolveW_I(Hostname: String): Integer;
external 'NETWORK_ResolveW@files:openwg.utils.dll cdecl setuponly';

function NETWORK_ResolveW_U(Hostname: String): Integer;
external 'NETWORK_ResolveW@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function NETWORK_Resolve(Hostname: String): Integer;
begin
    if IsUninstaller() then
        Result := NETWORK_ResolveW_U(Hostname)
    else
        Result := NETWORK_ResolveW_I(Hostname)
end;



//
// STRING
//

[Code]

// STRING/ReplaceRegex
function STRING_ReplaceRegex_I(Input: String; Search: String; Replace: String; Output: String; BufferSize: Integer): Integer;
external 'STRING_ReplaceRegex@files:openwg.utils.dll cdecl setuponly';

function STRING_ReplaceRegex_U(Input: String; Search: String; Replace: String; Output: String; BufferSize: Integer): Integer;
external 'STRING_ReplaceRegex@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function STRING_ReplaceRegex(Input: String; Search: String; Replace: String): String;
var
    ResultSize: Integer;
    ErrorCode: Integer;
begin
    ResultSize := Length(Input)*2;
    SetLength(Result, ResultSize);

    if IsUninstaller() then
        ErrorCode := STRING_ReplaceRegex_U(Input, Search, Replace, Result, ResultSize)
    else
        ErrorCode := STRING_ReplaceRegex_I(Input, Search, Replace, Result, ResultSize);

    // not enough space
    if (ErrorCode < 0) then
    begin
        ResultSize := -ErrorCode;
        SetLength(Result, ResultSize);
        if IsUninstaller() then
            ErrorCode := STRING_ReplaceRegex_U(Input, Search, Replace, Result, ResultSize)
        else
            ErrorCode := STRING_ReplaceRegex_I(Input, Search, Replace, Result, ResultSize);
    end;

    // general error
    if (ErrorCode = 0) then
    begin
        Result := Input;
        Exit;
    end;

    // crop result
    Result := Copy(Result, 1, Pos(#0, Result)-1);
end;


function STRING_Split(const Value: string; Delimiter: Char): TStringList;
var
    S: string;
begin
    S := Value;
    StringChangeEx(S, Delimiter, #13#10, True);
    Result := TStringList.Create()
    Result.Text := S;
end;




//
// PROCESS
//

[Code]

// PROCESS/GetRunningInDirectoryW
function PROCESS_GetRunningInDirectoryW_I(DirectoryPth: String; Buffer: String; BufferSize: Integer): Integer;
external 'PROCESS_GetRunningInDirectoryW@files:openwg.utils.dll cdecl setuponly';

function PROCESS_GetRunningInDirectoryW_U(DirectoryPth: String; Buffer: String; BufferSize: Integer): Integer;
external 'PROCESS_GetRunningInDirectoryW@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function PROCESS_GetRunningInDirectoryW(DirectoryPth: String; Buffer: String; BufferSize: Integer): Integer;
begin
    if IsUninstaller() then
        Result := PROCESS_GetRunningInDirectoryW_U(DirectoryPth, Buffer, BufferSize)
    else
        Result := PROCESS_GetRunningInDirectoryW_I(DirectoryPth, Buffer, BufferSize)
end;


//PROCESS/TerminateProcess
function PROCESS_TerminateProcess_I(ProcessPath: String): Boolean;
external 'PROCESS_TerminateProcess@files:openwg.utils.dll cdecl setuponly';

function PROCESS_TerminateProcess_U(ProcessPath: String): Boolean;
external 'PROCESS_TerminateProcess@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function PROCESS_TerminateProcess(ProcessPath: String): Boolean;
begin
    if IsUninstaller() then
        Result := PROCESS_TerminateProcess_U(ProcessPath)
    else
        Result := PROCESS_TerminateProcess_I(ProcessPath)
end;


function PROCESS_GetRunningProcesses(szPath: string): TStringList;
var
    Buffer: String;
    ProcCount: Integer;
begin
    SetLength(Buffer, 1024);
    ProcCount:=PROCESS_GetRunningInDirectoryW(szPath, Buffer, 1024);
    if ProcCount > 0 then
    begin
        Buffer:=Copy(Buffer, 1, Pos(#0, Buffer)-1);
        Result:=STRING_Split(Buffer,';');
        Exit;
    end;
    Result:=TStringList.Create();
end;


//
// SPLASHSCREEN
//

[Code]

//SPLASHSCREEN/ShowSplashScreenW
function SPLASHSCREEN_ShowSplashScreenW_I(FileName: String; SecondsToShow: Integer): Integer;
external 'SPLASHSCREEN_ShowSplashScreenW@files:openwg.utils.dll cdecl setuponly';

function SPLASHSCREEN_ShowSplashScreenW_U(FileName: String; SecondsToShow: Integer): Integer;
external 'SPLASHSCREEN_ShowSplashScreenW@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function SPLASHSCREEN_ShowSplashScreenW(FileName: String; SecondsToShow: Integer): Integer;
begin
    if IsUninstaller() then
        Result := SPLASHSCREEN_ShowSplashScreenW_U(FileName, SecondsToShow)
    else
        Result := SPLASHSCREEN_ShowSplashScreenW_I(FileName, SecondsToShow)
end;


// SPLASHSCREEN/Close
function SPLASHSCREEN_Close_I(Handle: Integer): Boolean;
external 'SPLASHSCREEN_Close@files:openwg.utils.dll cdecl setuponly';

function SPLASHSCREEN_Close_U(Handle: Integer): Boolean;
external 'SPLASHSCREEN_Close@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function SPLASHSCREEN_Close(Handle: Integer): Boolean;
begin
    if IsUninstaller() then
        Result := SPLASHSCREEN_Close_U(Handle)
    else
        Result := SPLASHSCREEN_Close_I(Handle)
end;


// SPLASHSCREEN/CloseAfter
function SPLASHSCREEN_CloseAfter_I(Handle: Integer; Msecs: Integer): Boolean;
external 'SPLASHSCREEN_CloseAfter@files:openwg.utils.dll cdecl setuponly';

function SPLASHSCREEN_CloseAfter_U(Handle: Integer; Msecs: Integer): Boolean;
external 'SPLASHSCREEN_CloseAfter@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function SPLASHSCREEN_CloseAfter(Handle: Integer; Msecs: Integer): Boolean;
begin
    if IsUninstaller() then
        Result := SPLASHSCREEN_CloseAfter_U(Handle, Msecs)
    else
        Result := SPLASHSCREEN_CloseAfter_I(Handle, Msecs)
end;


//SPLASHSCREEN/Show
function SPLASHSCREEN_ShowW_I(FileName: String): Integer;
external 'SPLASHSCREEN_ShowW@files:openwg.utils.dll cdecl setuponly';

function SPLASHSCREEN_ShowW_U(FileName: String): Integer;
external 'SPLASHSCREEN_ShowW@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function SPLASHSCREEN_Show(FileName: String): Integer;
begin
    if IsUninstaller() then
        Result := SPLASHSCREEN_ShowW_U(FileName)
    else
        Result := SPLASHSCREEN_ShowW_I(FileName)
end;





//
// WOT
//


[Code]

type
  ClientRecord = Record
    Index          : Integer;
    Branch         : Integer;
    LauncherFlavour: Integer; 
    Vendor         : Integer;
    Locale         : String;
    Path           : String;
    PathMods       : String;
    PathResmods    : String;
    Realm          : String;
    ContentType    : Integer;
    Version        : String;
    VersionExe     : String;
  end;

// WOT/AddClientW
function WOT_AddClientW_I(ClientPath: String): Integer;
external 'WOT_AddClientW@files:openwg.utils.dll cdecl setuponly';

function WOT_AddClientW_U(ClientPath: String): Integer;
external 'WOT_AddClientW@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function WOT_AddClientW(ClientPath: String): Integer;
begin
    if IsUninstaller() then
        Result := WOT_AddClientW_U(ClientPath)
    else
        Result := WOT_AddClientW_I(ClientPath)
end;


// WOT/LauncherGetPreferredClient
function WOT_LauncherGetPreferredClient_I(LauncherFlavour: Integer): Integer;
external 'WOT_LauncherGetPreferredClient@files:openwg.utils.dll cdecl setuponly';

function WOT_LauncherGetPreferredClient_U(LauncherFlavour: Integer): Integer;
external 'WOT_LauncherGetPreferredClient@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function WOT_LauncherGetPreferredClient(LauncherFlavour: Integer): Integer;
begin
    if IsUninstaller() then
        Result := WOT_LauncherGetPreferredClient_U(LauncherFlavour)
    else
        Result := WOT_LauncherGetPreferredClient_I(LauncherFlavour)
end;


// WOT/LauncherRescan
function WOT_LauncherRescan_I(): Integer;
external 'WOT_LauncherRescan@files:openwg.utils.dll cdecl setuponly';

function WOT_LauncherRescan_U(): Integer;
external 'WOT_LauncherRescan@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function WOT_LauncherRescan(): Integer;
begin
    if IsUninstaller() then
        Result := WOT_LauncherRescan_U()
    else
        Result := WOT_LauncherRescan_I()
end;


// WOT/LauncherSetDefault
function WOT_LauncherSetDefault_I(VendorFilter: Integer; VendorPriority: Integer): Integer;
external 'WOT_LauncherSetDefault@files:openwg.utils.dll cdecl setuponly';

function WOT_LauncherSetDefault_U(VendorFilter: Integer; VendorPriority: Integer): Integer;
external 'WOT_LauncherSetDefault@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

// filter  : 1 - WG, 2 - Lesta, 3 - WG + Lesta
// priority: 1 - WG, 2 - Lesta
function WOT_LauncherSetDefault(VendorFilter: Integer; VendorPriority: Integer): Integer;
begin
    if IsUninstaller() then
        Result := WOT_LauncherSetDefault_U(VendorFilter, VendorPriority)
    else
        Result := WOT_LauncherSetDefault_I(VendorFilter, VendorPriority)
end;


// WOT/ClientFind
function WOT_ClientFind_I(Path: String): Integer;
external 'WOT_ClientFind@files:openwg.utils.dll cdecl setuponly';

function WOT_ClientFind_U(Path: String): Integer;
external 'WOT_ClientFind@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function WOT_ClientFind(Path: String): Integer;
begin
    if IsUninstaller() then
        Result := WOT_ClientFind_U(Path)
    else
        Result := WOT_ClientFind_I(Path)
end;


// WOT/ClientIsStarted
function WOT_ClientIsStarted_I(ClientIndex: Integer): Integer;
external 'WOT_ClientIsStarted@files:openwg.utils.dll cdecl setuponly';

function WOT_ClientIsStarted_U(ClientIndex: Integer): Integer;
external 'WOT_ClientIsStarted@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function WOT_ClientIsStarted(ClientIndex: Integer): Boolean;
begin
    if IsUninstaller() then
        Result := WOT_ClientIsStarted_U(ClientIndex) = 1
    else
        Result := WOT_ClientIsStarted_I(ClientIndex) = 1
end;


// WOT/ClientIsVersionMatch
function WOT_ClientIsVersionMatch_I(ClientIndex: Integer; VersionPattern: String): Integer;
external 'WOT_ClientIsVersionMatch@files:openwg.utils.dll cdecl setuponly';

function WOT_ClientIsVersionMatch_U(ClientIndex: Integer; VersionPattern: String): Integer;
external 'WOT_ClientIsVersionMatch@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function WOT_ClientIsVersionMatch(ClientIndex: Integer; VersionPattern: String): Boolean;
begin
    if IsUninstaller() then
        Result := WOT_ClientIsVersionMatch_U(ClientIndex, VersionPattern) = 1
    else
        Result := WOT_ClientIsVersionMatch_I(ClientIndex, VersionPattern) = 1
end;


// WOT/ClientTerminate
function WOT_ClientTerminate_I(ClientIndex: Integer): Integer;
external 'WOT_ClientTerminate@files:openwg.utils.dll cdecl setuponly';

function WOT_ClientTerminate_U(ClientIndex: Integer): Integer;
external 'WOT_ClientTerminate@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function WOT_ClientTerminate(ClientIndex: Integer): Boolean;
begin
    if IsUninstaller() then
        Result := WOT_ClientTerminate_U(ClientIndex) = 1
    else
        Result := WOT_ClientTerminate_I(ClientIndex) = 1
end;


// WOT/GetClientsCount
function WOT_GetClientsCount_I(): Integer;
external 'WOT_GetClientsCount@files:openwg.utils.dll cdecl setuponly';

function WOT_GetClientsCount_U(): Integer;
external 'WOT_GetClientsCount@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function WOT_GetClientsCount(): Integer;
begin
    if IsUninstaller() then
        Result := WOT_GetClientsCount_U()
    else
        Result := WOT_GetClientsCount_I()
end;


// WOT/GetClientBranch
function WOT_GetClientBranch_I(ClientIndex: Integer): Integer;
external 'WOT_GetClientBranch@files:openwg.utils.dll cdecl setuponly';

function WOT_GetClientBranch_U(ClientIndex: Integer): Integer;
external 'WOT_GetClientBranch@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function WOT_GetClientBranch(ClientIndex: Integer): Integer;
begin
    if IsUninstaller() then
        Result := WOT_GetClientBranch_U(ClientIndex)
    else
        Result := WOT_GetClientBranch_I(ClientIndex)
end;


// WOT/GetClientLauncherFlavour
function WOT_GetClientLauncherFlavour_I(ClientIndex: Integer): Integer;
external 'WOT_GetClientLauncherFlavour@files:openwg.utils.dll cdecl setuponly';

function WOT_GetClientLauncherFlavour_U(ClientIndex: Integer): Integer;
external 'WOT_GetClientLauncherFlavour@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function WOT_GetClientLauncherFlavour(ClientIndex: Integer): Integer;
begin
    if IsUninstaller() then
        Result := WOT_GetClientLauncherFlavour_U(ClientIndex)
    else
        Result := WOT_GetClientLauncherFlavour_I(ClientIndex)
end;


// WOT/GetClientLocale
procedure WOT_GetClientLocaleW_I(Buffer: String; BufferSize: Integer; ClientIndex: Integer);
external 'WOT_GetClientLocaleW@files:openwg.utils.dll cdecl setuponly';

procedure WOT_GetClientLocaleW_U(Buffer: String; BufferSize: Integer; ClientIndex: Integer);
external 'WOT_GetClientLocaleW@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function WOT_GetClientLocaleW(ClientIndex: Integer): String;
var
    Buffer: String;
begin
    SetLength(Buffer, {#OPENWGUTILS_BUF_SIZE});

    if IsUninstaller() then
        WOT_GetClientLocaleW_U(Buffer, {#OPENWGUTILS_BUF_SIZE}, ClientIndex)
    else
        WOT_GetClientLocaleW_I(Buffer, {#OPENWGUTILS_BUF_SIZE}, ClientIndex);

    Result := Copy(Buffer, 1, Pos(#0, Buffer)-1);
end;


// WOT/GetClientPathW
procedure WOT_GetClientPathW_I(Buffer: String; BufferSize: Integer; ClientIndex: Integer);
external 'WOT_GetClientPathW@files:openwg.utils.dll cdecl setuponly';

procedure WOT_GetClientPathW_U(Buffer: String; BufferSize: Integer; ClientIndex: Integer);
external 'WOT_GetClientPathW@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function WOT_GetClientPathW(ClientIndex: Integer): String;
var
    Buffer: String;
begin
    SetLength(Buffer, {#OPENWGUTILS_BUF_SIZE});

    if IsUninstaller() then
        WOT_GetClientPathW_U(Buffer, {#OPENWGUTILS_BUF_SIZE}, ClientIndex)
    else
        WOT_GetClientPathW_I(Buffer, {#OPENWGUTILS_BUF_SIZE}, ClientIndex);

    Result := Copy(Buffer, 1, Pos(#0, Buffer)-1);
end;


// WOT/GetClientPathModsW
procedure WOT_GetClientPathModsW_I(Buffer: String; BufferSize: Integer; ClientIndex: Integer);
external 'WOT_GetClientPathModsW@files:openwg.utils.dll cdecl setuponly';

procedure WOT_GetClientPathModsW_U(Buffer: String; BufferSize: Integer; ClientIndex: Integer);
external 'WOT_GetClientPathModsW@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function WOT_GetClientPathModsW(ClientIndex: Integer): String;
var
    Buffer: String;
begin
    SetLength(Buffer, {#OPENWGUTILS_BUF_SIZE});

    if IsUninstaller() then
        WOT_GetClientPathModsW_U(Buffer, {#OPENWGUTILS_BUF_SIZE}, ClientIndex)
    else
        WOT_GetClientPathModsW_I(Buffer, {#OPENWGUTILS_BUF_SIZE}, ClientIndex);

    Result := Copy(Buffer, 1, Pos(#0, Buffer)-1);
end;


// WOT/GetClientPathResmodsW
procedure WOT_GetClientPathResmodsW_I(Buffer: String; BufferSize: Integer; ClientIndex: Integer);
external 'WOT_GetClientPathResmodsW@files:openwg.utils.dll cdecl setuponly';

procedure WOT_GetClientPathResmodsW_U(Buffer: String; BufferSize: Integer; ClientIndex: Integer);
external 'WOT_GetClientPathResmodsW@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function WOT_GetClientPathResmodsW(ClientIndex: Integer): String;
var
    Buffer: String;
begin
    SetLength(Buffer, {#OPENWGUTILS_BUF_SIZE});

    if IsUninstaller() then
        WOT_GetClientPathResmodsW_U(Buffer, {#OPENWGUTILS_BUF_SIZE}, ClientIndex)
    else
        WOT_GetClientPathResmodsW_I(Buffer, {#OPENWGUTILS_BUF_SIZE}, ClientIndex);

    Result := Copy(Buffer, 1, Pos(#0, Buffer)-1);
end;


// WOT/GetClientRealmW
procedure WOT_GetClientRealmW_I(Buffer: String; BufferSize: Integer; ClientIndex: Integer);
external 'WOT_GetClientRealmW@files:openwg.utils.dll cdecl setuponly';

procedure WOT_GetClientRealmW_U(Buffer: String; BufferSize: Integer; ClientIndex: Integer);
external 'WOT_GetClientRealmW@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function WOT_GetClientRealmW(ClientIndex: Integer): String;
var
    Buffer: String;
begin
    SetLength(Buffer, {#OPENWGUTILS_BUF_SIZE});

    if IsUninstaller() then
        WOT_GetClientRealmW_U(Buffer, {#OPENWGUTILS_BUF_SIZE}, ClientIndex)
    else
        WOT_GetClientRealmW_I(Buffer, {#OPENWGUTILS_BUF_SIZE}, ClientIndex);

    Result := Copy(Buffer, 1, Pos(#0, Buffer)-1);
end;


// WOT/GetClientType
function WOT_GetClientType_I(ClientIndex: Integer): Integer;
external 'WOT_GetClientType@files:openwg.utils.dll cdecl setuponly';

function WOT_GetClientType_U(ClientIndex: Integer): Integer;
external 'WOT_GetClientType@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function WOT_GetClientType(ClientIndex: Integer): Integer;
begin
    if IsUninstaller() then
        Result := WOT_GetClientType_U(ClientIndex)
    else
        Result := WOT_GetClientType_I(ClientIndex)
end;


// WOT/GetClientVendor
function WOT_GetClientVendor_I(ClientIndex: Integer): Integer;
external 'WOT_GetClientVendor@files:openwg.utils.dll cdecl setuponly';

function WOT_GetClientVendor_U(ClientIndex: Integer): Integer;
external 'WOT_GetClientVendor@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function WOT_GetClientVendor(ClientIndex: Integer): Integer;
begin
    if IsUninstaller() then
        Result := WOT_GetClientVendor_U(ClientIndex)
    else
        Result := WOT_GetClientVendor_I(ClientIndex)
end;


// WOT/GetClientVersionW
procedure WOT_GetClientVersionW_I(Buffer: String; BufferSize: Integer; ClientIndex: Integer);
external 'WOT_GetClientVersionW@files:openwg.utils.dll cdecl setuponly';

procedure WOT_GetClientVersionW_U(Buffer: String; BufferSize: Integer; ClientIndex: Integer);
external 'WOT_GetClientVersionW@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function WOT_GetClientVersionW(ClientIndex: Integer): String;
var
    Buffer: String;
begin
    SetLength(Buffer, {#OPENWGUTILS_BUF_SIZE});

    if IsUninstaller() then
        WOT_GetClientVersionW_U(Buffer, {#OPENWGUTILS_BUF_SIZE}, ClientIndex)
    else
        WOT_GetClientVersionW_I(Buffer, {#OPENWGUTILS_BUF_SIZE}, ClientIndex);

    Result := Copy(Buffer, 1, Pos(#0, Buffer)-1);
end;


// WOT/GetClientExeNameW
procedure WOT_GetClientExeNameW_I(Buffer: String; BufferSize: Integer; ClientIndex: Integer);
external 'WOT_GetClientExeNameW@files:openwg.utils.dll cdecl setuponly';

procedure WOT_GetClientExeNameW_U(Buffer: String; BufferSize: Integer; ClientIndex: Integer);
external 'WOT_GetClientExeNameW@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function WOT_GetClientExeName(ClientIndex: Integer): String;
var
    Buffer: String;
begin
    SetLength(Buffer, {#OPENWGUTILS_BUF_SIZE});

    if IsUninstaller() then
        WOT_GetClientExeNameW_U(Buffer, {#OPENWGUTILS_BUF_SIZE}, ClientIndex)
    else
        WOT_GetClientExeNameW_I(Buffer, {#OPENWGUTILS_BUF_SIZE}, ClientIndex);

    Result := Copy(Buffer, 1, Pos(#0, Buffer)-1);
end;


// WOT/GetClientExeVersionW
procedure WOT_GetClientExeVersionW_I(Buffer: String; BufferSize: Integer; ClientIndex: Integer);
external 'WOT_GetClientExeVersionW@files:openwg.utils.dll cdecl setuponly';

procedure WOT_GetClientExeVersionW_U(Buffer: String; BufferSize: Integer; ClientIndex: Integer);
external 'WOT_GetClientExeVersionW@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function WOT_GetClientExeVersionW(ClientIndex: Integer): String;
var
    Buffer: String;
begin
    SetLength(Buffer, {#OPENWGUTILS_BUF_SIZE});

    if IsUninstaller() then
        WOT_GetClientExeVersionW_U(Buffer, {#OPENWGUTILS_BUF_SIZE}, ClientIndex)
    else
        WOT_GetClientExeVersionW_I(Buffer, {#OPENWGUTILS_BUF_SIZE}, ClientIndex);

    Result := Copy(Buffer, 1, Pos(#0, Buffer)-1);
end;

//
// Cache
//
// Cache Types:
//   1 -- PDC

// WOT/WOT_GetClientCachePresent
function WOT_GetClientCachePresent_I(ClientIndex: Integer): Integer;
external 'WOT_GetClientCachePresent@files:openwg.utils.dll cdecl setuponly';

function WOT_GetClientCachePresent_U(ClientIndex: Integer): Integer;
external 'WOT_GetClientCachePresent@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function WOT_GetClientCachePresent(ClientIndex: Integer): Integer;
begin
    if IsUninstaller() then
        Result := WOT_GetClientCachePresent_U(ClientIndex)
    else
        Result := WOT_GetClientCachePresent_I(ClientIndex)
end;


// WOT/WOT_GetClientCacheSupported
function WOT_GetClientCacheSupported_I(ClientIndex: Integer): Integer;
external 'WOT_GetClientCacheSupported@files:openwg.utils.dll cdecl setuponly';

function WOT_GetClientCacheSupported_U(ClientIndex: Integer): Integer;
external 'WOT_GetClientCacheSupported@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function WOT_GetClientCacheSupported(ClientIndex: Integer): Integer;
begin
    if IsUninstaller() then
        Result := WOT_GetClientCacheSupported_U(ClientIndex)
    else
        Result := WOT_GetClientCacheSupported_I(ClientIndex)
end;


// WOT/WOT_GetClientCacheSupported
function WOT_ClearClientCache_I(ClientIndex: Integer; CacheType: Integer): Integer;
external 'WOT_ClearClientCache@files:openwg.utils.dll cdecl setuponly';

function WOT_ClearClientCache_U(ClientIndex: Integer; CacheType: Integer): Integer;
external 'WOT_ClearClientCache@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function WOT_ClearClientCache(ClientIndex: Integer; CacheType: Integer): Integer;
begin
    if IsUninstaller() then
        Result := WOT_ClearClientCache_U(ClientIndex, CacheType)
    else
        Result := WOT_ClearClientCache_I(ClientIndex, CacheType)
end;

//
// Record
//

function CLIENT_GetRecord(Index: Integer): ClientRecord;
begin
  Result.Index := Index;
  Result.Branch := WOT_GetClientBranch(Index);
  Result.LauncherFlavour := WOT_GetClientLauncherFlavour(Index);
  Result.Vendor := WOT_GetClientVendor(Index);
  Result.Locale :=  WOT_GetClientLocaleW(Index);
  Result.Path := WOT_GetClientPathW(Index);
  Result.PathMods :=  WOT_GetClientPathModsW(Index);
  Result.PathResmods := WOT_GetClientPathResmodsW(Index);
  Result.Realm :=  WOT_GetClientRealmW(Index);
  Result.ContentType := WOT_GetClientType(Index);
  Result.Version := WOT_GetClientVersionW(Index);
  Result.VersionExe := WOT_GetClientExeVersionW(Index);
end;


function CLIENT_FormatString(Client: ClientRecord): String;
begin
    case Client.Vendor of
        0: Result := 'Unknown Game';
        1: Result := 'WoT';
        2: Result := 'MT';
    end;

  Result := Result + ' ' + Client.Version;
  Result := Result + ' [';

  case Client.LauncherFlavour of
     0: Result := Result + ExpandConstant('{cm:openwg_unknown');
     1: Result := Result + 'WGC';
     2: Result := Result + '360';
     3: Result := Result + 'Steam';
     4: Result := Result + 'LGC';
     5: Result := Result + 'Standalone';
  end;

  case Client.Branch of
     0: Result := Result + ExpandConstant('/{cm:openwg_unknown}');
     1: begin
          if Client.LauncherFlavour = 1 then
          begin
            Result := Result + '/' + Client.Realm;
          end;
        end;
     2: Result := Result + ExpandConstant('/{cm:openwg_branch_ct}');
     3: Result := Result + ExpandConstant('/{cm:openwg_branch_st}');
     4: Result := Result + ExpandConstant('/{cm:openwg_branch_sb}');
  end;

  Result := Result + '] - ' + Client.Path;
end;


//
// WoT List
//
var
  wotlist_prev_idx: Integer;

procedure WotList_Update(List: TNewComboBox);
var
  Buffer: String;
  ClientsCount, Index, ListIndex: Integer;
  Str: String;
  Client: ClientRecord;
begin
  SetLength(Buffer, 1024);

  ListIndex := List.ItemIndex;
  ClientsCount := WOT_GetClientsCount();

  List.Items.Clear();

  if ClientsCount > 0 then
  begin
    for Index := 0 to ClientsCount - 1 do
    begin
      Client := CLIENT_GetRecord(Index);
      Str := CLIENT_FormatString(Client);
      List.Items.Add(Str);
    end;
  end;

  List.Items.Add(ExpandConstant('{cm:openwg_browse}'));
  List.ItemIndex := ListIndex;
end;


procedure WotList_AddClient(List: TNewComboBox; ClientPath: String);
var
  Index: Integer;
begin
  // do nothing in case of empty string
  if Length(ClientPath) = 0 then Exit;

  // try to add client
  Index := WOT_AddClientW(ClientPath);
  if Index >= 0 then
  begin
    WotList_Update(List);
    List.ItemIndex := Index;
  end else
  begin
    MsgBox(ExpandConstant('{cm:openwg_client_not_found}'), mbError, MB_OK);
    List.ItemIndex := -1;
  end;

end;


procedure WotList_OnChange(Sender: TObject);
var
  Combobox: TNewComboBox;
begin
  if Sender is TNewComboBox then
  begin
    Combobox := Sender as TNewComboBox;

    if Combobox.Text = ExpandConstant('{cm:openwg_browse}') then
    begin
      // call folder browser
      WizardForm.DirEdit.Text := '';
      WizardForm.DirBrowseButton.OnClick(nil);

      // try to add client
      WotList_AddClient(Combobox, WizardForm.DirEdit.Text);

      // fallback to the previous client in case of failure
      if ((Combobox.ItemIndex < 0) or (Combobox.Text = ExpandConstant('{cm:openwg_browse}'))) and (Combobox.Items.Count > 1) then
        Combobox.ItemIndex := wotlist_prev_idx;
    end
    else
      wotlist_prev_idx := Combobox.ItemIndex;

    WizardForm.DirEdit.Text := WOT_GetClientPathW(Combobox.ItemIndex);
  end;
end;


function WotList_Create(parent: TWinControl; pos_left, pos_top, pos_width, pos_height: Integer):TNewComboBox;
begin;
  Result := TNewComboBox.Create(WizardForm);
  Result.Parent := parent;
  Result.Style := csDropDownList;
  Result.OnChange := @WotList_OnChange;
  Result.SetBounds(pos_left,pos_top,pos_left + pos_width,pos_height);
  WotList_Update(Result);
end;


function WotList_Selected_Record(List: TNewComboBox): ClientRecord;
begin;
  Result := CLIENT_GetRecord(List.ItemIndex);
end;

function WotList_Selected_IsStarted(List: TNewComboBox): Boolean;
begin;
  Result := WOT_ClientIsStarted(List.ItemIndex);
end;

function WotList_Selected_Terminate(List: TNewComboBox): Boolean;
begin;
  Result := WOT_ClientTerminate(List.ItemIndex);
end;

function WotList_Selected_VersionMatch(List: TNewComboBox; VersionPattern: String): Boolean;
begin;
  Result := WOT_ClientIsVersionMatch(List.ItemIndex, VersionPattern);
end;



//
// WWISE
//

[Code]

// WWISE/OpenFile
function WWISE_OpenFileW_I(Path: String): Integer;
external 'WWISE_OpenFileW@files:openwg.utils.dll cdecl setuponly';

function WWISE_OpenFileW_U(Path: String): Integer;
external 'WWISE_OpenFileW@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function WWISE_OpenFile(Path: String): Integer;
begin
    if IsUninstaller() then
        Result := WWISE_OpenFileW_U(Path)
    else
        Result := WWISE_OpenFileW_I(Path)
end;


// WWISE/Close
function WWISE_Close_I(Handle: Integer): Boolean;
external 'WWISE_Close@files:openwg.utils.dll cdecl setuponly';

function WWISE_Close_U(Handle: Integer): Boolean;
external 'WWISE_Close@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function WWISE_Close(Handle: Integer): Boolean;
begin
    if IsUninstaller() then
        Result := WWISE_Close_U(Handle)
    else
        Result := WWISE_Close_I(Handle)
end;


// WWISE/LicenseGet
// result: 0 - Unknown, 1 - Unlicensed bank, 2 - Wargaming license
function WWISE_LicenseGet_I(Handle: Integer): Integer;
external 'WWISE_Close@files:openwg.utils.dll cdecl setuponly';

function WWISE_LicenseGet_U(Handle: Integer): Integer;
external 'WWISE_Close@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function WWISE_LicenseGet(Handle: Integer): Integer;
begin
    if IsUninstaller() then
        Result := WWISE_LicenseGet_U(Handle)
    else
        Result := WWISE_LicenseGet_I(Handle)
end;


// WWISE/LicenseSet
// license: 1 - unlicensed, 2 - wargaming
function WWISE_LicenseSet_I(Handle: Integer; License: Integer): Boolean;
external 'WWISE_LicenseSet@files:openwg.utils.dll cdecl setuponly';

function WWISE_LicenseSet_U(Handle: Integer; License: Integer): Boolean;
external 'WWISE_LicenseSet@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function WWISE_LicenseSet(Handle: Integer; License: Integer): Boolean;
begin
    if IsUninstaller() then
        Result := WWISE_LicenseSet_U(Handle, License)
    else
        Result := WWISE_LicenseSet_I(Handle, License)
end;


// WWISE/SaveFile
// null path - overwrite source file
function WWISE_SaveFileW_I(Handle: Integer; Path: String): Boolean;
external 'WWISE_SaveFileW@files:openwg.utils.dll cdecl setuponly';

function WWISE_SaveFileW_U(Handle: Integer; Path: String): Boolean;
external 'WWISE_SaveFileW@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function WWISE_SaveFile(Handle: Integer; Path: String): Boolean;
begin
    if IsUninstaller() then
        Result := WWISE_SaveFileW_U(Handle, Path)
    else
        Result := WWISE_SaveFileW_I(Handle, Path)
end;



//
// XML
//

[Code]

// XML/AddKey
function XML_AddKey_I(Handle: Integer; Path: String; Name: String; Value: String): Boolean;
external 'XML_AddKeyW@files:openwg.utils.dll cdecl setuponly';

function XML_AddKey_U(Handle: Integer; Path: String; Name: String; Value: String): Boolean;
external 'XML_AddKeyW@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function XML_AddKey(Handle: Integer; Path: String; Name: String; Value: String): Boolean;
begin
    if IsUninstaller() then
        Result := XML_AddKey_U(Handle, Path, Name, Value)
    else
        Result := XML_AddKey_I(Handle, Path, Name, Value)
end;


// XML/Close
function XML_Close_I(Handle: Integer): Boolean;
external 'XML_Close@files:openwg.utils.dll cdecl setuponly';

function XML_Close_U(Handle: Integer): Boolean;
external 'XML_Close@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function XML_Close(Handle: Integer): Boolean;
begin
    if IsUninstaller() then
        Result := XML_Close_U(Handle)
    else
        Result := XML_Close_I(Handle)
end;


// XML/ContainsKey
function XML_ContainsKey_I(Handle: Integer; Path: String): Boolean;
external 'XML_ContainsKeyW@files:openwg.utils.dll cdecl setuponly';

function XML_ContainsKey_U(Handle: Integer; Path: String): Boolean;
external 'XML_ContainsKeyW@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function XML_ContainsKey(Handle: Integer; Path: String): Boolean;
begin
    if IsUninstaller() then
        Result := XML_ContainsKey_U(Handle, Path)
    else
        Result := XML_ContainsKey_I(Handle, Path)
end;


// XML/ContainsKeyEx
function XML_ContainsKeyEx_I(Handle: Integer; Path: String; Value: String): Boolean;
external 'XML_ContainsKeyExW@files:openwg.utils.dll cdecl setuponly';

function XML_ContainsKeyEx_U(Handle: Integer; Path: String; Value: String): Boolean;
external 'XML_ContainsKeyExW@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function XML_ContainsKeyEx(Handle: Integer; Path: String; Value: String): Boolean;
begin
    if IsUninstaller() then
        Result := XML_ContainsKeyEx_U(Handle, Path, Value)
    else
        Result := XML_ContainsKeyEx_I(Handle, Path, Value)
end;


// XML/OpenFile
function XML_OpenFileW_I(Path: String; AllowCreation: Boolean): Integer;
external 'XML_OpenFileW@files:openwg.utils.dll cdecl setuponly';

function XML_OpenFileW_U(Path: String; AllowCreation: Boolean): Integer;
external 'XML_OpenFileW@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function XML_OpenFile(Path: String; AllowCreation: Boolean): Integer;
begin
    if IsUninstaller() then
        Result := XML_OpenFileW_U(Path, AllowCreation)
    else
        Result := XML_OpenFileW_I(Path, AllowCreation)
end;


// XML/SaveFile
function XML_SaveFileW_I(Handle: Integer; Path: String): Boolean;
external 'XML_SaveFileW@files:openwg.utils.dll cdecl setuponly';

function XML_SaveFileW_U(Handle: Integer; Path: String): Boolean;
external 'XML_SaveFileW@{app}\{#OPENWGUTILS_DIR_UNINST}\openwg.utils.dll cdecl uninstallonly';

function XML_SaveFile(Handle: Integer; Path: String): Boolean;
begin
    if IsUninstaller() then
        Result := XML_SaveFileW_U(Handle, Path)
    else
        Result := XML_SaveFileW_I(Handle, Path)
end;
