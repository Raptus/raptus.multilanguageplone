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
    
We set a multilingual site ('en' and 'fr'), with default lang = 'en', 
but using cookie negociation seems to be difficult in browser tests
so we force always_show_selector =1 and we use request negociation
    >>> langtool = getToolByName(self.portal, 'portal_languages')
    >>> langtool.manage_setLanguageSettings(supportedLanguages = ['en', 'fr'], defaultLanguage='fr') 
    >>> langtool.getSupportedLanguages()
    ['en', 'fr']
    >>> langtool.getDefaultLanguage()
    'fr'

Install raptus.multilanguageplone via quickinstaller
    >>> qi = getToolByName(self.portal, 'portal_quickinstaller')
    >>> _ = qi.installProducts(products=['raptus.multilanguageplone'])
    >>> qi.isProductInstalled('raptus.multilanguageplone')
    True

See if raptus.multilanguagefields is installed
    >>> qi.isProductInstalled('raptus.multilanguagefields')
    True
    
Create a multilingual document 
------------------------------    

Create a document with different values for each lang
    >>> self.portal.invokeFactory('Document', 'test-doc')
    'test-doc'
    >>> testdoc = getattr(self.portal, 'test-doc')

MultiLingual Fields are dicts using lang as key    
Edit multilingual title and text
    >>> multilingualtitle = {'fr' : 'Test doc fr', 'en' : 'Test doc en'}
    >>> multilingualtext = {'fr' : '<p>__FRENCH_CONTENT__</p>', 'en' : '<p>__ENGLISH_CONTENT__</p>'}
    >>> testdoc.edit( title = multilingualtitle, text= multilingualtext)

Publish test-doc
    >>> wf = getToolByName(self.portal, 'portal_workflow')
    >>> wf.doActionFor(testdoc, 'publish', comment='foo' )    

Get testdoc title, it must be french
    >>> testdoc.Title()
    'Test doc fr'

Get testdoc content, it must be french
    >>> testdoc.getText()
    '<p>__FRENCH_CONTENT__</p>'

Consultation tests in english
-----------------------------
It seems difficult to simulate a real language negociation in doctests
with the same user and without changing the portal default language
so ...
    >>> langtool.setDefaultLanguage('en')
    >>> self.portal.logout()    
    'http://nohost/logged_out'
    
Connect with default user, the accept-language HTTP ENV variable fixed to 'en'
The content response must be in english, and
must contain the english title and english content
    >>> from Products.PloneTestCase.setup import default_user, default_password
    >>> self.publish('%s/test-doc' %self.portal.absolute_url(1), 
    ...              '%s:%s' %(default_user,default_password), 
    ...              env={'HTTP_ACCEPT_LANGUAGE': 'en'})
    HTTPResponse(...
    ...lang="en"...
    ...Test doc en...
    ...<p>__ENGLISH_CONTENT__</p>...
    

Edition tests with testbrowser
------------------------------
It would be nice if we could test also lang negociation
with testbrowser but it seems complicated (see the problem below)
So we only test the multilingual edition form   

Set some variables for testbrowser connection
    >>> from Products.Five.testbrowser import Browser
    >>> browser = Browser()
    >>> portal_url = self.portal.absolute_url()
    >>> from Products.PloneTestCase.setup import portal_owner, default_password

I don't know why but testbrowser is broken with these classical
Plone connection lines on a multilingual plone site
If somebody can help me
"    >>> loginfield = browser.getControl(name=u'__ac_name')"
"    >>> loginfield.value = portal_owner"
"    >>> passfield = browser.getControl(name=u'__ac_password')"
"    >>> passfield.value = default_password"
"    >>> browser.getControl(name='submit').click()"


So connect as portal_owner using basic auth on zope instance
then on portal_url
    >>> browser.addHeader('Authorization', 'Basic portal_owner:portal_owner')
    >>> browser.addHeader('Accept-Language', 'en-us,en;q=0.7,fr;q=0.5')
    >>> browser.open(portal_url)
    
TODO ....   


