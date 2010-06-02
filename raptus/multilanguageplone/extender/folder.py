from zope.component import adapts
from plone.app.folder.folder import ATFolder

from base import DefaultExtender

class FolderExtender(DefaultExtender):
    adapts(ATFolder)