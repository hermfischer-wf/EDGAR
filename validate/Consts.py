'''
See COPYRIGHT.md for copyright information.
'''
import regex as re
from arelle.PythonUtil import attrdict

#qnFasbExtensibleListItemTypes = (qname("{http://fasb.org/us-types/2017-01-31}us-types:extensibleListItemType"),
#                                 qname("{http://fasb.org/srt-types/2018-01-31}srt-types:extensibleListItemType"))

""" removed per PCR22280 5/16/18
ifrsSrtConcepts = { # concepts of ifrs items or axes which have a corresponding srt element
    "CounterpartiesAxis": "CounterpartyNameAxis",
    "MajorCustomersAxis": "MajorCustomersAxis",
    "ProductsAndServicesAxis": "ProductOrServiceAxis",
    "RangeAxis": "RangeAxis"
    }
srtAxisIfrsMembers = { # members of IFRS axes which have SRT corresponding member elements
    "CounterpartyNameAxis": {"CounterpartiesMember", "IndividuallyInsignificantCounterpartiesMember"},
    "MajorCustomersAxis": {"MajorCustomersMember", "GovernmentMember"},
    "ProductOrServiceAxis": {"ProductsAndServicesMember"},
    "RangeAxis": {"RangesMember", "BottomOfRangeMember", "WeightedAverageMember", "TopOfRangeMember"}    }
"""

# doc type requirements are for EFM 6.5.20 and are in some cases a superset of what the submission allows.
docTypesRR = {"497", "485APOS", "485BPOS", "485BXT", "N-1A", "N-1A/A"}
docTypesAllowingRedact = {"17AD-27"} | {f"EX-99.{c}.SBSEF" for c in "CDEFHIJKLPQRS"} | {f"SBSEF-{x}" for x in ("CCO-RPT","FIN-REQ","FIN-QTR")}

submissionTypesAllowingSeriesClasses = docTypesRR | {
    'N-Q', 'N-Q/A'}
invCompanyTypesAllowingSeriesClasses = {"N-1A", "N-3"}
invCompanyTypesRequiringOefClasses = {"N-1A"}
submissionTypesRequiringOefClasses = {'N-CSR', 'N-CSR/A', 'N-CSRS', 'N-CSRS/A',}

docTypesRequiringPeriodOfReport = {"10", "10-K", "10-Q", "20-F", "40-F", "6-K", "8-K",
    "F-1", "F-10", "F-3", "F-4", "F-9", "S-1", "S-11", "S-3", "S-4", "POS AM", "10-KT", "10-QT", "POS EX",
    "10/A", "10-K/A", "10-Q/A", "20-F/A", "40-F/A", "6-K/A", "8-K/A", "F-1/A", "F-10/A", "F-3/A", "F-4/A",
    "F-9/A", "S-1/A", "S-11/A", "S-3/A", "S-4/A", "10-KT/A", "10-QT/A", "485APOS", "485BPOS", "485BXT", "497",
    "N-CSR", "N-CSRS", "N-Q", "N-CSR/A", "N-CSRS/A", "N-Q/A", "K SDR", "L SDR" }

docTypesRequiringRrSchema = \
docTypesExemptFromRoleOrder = \
submissionTypesExemptFromRoleOrder = ('485APOS', '485BPOS','485BXT', '497', 'N-1A', 'N-1A/A',
                                      'N-2', 'N-2/A', 'N-2MEF', 'N-2ASR', 'N-2 POSASR', 'N-CSR', 'N-CSR/A','N-CSRS', 'N-CSRS/A')

docTypesNotAllowingIfrs = ('485APOS', '485BPOS','485BXT', '497', 'N-1A', 'N-1A/A',
                           'N-CSR', 'N-CSR/A', 'N-CSRS', 'N-CSRS/A', 'N-Q', 'N-Q/A',
                           'K SDR', 'L SDR')

docTypesNotAllowingInlineXBRL = {
    "K SDR", "L SDR"}
docTypesAttachmentDocumentType = {
    "2.01 SD": "EX-2.01",
    "K SDR": "EX-99.K SDR",
    "L SDR": "EX-99.L SDR"
    # default is attachmentDocumentType parameter is the same as dei:DocumentType
    }
