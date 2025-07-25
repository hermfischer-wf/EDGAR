'''
This is a collective work.
See COPYRIGHT.md for copyright information for original work.
Subsequent validations and enhancements created by staff of the U.S. Securities and Exchange Commission.
Data and content created by government employees within the scope of their employment are not subject
to domestic copyright protection. 17 U.S.C. 105.
Implementation of DQC rules invokes https://xbrl.us/dqc-license and https://xbrl.us/dqc-patent.

Input file parameters may be in JSON (without newlines for pretty printing as below):


[ {# current fields in JSON structure from Arelle Wrapper, per instance
   "file": "file path to instance or html"
      or "ixds":[{"file": "file path to first html"},...]
   "cik": "1234567890",
   "cikNameList": { "cik1": "name1", "cik2":"name2", "cik3":"name3"...},
   "submissionType" : "SDR-A",
   "exhibitType": "EX-99.K", # this is a legal term, separate from attachmentDocumentType (below)
   "itemsList": [] # array of items, e.g. ["5.03"] (either array of strings blank-separated items in string)
   "accessionNumber":"0001125840-15-000159" ,
   # new fields
   "periodOfReport": "mm-dd-yyyy",
   "entityRegistration.fyEnd": "mm/dd", # the FY End value from entity (CIK) registration
   "entity.repFileNum": file number from entity (CIK) registration
   "submissionHeader.fyEnd": "mm/dd", # the FY End value from submission header
   "voluntaryFilerFlag": true/false, # JSON Boolean, string Yes/No, yes/no, Y/N, y/n or absent
   "wellKnownSeasonedIssuerFlag": true/false, # JSON Boolean, string Yes/No, yes/no, Y/N, y/n or absent
   "shellCompanyFlag": true/false, true/false, # JSON Boolean, string Yes/No, yes/no, Y/N, y/n or absent
   "acceleratedFilerStatus": true/false, # JSON Boolean, string Yes/No, yes/no, Y/N, y/n or absent
   "smallBusinessFlag": true/false, # JSON Boolean, string Yes/No, yes/no, Y/N, y/n or absent
   "closedEndedCompanyFlag": true/false, # JSON Boolean, string Yes/No, yes/no, Y/N, y/n or absent
   "emergingGrowthCompanyFlag": true/false, # JSON Boolean, string Yes/No, yes/no, Y/N, y/n or absent
   "exTransitionPeriodFlag": true/false, # JSON Boolean, string Yes/No, yes/no, Y/N, y/n or absent
   # filer - use "cik" above
   "invCompanyType": "N-1A" # from table of investment company types
   "rptIncludeAllSeriesFlag": true/false, # JSON Boolean, string Yes/No, yes/no, Y/N, y/n or absent
   "rptSeriesClassInfo.seriesIds": ["S0000990666", ...] # list of EDGAR seriesId values
   "newClass2.seriesIds": [] # //seriesId xpath result on submission headers
   "rptIncludeAllClassesFlag": true/false, # JSON Boolean, string Yes/No, yes/no, Y/N, y/n or absent
   "rptSeriesClassInfo.classIds": ["C000000123", ...] # list of EDGAR classId values
   "newClass2.classIds": [] # //classId xpath result on submission headers
   "saveCoverFacts": test environment file into which to save JSON output
   # CEF forms
   "eligibleFundFlag": true/false, # JSON Boolean, string Yes/No, yes/no, Y/N, y/n or absent
   "pursuantGeneralInstructionFlag": true/false, # JSON Boolean, string Yes/No, yes/no, Y/N, y/n or absent
   "filerNewRegistrantFlag": true/false, # JSON Boolean, string Yes/No, yes/no, Y/N, y/n or absent
   # Test/debug fields
   datetimeForTesting: xml-syntax datetime to override clock time for test/debug purposes
   dqcRuleFilter: null or absent for all Python-implemented DQC rules for us-gaap pre-2025, else for the DQCRT subset of XULE rules,
       if not null, for Python implemented DQC rules, a regular expression to filter which rules run
       (e.g. "DQC.US.00(04|15)" ), but not including the id suffix (which is not filterable)

       If parameter is absent and config.xml for disclosureSystem options specifies a dqc-rule-filter, it will be in effect.

       For XULE implementations XULE:yyyy specifies to run XULE for taxonomies beginning with year yyyy (default 2025).
       E.g. "XULE:2026|DQC.US.00(04|15)" would specify running XULE-implemented validation for 2026 or later US-GAAP else
       run only the python-implmented rules DQC.US.0004 and DQC.US.0015.  Or to block XULE and match all Python-coded rules "XULE:9999|.*"
       When running XULE-implemented rules the following additional entries activate XULE features
           XULE_RUN_ALL - instead of DQCRT subset of DQC rules, run the full set.  (Xule --xule-run-only and --xule-run-only-pattern override this, if provided)
           XULE_time:secs - print xule rule run times for rules > 1 sec on stdout (Xule --xule-time overrides this)
           XULE_debug - print xule debug on stdout (Xule --xule-debug overrides this)
           XULE_trace - print xule trace on stdout (Xule --xule-trace overrides this)

           e.g. XULE:2023|XULE_time:.5|XULE_debug|.* to run XULE after 2023 with timings over 1/2 sec and debug to stdout, else all python-coded rules
   # fee table instance validations (only):
   "attachmentDocumentType": "EX-FILINGS FEES",  # this field is mandatory for fee table instance validations else instance will be validated as a financial report
   # attachmentDocumentType must match an entry in feeTaggingExhibitTypes (Consts.py) for instance to be recognized as a fee table instance
   "submissionType" : "S-1", # this field is mandatory for fee table instance validations
   "feeRate": "0.000130" # decimal number expressed in string - feeRate on the filing date
   "feeValuesFromFacts": true # save fee facts in json
   "saveFeeFacts": test environment file into which to save JSON output
   # EX-26 attachment document types
   "attachmentDocumentType": "EX-26",  # this field is mandatory for EX-26 validations else instance will be validated as a financial report
   "fileNumber": "333-12345", # the file number for amending submission
   # SBSEF attachment document types
   "securityClassification": "confidential" when filer has requested confidential treatment on this exhibit file
   },
 {"file": "file 2"...
]

For test case operation, the above fields accepted from testcase variation:
  <data>
     <parameter name="cikName" datatype="xs:string" value="cik1:name1" />
     <parameter name="cikName" datatype="xs:string" value="cik2:name2" />
     <parameter name="cikName" datatype="xs:string" value="cik3:name3" />
     <parameter name="submissionType" datatype="xs:string" value="8-K" />
     <parameter name="periodOfReport" datatype="xs:string" value="12-31-2017" />
     <parameter name="voluntaryFilerFlag" datatype="xs:boolean" value="true" />
     <parameter name="coregCikFileNumber" datatype="xs:string" value="cik1:fileNbr1" />
     <parameter name="coregCikFileNumber" datatype="xs:string" value="cik2:fileNbr2" />
     <parameter name="coregCikFileNumber" datatype="xs:string" value="cik3:fileNbr3" />
     <parameter name="sroId" datatype="xs:string" value="NASD" />
     <parameter name="sroId" datatype="xs:string" value="NYSE" />
     ...
     <instance readMeFirst="true">e9999999ng-20081231.xml</instance>
   <data>

(Accession number is only needed for those EdgarRenderer output transformations of
FilingSummary.xml which require it as a parameter (such as EDGAR's internal workstations,
which have a database that requires accession number as part of the query string to retrieve
a file of a submission.)

On Windows, the input file argument must be specially quoted if passed in via Java
due to a Java bug on Windows shell interface (without the newlines for pretty printing below):

"[{\"file\":\"z:\\Documents\\dir\\gpc_gd1-20130930.htm\",
    \"cik\": \"0000350001\",
    \"cikNameList\": {\"0000350001\":\"BIG FUND TRUST CO\"},
    \"submissionType\":\"SDR-A\", \"attachmentDocumentType\":\"EX-99.K SDR.INS\"}]"

To build cached deprecated concepts files (requires internet access):
   First delete any resources/*deprecated-concept.json which you want to rebuild
   arelleCmdLine --plugin validate/EFM --build-deprecated-concepts-file

In GUI mode please use formula parameters dialog to emulate the above.  The parameters are named as above (with no prefix), and
an additional EdgarRenderer parameters:
   noLogsInSummary or includeLogsInSummary (default) (this parameter does not need a value, just presence)
The parameters with array values are entered to the GUI as blank-separated strings (no quotes):
   itemsList could be 5.03 6.99
   rptSeriesClassInfo.seriesIds could be S0000990666 S0000990777 S0000990888
   classIDs could be C000000123 C000000124 C000000125


For GUI mode there are two ways to set rendering output, (1) by formula parameter and (2) by GUI view menu.
  If both formula parameters summaryXslt and reportXslt are provided they override use of the GUI menu setting
  ("view/Workstation Redline Mode"):
     summaryXslt (use EdgarWorkstationSummarize.xslt to emulate EDGAR workstation)
     reportXslt (use EdgarWorkstationInstanceReport.xslt to emulate EDGAR workstation)
     ixRedline (when emulating EDGAR workstation, true specifies showing workstation inline XBRL redlines)
  Otherwise menu entry view/Workstation Redline Mode, when checked, selects Edgar Workstation xslt's and ixRedline as above.

Test cases can verify via introduce processing flow exceptions, that the exceptions are caught, logged,
and that processing flow completes as expected given the remaining processing which the exception terminated.

	A test case inline XBRL document may have a processing instruction of this format:
		<?arelle-unit-test location="EFM/Filing.py#validateFiling_start" action="AssertionError"?>
	This will cause code in EFM/Filing.py (search on the location string) to raise an assertion error
	which would correspond to the expected unit test code (see conformance test i003004gw testcase and
	htm files).

	The currently implemented assertion test locations are
		Filing, before starting first IXDS validation: EFM/Filing.py#validateFiling_start
		Filing, after completion of first IXDS validation: EFM/Filing.py#validateFiling_end
		Rendering, after pass 1 of all filings EdgarRenderer/__init__.py#filingPass1
		Rendering, after completion of all filings EdgarRenderer/__init__.py#filingEnd

'''
import os, io, json, zipfile, logging
jsonIndent = 1  # None for most compact, 0 for left aligned
from decimal import Decimal, InvalidOperation
from lxml.etree import XML, XMLSyntaxError
from arelle import ModelDocument, ModelValue, XmlUtil, FileSource
from arelle.ModelDocument import Type
from arelle.ModelInstanceObject import ModelFact
from arelle.ModelValue import qname
from arelle.PluginManager import pluginClassMethods  # , pluginMethodsForClasses, modulePluginInfos
from arelle.PythonUtil import flattenSequence
from arelle.UrlUtil import authority, relativeUri
from arelle.ValidateFilingText import referencedFiles
from arelle.Version import authorLabel, copyrightLabel
from arelle.XmlValidateConst import VALID
from .Document import checkDTSdocument
from .Consts import (feeTagEltsNotRelevelable, feeTagMessageCodesRelevelable, feeTaggingAttachmentDocumentTypePattern,
                     supplementalAttachmentDocumentTypesPattern, exhibitTypesStrippingOnErrorPattern,
                     exhibitTypesPrivateNotDisseminated, primaryAttachmentDocumentTypesPattern)
