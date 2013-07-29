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

from ato.tool.vocabulary import ControlPriorityVocab
from ato.tool.vocabulary import ControlBaselineVocab

from ato.tool.compliancefamily import IComplianceFamily
from ato.tool import MessageFactory as _


# Interface class; used to define content-type schema.

class IComplianceControl(form.Schema, IImageScaleTraversable):
    """
    A specific security control

    Each control in this tool may have the following properties:

    * Title or Control ID - title (can be same as 800-53 control title)
    * 800-53 - Referenced 800-53 control & Title (AC-3 Access enforcement)
    * Control definition - the control definition
      (could be NIST 800-53 reference, PSP reference, etc.)
    * Supplemental control information
    * Policy - Description. May include min baseline standards,
      links to policy document(s), or references to policy document(s).
    * Deviation - deviations from controls with justifications
    * Gap - Is there a known gap? What is it? Justification?
    * Work Instruction - link to work instruction, how to, Config scripts, etc.
    * ATO response/todo instructions per period, e.g., 2013.
    * artifacts for that period - 0 or more files
    * baselines [low, moderate, high]
    * priority [0,1,2,3]
    Note: Only including a sub-set of these for my current needs.

     """
    # title = schema.TextLine(
    #     title=_(u"Control title or ID"),
    #     required=True,
    # )
    #
    # description = schema.Text(
    #     title=_(u"Brief description"),
    #     required=False,
    # )

    controlref = schema.Text(
        title=_(u"Control Reference"),
        description=_(u"""Referenced Control & Title.
                      Example: (AC-3 Access enforcement)"""),
        required=False,
    )

    controlinfo = RichText(
        title=_(u"Control detail"),
        description=_(u"""Optionally include the detailed description
            from the referenced control."""),
        required=False,
    )

    #Priority [P0 - P3]
    controlpriority = schema.Choice(
        title=_(u"Priority"),
        description=_(u"""The priority of the referenced control.
        A Priority Code 1 [P1] control has a higher priority for
        implementation than a Priority Code 2 [P2] control."""),
        vocabulary=ControlPriorityVocab,
        default=0
    )

    #(low, moderate, high)
    controlbaseline = schema.Choice(
        title=_(u"Control Baseline"),
        description=_(u"""The priority of the referenced control.
        A Priority Code 1 [P1] control has a higher priority for
        implementation than a Priority Code 2 [P2] control."""),
        vocabulary=ControlBaselineVocab,
        default=0
    )

    policy = RichText(
        title=_(u"Policy"),
        description=_(u"""Details about our policy for this control.
            Include links where appropriate."""),
        required=False,
    )

    deviation = RichText(
        title=_(u"Deviation"),
        description=_(u"""Are there deviations from the controls?
            Known gaps? enter details with justifications where
            appropriate."""),
        required=False,
    )

    workinstruction = schema.TextLine(
        title=_(u"Work Instruction"),
        description=_(u"Link/URL to work instruction."),
        required=False,
    )

    compliancefamily = RelationList(
        title=_(u"Compliance Family/Class"),
        description=_(u"""To what organizational
            Compliance Family does this control belong?"""),

        value_type=RelationChoice(
            source=ObjPathSourceBinder(
                object_provides=IComplianceFamily.__identifier__
            ),
        ),
        required=True,
    )


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class ComplianceControl(dexterity.Container):
    grok.implements(IComplianceControl)

    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# compliancecontrol_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class ComplianceView(grok.View):
    grok.context(IComplianceControl)
    grok.require('zope2.View')

    grok.name('complianceview')