docTypesSubType = {
    "2.01 SD": "SD",
    "EX-99.4R HISTORIC": "N-4"
    # default is submissionType parameter is the same as dei:DocumentType
    }

feeTaggingAttachmentDocumentTypePattern = re.compile(r"EX-FILING FEES.*")

attachmentDocumentTypeValidationRulesFiles = ( # match attachment doc type pattern to rules file
    (feeTaggingAttachmentDocumentTypePattern, "ft-validations.json"),
    (re.compile(r"EX-26.*"), "ex26-validations.json"),
    (None, "dei-validations.json")
    )
supplementalAttachmentDocumentTypesPattern = re.compile(r"EX-FILING FEES.*|EX-99\.[C-S]\.SBSEF.*")
exhibitTypesStrippingOnErrorPattern = re.compile(r"EX-26.*|EX-99\.[C-S]\.SBSEF.*|EX-98")
exhibitTypesPrivateNotDisseminated = re.compile(r"EX-99\.[DEFHIJKNOPQRS]\.SBSEF")
primaryAttachmentDocumentTypesPattern = re.compile(r"(?!EX-)")
attachmentDocumentTypeReqSubDocTypePattern = re.compile(r"EX-98")
nsPatternNotAllowedinxBRLXML = re.compile(r".*sec.gov/spac/.*")

rxpAlternativeReportingRegimes = ["EU", "UK", "NO", "CA"]

standardNamespacesPattern = re.compile(
    # non-IFRS groups 1 - authority, 2 - taxonomy (e.g. us-gaap, us-types), 3 - year
    r"http://(xbrl\.us|fasb\.org|xbrl\.sec\.gov)/("
            r"dei|us-gaap|srt|us-types|us-roles|srt-types|srt-roles|rr|cef|oef|country|currency|cyd|ecd|exch|invest|naics|rxp|sbs|sro|sic|stpr|vip|spac"
            r")/([0-9]{4}|[0-9]{4}q[1-4])(-[0-9]{2}-[0-9]{2})?$"
    # ifrs groups 4 - year, 5 - taxonomy (e.g. ifrs-full)
    r"|https?://xbrl.ifrs.org/taxonomy/([0-9]{4})-[0-9]{2}-[0-9]{2}/(ifrs[\w-]*)$")

# hidden references
untransformableTypes = {"anyURI", "base64Binary", "hexBinary", "NOTATION", "QName", "time",
                        "token", "language"}

# hideable namespaceURIs
hideableNamespacesPattern = re.compile("http://xbrl.sec.gov/(dei|vip|ffd)/")

# RR untransformable facts
rrUntransformableEltsPattern = re.compile(r"(\w*TableTextBlock|RiskNarrativeTextBlock|BarChart\w+|AnnualReturn(19|20)[0-9][0-9])") # WcH RiskNarrative exception is an ABSOLUTELY TEMPORARY HACK
usDeprecatedLabelPattern = re.compile(r"^.* \(Deprecated (....(-..-..)?)\)$")
usDeprecatedLabelRole = "http://www.xbrl.org/2003/role/label"
ifrsDeprecatedLabelPattern = re.compile(r"^\s*([0-9]{4}-[0-1][0-9]-[0-2][0-9])\s*$")
ifrsDeprecatedLabelRole = "http://www.xbrl.org/2009/role/deprecatedDateLabel"