from .Filing import validateFiling
from .MessageNumericId import messageNumericId
from .XuleInterface import (menuTools as xuleMenuTools, validateMenuTools as xuleValidateMenuTools,
                            cntrlrCmdLineUtilityRun as xuleCntrlrCmdLineUtilityRun,
                            cmdOptions as xuleCmdOptions, init as xuleInit, close as xuleClose,
                            blockXuleValidateFinally, xule_error_code_pattern)
import regex as re
from collections import defaultdict


def dislosureSystemTypes(disclosureSystem, *args, **kwargs):
    # return ((disclosure system name, variable name), ...)
    return (("EFM", "EFMplugin"),)

def disclosureSystemConfigURL(disclosureSystem, *args, **kwargs):
    return os.path.join(os.path.dirname(__file__), "config.xml")

def validateXbrlStart(val, parameters=None, *args, **kwargs):
    val.validateEFMplugin = val.validateDisclosureSystem and getattr(val.disclosureSystem, "EFMplugin", False)
    if not (val.validateEFMplugin):
        return

    val.params = {}
    parameterNames = {"CIK", "cik", "cikList", "cikNameList", "submissionType", "exhibitType", "attachmentDocumentType", # CIK or cik both allowed
                      "itemsList", "accessionNumber", "entity.repFileNum",
                      "periodOfReport", "entityRegistration.fyEnd", "submissionHeader.fyEnd", "voluntaryFilerFlag",
                      "wellKnownSeasonedIssuerFlag", "shellCompanyFlag", "acceleratedFilerStatus", "smallBusinessFlag",
                      "emergingGrowthCompanyFlag", "exTransitionPeriodFlag", "invCompanyType",
                      "rptIncludeAllSeriesFlag", "rptSeriesClassInfo.seriesIds", "newClass2.seriesIds",
                      "rptIncludeAllClassesFlag", "rptSeriesClassInfo.classIds", "newClass2.classIds",
                      "eligibleFundFlag", "pursuantGeneralInstructionFlag", "filerNewRegistrantFlag",
                      "datetimeForTesting", "dqcRuleFilter", "saveCoverFacts",
                      "feeRate", "feeValuesFromFacts", "saveFeeFacts", "fiscalYearEnd", "intrstRate", "issrNm", "fileNumber", "closedEndedCompanyFlag"}
    boolParameterNames = {"voluntaryFilerFlag", "wellKnownSeasonedIssuerFlag", "shellCompanyFlag", "acceleratedFilerStatus",
                          "smallBusinessFlag", "emergingGrowthCompanyFlag", "exTransitionPeriodFlag", "rptIncludeAllSeriesFlag",
                          "filerNewRegistrantFlag", "pursuantGeneralInstructionFlag", "eligibleFundFlag", "closedEndedCompanyFlag"}
    parameterEisFileTags = {
        "cik":["depositorId", "cik", "filerId"],
        "submissionType": "submissionType",
        "itemsList": "item",
        "periodOfReport": "periodOfReport",
        #"headerFyEnd": ?,
        #"voluntaryFilerFlag": ?,
        "wellKnownSeasonedIssuerFlag": "wellKnownSeasonedIssuerFlag",
        #"shellCompanyFlag": ?,
        "acceleratedFilerStatus": "acceleratedFilerStatus",
        "smallBusinessFlag": "smallBusinessFlag",
        "emergingGrowthCompanyFlag": "emergingGrowthCompanyFlag",
        "exTransitionPeriodFlag": "exTransitionPeriodFlag",
        "invCompanyType": "invCompany",
        #"rptIncludeAllSeriesFlag": ?,
        #"rptSeriesClassInfo.seriesIds": ?,
        #"newClass2.seriesIds": ?,
        "filerNewRegistrantFlag": "filerNewRegistrantFlag",
        "pursuantGeneralInstructionFlag": "pursuantGeneralInstructionFlag",
        "eligibleFundFlag": "eligibleFundFlag",
        "feeRate": "feeRate",
    }
    # retrieve any EIS file parameters first
    if val.modelXbrl.fileSource and val.modelXbrl.fileSource.isEis and hasattr(val.modelXbrl.fileSource, "eisDocument"):
        eisDoc = val.modelXbrl.fileSource.eisDocument
        for paramName, eisEltNames in parameterEisFileTags.items():
            paramQName = ModelValue.qname(paramName,noPrefixIsNoNamespace=True)
            for eisElt in eisDoc.iter(*("{*}"+e for e in flattenSequence(eisEltNames))):
                if paramName in ("itemsList",):
                    parameters.setdefault(paramQName, []).append(eisElt.text)
                else:
                    parameters[paramQName] = ("", "".join(eisElt.itertext()).strip())
    if parameters: # parameter-provided CIKs and registrant names
        for paramQName, p in parameters.items():
            paramName = paramQName.localName # allow parameters to be in any namespace (no xmlns="" required)
            if paramName in parameterNames and p and len(p) == 2 and p[1] not in ("null", "None", None):
                v = p[1] # formula dialog and cmd line formula parameters may need type conversion
                if isinstance(v, str):
                    if paramName in boolParameterNames:
                        v = {"true":True, "false":False}.get(v, v)
                    elif paramName in {"itemsList", "rptSeriesClassInfo.seriesIds", "newClass2.seriesIds", "rptSeriesClassInfo.classIds", "newClass2.classIds"}:
                        v = v.split()
                    elif paramName == "feeRate":
                        if isinstance(v, float):
                            val.modelXbrl.warning("arelle.Parameters",
                                _("parameter %(name)s has should not have float value %(value)s"),
                                modelXbrl=val.modelXbrl, name=paramName, value=v)
                        try:
                            v = Decimal(v)
                        except (ValueError, InvalidOperation):
                            val.modelXbrl.error("arelle.Parameters",
                                _("parameter %(name)s has non-decimal value %(value)s"),
                                modelXbrl=val.modelXbrl, name=paramName, value=v)
                            continue # don't use parameter
                val.params[paramName] = v
        if "CIK" in val.params: # change to lower case key
            val.params["cik"] = val.params["CIK"]
            del val.params["CIK"]
        for paramName, p in parameters.items(): # allow ELOparams to be in any namespace (no xmlns="" required)
            if paramName and paramName.localName == "ELOparams" and len(p) == 2 and p[1] not in ("null", "None", None):
                try:
                    for key, value in json.loads(p[1]).items():
                        if key == "feeRate":
                            try:
                                value = Decimal(value)
                            except (ValueError, InvalidOperation):
                                val.modelXbrl.error("arelle.Parameters",
                                    _("parameter %(name)s has non-decimal value %(value)s"),
                                    modelXbrl=val.modelXbrl, name=key, value=value)
                                continue # don't use parameter
                        val.params[{"CIK":"cik"}.get(key,key)] = value # change upper case CIK to lower case
                except (ValueError, AttributeError, TypeError):
                    val.modelXbrl.error("arelle.testcaseVariationParameters",
                        _("parameter ELOparams has malformed JSON %(json)s object"),
                        modelXbrl=val.modelXbrl, json=p[1][:100])
                break
    # parameters may also come from report entryPoint (such as attachmentDocumentType for SDR)
    if hasattr(val.modelXbrl.modelManager, "efmFiling"):
        efmFiling = val.modelXbrl.modelManager.efmFiling
        if efmFiling.reports: # possible that there are no reports
            entryPoint = efmFiling.reports[-1].entryPoint
            for paramName in parameterNames: # cik is lower case here
                v = entryPoint.get(paramName)
                if paramName in boolParameterNames:
                    v = {"true":True, "false":False}.get(v, v)
                elif paramName == "feeRate" and v not in (None, ""):
                    if isinstance(v, float):
                        val.modelXbrl.warning("arelle.Parameters",
                            _("parameter %(name)s should not have float value %(value)s"),
                            modelXbrl=val.modelXbrl, name=paramName, value=v)
                    try:
                        v = Decimal(v)
                    except (ValueError, InvalidOperation):
                        val.modelXbrl.error("arelle.Parameters",
                            _("parameter %(name)s has non-decimal value %(value)s"),
                            modelXbrl=val.modelXbrl, name=paramName, value=v)
                        v = None
                if v not in (None, ""):
                    val.params[paramName] = v # if not set uses prior value
    if "CIK" in val.params: # change to lower case key
        val.params["cik"] = val.params["CIK"]
        del val.params["CIK"]

    # attachmentType, if xBRL-XML, is suffixed ".INS", remove that
    if val.params.get("attachmentDocumentType", "").endswith(".INS"):
        val.params["attachmentDocumentType"] = val.params["attachmentDocumentType"][:-4]

    if isinstance(val.params.get("cikNameList", None), str):
        # cik1, cik2, cik3 in cikList and name1|Edgar|name2|Edgar|name3 in cikNameList strings
        _filerIdentifiers = val.params["cikList"].split(",") if "cikList" in val.params else []
        _filerNames = val.params["cikNameList"].split("|Edgar|") if "cikNameList" in val.params else []
        if _filerIdentifiers:
            if len(_filerNames) not in (0, len(_filerIdentifiers)):
                val.modelXbrl.error(("EFM.6.05.24.parameters", "GFM.3.02.02"),
                    _("parameters for cikList and cikNameList different list entry counts: %(cikList)s, %(cikNameList)s"),
                    modelXbrl=val.modelXbrl, cikList=_filerIdentifiers, cikNameList=_filerNames)
            if _filerNames:
                val.params["cikNameList"]=dict((_cik,_filerNames[i] if i < len(_filerNames) else None)
                                                for i, _cik in enumerate(_filerIdentifiers))
            else:
                val.params["cikNameList"]=dict((_cik,None) for _cik in _filerIdentifiers)
            del val.params["cikList"]
        elif _filerNames:
            val.modelXbrl.error(("EFM.6.05.24.parameters", "GFM.3.02.02"),
                _("parameters for cikNameList provided but missing corresponding cikList: %(cikNameList)s"),
                modelXbrl=val.modelXbrl, cikNameList=_filerNames)
            del val.params["cikNameList"] # can't process without cik's as keys

    if val.params.get("attachmentDocumentType",  val.params.get("exhibitType", "")).startswith("EX-2.01"): # only applicable for edgar production and parameterized testcases
        val.EFM60303 = "EFM.6.23.01"
    else:
        val.EFM60303 = "EFM.6.03.03"

    if any((concept.qname.namespaceURI in val.disclosureSystem.standardTaxonomiesDict and concept.modelDocument.inDTS)
           for concept in val.modelXbrl.nameConcepts.get("UTR",())):
        val.validateUTR = True

    if "dqcRuleFilter" not in val.params and val.disclosureSystem.options and "dqc-rule-filter=" in val.disclosureSystem.options:
        val.params["dqcRuleFilter"] = val.disclosureSystem.options.partition("dqc-rule-filter=")[2]

    modelManager = val.modelXbrl.modelManager
    if hasattr(modelManager, "efmFiling"):
        efmFiling = modelManager.efmFiling
        efmFiling.submissionType = val.params.get("submissionType")
        efmFiling.attachmentDocumentType = val.params.get("attachmentDocumentType")

    blockXuleValidateFinally(val) # block XULE Validate.Finally for RSS feed and testcases

