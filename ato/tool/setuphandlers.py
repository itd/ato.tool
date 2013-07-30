import csv
import transaction
import logging

from zope.component import getUtility

from plone import api
from plone.dexterity.utils import createContentInContainer
from plone.i18n.normalizer.interfaces import IIDNormalizer

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import normalizeString
from Products.CMFPlone.utils import _createObjectByType

import ato.tool

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

CSVROOT = "import_data"
ATO_FOLDER = 'ato'


def createComplianceTracker(portal):
    logger.info('START: create Compliance Tracker')
    container = portal
    ids = portal.objectIds()
    if ATO_FOLDER not in ids: #ato.tool.compliancetracker
        _createObjectByType('ComplianceTracker', container,
                            id=ATO_FOLDER, title='ATO Compliance Tracker',
                            description="Track the organization's cyber "
                            "security compliance.")
        transaction.commit()
        logger.info('>> DONE: Compliance Tracker folder was created')
    else:
        logger.info('>> WHAT?! Compliance Tracker "ATO" already exists!')
        # move folder to the top
        #ordered = IOrderedContainer(portal.SOMETHING, None)
        #container.moveObjectToPosition(ATO_FOLDER, 0)


def createComplianceFamilyFolders(portal):
    logger.info('>> START: create Compliance Family Folders')
    container = portal[ATO_FOLDER]
    ids = container.objectIds()
    norm = getUtility(IIDNormalizer)

    dat = ato.tool.import_data.SP800_53_compliance_family_classes.csv
    dat = open(dat, 'rb')
    reader = csv.DictReader(dat)
    #headers = reader.fieldnames # ['ControlType', 'ControlClass', 'ClassName']
    for row in reader:
        #Handle blank lines:
        #row = [x.strip() for x in row if x]
        #if row:
        # trap for blank or bad lines
        try:
            controltype = row['ControlType']
            objtitle = row['ClassName']
            objid = row['ControlClass']
            objtitle = "%s, %s" % (objid, objtitle)
            objid = norm.normalize(objid)
            logger.info(' -- creating %s' % objid)
            if not container[objid]:
                createContentInContainer(container, 'ato.tool.compliancefamily',
                                         id=objid, title=objtitle,
                                         controltype=controltype)
            transaction.commit()
        except IndexError:
            print " -- blank or bad line.\n -- row = %s" % ';'.join(row)
            pass
        else:
            logger.info(' -- WARNING: %s already exists' % objid)

    logger.info('>> DONE: Compliance Family folders created.')


def createComplianceControls(portal):
    """
    """
    logger.info('>> START: creating individual Compliance controls')
    container = portal[ATO_FOLDER]
    norm = getUtility(IIDNormalizer)

    dat = ato.tool.import_data.SP800_53_controls.csv
    dat = open(dat, 'rb')
    reader = csv.DictReader(dat)
    headers = reader.fieldnames
    #['controlclass','controlid','controltitle','controldetail']
    for row in reader:
        cfamily = row['controlclass']
        controlid = row['controlid']
        ctitle = row['controltitle']
        cdetail = row['controldetail']
        #Handle blank lines:
        row = [x.strip() for x in row if x]
        if row:
            # assume the compliance family folders are already there
            container = container[cfamily]
            ids = container.objectIds()
            # Don't want object ids like "SC-09 (1)". So, normalize.
            cid = norm.normalize(controlid)
            if cid not in ids:
                cref = "%s - %s" % (controlid, ctitle)
                createContentInContainer(container, 'ato.tool.compliancecontrol',
                                    id=cid, title=ctitle, controlref=cref,
                                    controlinfo=cdetail)
                transaction.commit()
                logger.info('-- Compliance control item %s created' %ctitle)
            else:
                logger.info('>> WHAT???? Status folder already exists!')
                # move folder to the top
                #ordered = IOrderedContainer(portal.SOMETHING, None)
                #container.moveObjectToPosition(ATO_FOLDER, 0)


def publishItem(portal, item):
    """I'm assuming that I've already checked for and/or created
    the portal.status object. Now, setting the status to 'published'
    """
    logger.info('-- Attempting to publish  item')
    content = item
    wftool = getToolByName(content, 'portal_workflow')
    if not wftool.getInfoFor(content, 'review_state', '') == 'published':
        wftool.doActionFor(content, action='publish')
    else:
        logger.info("WARN: item already in published state!")
    logger.info(">> Done publishing the item.")


def setTrackerFolderView(portal):
    """set the default view of the compliance tracker folder
    """

    portal_ids = portal.users.contentIds()
    if ATO_FOLDER in portal_ids:
        portal.users.status.setLayout('@@SOME-view')
        logger.info('> folder default view set to @@SOME-view')


def setATOFolderContentRestrictions(context):
    """Restrict addable types in ato Folder ')
    """

    site = api.portal.get()
    #if not 'status' in site.users.objectIds():
    #createStatusFolder(context)
    #else:
    sfolder = site.users._getOb(ATO_FOLDER)
    # Add type restrictions
    logger.info('Restricting addable types in the ATO Folder')
    sfolder.setConstrainTypesMode(1)
    #sfolder.setLocallyAllowedTypes(['ato.tool.compliancefamily', ])
    sfolder.setImmediatelyAddableTypes(['ato.tool.compliancefamily'])


def delOldFolder(portal):
    """ Delete the old status folder if it exists.
    """
    try:
        portal.manage_delObjects([ATO_FOLDER])
        transaction.commit()
        logger.info("Old ato folder is now deleted.")
    except:
        logger.info("Looks like the old ato folder is already gone.")


def importATOContent(context):
    """Run the handlers for the builder profile
    """

    logger.info('BEGIN: Import 800-53 ATO Builder content.')
    if context.readDataFile('ato.tool.builder_various.txt') is None:
        return
    portal = api.portal.get()
    createComplianceTracker(portal)
    import ipdb; ipdb.set_trace()

    createComplianceFamilyFolders(portal)
    import ipdb; ipdb.set_trace()

    createComplianceControls(portal)
    import ipdb; ipdb.set_trace()

    setTrackerFolderView(portal)
    logger.info('END: hpc.systemstatus installation complete!')