latestTaxonomyDocs = { # note that these URLs are blocked by EFM validation modes
    # deprecatedLabels may be a single file name or list of file names
    # US FASB/SEC taxonomies
    "cef/*": {
        "deprecatedLabels": ["https://xbrl.sec.gov/cef/2023/cef-entire-2023.xsd",
                             "https://xbrl.sec.gov/cef/2024/cef-entire-2024.xsd"],
        "deprecatedLabelRole": usDeprecatedLabelRole,
        "deprecationDatePattern": usDeprecatedLabelPattern
        },
    "country/*": {
        "deprecatedLabels": ["http://xbrl.sec.gov/country/2016/country-lab-2016-01-31.xml",
                             "http://xbrl.sec.gov/country/2017/country-lab-2017-01-31.xml",
                             "https://xbrl.sec.gov/country/2020/country-lab-2020-01-31.xml",
                             "https://xbrl.sec.gov/country/2021/country-entire-2021.xsd",
                             "https://xbrl.sec.gov/country/2022/country-entire-2022.xsd",
                             "https://xbrl.sec.gov/country/2023/country-entire-2023.xsd",
                             "https://xbrl.sec.gov/country/2024/country-entire-2024.xsd"],
        "deprecatedLabelRole": usDeprecatedLabelRole,
        "deprecationDatePattern": usDeprecatedLabelPattern
        },
    "currency/*": {
        "deprecatedLabels": ["https://xbrl.sec.gov/currency/2017/currency-lab-2017-01-31.xml",
                             "https://xbrl.sec.gov/currency/2019/currency-lab-2019-01-31.xml",
                             "https://xbrl.sec.gov/currency/2020/currency-lab-2020-01-31.xml",
                             "https://xbrl.sec.gov/currency/2021/currency-entire-2021.xsd",
                             "https://xbrl.sec.gov/currency/2022/currency-entire-2022.xsd",
                             "https://xbrl.sec.gov/currency/2023/currency-entire-2023.xsd",
                             "https://xbrl.sec.gov/currency/2024/currency-entire-2024.xsd"],
        "deprecatedLabelRole": usDeprecatedLabelRole,
        "deprecationDatePattern": usDeprecatedLabelPattern
        },
    "dei/*": {
        "deprecatedLabels": ["http://xbrl.sec.gov/dei/2012/dei-lab-2012-01-31.xml",
                             "https://xbrl.sec.gov/dei/2018/dei-lab-2018-01-31.xml",
                             "https://xbrl.sec.gov/dei/2019/dei-lab-2019-01-31.xml",
                             "https://xbrl.sec.gov/dei/2021/dei-2021_lab.xsd",
                             "https://xbrl.sec.gov/dei/2022/dei-2022_lab.xsd",
                             "https://xbrl.sec.gov/dei/2023/dei-2023_lab.xsd",
                             "https://xbrl.sec.gov/dei/2024/dei-2024_lab.xsd"],
        "deprecatedLabelRole": usDeprecatedLabelRole,
        "deprecationDatePattern": usDeprecatedLabelPattern
        },
    "ecd/*": {
        "deprecatedLabels": [ "https://xbrl.sec.gov/ecd/2023/ecd-entire-2023.xsd",
                              "https://xbrl.sec.gov/ecd/2024/ecd-entire-2024.xsd"],
        "deprecatedLabelRole": usDeprecatedLabelRole,
        "deprecationDatePattern": usDeprecatedLabelPattern
        },
    "exch/*": {
        "deprecatedLabels": ["https://xbrl.sec.gov/exch/2018/exch-lab-2018-01-31.xml",
                             "https://xbrl.sec.gov/exch/2019/exch-lab-2019-01-31.xml",
                             "https://xbrl.sec.gov/exch/2020/exch-lab-2020-01-31.xml",
                             "https://xbrl.sec.gov/exch/2021/exch-entire-2021.xsd",
                             "https://xbrl.sec.gov/exch/2022/exch-entire-2022.xsd",
                             "https://xbrl.sec.gov/exch/2023/exch-entire-2023.xsd",
                             "https://xbrl.sec.gov/exch/2024/exch-entire-2024.xsd"],
        "deprecatedLabelRole": usDeprecatedLabelRole,
        "deprecationDatePattern": usDeprecatedLabelPattern
        },
    "fnd/*": {
        "deprecatedLabels": [ "https://xbrl.sec.gov/fnd/2023/fnd-entire-2023.xsd",
                              "https://xbrl.sec.gov/fnd/2024/fnd-entire-2024.xsd"],
        "deprecatedLabelRole": usDeprecatedLabelRole,
        "deprecationDatePattern": usDeprecatedLabelPattern
        },
    "invest/*": {
        # do not rebuild, all labels are deprecated
        "deprecatedLabels": "https://xbrl.sec.gov/invest/2013/invest-lab-2013-01-31.xml",
        "deprecatedLabelRole": usDeprecatedLabelRole,
        "deprecationDatePattern": usDeprecatedLabelPattern
        },
    "naics/*": {
        "deprecatedLabels": ["https://xbrl.sec.gov/naics/2021/naics-entire-2021.xsd",
                             "https://xbrl.sec.gov/naics/2022/naics-entire-2022.xsd",
                             "https://xbrl.sec.gov/naics/2023/naics-entire-2023.xsd",
                             "https://xbrl.sec.gov/naics/2024/naics-entire-2024.xsd"],
        "deprecatedLabelRole": usDeprecatedLabelRole,
        "deprecationDatePattern": usDeprecatedLabelPattern
        },
    "oef/*": {
        "deprecatedLabels": [ "https://xbrl.sec.gov/oef/2023/oef-entire-2023.xsd",
                             "https://xbrl.sec.gov/oef/2024/oef-entire-2024.xsd"],
        "deprecatedLabelRole": usDeprecatedLabelRole,
        "deprecationDatePattern": usDeprecatedLabelPattern
        },
    "rr/*": {
        "deprecatedLabels": ["http://xbrl.sec.gov/rr/2012/rr-lab-2012-01-31.xml",
                             "https://xbrl.sec.gov/rr/2018/rr-lab-2018-01-31.xml",
                             "https://xbrl.sec.gov/rr/2021/rr-2021_lab.xsd",
                             "https://xbrl.sec.gov/rr/2022/rr-2022_lab.xsd",
                             "https://xbrl.sec.gov/rr/2023/rr-2023_lab.xsd"],
        "deprecatedLabelRole": usDeprecatedLabelRole,
        "deprecationDatePattern": usDeprecatedLabelPattern
        },
    "rxp/*": {
        "deprecatedLabels": [ "https://xbrl.sec.gov/rxp/2023/rxp-entire-2023.xsd",
                             "https://xbrl.sec.gov/rxp/2024/rxp-entire-2024.xsd"],
        "deprecatedLabelRole": usDeprecatedLabelRole,
        "deprecationDatePattern": usDeprecatedLabelPattern
        },
    "sic/*": {
        "deprecatedLabels": ["https://xbrl.sec.gov/sic/2023/sic-entire-2023.xsd",
                             "https://xbrl.sec.gov/sic/2024/sic-entire-2024.xsd"],
        "deprecatedLabelRole": usDeprecatedLabelRole,
        "deprecationDatePattern": usDeprecatedLabelPattern
        },
    "snj/*": {
        "deprecatedLabels": ["https://xbrl.sec.gov/snj/2023/snj-entire-2023.xsd",
                             "https://xbrl.sec.gov/snj/2024/snj-entire-2024.xsd"],
        "deprecatedLabelRole": usDeprecatedLabelRole,
        "deprecationDatePattern": usDeprecatedLabelPattern
        },
    "sro/*": {
        "deprecatedLabels": ["https://xbrl.sec.gov/sro/2024/sro-entire-2024.xsd"],
        "deprecatedLabelRole": usDeprecatedLabelRole,
        "deprecationDatePattern": usDeprecatedLabelPattern
        },
    "srt/*": {
        "deprecatedLabels": ["http://xbrl.fasb.org/srt/2018/elts/srt-lab-2018-01-31.xml",
                             "http://xbrl.fasb.org/srt/2019/elts/srt-lab-2019-01-31.xml",
                             "http://xbrl.fasb.org/srt/2020/elts/srt-lab-2020-01-31.xml",
                             "https://xbrl.fasb.org/srt/2021/elts/srt-lab-2021-01-31.xml",
                             "https://xbrl.fasb.org/srt/2022/elts/srt-lab-2022.xml",
                             "https://xbrl.fasb.org/srt/2023/elts/srt-lab-2023.xml",
                             "https://xbrl.fasb.org/srt/2024/elts/srt-lab-2024.xml"],
        "deprecatedLabelRole": usDeprecatedLabelRole,
        "deprecationDatePattern": usDeprecatedLabelPattern
        },
    "stpr/*": {
        "deprecatedLabels": ["https://xbrl.sec.gov/stpr/2023/stpr-entire-2023.xsd",
                             "https://xbrl.sec.gov/stpr/2024/stpr-entire-2024.xsd"],
        "deprecatedLabelRole": usDeprecatedLabelRole,
        "deprecationDatePattern": usDeprecatedLabelPattern
        },
    "us-gaap/*": {
        "deprecatedLabels": ["http://xbrl.fasb.org/us-gaap/2018/elts/us-gaap-lab-2018-01-31.xml",
                             "http://xbrl.fasb.org/us-gaap/2019/elts/us-gaap-lab-2019-01-31.xml",
                             "http://xbrl.fasb.org/us-gaap/2020/elts/us-gaap-lab-2020-01-31.xml",
                             "https://xbrl.fasb.org/us-gaap/2021/elts/us-gaap-lab-2021-01-31.xml",
                             "https://xbrl.fasb.org/us-gaap/2022/elts/us-gaap-lab-2022.xml",
                             "https://xbrl.fasb.org/us-gaap/2023/elts/us-gaap-lab-2023.xml",
                             "https://xbrl.fasb.org/us-gaap/2024/elts/us-gaap-lab-2024.xml"],
        "deprecatedLabelRole": usDeprecatedLabelRole,
        "deprecationDatePattern": usDeprecatedLabelPattern,
        "dqcRuleArcrole": "http://fasb.org/dqcRules/arcrole/concept-rule",
        },
    "vip/*": {
        "deprecatedLabels": ["https://xbrl.sec.gov/vip/2022/vip-entire-2022.xsd",
                             "https://xbrl.sec.gov/vip/2023/vip-entire-2023.xsd",
                             "https://xbrl.sec.gov/vip/2024/vip-entire-2024.xsd"],
        "deprecatedLabelRole": usDeprecatedLabelRole,
        "deprecationDatePattern": usDeprecatedLabelPattern
        },
    # International taxonomies
    "ifrs-full/*": {
        "deprecatedLabels": ["http://xbrl.ifrs.org/taxonomy/2018-03-16/deprecated/depr-lab_full_ifrs-en_2018-03-16.xml",
                             "http://xbrl.ifrs.org/taxonomy/2019-03-27/deprecated/depr-lab_full_ifrs-en_2019-03-27.xml",
                             "http://xbrl.ifrs.org/taxonomy/2020-03-16/deprecated/depr-lab_full_ifrs-en_2020-03-16.xml",
                             "http://xbrl.ifrs.org/taxonomy/2021-03-24/deprecated/depr-lab_full_ifrs-en_2021-03-24.xml",
                             "http://xbrl.ifrs.org/taxonomy/2022-03-24/deprecated/depr-lab_full_ifrs-en_2022-03-24.xml",
                             "https://xbrl.ifrs.org/taxonomy/2023-03-24/deprecated/depr-lab_full_ifrs-en_2023-03-23.xml"],
        "deprecatedLabelRole": ifrsDeprecatedLabelRole,
        "deprecationDatePattern": ifrsDeprecatedLabelPattern
        }
    }