def severityReleveler(modelXbrl, level, messageCode, args, **kwargs):
    if getattr(modelXbrl.modelManager.disclosureSystem, "EFMplugin", False):
        if messageCode and feeTagMessageCodesRelevelable.match(messageCode) and level == "ERROR":
            if not hasattr(modelXbrl, "isFeeTagging"):
                modelXbrl.isFeeTagging = any(ns.startswith("http://xbrl.sec.gov/ffd") for ns in modelXbrl.namespaceDocs)
            if modelXbrl.isFeeTagging:
                modelObject = args.get("modelObject")
                if (isinstance(modelObject, ModelFact) and
                    str(modelObject.qname) not in feeTagEltsNotRelevelable):
                        level = "WARNING"
        if messageCode and xule_error_code_pattern.match(messageCode) and level == "ERROR":
            level = "WARNING"
            if args.get("severity") == "error":
                args["severity"] = "warning"
        # add message number
        messageCode, msgNum = messageNumericId(modelXbrl, level, messageCode, args)
        if msgNum:
            args["edgarMessageNumericId"] = msgNum
        if getattr(modelXbrl, "loadedFromFtJson", False) and level == "ERROR":
            # demote to warning for EFMS call
            level = "WARNING"
    return level, messageCode

def isolateSeparateIXDSes(modelXbrl, primaryIxdsDocument, *args, **kwargs):
    separateIXDSes = defaultdict(list)
    entrypoint = kwargs.get("entrypoint") or {}
    for htmlElt in modelXbrl.ixdsHtmlElements:
        tp = "" # attachment document type inferred from document type and ffd:SubmissnTp
        for qn in ("dei:DocumentType", "ffd:FeeExhibitTp"):
            for elt in htmlElt.iterfind(f".//{{{htmlElt.modelDocument.ixNS}}}nonNumeric[@name='{qn}']"):
                tp = elt.stringValue.strip()
                if tp:
                    # add the attachment document type if it was not specified in the entrypoint or entrypoint was a zip file
                    for ep in entrypoint.get("ixds", []):
                        if not ep.get("attachmentDocumentType") and ep.get("file") == htmlElt.document.filepath:
                            ep["attachmentDocumentType"] = tp
                    break
        separateIXDSes[tp if supplementalAttachmentDocumentTypesPattern.match(tp) else ""].append(htmlElt)
    # find targetDocumentPreferredFilename for primary ixds
    if "ixds" in entrypoint and "" in separateIXDSes:
        for ep in entrypoint["ixds"]:
            if isinstance(ep,dict) and "attachmentDocumentType" in ep \
                and primaryAttachmentDocumentTypesPattern.match(ep.get("attachmentDocumentType","")) and "file" in ep:
                primaryIxdsDocument.targetDocumentPreferredFilename = os.path.splitext(os.path.basename(ep["file"]))[0] + ".xbrl"
                modelXbrl.efmIxdsType = ep.get("attachmentDocumentType")
                break
    return [htmlElts for tp,htmlElts in sorted(separateIXDSes.items(), key=lambda i:i[0])]

