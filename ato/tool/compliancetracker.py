from five import grok
from plone.directives import dexterity, form

from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from zope.interface import invariant, Invalid

from z3c.form import group, field

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from plone.app.textfield import RichText

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from ato.tool import MessageFactory as _


# Interface class; used to define content-type schema.

class IComplianceTracker(form.Schema, IImageScaleTraversable):
    """
    Master container for a compliance tracker
    """

    # title = schema.TextLine(
    #     title=_(u"Title"),
    #     description=_(u"Compliance Tracker Title")
    # )
    #
    # description = schema.Text(
    #     title=_(u"Description"),
    #     description=_("Brief summary of this tracker")
    # )

    details = RichText(
        title=_(u"Tracker Details"),
        description=_(u"Longer form overview of this tracker"),
        required=False,
    )

    neftimport = schema.Bool(
        title=_(u"Imported"),
        description=_(u"If set to true, NIST 800 53 content "
            "will attempt to be imported"),
        default=False,
    )
class ComplianceTracker(dexterity.Container):
    grok.implements(IComplianceTracker)

    # Add your class methods and properties here



class View(grok.View):
    grok.context(IComplianceTracker)
    grok.require('zope2.View')

    grok.name('view')