''' Moved to Ugt resource files
latestDqcrtDocs = {
    "us-gaap/2020": "http://xbrl.fasb.org/us-gaap/2020/dqcrules/dqcrules-2020-01-31.xsd",
    "us-gaap/2021": "http://xbrl.fasb.org/us-gaap/2021/dqcrules/dqcrules-2021-01-31.xsd"
    }
'''
latestEntireUgt = {
    "us-gaap/2019": ["http://xbrl.fasb.org/us-gaap/2019/entire/us-gaap-entryPoint-std-2019-01-31.xsd", None],
    "us-gaap/2020": ["http://xbrl.fasb.org/us-gaap/2020/entire/us-gaap-entryPoint-std-2020-01-31.xsd",
                     # use 2021 DQCRT for 2020 us-gaap checks
                     "http://xbrl.fasb.org/us-gaap/2021/dqcrules/dqcrules-2021-01-31.xsd"],
    "us-gaap/2021": ["http://xbrl.fasb.org/us-gaap/2021/entire/us-gaap-entryPoint-std-2021-01-31.xsd",
                     # "http://xbrl.fasb.org/us-gaap/2021/dqcrules/dqcrules-2021-01-31.xsd"
                     "https://xbrl.fasb.org/us-gaap/2022/dqcrules/dqcrules-entire-2022.xsd"],
    "us-gaap/2022": ["https://xbrl.fasb.org/us-gaap/2022/entire/us-gaap-entryPoint-std-2022.xsd",
                     "https://xbrl.fasb.org/us-gaap/2022/dqcrules/dqcrules-entire-2022.xsd"],
    "us-gaap/2023": ["https://xbrl.fasb.org/us-gaap/2023/entire/us-gaap-entryPoint-std-2023.xsd",
                     "https://xbrl.fasb.org/us-gaap/2023/dqcrules/dqcrules-entire-2023.xsd"],
    "us-gaap/2024": ["https://xbrl.fasb.org/us-gaap/2024/entire/us-gaap-entryPoint-std-2024.xsd",
                     "https://xbrl.fasb.org/us-gaap/2024/dqcrules/dqcrules-entire-2024.xsd"]
    }