def validateXbrlFinally(val, *args, **kwargs):
    if not (val.validateEFMplugin):
        return

    modelXbrl = val.modelXbrl

    _statusMsg = _("validating {0} filing rules").format(val.disclosureSystem.name)
    modelXbrl.profileActivity()
    modelXbrl.modelManager.showStatus(_statusMsg)

    validateFiling(val, modelXbrl, isEFM=True)

    modelXbrl.profileActivity(_statusMsg, minTimeToShow=0.0)
    modelXbrl.modelManager.showStatus(None)

def validateXbrlDtsDocument(val, modelDocument, isFilingDocument, *args, **kwargs):
    if not (val.validateEFMplugin):
        return

    checkDTSdocument(val, modelDocument, isFilingDocument)

def filingStart(cntlr, options, filesource, entrypointFiles, sourceZipStream=None, responseZipStream=None, *args, **kwargs):
    modelManager = cntlr.modelManager
    # cntlr.addToLog("TRACE EFM filing start val={} plugin={}".format(modelManager.validateDisclosureSystem, getattr(modelManager.disclosureSystem, "EFMplugin", False)))
    if modelManager.validateDisclosureSystem and (getattr(modelManager.disclosureSystem, "EFMplugin", False) or
                                                  getattr(modelManager.disclosureSystem, "ESEFplugin", False)):
        # if there are any IXDSes in entrypoint files with attachmentDocumentType, ensure primary document is first
        if isinstance(entrypointFiles, (list,tuple)):
            ixdsIndex = primaryIndex = -1
            for i, ep in enumerate(entrypointFiles):
                if "ixds" in ep:
                    ixdsIndex = i
                    for i, ixdsEntry in enumerate(ep["ixds"]):
                        submissionType = ixdsEntry.get("submissionType")
                        attachmentDocumentType = ixdsEntry.get("attachmentDocumentType")
                        # primary document type has submission type possibly followed by other description provided by filer
                        if submissionType and attachmentDocumentType and attachmentDocumentType.startswith(submissionType):
                            if i > 0:
                                prevIxds = ep["ixds"]
                                ep["ixds"] = prevIxds[i:i+1] + prevIxds[:i] + prevIxds[i+1:]
                            break
                elif "file" in ep: # non-IXDS entry, is it primary
                    submissionType = ep.get("submissionType")
                    attachmentDocumentType = ep.get("attachmentDocumentType")
                    # primary document type has submission type possibly followed by other description provided by filer
                    if submissionType and attachmentDocumentType and attachmentDocumentType.startswith(submissionType):
                        if i > 0:
                            primaryIndex = i
                    elif i > 0 and primaryIndex < 0 and not submissionType and attachmentDocumentType and not attachmentDocumentType.startswith("EX"):
                        # no submissionType but attachmentDocType doesn't start with EX, can be primary
                        primaryIndex = i

            # ensure any ixds is first entrypoint
            if ixdsIndex > 0:
                entrypointFiles.insert(0, entrypointFiles.pop(ixdsIndex))
            elif primaryIndex > 0:
                entrypointFiles.insert(0, entrypointFiles.pop(primaryIndex))
        # cntlr.addToLog("TRACE EFM filing start 2 classes={} moduleInfos={}".format(pluginMethodsForClasses, modulePluginInfos))
        modelManager.efmFiling = Filing(cntlr, options, filesource, entrypointFiles, sourceZipStream, responseZipStream)
        # this event is called for filings (of instances) as well as test cases, for test case it just keeps options accessible
        for pluginXbrlMethod in pluginClassMethods("EdgarRenderer.Filing.Start"):
            pluginXbrlMethod(cntlr, options, entrypointFiles, modelManager.efmFiling)
        # check if any entrypointFiles have an encryption is specified
        if isinstance(entrypointFiles, list):
            for pluginXbrlMethod in pluginClassMethods("Security.Crypt.Filing.Start"):
                pluginXbrlMethod(modelManager.efmFiling, options, filesource, entrypointFiles, sourceZipStream)


