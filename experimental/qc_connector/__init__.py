#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
Module QCCONNECTOR
A simple QC Toolbox module
Docstrings: http://www.python.org/dev/peps/pep-0257/
"""

import logging
from HTMLParser import HTMLParser
from win32com.client import Dispatch

# Log Configuration
FORMAT = "%(levelname)-4s %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)

class QCConnector(object):
    """QCConnector Class"""

    def __init__(self, url):
        """QCConnector Constructor
        :param url quality center server URL"""
        assert url, "QC Server URL is not defined"
        self.url = url
        self.username = None
        self.domain = None
        self.project = None
        self.tree_manager = None
        self.test_folder_factory = None
        logging.info("Initializing connection to %s", url)
        self.quality_center = Dispatch("TDApiOle80.TDConnection")
        self.quality_center.InitConnection(url)
        logging.info("Connection is ready")

    def login(self, username, password):
        """Login to quality center server
        :param username client username
        :param password client password"""
        assert username, "Username is not defined"
        assert password, "Password is not defined"
        self.username = username
        self.quality_center.Login(username, password)
        logging.info("User %s is logged in", username)

    def connect(self, domain, project):
        """Connect to the quality center server
        :param domain project domain
        :param project project name"""
        assert domain, "Project domain is not defined"
        assert project, "Project name is not defined"
        self.domain = domain
        self.project = project
        logging.info("Connecting to %s", self.url)
        logging.info("\tDomain: %s", self.domain)
        logging.info("\tProject: %s", self.project)
        self.quality_center.Connect(domain, project)
        logging.info("User %s is connected", self.username)

    def login_and_connect(self, username, password, domain, project):
        """Login and connect to the quality center server
        :param username client username
        :param password client password
        :param domain project domain
        :param project project name"""
        self.login(username, password)
        self.connect(domain, project)

    def logout(self):
        """Logout from the quality center server"""
        self.quality_center.Logout()
        logging.info("User %s has logged out", self.username)

    def disconnect(self):
        """Disconnect from the quality center server"""
        logging.info("Disconnecting from %s", self.url)
        self.quality_center.Disconnect()

    def disconnect_and_logout(self):
        """Logout and disconnect from the quality center server"""
        self.disconnect()
        self.logout()

    def reconnect(self, username, password):
        """Reconnect to the quality center server
        :param username client username
        :param password client password"""
        self.login(username, password)
        self.connect(self.domain, self.project)

    def reset_connection(self):
        """Reset quality center connector"""
        self.disconnect()
        self.logout()
        logging.info("Resetting username")
        self.username = None
        logging.info("Resetting domain")
        self.domain = None
        logging.info("Resetting project")
        self.project = None
        self.__init__(self.url)

    def get_tree_manager(self):
        """Tree Manager"""
        logging.info("Initializing QC Tree Manager")
        self.tree_manager = self.quality_center.TreeManager
        return self.tree_manager

    def get_test_folder_factory(self):
        """Test Folder Factory"""
        logging.info("Initializing QC Test Folder Factory")
        self.test_folder_factory = self.quality_center.TestFolderFactory
        return self.test_folder_factory

    def get_node_by_path(self, node_path):
        """Get Node By Path
        :param node_path quality center node path"""
        assert node_path, "Node path is not defined"
        if self.tree_manager:
            logging.info("Accessing node %s", node_path)
            return self.tree_manager.NodeByPath(node_path)
        else:
            logging.error("No tree manager defined.")
            logging.error("Call method QCConnector.get_tree_manager")
            return None

    def get_filtered_children(self, father_id, filt):
        """Get Filtered Children
        :param father_id parent identified
        :param filt children filter"""
        assert father_id, "Father Node ID is not defined"
        assert filt, "Children filter is not defined"
        if self.test_folder_factory:
            logging.info("Filtering %s child nodes", father_id)
            return self.test_folder_factory.GetFilteredChildren(father_id, filt)
        else:
            logging.error("No test node factory defined.")
            logging.error("Call method QCConnector.get_test_folder_factory")
            return None

    def get_children_count(self, node_path):
        """Get child count
        :param node_path parent node path"""
        parent_node = self.get_node_by_path(node_path)
        print parent_node.Count

class MLStripper(HTMLParser):
    """MLStripper Class
    For more information, please check:
    Dipanjan Sarkar (2016) - Text Analytics with Python and
    http://stackoverflow.com/questions/753052/strip-html-from-strings-in-python"""

    def __init__(self):
        """MLStripper Constructor"""
        HTMLParser.__init__()
        self.fed = []

    def handle_data(self, data):
        """Handle data
        :param data"""
        self.fed.append(data)

    def get_data(self):
        """Get Data"""
        return self.fed

def strip_tags(html):
    """Strip HTML Tags
    :param html HTML content"""
    parser = HTMLParser()
    stripper = MLStripper()
    html = parser.unescape(html)
    stripper.feed(html)
    return stripper.get_data()
