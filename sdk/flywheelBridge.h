/* Created by "go tool cgo" - DO NOT EDIT. */

/* package flywheel.io/sdk/bridge/dist */

/* Start of preamble from import "C" comments.  */




/* End of preamble from import "C" comments.  */


/* Start of boilerplate cgo prologue.  */
#line 1 "cgo-gcc-export-header-prolog"

#ifndef GO_CGO_PROLOGUE_H
#define GO_CGO_PROLOGUE_H

typedef signed char GoInt8;
typedef unsigned char GoUint8;
typedef short GoInt16;
typedef unsigned short GoUint16;
typedef int GoInt32;
typedef unsigned int GoUint32;
typedef long long GoInt64;
typedef unsigned long long GoUint64;
typedef GoInt64 GoInt;
typedef GoUint64 GoUint;
typedef __SIZE_TYPE__ GoUintptr;
typedef float GoFloat32;
typedef double GoFloat64;
typedef float _Complex GoComplex64;
typedef double _Complex GoComplex128;

/*
  static assertion to make sure the file is being used on architecture
  at least with matching size of GoInt.
*/
typedef char _check_for_64_bit_pointer_matching_GoInt[sizeof(void*)==64/8 ? 1:-1];

typedef struct { const char *p; GoInt n; } GoString;
typedef void *GoMap;
typedef void *GoChan;
typedef struct { void *t; void *v; } GoInterface;
typedef struct { void *data; GoInt len; GoInt cap; } GoSlice;

#endif

/* End of boilerplate cgo prologue.  */

