#!/usr/bin/env python

import ctypes
import json
import six
import sys
import os


# Detect platform
# https://docs.python.org/2/library/sys.html#sys.platform
# https://docs.python.org/3/library/sys.html#sys.platform
_platform = sys.platform

if _platform.startswith('linux') or _platform.startswith('freebsd'):
    _filename = 'flywheelBridge.so'    # Linux-ish
elif _platform.startswith('darwin'):
    _filename = 'flywheelBridge.dylib' # OSX
elif _platform.startswith('win') or _platform.startswith('cygwin'):
    _filename = 'flywheelBridge.so'    # Windows-ish
else:
    _filename = 'flywheelBridge.so'    # Guess

# Load the shared object file. Further details are added at the end of the file.
bridge = ctypes.cdll.LoadLibrary(os.path.join(os.path.dirname(__file__), _filename))

def test_bridge(s):
    """
    Test if the C bridge is functional.
    Should return "Hello <s>".
    """

    pointer = bridge.TestBridge(six.b(s))
    value = ctypes.cast(pointer, ctypes.c_char_p).value
    return value.decode('utf-8')

class FlywheelException(Exception):
    pass

class Flywheel:

    def __init__(self, key):
        if len(key.split(':')) < 2:
            raise FlywheelException('Invalid API key.')
        self.key = six.b(key)

    @staticmethod
    def _handle_return(status, pointer):
        status_code = status.value
        value = ctypes.cast(pointer, ctypes.c_char_p).value

        # In python 2, the casted pointer value will be of type str.
        # In python 3, it will instead be of type bytes.
        #
        # In python 3.6, json.loads gained the ability to process bytes objects.
        # Earlier versions did not have this capability.
        # So, to workaround, decode any non-str object.
        # This could later be changed to detect the python version -.-
        #
        # https://bugs.python.org/issue10976
        # https://bugs.python.org/msg275615
        if not isinstance(value, str):
            value = value.decode('utf-8')

        if status_code == 0 and value is None:
            return None
        elif status_code == 0:
            return json.loads(value)['data']
        else:
            try:
                msg = json.loads(value)['message']
            except:
                msg = 'Unknown error (status ' + str(status_code) + ').'
            raise FlywheelException(msg)

    @staticmethod
    def get_sdk_version():
        """
        Returns the release version of the Flywheel SDK.
        """

        return '0.2.0'

    #
    # AUTO GENERATED CODE FOLLOWS
    #
    
    def get_all_batches(self):
        status = ctypes.c_int(-100)
        pointer = bridge.GetAllBatches(self.key, ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def get_batch(self, id):
        status = ctypes.c_int(-100)
        pointer = bridge.GetBatch(self.key, six.b(str(id)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def start_batch(self, id):
        status = ctypes.c_int(-100)
        pointer = bridge.StartBatch(self.key, six.b(str(id)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def get_all_acquisitions(self):
        status = ctypes.c_int(-100)
        pointer = bridge.GetAllAcquisitions(self.key, ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def get_acquisition(self, id):
        status = ctypes.c_int(-100)
        pointer = bridge.GetAcquisition(self.key, six.b(str(id)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def add_acquisition(self, acquisition):
        status = ctypes.c_int(-100)
        acquisition = json.dumps(acquisition)
        pointer = bridge.AddAcquisition(self.key, six.b(str(acquisition)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def add_acquisition_note(self, id, text):
        status = ctypes.c_int(-100)
        pointer = bridge.AddAcquisitionNote(self.key, six.b(str(id)), six.b(str(text)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def add_acquisition_tag(self, id, tag):
        status = ctypes.c_int(-100)
        pointer = bridge.AddAcquisitionTag(self.key, six.b(str(id)), six.b(str(tag)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def modify_acquisition(self, id, acquisition):
        status = ctypes.c_int(-100)
        acquisition = json.dumps(acquisition)
        pointer = bridge.ModifyAcquisition(self.key, six.b(str(id)), six.b(str(acquisition)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def delete_acquisition(self, id):
        status = ctypes.c_int(-100)
        pointer = bridge.DeleteAcquisition(self.key, six.b(str(id)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def modify_acquisition_file(self, id, filename, attributes):
        status = ctypes.c_int(-100)
        attributes = json.dumps(attributes)
        pointer = bridge.ModifyAcquisitionFile(self.key, six.b(str(id)), six.b(str(filename)), six.b(str(attributes)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def set_acquisition_file_info(self, id, filename, set):
        status = ctypes.c_int(-100)
        set = json.dumps(set)
        pointer = bridge.SetAcquisitionFileInfo(self.key, six.b(str(id)), six.b(str(filename)), six.b(str(set)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def replace_acquisition_file_info(self, id, filename, replace):
        status = ctypes.c_int(-100)
        replace = json.dumps(replace)
        pointer = bridge.ReplaceAcquisitionFileInfo(self.key, six.b(str(id)), six.b(str(filename)), six.b(str(replace)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def delete_acquisition_file_info_fields(self, id, filename, keys):
        status = ctypes.c_int(-100)
        keys = json.dumps(keys)
        pointer = bridge.DeleteAcquisitionFileInfoFields(self.key, six.b(str(id)), six.b(str(filename)), six.b(str(keys)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def upload_file_to_acquisition(self, id, path):
        status = ctypes.c_int(-100)
        pointer = bridge.UploadFileToAcquisition(self.key, six.b(str(id)), six.b(str(path)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def download_file_from_acquisition(self, id, name, path):
        status = ctypes.c_int(-100)
        pointer = bridge.DownloadFileFromAcquisition(self.key, six.b(str(id)), six.b(str(name)), six.b(str(path)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def get_config(self):
        status = ctypes.c_int(-100)
        pointer = bridge.GetConfig(self.key, ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def get_version(self):
        status = ctypes.c_int(-100)
        pointer = bridge.GetVersion(self.key, ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def get_job(self, id):
        status = ctypes.c_int(-100)
        pointer = bridge.GetJob(self.key, six.b(str(id)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def get_job_logs(self, id):
        status = ctypes.c_int(-100)
        pointer = bridge.GetJobLogs(self.key, six.b(str(id)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def add_job(self, job):
        status = ctypes.c_int(-100)
        job = json.dumps(job)
        pointer = bridge.AddJob(self.key, six.b(str(job)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def heartbeat_job(self, id):
        status = ctypes.c_int(-100)
        pointer = bridge.HeartbeatJob(self.key, six.b(str(id)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def get_all_gears(self):
        status = ctypes.c_int(-100)
        pointer = bridge.GetAllGears(self.key, ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def get_gear(self, id):
        status = ctypes.c_int(-100)
        pointer = bridge.GetGear(self.key, six.b(str(id)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def add_gear(self, gear):
        status = ctypes.c_int(-100)
        gear = json.dumps(gear)
        pointer = bridge.AddGear(self.key, six.b(str(gear)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def delete_gear(self, id):
        status = ctypes.c_int(-100)
        pointer = bridge.DeleteGear(self.key, six.b(str(id)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def get_current_user(self):
        status = ctypes.c_int(-100)
        pointer = bridge.GetCurrentUser(self.key, ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def get_all_users(self):
        status = ctypes.c_int(-100)
        pointer = bridge.GetAllUsers(self.key, ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def get_user(self, id):
        status = ctypes.c_int(-100)
        pointer = bridge.GetUser(self.key, six.b(str(id)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def add_user(self, user):
        status = ctypes.c_int(-100)
        user = json.dumps(user)
        pointer = bridge.AddUser(self.key, six.b(str(user)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def modify_user(self, id, user):
        status = ctypes.c_int(-100)
        user = json.dumps(user)
        pointer = bridge.ModifyUser(self.key, six.b(str(id)), six.b(str(user)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def delete_user(self, id):
        status = ctypes.c_int(-100)
        pointer = bridge.DeleteUser(self.key, six.b(str(id)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def get_all_groups(self):
        status = ctypes.c_int(-100)
        pointer = bridge.GetAllGroups(self.key, ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def get_group(self, id):
        status = ctypes.c_int(-100)
        pointer = bridge.GetGroup(self.key, six.b(str(id)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def add_group(self, group):
        status = ctypes.c_int(-100)
        group = json.dumps(group)
        pointer = bridge.AddGroup(self.key, six.b(str(group)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def add_group_tag(self, id, tag):
        status = ctypes.c_int(-100)
        pointer = bridge.AddGroupTag(self.key, six.b(str(id)), six.b(str(tag)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def modify_group(self, id, group):
        status = ctypes.c_int(-100)
        group = json.dumps(group)
        pointer = bridge.ModifyGroup(self.key, six.b(str(id)), six.b(str(group)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def delete_group(self, id):
        status = ctypes.c_int(-100)
        pointer = bridge.DeleteGroup(self.key, six.b(str(id)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def get_all_collections(self):
        status = ctypes.c_int(-100)
        pointer = bridge.GetAllCollections(self.key, ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def get_collection(self, id):
        status = ctypes.c_int(-100)
        pointer = bridge.GetCollection(self.key, six.b(str(id)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def get_collection_sessions(self, id):
        status = ctypes.c_int(-100)
        pointer = bridge.GetCollectionSessions(self.key, six.b(str(id)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def get_collection_acquisitions(self, id):
        status = ctypes.c_int(-100)
        pointer = bridge.GetCollectionAcquisitions(self.key, six.b(str(id)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def get_collection_session_acquisitions(self, id, sid):
        status = ctypes.c_int(-100)
        pointer = bridge.GetCollectionSessionAcquisitions(self.key, six.b(str(id)), six.b(str(sid)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def add_collection(self, collection):
        status = ctypes.c_int(-100)
        collection = json.dumps(collection)
        pointer = bridge.AddCollection(self.key, six.b(str(collection)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def add_acquisitions_to_collection(self, id, aqids):
        status = ctypes.c_int(-100)
        aqids = json.dumps(aqids)
        pointer = bridge.AddAcquisitionsToCollection(self.key, six.b(str(id)), six.b(str(aqids)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def add_sessions_to_collection(self, id, sessionids):
        status = ctypes.c_int(-100)
        sessionids = json.dumps(sessionids)
        pointer = bridge.AddSessionsToCollection(self.key, six.b(str(id)), six.b(str(sessionids)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def add_collection_note(self, id, text):
        status = ctypes.c_int(-100)
        pointer = bridge.AddCollectionNote(self.key, six.b(str(id)), six.b(str(text)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def modify_collection(self, id, collection):
        status = ctypes.c_int(-100)
        collection = json.dumps(collection)
        pointer = bridge.ModifyCollection(self.key, six.b(str(id)), six.b(str(collection)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def delete_collection(self, id):
        status = ctypes.c_int(-100)
        pointer = bridge.DeleteCollection(self.key, six.b(str(id)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def modify_collection_file(self, id, filename, attributes):
        status = ctypes.c_int(-100)
        attributes = json.dumps(attributes)
        pointer = bridge.ModifyCollectionFile(self.key, six.b(str(id)), six.b(str(filename)), six.b(str(attributes)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def set_collection_file_info(self, id, filename, set):
        status = ctypes.c_int(-100)
        set = json.dumps(set)
        pointer = bridge.SetCollectionFileInfo(self.key, six.b(str(id)), six.b(str(filename)), six.b(str(set)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def replace_collection_file_info(self, id, filename, replace):
        status = ctypes.c_int(-100)
        replace = json.dumps(replace)
        pointer = bridge.ReplaceCollectionFileInfo(self.key, six.b(str(id)), six.b(str(filename)), six.b(str(replace)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def delete_collection_file_info_fields(self, id, filename, keys):
        status = ctypes.c_int(-100)
        keys = json.dumps(keys)
        pointer = bridge.DeleteCollectionFileInfoFields(self.key, six.b(str(id)), six.b(str(filename)), six.b(str(keys)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def upload_file_to_collection(self, id, path):
        status = ctypes.c_int(-100)
        pointer = bridge.UploadFileToCollection(self.key, six.b(str(id)), six.b(str(path)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def download_file_from_collection(self, id, name, path):
        status = ctypes.c_int(-100)
        pointer = bridge.DownloadFileFromCollection(self.key, six.b(str(id)), six.b(str(name)), six.b(str(path)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def get_analysis(self, id):
        status = ctypes.c_int(-100)
        pointer = bridge.GetAnalysis(self.key, six.b(str(id)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def add_session_analysis_note(self, sessionId, analysisId, text):
        status = ctypes.c_int(-100)
        pointer = bridge.AddSessionAnalysisNote(self.key, six.b(str(sessionId)), six.b(str(analysisId)), six.b(str(text)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def get_all_sessions(self):
        status = ctypes.c_int(-100)
        pointer = bridge.GetAllSessions(self.key, ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def get_session(self, id):
        status = ctypes.c_int(-100)
        pointer = bridge.GetSession(self.key, six.b(str(id)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def get_session_acquisitions(self, id):
        status = ctypes.c_int(-100)
        pointer = bridge.GetSessionAcquisitions(self.key, six.b(str(id)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def add_session(self, session):
        status = ctypes.c_int(-100)
        session = json.dumps(session)
        pointer = bridge.AddSession(self.key, six.b(str(session)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def add_session_note(self, id, text):
        status = ctypes.c_int(-100)
        pointer = bridge.AddSessionNote(self.key, six.b(str(id)), six.b(str(text)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def add_session_tag(self, id, tag):
        status = ctypes.c_int(-100)
        pointer = bridge.AddSessionTag(self.key, six.b(str(id)), six.b(str(tag)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def modify_session(self, id, session):
        status = ctypes.c_int(-100)
        session = json.dumps(session)
        pointer = bridge.ModifySession(self.key, six.b(str(id)), six.b(str(session)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def delete_session(self, id):
        status = ctypes.c_int(-100)
        pointer = bridge.DeleteSession(self.key, six.b(str(id)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def modify_session_file(self, id, filename, attributes):
        status = ctypes.c_int(-100)
        attributes = json.dumps(attributes)
        pointer = bridge.ModifySessionFile(self.key, six.b(str(id)), six.b(str(filename)), six.b(str(attributes)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def set_session_file_info(self, id, filename, set):
        status = ctypes.c_int(-100)
        set = json.dumps(set)
        pointer = bridge.SetSessionFileInfo(self.key, six.b(str(id)), six.b(str(filename)), six.b(str(set)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def replace_session_file_info(self, id, filename, replace):
        status = ctypes.c_int(-100)
        replace = json.dumps(replace)
        pointer = bridge.ReplaceSessionFileInfo(self.key, six.b(str(id)), six.b(str(filename)), six.b(str(replace)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def delete_session_file_info_fields(self, id, filename, keys):
        status = ctypes.c_int(-100)
        keys = json.dumps(keys)
        pointer = bridge.DeleteSessionFileInfoFields(self.key, six.b(str(id)), six.b(str(filename)), six.b(str(keys)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def upload_file_to_session(self, id, path):
        status = ctypes.c_int(-100)
        pointer = bridge.UploadFileToSession(self.key, six.b(str(id)), six.b(str(path)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def download_file_from_session(self, id, name, path):
        status = ctypes.c_int(-100)
        pointer = bridge.DownloadFileFromSession(self.key, six.b(str(id)), six.b(str(name)), six.b(str(path)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def get_all_projects(self):
        status = ctypes.c_int(-100)
        pointer = bridge.GetAllProjects(self.key, ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def get_project(self, id):
        status = ctypes.c_int(-100)
        pointer = bridge.GetProject(self.key, six.b(str(id)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def get_project_sessions(self, id):
        status = ctypes.c_int(-100)
        pointer = bridge.GetProjectSessions(self.key, six.b(str(id)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def add_project(self, project):
        status = ctypes.c_int(-100)
        project = json.dumps(project)
        pointer = bridge.AddProject(self.key, six.b(str(project)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def add_project_note(self, id, text):
        status = ctypes.c_int(-100)
        pointer = bridge.AddProjectNote(self.key, six.b(str(id)), six.b(str(text)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def add_project_tag(self, id, tag):
        status = ctypes.c_int(-100)
        pointer = bridge.AddProjectTag(self.key, six.b(str(id)), six.b(str(tag)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def modify_project(self, id, project):
        status = ctypes.c_int(-100)
        project = json.dumps(project)
        pointer = bridge.ModifyProject(self.key, six.b(str(id)), six.b(str(project)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def delete_project(self, id):
        status = ctypes.c_int(-100)
        pointer = bridge.DeleteProject(self.key, six.b(str(id)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def modify_project_file(self, id, filename, attributes):
        status = ctypes.c_int(-100)
        attributes = json.dumps(attributes)
        pointer = bridge.ModifyProjectFile(self.key, six.b(str(id)), six.b(str(filename)), six.b(str(attributes)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def set_project_file_info(self, id, filename, set):
        status = ctypes.c_int(-100)
        set = json.dumps(set)
        pointer = bridge.SetProjectFileInfo(self.key, six.b(str(id)), six.b(str(filename)), six.b(str(set)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def replace_project_file_info(self, id, filename, replace):
        status = ctypes.c_int(-100)
        replace = json.dumps(replace)
        pointer = bridge.ReplaceProjectFileInfo(self.key, six.b(str(id)), six.b(str(filename)), six.b(str(replace)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def delete_project_file_info_fields(self, id, filename, keys):
        status = ctypes.c_int(-100)
        keys = json.dumps(keys)
        pointer = bridge.DeleteProjectFileInfoFields(self.key, six.b(str(id)), six.b(str(filename)), six.b(str(keys)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def upload_file_to_project(self, id, path):
        status = ctypes.c_int(-100)
        pointer = bridge.UploadFileToProject(self.key, six.b(str(id)), six.b(str(path)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def download_file_from_project(self, id, name, path):
        status = ctypes.c_int(-100)
        pointer = bridge.DownloadFileFromProject(self.key, six.b(str(id)), six.b(str(name)), six.b(str(path)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    
    def search(self, search_query):
        status = ctypes.c_int(-100)
        search_query = json.dumps(search_query)
        pointer = bridge.Search(self.key, six.b(str(search_query)), ctypes.byref(status))
        return self._handle_return(status, pointer)
    

# Every bridge function returns a char*.
# Declaring this explicitly prevents segmentation faults on OSX.

# Manual functions
bridge.TestBridge.restype = ctypes.POINTER(ctypes.c_char)

# API client functions
bridge.GetAllBatches.restype = ctypes.POINTER(ctypes.c_char)
bridge.GetBatch.restype = ctypes.POINTER(ctypes.c_char)
bridge.StartBatch.restype = ctypes.POINTER(ctypes.c_char)
bridge.GetAllAcquisitions.restype = ctypes.POINTER(ctypes.c_char)
bridge.GetAcquisition.restype = ctypes.POINTER(ctypes.c_char)
bridge.AddAcquisition.restype = ctypes.POINTER(ctypes.c_char)
bridge.AddAcquisitionNote.restype = ctypes.POINTER(ctypes.c_char)
bridge.AddAcquisitionTag.restype = ctypes.POINTER(ctypes.c_char)
bridge.ModifyAcquisition.restype = ctypes.POINTER(ctypes.c_char)
bridge.DeleteAcquisition.restype = ctypes.POINTER(ctypes.c_char)
bridge.ModifyAcquisitionFile.restype = ctypes.POINTER(ctypes.c_char)
bridge.SetAcquisitionFileInfo.restype = ctypes.POINTER(ctypes.c_char)
bridge.ReplaceAcquisitionFileInfo.restype = ctypes.POINTER(ctypes.c_char)
bridge.DeleteAcquisitionFileInfoFields.restype = ctypes.POINTER(ctypes.c_char)
bridge.UploadFileToAcquisition.restype = ctypes.POINTER(ctypes.c_char)
bridge.DownloadFileFromAcquisition.restype = ctypes.POINTER(ctypes.c_char)
bridge.GetConfig.restype = ctypes.POINTER(ctypes.c_char)
bridge.GetVersion.restype = ctypes.POINTER(ctypes.c_char)
bridge.GetJob.restype = ctypes.POINTER(ctypes.c_char)
bridge.GetJobLogs.restype = ctypes.POINTER(ctypes.c_char)
bridge.AddJob.restype = ctypes.POINTER(ctypes.c_char)
bridge.HeartbeatJob.restype = ctypes.POINTER(ctypes.c_char)
bridge.GetAllGears.restype = ctypes.POINTER(ctypes.c_char)
bridge.GetGear.restype = ctypes.POINTER(ctypes.c_char)
bridge.AddGear.restype = ctypes.POINTER(ctypes.c_char)
bridge.DeleteGear.restype = ctypes.POINTER(ctypes.c_char)
bridge.GetCurrentUser.restype = ctypes.POINTER(ctypes.c_char)
bridge.GetAllUsers.restype = ctypes.POINTER(ctypes.c_char)
bridge.GetUser.restype = ctypes.POINTER(ctypes.c_char)
bridge.AddUser.restype = ctypes.POINTER(ctypes.c_char)
bridge.ModifyUser.restype = ctypes.POINTER(ctypes.c_char)
bridge.DeleteUser.restype = ctypes.POINTER(ctypes.c_char)
bridge.GetAllGroups.restype = ctypes.POINTER(ctypes.c_char)
bridge.GetGroup.restype = ctypes.POINTER(ctypes.c_char)
bridge.AddGroup.restype = ctypes.POINTER(ctypes.c_char)
bridge.AddGroupTag.restype = ctypes.POINTER(ctypes.c_char)
bridge.ModifyGroup.restype = ctypes.POINTER(ctypes.c_char)
bridge.DeleteGroup.restype = ctypes.POINTER(ctypes.c_char)
bridge.GetAllCollections.restype = ctypes.POINTER(ctypes.c_char)
bridge.GetCollection.restype = ctypes.POINTER(ctypes.c_char)
bridge.GetCollectionSessions.restype = ctypes.POINTER(ctypes.c_char)
bridge.GetCollectionAcquisitions.restype = ctypes.POINTER(ctypes.c_char)
bridge.GetCollectionSessionAcquisitions.restype = ctypes.POINTER(ctypes.c_char)
bridge.AddCollection.restype = ctypes.POINTER(ctypes.c_char)
bridge.AddAcquisitionsToCollection.restype = ctypes.POINTER(ctypes.c_char)
bridge.AddSessionsToCollection.restype = ctypes.POINTER(ctypes.c_char)
bridge.AddCollectionNote.restype = ctypes.POINTER(ctypes.c_char)
bridge.ModifyCollection.restype = ctypes.POINTER(ctypes.c_char)
bridge.DeleteCollection.restype = ctypes.POINTER(ctypes.c_char)
bridge.ModifyCollectionFile.restype = ctypes.POINTER(ctypes.c_char)
bridge.SetCollectionFileInfo.restype = ctypes.POINTER(ctypes.c_char)
bridge.ReplaceCollectionFileInfo.restype = ctypes.POINTER(ctypes.c_char)
bridge.DeleteCollectionFileInfoFields.restype = ctypes.POINTER(ctypes.c_char)
bridge.UploadFileToCollection.restype = ctypes.POINTER(ctypes.c_char)
bridge.DownloadFileFromCollection.restype = ctypes.POINTER(ctypes.c_char)
bridge.GetAnalysis.restype = ctypes.POINTER(ctypes.c_char)
bridge.AddSessionAnalysisNote.restype = ctypes.POINTER(ctypes.c_char)
bridge.GetAllSessions.restype = ctypes.POINTER(ctypes.c_char)
bridge.GetSession.restype = ctypes.POINTER(ctypes.c_char)
bridge.GetSessionAcquisitions.restype = ctypes.POINTER(ctypes.c_char)
bridge.AddSession.restype = ctypes.POINTER(ctypes.c_char)
bridge.AddSessionNote.restype = ctypes.POINTER(ctypes.c_char)
bridge.AddSessionTag.restype = ctypes.POINTER(ctypes.c_char)
bridge.ModifySession.restype = ctypes.POINTER(ctypes.c_char)
bridge.DeleteSession.restype = ctypes.POINTER(ctypes.c_char)
bridge.ModifySessionFile.restype = ctypes.POINTER(ctypes.c_char)
bridge.SetSessionFileInfo.restype = ctypes.POINTER(ctypes.c_char)
bridge.ReplaceSessionFileInfo.restype = ctypes.POINTER(ctypes.c_char)
bridge.DeleteSessionFileInfoFields.restype = ctypes.POINTER(ctypes.c_char)
bridge.UploadFileToSession.restype = ctypes.POINTER(ctypes.c_char)
bridge.DownloadFileFromSession.restype = ctypes.POINTER(ctypes.c_char)
bridge.GetAllProjects.restype = ctypes.POINTER(ctypes.c_char)
bridge.GetProject.restype = ctypes.POINTER(ctypes.c_char)
bridge.GetProjectSessions.restype = ctypes.POINTER(ctypes.c_char)
bridge.AddProject.restype = ctypes.POINTER(ctypes.c_char)
bridge.AddProjectNote.restype = ctypes.POINTER(ctypes.c_char)
bridge.AddProjectTag.restype = ctypes.POINTER(ctypes.c_char)
bridge.ModifyProject.restype = ctypes.POINTER(ctypes.c_char)
bridge.DeleteProject.restype = ctypes.POINTER(ctypes.c_char)
bridge.ModifyProjectFile.restype = ctypes.POINTER(ctypes.c_char)
bridge.SetProjectFileInfo.restype = ctypes.POINTER(ctypes.c_char)
bridge.ReplaceProjectFileInfo.restype = ctypes.POINTER(ctypes.c_char)
bridge.DeleteProjectFileInfoFields.restype = ctypes.POINTER(ctypes.c_char)
bridge.UploadFileToProject.restype = ctypes.POINTER(ctypes.c_char)
bridge.DownloadFileFromProject.restype = ctypes.POINTER(ctypes.c_char)
bridge.Search.restype = ctypes.POINTER(ctypes.c_char)
