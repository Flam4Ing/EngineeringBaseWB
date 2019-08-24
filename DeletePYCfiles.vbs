
' Global FileSystemObject
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Start at the root
DoFolder objFSO.GetParentFolderName(WScript.ScriptFullName)

' Recursive function
Sub DoFolder(strFolder)

    With objFSO.GetFolder(strFolder)

        For Each File In .Files
            If Right(File.name, 4) = ".pyc" Then
                objFSO.DeleteFile(.Path & "\" & File.name)
            End If
        Next

        For Each objFolder In .SubFolders
            DoFolder objFolder.Path
        Next
    End With

End Sub