#ifdef __cplusplus
extern "C" {
#endif


extern void Free(char* p0);

extern char* TestBridge(char* p0);

extern char* GetAllCollections(char* p0, int* p1);

extern char* GetCollection(char* p0, char* p1, int* p2);

extern char* GetCollectionSessions(char* p0, char* p1, int* p2);

extern char* GetCollectionAcquisitions(char* p0, char* p1, int* p2);

extern char* GetCollectionSessionAcquisitions(char* p0, char* p1, char* p2, int* p3);

extern char* AddCollection(char* p0, char* p1, int* p2);

extern char* AddAcquisitionsToCollection(char* p0, char* p1, char* p2, int* p3);

extern char* AddSessionsToCollection(char* p0, char* p1, char* p2, int* p3);

extern char* AddCollectionNote(char* p0, char* p1, char* p2, int* p3);

extern char* ModifyCollection(char* p0, char* p1, char* p2, int* p3);

extern char* DeleteCollection(char* p0, char* p1, int* p2);

extern char* ModifyCollectionFile(char* p0, char* p1, char* p2, char* p3, int* p4);

extern char* SetCollectionFileInfo(char* p0, char* p1, char* p2, char* p3, int* p4);

extern char* ReplaceCollectionFileInfo(char* p0, char* p1, char* p2, char* p3, int* p4);

extern char* DeleteCollectionFileInfoFields(char* p0, char* p1, char* p2, char* p3, int* p4);

extern char* UploadFileToCollection(char* p0, char* p1, char* p2, int* p3);

extern char* DownloadFileFromCollection(char* p0, char* p1, char* p2, char* p3, int* p4);

extern char* GetCurrentUser(char* p0, int* p1);

extern char* GetAllUsers(char* p0, int* p1);

extern char* GetUser(char* p0, char* p1, int* p2);

extern char* AddUser(char* p0, char* p1, int* p2);

extern char* ModifyUser(char* p0, char* p1, char* p2, int* p3);

extern char* DeleteUser(char* p0, char* p1, int* p2);

extern char* GetAllGears(char* p0, int* p1);

extern char* GetGear(char* p0, char* p1, int* p2);

extern char* AddGear(char* p0, char* p1, int* p2);

extern char* DeleteGear(char* p0, char* p1, int* p2);

extern char* GetAllGroups(char* p0, int* p1);

extern char* GetGroup(char* p0, char* p1, int* p2);

extern char* AddGroup(char* p0, char* p1, int* p2);

extern char* AddGroupTag(char* p0, char* p1, char* p2, int* p3);

extern char* ModifyGroup(char* p0, char* p1, char* p2, int* p3);

extern char* DeleteGroup(char* p0, char* p1, int* p2);

extern char* GetJob(char* p0, char* p1, int* p2);

extern char* GetJobLogs(char* p0, char* p1, int* p2);

extern char* AddJob(char* p0, char* p1, int* p2);

extern char* HeartbeatJob(char* p0, char* p1, int* p2);

extern char* GetConfig(char* p0, int* p1);

extern char* GetVersion(char* p0, int* p1);

extern char* GetAllSessions(char* p0, int* p1);

extern char* GetSession(char* p0, char* p1, int* p2);

extern char* GetSessionAcquisitions(char* p0, char* p1, int* p2);

extern char* AddSession(char* p0, char* p1, int* p2);

extern char* AddSessionNote(char* p0, char* p1, char* p2, int* p3);

extern char* AddSessionTag(char* p0, char* p1, char* p2, int* p3);

extern char* ModifySession(char* p0, char* p1, char* p2, int* p3);

extern char* DeleteSession(char* p0, char* p1, int* p2);

extern char* ModifySessionFile(char* p0, char* p1, char* p2, char* p3, int* p4);

extern char* SetSessionFileInfo(char* p0, char* p1, char* p2, char* p3, int* p4);

extern char* ReplaceSessionFileInfo(char* p0, char* p1, char* p2, char* p3, int* p4);

extern char* DeleteSessionFileInfoFields(char* p0, char* p1, char* p2, char* p3, int* p4);

extern char* UploadFileToSession(char* p0, char* p1, char* p2, int* p3);

extern char* DownloadFileFromSession(char* p0, char* p1, char* p2, char* p3, int* p4);

extern char* GetAllAcquisitions(char* p0, int* p1);

extern char* GetAcquisition(char* p0, char* p1, int* p2);

extern char* AddAcquisition(char* p0, char* p1, int* p2);

extern char* AddAcquisitionNote(char* p0, char* p1, char* p2, int* p3);

extern char* AddAcquisitionTag(char* p0, char* p1, char* p2, int* p3);

extern char* ModifyAcquisition(char* p0, char* p1, char* p2, int* p3);

extern char* DeleteAcquisition(char* p0, char* p1, int* p2);

extern char* ModifyAcquisitionFile(char* p0, char* p1, char* p2, char* p3, int* p4);

extern char* SetAcquisitionFileInfo(char* p0, char* p1, char* p2, char* p3, int* p4);

extern char* ReplaceAcquisitionFileInfo(char* p0, char* p1, char* p2, char* p3, int* p4);

extern char* DeleteAcquisitionFileInfoFields(char* p0, char* p1, char* p2, char* p3, int* p4);

extern char* UploadFileToAcquisition(char* p0, char* p1, char* p2, int* p3);

extern char* DownloadFileFromAcquisition(char* p0, char* p1, char* p2, char* p3, int* p4);

extern char* GetAllBatches(char* p0, int* p1);

extern char* GetBatch(char* p0, char* p1, int* p2);

extern char* StartBatch(char* p0, char* p1, int* p2);

extern char* GetAllProjects(char* p0, int* p1);

extern char* GetProject(char* p0, char* p1, int* p2);

extern char* GetProjectSessions(char* p0, char* p1, int* p2);

extern char* AddProject(char* p0, char* p1, int* p2);

extern char* AddProjectNote(char* p0, char* p1, char* p2, int* p3);

extern char* AddProjectTag(char* p0, char* p1, char* p2, int* p3);

extern char* ModifyProject(char* p0, char* p1, char* p2, int* p3);

extern char* DeleteProject(char* p0, char* p1, int* p2);

extern char* ModifyProjectFile(char* p0, char* p1, char* p2, char* p3, int* p4);

extern char* SetProjectFileInfo(char* p0, char* p1, char* p2, char* p3, int* p4);

extern char* ReplaceProjectFileInfo(char* p0, char* p1, char* p2, char* p3, int* p4);

extern char* DeleteProjectFileInfoFields(char* p0, char* p1, char* p2, char* p3, int* p4);

extern char* UploadFileToProject(char* p0, char* p1, char* p2, int* p3);

extern char* DownloadFileFromProject(char* p0, char* p1, char* p2, char* p3, int* p4);

extern char* Search(char* p0, char* p1, int* p2);

#ifdef __cplusplus
}
#endif