def guiTestcasesStart(cntlr, modelXbrl, *args, **kwargs):
    modelManager = cntlr.modelManager
    if cntlr.hasGui: # enable EdgarRenderer to initiate ixviewer irregardless of whether an EFM disclosure system is active
        for pluginXbrlMethod in pluginClassMethods("EdgarRenderer.Gui.Run"):
            xuleInit(cntlr)
            pluginXbrlMethod(cntlr, modelXbrl, *args,
                             # pass plugin items to GUI mode of EdgarRenderer
                             exhibitTypesStrippingOnErrorPattern=exhibitTypesStrippingOnErrorPattern,
                             exhibitTypesPrivateNotDisseminated=exhibitTypesPrivateNotDisseminated,
                             setReportAttrs=setReportAttrs, **kwargs)
            xuleClose(cntlr)

def testcasesStart(cntlr, options, modelXbrl, *args, **kwargs):
    # a test or RSS cases run is starting, in which case testcaseVariation... events have unique efmFilings
    modelManager = cntlr.modelManager
    if (hasattr(modelManager, "efmFiling") and
        modelXbrl.modelDocument and
        (modelXbrl.modelDocument.type in Type.TESTCASETYPES or modelXbrl.modelDocument.type == Type.RSSFEED)):
        efmFiling = modelManager.efmFiling
        efmFiling.close() # not needed, dereference
        del modelManager.efmFiling
        if not hasattr(modelXbrl, "efmOptions") and options: # may have already been set by EdgarRenderer in gui startup
            modelXbrl.efmOptions = options  # save options in testcase's modelXbrl

def xbrlLoad(modelManager, filesource, entrypoint=None, **kwargs):
    # starting to load an instance
    if hasattr(modelManager, "efmFiling"):
        if entrypoint:
            attachmentDocumentType = entrypoint.get("attachmentDocumentType")
            if feeTaggingAttachmentDocumentTypePattern.match(attachmentDocumentType or ""):
                # set html log title
                modelManager.cntlr.logHandler.htmlTitle = "Fee Exhibit Message Log"
            modelManager.cntlr.addToLog(
                f"Attachment Document Type {attachmentDocumentType}",
                level="INFO-RESULT",
                messageCode="EFM.attachmentDocumentType",
                messageArgs={"attachmentDocumentType":attachmentDocumentType},
                file=os.path.basename(entrypoint.get("file"))
                )

def xbrlLoaded(cntlr, options, modelXbrl, entryPoint, *args, **kwargs):
    # cntlr.addToLog("TRACE EFM xbrl loaded")
    modelManager = cntlr.modelManager
    if hasattr(modelManager, "efmFiling") and modelXbrl.modelDocument:
        if modelXbrl.modelDocument.type in (Type.INSTANCE, Type.INLINEXBRL, Type.INLINEXBRLDOCUMENTSET):
            efmFiling = modelManager.efmFiling
            efmFiling.addReport(modelXbrl)
            _report = efmFiling.reports[-1]
            _report.entryPoint = entryPoint
            if "accessionNumber" in entryPoint and not hasattr(efmFiling, "accessionNumber"):
                efmFiling.accessionNumber = entryPoint["accessionNumber"]
            efmFiling.arelleUnitTests = modelXbrl.arelleUnitTests.copy() # allow unit tests to be used after instance processing finished
            for supplementalXbrl in getattr(modelXbrl, "supplementalModelXbrls", []):
                if hasattr(supplementalXbrl, "ixdsDocUrls"):
                    entryPoint = {"ixds":[{"file":f} for f in supplementalXbrl.ixdsDocUrls]}
                xbrlLoaded(cntlr, options, supplementalXbrl, entryPoint)
            xuleInit(cntlr)
        elif modelXbrl.modelDocument.type == Type.RSSFEED:
            testcasesStart(cntlr, options, modelXbrl)

def xbrlRun(cntlr, options, modelXbrl, *args, **kwargs):
    # cntlr.addToLog("TRACE EFM xbrl run")
    modelManager = cntlr.modelManager
    if (hasattr(modelManager, "efmFiling") and modelXbrl.modelDocument and
        modelXbrl.modelDocument.type in (Type.INSTANCE, Type.INLINEXBRL, Type.INLINEXBRLDOCUMENTSET)):
        efmFiling = modelManager.efmFiling
        _report = efmFiling.getReport(modelXbrl)
        if _report is not None: # HF TESTING: not (options.abortOnMajorError and len(modelXbrl.errors) > 0):
            for pluginXbrlMethod in pluginClassMethods("EdgarRenderer.Xbrl.Run"):
                pluginXbrlMethod(cntlr, options, modelXbrl, modelManager.efmFiling, _report)

def filingValidate(cntlr, options, filesource, entrypointFiles, sourceZipStream=None, responseZipStream=None, *args, **kwargs):
    # cntlr.addToLog("TRACE EFM xbrl validate")
    modelManager = cntlr.modelManager
    if hasattr(modelManager, "efmFiling"):
        efmFiling = modelManager.efmFiling
        reports = efmFiling.reports
        # check for dup inline and regular instances
        # SDR checks
        if any(report.deiDocumentType and report.deiDocumentType.endswith(" SDR")
               for report in reports):
            _kSdrs = [r for r in reports if r.deiDocumentType == "K SDR"]
            if not _kSdrs and efmFiling.submissionType in ("SDR", "SDR-A"):
                efmFiling.error("EFM.6.03.08.sdrHasNoKreports",
                                _("SDR filing has no K SDR reports"))
            elif len(_kSdrs) > 1:
                efmFiling.error("EFM.6.03.08.sdrHasMultipleKreports",
                                _("SDR filing has multiple K SDR reports for %(entities)s"),
                                {"entities": ", ".join(r.entityRegistrantName for r in _kSdrs),
                                 "edgarCode": "cp-0308-Sdr-Has-Multiple-K-Reports"},
                                (r.url for r in _kSdrs))
            _lSdrEntityReports = defaultdict(list)
            for r in reports:
                if r.deiDocumentType == "L SDR":
                    _lSdrEntityReports[r.entityCentralIndexKey if r.entityCentralIndexKey != "0000000000"
                                       else r.entityRegistrantName].append(r)
            for lSdrEntity, lSdrEntityReports in _lSdrEntityReports.items():
                if len(lSdrEntityReports) > 1:
                    efmFiling.error("EFM.6.05.24.multipleLSdrReportsForEntity",
                                    _("Filing entity has multiple L SDR reports: %(entity)s"),
                                    {"entity": lSdrEntity},
                                    (r.url for r in lSdrEntityReports))
            # check for required extension files (schema, pre, lbl)
            for r in reports:
                hasSch = hasPre = hasCal = hasLbl = False
                for f in r.reportedFiles:
                    if f.endswith(".xsd"): hasSch = True
                    elif f.endswith("_pre.xml"): hasPre = True
                    elif f.endswith("_cal.xml"): hasCal = True
                    elif f.endswith("_lab.xml"): hasLbl = True
                missingFiles = ""
                if not hasSch: missingFiles += ", schema"
                #if not hasPre: missingFiles += ", presentation linkbase"
                #if not hasLbl: missingFiles += ", label linkbase"
                if missingFiles:
                    efmFiling.error("EFM.6.03.02.sdrMissingFiles",
                                    _("%(deiDocumentType)s report missing files: %(missingFiles)s"),
                                    {"deiDocumentType": r.deiDocumentType, "missingFiles": missingFiles[2:],
                                     "edgarCode": "cp-0302-Sdr-Missing-Files"},
                                    r.url)
                if not r.hasUsGaapTaxonomy:
                    efmFiling.error("EFM.6.03.02.sdrMissingStandardSchema",
                                    _("%(deiDocumentType)s submission must use a US GAAP standard schema"),
                                    {"deiDocumentType": r.deiDocumentType,
                                     "edgarCode": "cp-0302-Sdr-Missing-Standard-Schema"},
                                    r.url)
                if hasattr(r, "attachmentDocumentType") and r.attachmentDocumentType not in ("EX-99.K SDR", "EX-99.L SDR", "EX-99.K SDR.INS", "EX-99.L SDR.INS"):
                    efmFiling.error("EFM.6.03.02.sdrHasNonSdrAttachment",
                                    _("An SDR filing contains non-SDR attachment document type %(attachmentDocumentType)s dei document type %(deiDocumentType)s"),
                                    {"deiDocumentType": r.deiDocumentType, "attachmentDocumentType": r.attachmentDocumentType,
                                     "edgarCode": "cp-0302-Sdr-Has-Non-Sdr-Attachment"},
                                    r.url)

        hasInline = False
        hasInstance = False
        _attachmentDocumentTypeReports = defaultdict(list)
        for r in reports:
            if hasattr(r, "attachmentDocumentType") and r.attachmentDocumentType and not supplementalAttachmentDocumentTypesPattern.match(r.attachmentDocumentType):
                _attachmentDocumentTypeReports[r.attachmentDocumentType.partition(".")[0]].append(r)
            if r.isInline:
                hasInline = True
            else:
                hasInstance = True

        # EDGAR will not accept an Inline XBRL document that includes a separate instance document in the submission process.
        if hasInline and hasInstance:
            efmFiling.error("EFM.5.02.05", "You can not attach an Instance XBRL document and an Inline XBRL document on the same Submission.")

        if len(_attachmentDocumentTypeReports) > 1:
            efmFiling.error("EFM.6.03.08",
                            _("A filling contains multiple attachment document types %(attachmentDocumentType)s."),
                            {"attachmentDocumentTypes": ", ".join(_attachmentDocumentTypeReports.keys())},
                            [r.url for r in reports])
        for _attachmentDocumentType, _exhibitReports in _attachmentDocumentTypeReports.items():
            if _attachmentDocumentType not in ("EX-99",) and len(_attachmentDocumentTypeReports) > 1:
                efmFiling.error("EFM.6.03.08.moreThanOneIns",
                                _("A filing contains more than one instance for attachment document type %(attachmentDocumentType)s."),
                                {"attachmentDocumentType": _attachmentDocumentType},
                                [r.url for r in _attachmentDocumentTypeReports])

