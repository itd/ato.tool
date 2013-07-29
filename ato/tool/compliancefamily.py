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

from ato.tool.vocabulary import ControlTypeVocab

# Interface class; used to define content-type schema.

class IComplianceFamily(form.Schema, IImageScaleTraversable):
    """
    A grouping of compliance controls
    """

    # title = schema.TextLine(
    #     title=_(u"Control family name"),
    #     required=True,
    # )
    #
    # description = schema.Text(
    #     title=_(u"Brief description"),
    #     required=False,
    # )

    info = RichText(
        title=_(u"Supporting Info"),
        description=_(u"""List any high-level issues regarding
            this control. Include links and references to other
            documents if appropriate."""),
        required=False,
    )

    controltype = schema.Choice(
        title=_(u"Control Type"),
        description=_(u"""."""),
        vocabulary=ControlTypeVocab,
        default=u"none"
    )


    # If you want a schema-defined interface, delete the form.model
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/compliancefamily.xml to define the content type
    # and add directives here as necessary.

    # form.model("models/compliancefamily.xml")


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class ComplianceFamily(dexterity.Container):
    grok.implements(IComplianceFamily)

    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# compliancefamily_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class View(grok.View):
    grok.context(IComplianceFamily)
    grok.require('zope2.View')

    grok.name('view')
