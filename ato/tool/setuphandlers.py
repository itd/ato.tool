from Products.CMFCore.utils import getToolByName
from plone import api
#from OFS.interfaces import IOrderedContainer
from zope.component import queryUtility
from Products.CMFPlone.utils import normalizeString
from Products.CMFPlone.utils import _createObjectByType
from plone.dexterity.utils import createContentInContainer
import transaction
from zope.component import getUtility
from plone.i18n.normalizer.interfaces import IIDNormalizer
#from Products.GenericSetup.upgrade import _upgrade_registry
#from Products.GenericSetup.registry import _profile_registry
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
import csv
import ato.tool

CSVROOT = "import_data"

ATO_FOLDER = 'ato'


def createComplianceTracker(portal):
    """
    """

    logger.info('START: create Compliance Tracker')
    container = portal
    ids = portal.objectIds()
    if ATO_FOLDER not in ids:
        _createObjectByType('ato.tool.compliancetracker', container,
                            id=ATO_FOLDER, title='ATO Compliance Tracker',
                            description='Track the organizations compliance')
        transaction.commit()
        logger.info('>> DONE: Compliance Tracker folder was created')
    else:
        logger.info('>> WHAT???? Compliance Tracker folder already exists!')
        # move folder to the top
        #ordered = IOrderedContainer(portal.SOMETHING, None)
        #container.moveObjectToPosition(ATO_FOLDER, 0)


def createComplianceFamilyFolders(portal):
    """
    """

    logger.info('>> START: create Compliance Family Folders')
    container = portal[ATO_FOLDER]
    ids = container.objectIds()
    norm = getUtility(IIDNormalizer)

    dat = ato.tool.import_data.SP800_53_compliance_family_classes.csv
    dat = open(dat, 'rb')
    reader = csv.DictReader(dat)
    headers = reader.fieldnames # ['ControlType', 'ControlClass', 'ClassName']

    for row in reader:
        #Handle blank lines:
        #row = [x.strip() for x in row if x]
        #if row:
        # trap for blank or bad lines
        try:
            controltype = row['ControlType']
            objtitle = row['ClassName']
            objid = row['ControlClass']
            objtitle = "%s, %s" % (obid, objtitle)
            objid = norm.normalize(objid)
            logger.info(' -- creating %s' % objid)
            createContentInContainer(container, 'ato.tool.compliancefamily',
                                     id=objid, title=objtitle,
                                     controltype=controltype)
            transaction.commit()
        except IndexError:
            print " -- blank or bad line.\n -- row = %s" % ';'.join(row)

    logger.info('>> DONE: Compliance Tracker folder was created')


def createComplianceControls(portal):
    """
    """

    logger.info('START: create Compliance Family Folders')
    container = portal[ATO_FOLDER]
    ids = container.objectIds()
    #import controlTypes

    if ATO_FOLDER not in ids:
        _createObjectByType('ato.tool.compliancetracker', container,
                            id=ATO_FOLDER, title='ATO Compliance Tracker',
                            description='Track the organizations compliance')
        transaction.commit()
        logger.info('>> DONE: Compliance Tracker folder was created')
    else:
        logger.info('>> WHAT???? Status folder already exists!')
        # move folder to the top
        #ordered = IOrderedContainer(portal.SOMETHING, None)
        #container.moveObjectToPosition(ATO_FOLDER, 0)


def publishStatusFolder(portal):
    """I'm assuming that I've already checked for and/or created
    the portal.status object. Now, setting the status to 'published'
    """
    logger.info('Attempting to publish status folder...')
    content = portal.users.status
    wftool = getToolByName(content, 'portal_workflow')
    if not wftool.getInfoFor(content, 'review_state', '') == 'published':
        wftool.doActionFor(content, action='publish')
    else:
        logger.info("status folder already in published state!")
    logger.info("I'm done publishing the status folder.")


def setStatusFolderView(portal):
    """set the default view of the status folder
    """

    portal_ids = portal.users.contentIds()
    if 'status' in portal_ids:
        portal.users.status.setLayout('@@status-view')
        logger.info('> status folder default view set to @@status-view')


def setStatusFolderContentRestrictions(context):
    """Restrict addable types in status Folder to hpcsystem')
    """

    site = api.portal.get()
    #if not 'status' in site.users.objectIds():
    #createStatusFolder(context)
    #else:
    sfolder = site.users._getOb('status')
    # Add type restrictions
    logger.info('Restricting addable types in status Folder to hpcsystem')
    sfolder.setConstrainTypesMode(1)
    sfolder.setLocallyAllowedTypes(['hpc.systemstatus.hpcsystem', ])
    sfolder.setImmediatelyAddableTypes(['hpc.systemstatus.hpcsystem'])


def delOldStatusFolder(portal):
    """ Delete the old status folder if it exists.
    """
    try:
        portal.manage_delObjects(['status'])
        transaction.commit()
        logger.info("Old status folder is now deleted.")
    except:
        logger.info("Looks like the old status folder is already gone.")


def addSystems(portal):
    """
    Adds some systems into the status folder
    """
    systems = [u'Peregrine', u'Red Mesa', u'Red Rock', u'Mass Storage']
    folder = portal.users.status
    wftool = getToolByName(portal, 'portal_workflow')
    # Add the systems
    for system in systems:
        # check to see if the system exists yet
        sid = normalizeString(system)
        if sid not in folder.objectIds():
            createContentInContainer(folder, 'hpc.systemstatus.hpcsystem',
                                     checkConstraints=False,
                                     title=system,
            )
            transaction.commit()
        #publish the systems
    obs = folder.objectIds()
    for obj in obs:
        ob = folder[obj]
        if not wftool.getInfoFor(ob, 'review_state', '') == 'published':
            wftool.doActionFor(ob, action='publish')
        else:
            logger.info("status folder already in published state!")
        logger.info("I'm done publishing the status folder.")


def importVarious(context):
    """Run the handlers for the default profile
    """

    logger.info('BEGIN: hpc.systemstatus installation...')
    if context.readDataFile('hpc.systemstatus_various.txt') is None:
        return
    portal = api.portal.get()
    createStatusFolder(portal)
    setStatusFolderView(portal)
    setStatusFolderContentRestrictions(context)
    publishStatusFolder(portal)
    delOldStatusFolder(portal)
    addSystems(portal)
    logger.info('END: hpc.systemstatus installation complete!')