def roleTypeName(modelXbrl, roleURI, *args, **kwargs):
    modelManager = modelXbrl.modelManager
    if hasattr(modelManager, "efmFiling"):
        modelRoles = modelXbrl.roleTypes.get(roleURI, ())
        if modelRoles and modelRoles[0].definition:
            return re.sub(r"\{\s*(transposed|unlabeled|elements)\s*\}","", modelRoles[0].definition.rpartition('-')[2], flags=re.I).strip()
        return roleURI
    return None

def filingEnd(cntlr, options, filesource, entrypointFiles, sourceZipStream=None, responseZipStream=None, *args, **kwargs):
    #cntlr.addToLog("TRACE EFM filing end")
    modelManager = cntlr.modelManager
    if hasattr(modelManager, "efmFiling"):
        for pluginXbrlMethod in pluginClassMethods("EdgarRenderer.Filing.End"):
            pluginXbrlMethod(cntlr, options, filesource, modelManager.efmFiling, sourceZipStream=sourceZipStream)
        #cntlr.addToLog("TRACE EdgarRenderer end")
        # save JSON file of instances and referenced documents
        filingReferences = dict((report.url, report)
                                for report in modelManager.efmFiling.reports)

        modelManager.efmFiling.close()
        del modelManager.efmFiling
        #cntlr.addToLog("TRACE EFN filing end complete")

def rssItemXbrlLoaded(modelXbrl, rssWatchOptions, rssItem, *args, **kwargs):
    # Validate of RSS feed item (simulates filing & cmd line load events
    if not hasattr(rssItem.modelXbrl, "efmOptions"): # may have already been set by EdgarRenderer in gui startup
        rssItem.modelXbrl.efmOptions = rssWatchOptions  # save options in rss's modelXbrl
    testcaseVariationXbrlLoaded(rssItem.modelXbrl, modelXbrl, None)

def rssItemValidated(val, modelXbrl, rssItem, *args, **kwargs):
    # After validate of RSS feed item (simulates report and end of filing events)
    if hasattr(rssItem.modelXbrl, "efmOptions"):
        testcaseVariationValidated(rssItem.modelXbrl, modelXbrl)

def testcaseVariationXbrlLoaded(testcaseModelXbrl, instanceModelXbrl, modelTestcaseVariation, *args, **kwargs):
    # Validate of RSS feed item or testcase variation (simulates filing & cmd line load events
    modelManager = instanceModelXbrl.modelManager
    if (hasattr(testcaseModelXbrl, "efmOptions") and
        modelManager.validateDisclosureSystem and getattr(modelManager.disclosureSystem, "EFMplugin", False) and
        instanceModelXbrl.modelDocument.type in (Type.INSTANCE, Type.INLINEXBRL, Type.INLINEXBRLDOCUMENTSET)):
        cntlr = modelManager.cntlr
        options = testcaseModelXbrl.efmOptions
        entrypointFiles = [{"file":instanceModelXbrl.modelDocument.uri}]
        if not hasattr(modelManager, "efmFiling"): # first instance of filing
            modelManager.efmFiling = Filing(cntlr, options, instanceModelXbrl.fileSource, entrypointFiles, None, None, instanceModelXbrl.errorCaptureLevel)
            # this event is called for filings (of instances) as well as test cases, for test case it just keeps options accessible
            for pluginXbrlMethod in pluginClassMethods("EdgarRenderer.Filing.Start"):
                pluginXbrlMethod(cntlr, options, entrypointFiles, modelManager.efmFiling)
        xuleInit(cntlr)
        modelManager.efmFiling.addReport(instanceModelXbrl)
        _report = modelManager.efmFiling.reports[-1]
        _report.entryPoint = entrypointFiles[0]
        modelManager.efmFiling.arelleUnitTests = instanceModelXbrl.arelleUnitTests.copy() # allow unit tests to be used after instance processing finished
        # check for parameters on instance
        for _instanceElt in XmlUtil.descendants(modelTestcaseVariation, "*", "instance", "readMeFirst", "true", False):
            if instanceModelXbrl.modelDocument.uri.endswith(_instanceElt.text):
                if _instanceElt.get("attachmentDocumentType"):
                    _report.entryPoint["attachmentDocumentType"] = _report.attachmentDocumentType = _instanceElt.get("attachmentDocumentType")
                break

def testcaseVariationXbrlValidated(testcaseModelXbrl, instanceModelXbrl, *args, **kwargs):
    modelManager = instanceModelXbrl.modelManager
    if (hasattr(modelManager, "efmFiling") and
        instanceModelXbrl.modelDocument.type in (Type.INSTANCE, Type.INLINEXBRL, Type.INLINEXBRLDOCUMENTSET)):
        efmFiling = modelManager.efmFiling
        _report = efmFiling.getReport(instanceModelXbrl)
        if _report is not None: # HF TESTING: not (options.abortOnMajorError and len(modelXbrl.errors) > 0):
            for pluginXbrlMethod in pluginClassMethods("EdgarRenderer.Xbrl.Run"):
                pluginXbrlMethod(modelManager.cntlr, efmFiling.options, instanceModelXbrl, efmFiling, _report)