linkbaseValidations = {
    # key - validation taxonomy prefix
    # efmPre, Cal, Def - EFM section for linkbase constraint
    # elrPre - regex matching allowed linkrole for extension
    # elrPreDocTypes - list of doc types which are checked for this validation
    # elrDefInNs - regex of linkroles permitting extension relationships between base taxonomy concepts
    # elrDefExNs - regex of linkroles permitting extension relationships between base and non-base concepts
    # elrDefRowSrc - patterns of role and allowed source concept qname
    # elrDefNoTgtRole - true to block extension arcs with target role
    # preSources - local names of allowed source elements
    # preCustELFs - true to allow custom linkroles in extension
    "cef": attrdict(
        exgPre = "10.08.01",
        exgCal = "10.08.01",
        exgDef = "10.08.01",
        elrPre = re.compile("http://xbrl.sec.gov/cef/role/N2"),
        elrPreDocTypes = ("N-2", "N-2/A"), # only these doc types are checked
        elrDefInNs = re.compile("http://xbrl.sec.gov/cef/role/N2"),
        elrDefExNs = re.compile("http://xbrl.sec.gov/cef/role/(Security|Risk|Coregistrant)Only"),
        elrDefRoleSrc = (),
        elrDefNoTgtRole = False,
        preSources = ("AllCoregistrantsMember", "AllSecuritiesMember", "AllRisksMember", "ClassOfStockDomain", "DebtInstrumentNameDomain"),
        preCustELRs = False
    ),
    "vip": attrdict(
        exgPre = "10.08.06",
        exgCal = "10.08.06",
        exgDef = "10.08.06",
        elrPre = re.compile("http://xbrl.sec.gov/vip/role/N[346]"),
        elrDefInNs = re.compile("http://xbrl.sec.gov/vip/role/[^/]*Only"),
        elrDefExNs = re.compile("http://xbrl.sec.gov/vip/role/[^/]*Only"),
        elrDefRoleSrc = (),
        elrDefNoTgtRole = False,
        preSources = (),
        preCustELRs = False
    ),
    "ecd": attrdict(
        efmPre = None,
        exgCal = "10.08.02",
        exgDef = "10.08.02",
        elrPre = None,
        elrDefInNs = re.compile("http://xbrl.sec.gov/ecd/role/"),
        elrDefExNs = re.compile("http://xbrl.sec.gov/ecd/role/[^/]*Only"),
        elrDefRoleSrc = (),
        elrDefNoTgtRole = False,
        preSources = (),
        preCustELRs = True
    ),
    "oef": attrdict(
        exgCal = "10.08.04",
        elrCalDocTypes = ('N-CSR','N-CSRS','N-CSR/A','N-CSRS/A'),
        exgDef = "10.08.04", #elrDefDocTypes = ('N-CSR','N-CSRS','N-CSR/A','N-CSRS/A'),
        # Need to add the "Only" suffix to these rr roles for consistency.
        elrDefInNs = re.compile("http://xbrl.sec.gov/(oef/role/[^/]*Only|rr/role/(Series|Class|Coregistrant|Prospectus|Risk|PerformanceMeasure))"),
        elrDefExNs = re.compile("http://xbrl.sec.gov/(oef/role/[^/]*Only|rr/role/(Series|Class|Coregistrant|Prospectus|Risk|PerformanceMeasure))"),
        elrDefRoleSrc = (),
        elrDefNoTgtRole = False,
        preSources = (),
        efmPre = None,
        preCustELRs = True
    ),
    "rxp": attrdict(
        exgCal = "10.08.05",
        elrCalDocTypes = ('2.01 SD',),
        exgDef = "10.08.05",
        elrDefDocTypes = ('2.01 SD',),
        elrDefInNs = re.compile("never permitted"),
        elrDefExNs = re.compile("http://xbrl.sec.gov/rxp/role/(Projects|Governments|Segments|Entities|Resources)Only"),
        elrDefRoleSrc = (
            (re.compile(r".*sec\.gov/rxp/role/ProjectsOnly"), re.compile(r"rxp:AllProjectsMember")),
            (re.compile(r".*sec\.gov/rxp/role/GovernmentsOnly"), re.compile(r"rxp:AllGovernmentsMember")),
            (re.compile(r".*sec\.gov/rxp/role/SegmentsOnly"), re.compile(r"rxp:AllSegmentsMember")),
            (re.compile(r".*sec\.gov/rxp/role/EntitiesOnly"), re.compile(r"dei:EntityDomain")),
            (re.compile(r".*sec\.gov/rxp/role/ResourcesOnly"), re.compile(r"rxp:AllResourcesMember"))
        ),
        elrDefNoTgtRole = True,
        elrDefRgtMemsRole = re.compile("http://xbrl.sec.gov/rxp/"),
        exgDefTgtMemsUnique = "10.08.05",
        preSources = (),
        efmPre = None,
        preCustELRs = True,
    ),
    "sro": attrdict(
        exgPre = "10.08.07",
        exgCal = "10.08.07",
        exgDef = "10.08.07",
        elrPre = None,
        elrDefInNs = re.compile("."), # skip this test
        elrDefExNs = re.compile("."), # skip this test
        elrDefRoleSrc = (
            (re.compile(r".*sec\.gov/17ad27/role/.*Only$"),
                re.compile(r"sro:Cmsp(SvcTyp|UsrTyp|AsstCls|SubmHdrs)Domain$")),
            (re.compile(r".*sec\.gov/17ad27/role/ProgressTable$"),
                re.compile(r".")), # match any QName
            (re.compile(r".*sec\.gov/17ad27/role/(?!(.*Only|ProgressTable))."),
                re.compile(r"matchnothing^")) # match nothing
        ),
        elrDefNoTgtRole = False,
        preSources = (),
        preCustELRs = False
    ),
    "spac": attrdict(
        exgPre = "10.08.10",
        exgCal = "10.08.10",
        exgDef = "10.08.10",
        elrPre = re.compile("@match-nothing@"),
        elrDefInNs = re.compile("never permitted"),
        elrDefExNs = re.compile(".*sec.gov/spac/([^/]*/)*role/[^/]*Only$"),
        elrDefRoleSrc = (
            (re.compile(r".*sec.gov/spac/([^/]*/)*role/[^/]*Only$"),
                re.compile(r".")), # match any member QName
        ),
        elrDefNoTgtRole = False,
        preSources = (),
        preCustELRs = False
    ),
}

# constants for fee tagging message severity releveling
feeTagMessageCodesRelevelable = re.compile(r"xmlSchema:|ix11\.|xbrl\.")

feeTagEltsNotRelevelable = {
        "dei:CentralIndexKey", "ffd:RegnFileNb", "ffd:FormTp", "ffd:SubmissnTp", "ffd:FormTp",
        "ffd:FeeExhibitTp", "ffd:TtlFeeAmt", "ffd:TtlPrevslyPdAmt", "ffd:TtlOffsetAmt", "ffd:NetFeeAmt"
}
