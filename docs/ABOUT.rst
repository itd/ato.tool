ATO Tool overview
+++++++++++++++++++++

The idea is to have a common place for sysadmins and cyber compliance
to reference controls, policy, exceptions, identify gaps,
and link to work instructions.

Reference the NIST 800-53 rev3 at these URLs:

* http://csrc.nist.gov/publications/nistpubs/800-53-Rev3/sp800-53-rev3-final_updated-errata_05-01-2010.pdf
* http://www.nist.gov/manuscript-publication-search.cfm?pub_id=903280

Note that 800-53 rev 4 is out as of April 30, 2013:

* http://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r4.pdf
* http://www.nist.gov/manuscript-publication-search.cfm?pub_id=913693


I'm going to assume that the tool will be used for dual purposes:

* Assist in defining risk and compliance-based operational policy awareness
  for systems admins, developers, etc. in the organization.

* Use the collected data to stream-line reporting
  (or at least data collection) for a particular ATO review.


About how the tool organizes information
============================================================

- Individual controls should be grouped by families.
  Since we often have to rely on NIST 800-53, the content organization
  should roughly follow those control groupings.

- In theory, those groupings would be added to map roughly to
  coordinate with the NIST 800-53 controls. Although, it could
  be used to manage any set of security control frameworks
  such as ISO/IEC 27001 AND 15408.

- Each control in this tool may have the following properties:

 * Title or Control ID - title (can be same as 800-53 control title)
 * 800-53 - Referenced 800-53 control & Title (AC-3 Access enforcement)
 * Control definition - the control definition
   (could be NIST 800-53 reference, PSP reference, etc.)
 * Supplemental control information
 * Policy - Description. May include min baseline standards,
   links to policy document(s), or references to policy document(s).
 * Deviation - deviations from controls with justifications
 * Gap - Is there a known gap? What is it? Justification?
 * Work Instruction - link to work instruction - how to - Config scripts, etc.
 * ATO response/todo instructions per period, e.g., 2013.
 * artifacts for that period - 0 or more files
 * Priority (low, moderate, high)

- The policy and work instructions can be links to other documents
  or web resources.

- There needs to be a specific ATO-Response instance that
  may be created per control.

- The specific ATO response content would need to be creatable and trackable
  to link with a specific ATO review instance and individual control.

- Revision history is enabled. All revisions to a control are tracked.

- Requiring revision comments may be optionally enforced.


Access to the tool
====================
Access to the tool can be limited to allow specific authenticated
individuals be given the editor role, while other authenticated users
have read-only. Anonymous users are not granted access.

There should be the option to have controls be in states:

* work in progress
* final


Content Types overview for the tool
========================================

**ComplianceTracker**
 The wrapper for the whole tool.
 I'm not sure it would need many fields.
 It would use standard workflows to control roles and permissions.
 There would be a view on it.

**ComplianceFamily**
 A grouping for compliance controls

**ComplianceControl**
 A specific control

**ReviewEvent**
 Describes a specific ATO or review event.
 A tracker may have one or more ReviewEvents.

**ControlReviewDetail**
 | A folderish type
 | Optionally addable in a ComplianceControl and linked to a ReviewEvent
   if data is required to be collected for an ATO event for that control.
 | Has a "Details" field.
 | Can contain artifacts [page, file, or image]


Views / Reports
=================
I envision a view at the top level that has [+] expandable sections
One for ATOs and another for ComplianceFamilies.

Clicking on a compliance family would show a list of the controls in that family.

Clicking on a control would switch to that control's "view".

Clicking on an ATO would expand to show some detail on that ATO.
A link in the expanded ATO section would go to an ATO view,
showing the ATO overview info and a list of ATOControlDetail folders
linked to that ATO.


Pre-configure option
=======================
I'd likely create a "profile" that would pre-configure
family groupings and controls based on the 800-53 outline.
Once one is created, creating a profile for updated revisions
or even other frameworks such as ISO/IEC 27001 should be doable
by others in the community.