def testcaseVariationValidated(testcaseModelXbrl, instanceModelXbrl, errors=None, *args, **kwargs):
    modelManager = instanceModelXbrl.modelManager
    if (hasattr(modelManager, "efmFiling") and
        instanceModelXbrl.modelDocument.type in (Type.INSTANCE, Type.INLINEXBRL, Type.INLINEXBRLDOCUMENTSET)):
        efmFiling = modelManager.efmFiling
        if isinstance(errors, list):
            del efmFiling.errors[:]
        # validate report types
        filingValidate(efmFiling.cntlr, efmFiling.options, efmFiling.filesource, efmFiling.entrypointfiles, efmFiling.sourceZipStream, efmFiling.responseZipStream)        # validate each report
        if isinstance(errors, list):
            errors.extend(efmFiling.errors)
        # simulate filingEnd
        filingEnd(modelManager.cntlr, efmFiling.options, modelManager.filesource, [])
        # flush logfile (assumed to be buffered, empty the buffer for next filing)
        testcaseModelXbrl.modelManager.cntlr.logHandler.flush()
        xuleClose(modelManager.cntlr)

def fileSourceFile(cntlr, filepath, binary, stripDeclaration):
    modelManager = cntlr.modelManager
    if hasattr(modelManager, "efmFiling"):
        for pluginXbrlMethod in pluginClassMethods("Security.Crypt.FileSource.File"):
            _file = pluginXbrlMethod(cntlr, modelManager.efmFiling, filepath, binary, stripDeclaration)
            if _file is not None:
                return _file
    return None

def fileSourceExists(cntlr, filepath):
    modelManager = cntlr.modelManager
    if hasattr(modelManager, "efmFiling"):
        for pluginXbrlMethod in pluginClassMethods("Security.Crypt.FileSource.Exists"):
            _existence = pluginXbrlMethod(modelManager.efmFiling, filepath)
            if _existence is not None:
                return _existence
    return None

def commandLineOptionExtender(parser, *args, **kwargs):
    # extend command line options to store to database
    parser.add_option("--build-deprecated-concepts-file",
                      action="store_true",
                      dest="buildDeprecatedConceptsFile",
                      help=_("Build EFM Validation deprecated concepts file (pre-cache before use)"))

    parser.add_option("--build-ft-validations-file",
                      action="store_true",
                      dest="buildFTValidationsFile",
                      help=_("Build EFM Validation deprecated concepts file (pre-cache before use)"))
    # xule cmd options
    xuleCmdOptions(parser, *args, **kwargs)

def utilityRun(self, options, *args, **kwargs):
    if options.buildDeprecatedConceptsFile:
        from .Util import buildDeprecatedConceptDatesFiles
        buildDeprecatedConceptDatesFiles(self)
    if options.buildFTValidationsFile:
        from .Util import buildFTValidationsFile
        buildFTValidationsFile(self)
    # call Xule's cntrlrCmdLineUtilityRun
    xuleCntrlrCmdLineUtilityRun(self, options, *args, **kwargs)

class Filing:
    def __init__(self, cntlr, options=None, filesource=None, entrypointfiles=None, sourceZipStream=None, responseZipStream=None, errorCaptureLevel=None):
        self.cntlr = cntlr
        self.options = options
        self.filesource = filesource
        self.entrypointfiles = entrypointfiles
        self.sourceZipStream = sourceZipStream
        self.responseZipStream = responseZipStream
        self.submissionType = None
        self.reports = []
        self.renderedFiles = set() # filing-level rendered files
        self.strippedFiles = defaultdict(set) # files to be stripped due to error, by attachmentExhibitType
        self.reportZip = None
        if responseZipStream:
            self.setReportZipStreamMode('w')
        else:
            try: #zipOutputFile only present with EdgarRenderer plugin options
                if options and options.zipOutputFile:
                    if not os.path.isabs(options.zipOutputFile):
                        zipOutDir = os.path.dirname(filesource.basefile)
                        zipOutFile = os.path.join(zipOutDir,options.zipOutputFile)
                    else:
                        zipOutFile = options.zipOutputFile
                    self.reportZip = zipfile.ZipFile(zipOutFile, 'w', zipfile.ZIP_DEFLATED, True)
            except AttributeError:
                self.reportZip = None
        self.errorCaptureLevel = errorCaptureLevel or logging._checkLevel("INCONSISTENCY")
        self.errors = []
        self.arelleUnitTests = {} # copied from each instance loaded
        for pluginXbrlMethod in pluginClassMethods("Security.Crypt.Init"):
            pluginXbrlMethod(self, options, filesource, entrypointfiles, sourceZipStream)
        self.exhibitTypesStrippingOnErrorPattern = exhibitTypesStrippingOnErrorPattern
        self.exhibitTypesPrivateNotDisseminated = exhibitTypesPrivateNotDisseminated

    def getReport(self, modelXbrl):
        for report in self.reports:
            if modelXbrl == report.modelXbrl:
                return report
        return None

    def setReportZipStreamMode(self, mode): # mode is 'w', 'r', 'a'
        # required to switch in-memory zip stream between write, read, and append modes
        if self.responseZipStream:
            if self.reportZip: # already open, close and reseek underlying stream
                self.reportZip.close()
                self.responseZipStream.seek(0)
            self.reportZip = zipfile.ZipFile(self.responseZipStream, mode, zipfile.ZIP_DEFLATED, True)

    def close(self):
        ''' MetaFiling.json (not needed?) list of all files written out
        _reports = dict((report.basename, report.json) for report in self.reports)
        _reports["filing"] = {"renderedFiles": sorted(self.renderedFiles)}
        if self.options.logFile:
            _reports["filing"]["logFile"] = self.options.logFile
        if self.reportZip:
            self.reportZip.writestr("MetaFiling.json", json.dumps(_reports, sort_keys=True, indent=jsonIndent))
        else:
            try:
                if self.options.reportsFolder:
                    with open(os.path.join(self.options.reportsFolder, "MetaFiling.json"), mode='w') as f:
                        json.dump(_reports, f, sort_keys=True, indent=jsonIndent)
            except AttributeError: # no reportsFolder attribute
                pass
        '''
        if self.options and self.options.logFile:
            if self.reportZip and self.reportZip.fp is not None:  # open zipfile
                _logFile = self.options.logFile
                _logFileExt = os.path.splitext(_logFile)[1]
                if _logFileExt == ".xml":
                    _logStr = self.cntlr.logHandler.getXml(clearLogBuffer=False)  # may be saved to file later or flushed in web interface
                elif _logFileExt == ".json":
                    _logStr = self.cntlr.logHandler.getJson(clearLogBuffer=False)
                else:  # no ext or  _logFileExt == ".txt":
                    _logStr = self.cntlr.logHandler.getText(clearLogBuffer=False)
                self.reportZip.writestr(_logFile, _logStr)
            #else:
            #    with open(_logFile, "wt", encoding="utf-8") as fh:
            #        fh.write(_logStr)
        if self.reportZip:  # ok to close if already closed
            self.reportZip.close()
        self.__dict__.clear() # dereference all contents

    def addReport(self, modelXbrl):
        if modelXbrl.modelDocument:
            _report = Report(modelXbrl)
            self.reports.append(_report)

    def error(self, messageCode, message, messageArgs=None, file=None):
        if file and len(self.entrypointfiles) > 0:
            # relativize file(s)
            if isinstance(file, str):
                file = (file,)
            if isinstance(self.entrypointfiles[0], dict):
                _baseFile = self.entrypointfiles[0].get("file", ".")
            else:
                _baseFile = self.entrypointfiles[0]
            relFiles = [relativeUri(_baseFile, f) for f in file]
        else:
            relFiles = None
        self.cntlr.addToLog(message, messageCode=messageCode, messageArgs=messageArgs, file=relFiles, level=logging.ERROR)
        self.errors.append(messageCode)

    @property
    def hasInlineReport(self):
        return any(getattr(report, "isInline", False) for report in self.reports)

    def writeFile(self, filepath, data):
        # write the data (string or binary)
        for pluginXbrlMethod in pluginClassMethods("Security.Crypt.Write"):
            if pluginXbrlMethod(self, filepath, data):
                return
        with io.open(filepath, "wt" if isinstance(data, str) else "wb") as fh:
            fh.write(data)

