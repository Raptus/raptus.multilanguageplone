raptus.multilanguageplone
=========================

Installation
------------

Login as Manager and try to install product raptus.multilanguageplone
To verify that nothing's wrong is happening

Login as manager
    >>> self.login()
    >>> self.setRoles(('Manager',))
    >>> from Products.CMFCore.utils import getToolByName
    
We set a multilingual site ('en' and 'fr'), with default lang = 'fr'  
    >>> langtool = getToolByName(self.portal, 'portal_languages')
    >>> langtool.manage_setLanguageSettings(supportedLanguages = ('en', 'fr'), defaultLanguage='fr') 

Install raptus.multilanguageplone via quickinstaller
    >>> qi = getToolByName(self.portal, 'portal_quickinstaller')
    >>> _ = qi.installProducts(products=['raptus.multilanguageplone'])
    >>> qi.isProductInstalled('raptus.multilanguageplone')
    True

See if raptus.multilanguagefields is installed
    >>> qi.isProductInstalled('raptus.multilanguagefields')
    True
    
Create a document
-----------------    