REPORT_ATTRS = {"DocumentType", "DocumentPeriodEndDate", "EntityRegistrantName",
                "EntityCentralIndexKey", "CurrentFiscalYearEndDate", "DocumentFiscalYearFocus",
                "FeeExhibitTp"}
def lc(name):
    if name == "DocumentType":
        return "deiDocumentType" # special case to disambiguate from attachmentDocumentType
    return name[0].lower() + name[1:]

def setReportAttrs(report, modelXbrl):
    for attrName in REPORT_ATTRS:
        setattr(report, lc(attrName), None)
    for f in modelXbrl.facts:
        cntx = f.context
        if cntx is not None and cntx.isStartEndPeriod and not cntx.hasSegment:
            if f.qname is not None and f.qname.localName in REPORT_ATTRS and f.xValid >= VALID and f.xValue:
                setattr(report, lc(f.qname.localName), f.xValue)

class Report:

    def __init__(self, modelXbrl):
        self.modelXbrl = modelXbrl
        self.isInline = modelXbrl.modelDocument.type in (Type.INLINEXBRL, Type.INLINEXBRLDOCUMENTSET)
        self.url = modelXbrl.modelDocument.uri
        self.reportedFiles = set()
        if modelXbrl.modelDocument.type == Type.INLINEXBRLDOCUMENTSET:
            self.basenames = []
            self.filepaths = []
            for ixDoc in sorted(modelXbrl.modelDocument.referencesDocument.keys(), key=lambda d: d.objectIndex): # preserve order
                if ixDoc.type == Type.INLINEXBRL:
                    self.basenames.append(ixDoc.basename)
                    self.filepaths.append(ixDoc.filepath)
                    self.reportedFiles.add(ixDoc.basename)
        else:
            self.basenames = [modelXbrl.modelDocument.basename]
            self.filepaths = [modelXbrl.modelDocument.filepath]
            self.reportedFiles.add(modelXbrl.modelDocument.basename)
        self.instanceName = self.basenames[0]
        setReportAttrs(self, modelXbrl)
        self.reportedFiles |= referencedFiles(modelXbrl)
        self.renderedFiles = set()
        self.hasUsGaapTaxonomy = False
        sourceDir = os.path.dirname(modelXbrl.modelDocument.filepath)
        # add referenced files that are xbrl-referenced local documents
        refDocUris = set()
        def addRefDocs(doc):
            if doc.type == Type.INLINEXBRLDOCUMENTSET:
                for ixDoc in doc.referencesDocument.keys():
                    if ixDoc.type == Type.INLINEXBRL:
                        addRefDocs(ixDoc)
            for refDoc in doc.referencesDocument.keys():
                _file = refDoc.filepath
                if refDoc.uri not in refDocUris:
                    refDocUris.add(refDoc.uri)
                    if refDoc.filepath and refDoc.filepath.startswith(sourceDir):
                        self.reportedFiles.add(refDoc.filepath[len(sourceDir)+1:]) # add file name within source directory
                    addRefDocs(refDoc)
                if refDoc.type == Type.SCHEMA and refDoc.targetNamespace:
                    nsAuthority = authority(refDoc.targetNamespace, includeScheme=False)
                    nsPath = refDoc.targetNamespace.split('/')
                    if len(nsPath) > 2:
                        if nsAuthority in ("fasb.org", "xbrl.us") and nsPath[-2] == "us-gaap":
                            self.hasUsGaapTaxonomy = True
        addRefDocs(modelXbrl.modelDocument)

    def close(self):
        self.__dict__.clear() # dereference all contents

    @property
    def json(self): # stringify un-jsonable attributes
        return dict((name, value if isinstance(value,(str,int,float,Decimal,list,dict))
                           else sorted(value) if isinstance(value, set)
                           else str(value))
                    for name, value in self.__dict__.items())

__pluginInfo__ = {
    # Do not use _( ) in pluginInfo itself (it is applied later, after loading
    'name': 'Validate EFM',
    'version': '1.25.2', # SEC EDGAR release 25.2
    'description': '''EFM Validation.''',
    'license': 'Apache-2',
    'import': ('EDGAR/transform',), # SEC inline can use SEC transformations
    'author': authorLabel,
    'copyright': copyrightLabel,
    'aliases': ('validate/EFM', ),
    # classes of mount points (required)
    'DisclosureSystem.Types': dislosureSystemTypes,
    'DisclosureSystem.ConfigURL': disclosureSystemConfigURL,
    'Validate.XBRL.Start': validateXbrlStart,
    'Validate.XBRL.Finally': validateXbrlFinally,
    'Validate.XBRL.DTS.document': validateXbrlDtsDocument,
    'ModelXbrl.RoleTypeName': roleTypeName,
    'CntlrCmdLine.Filing.Start': filingStart,
    'CntlrWinMain.Xbrl.Loaded': guiTestcasesStart,
    'Testcases.Start': testcasesStart,
    'CntlrCmdLine.Options': commandLineOptionExtender,
    'CntlrCmdLine.Utility.Run': utilityRun,
    'CntlrCmdLine.Xbrl.Loaded': xbrlLoaded,
    'CntlrCmdLine.Xbrl.Run': xbrlRun,
    'CntlrCmdLine.Filing.Validate': filingValidate,
    'CntlrCmdLine.Filing.End': filingEnd,
    'ModelManager.Load': xbrlLoad,
    'RssItem.Xbrl.Loaded': rssItemXbrlLoaded,
    'Validate.RssItem': rssItemValidated,
    'TestcaseVariation.Xbrl.Loaded': testcaseVariationXbrlLoaded,
    'TestcaseVariation.Xbrl.Validated': testcaseVariationXbrlValidated,
    'TestcaseVariation.Validated': testcaseVariationValidated,
    'FileSource.File': fileSourceFile,
    'FileSource.Exists': fileSourceExists,
    'Logging.Severity.Releveler': severityReleveler,
    'InlineDocumentSet.IsolateSeparateIXDSes': isolateSeparateIXDSes,
    # Xule interfaces
    'CntlrWinMain.Menu.Tools': xuleMenuTools,
    'CntlrWinMain.Menu.Validation': xuleValidateMenuTools
}
