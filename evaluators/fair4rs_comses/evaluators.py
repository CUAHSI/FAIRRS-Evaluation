from abc import ABC, abstractmethod
from typing import Dict, Any, List, Tuple
from utils import evaluator_utils
from utils import codemeta_parser
from constants import SOFTWARE_REGISTRIES, APPROVED_LICENSES, ACCEPTED_DATA_FORMATS, API_KEYWORDS, ACCEPTED_FAIR_REPOSITORIES, ACCEPTED_SOFTWARE_REPOSITORIES
 

class Evaluator(ABC):
    """
    Abstract base class for FAIR4RS indicators.
    """

    @abstractmethod
    def evalF1_1(self, citation=None, identifier=None, sameAs=None, isPartOf=None, url=None) -> Tuple[bool, List[str]]:
        raise NotImplementedError   

    @abstractmethod
    def evalF1_2(self, softwareVersion=None, version=None) -> bool:
        raise NotImplementedError

    @abstractmethod
    def evalF2(self, description=None, fileSize=None) -> bool:
        raise NotImplementedError

    @abstractmethod
    def evalF3(self, codeRepository=None, hasPart=None, identifier=None, publisher=None) -> bool:
        raise NotImplementedError


    @abstractmethod
    def evalF4(self, applicationCategory=None, applicationSubCategory=None, isAccessibleForFree=None, keywords=None, identifier=None) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    def evalA1_1(self, downloadUrl=None, installUrl=None, isAccessibleForFree=None, license=None, permissions=None, url=None) -> bool:
        raise NotImplementedError   

    @abstractmethod
    def evalA1_2(self, downloadUrl=None, hasPart=None, installUrl=None, isAccessibleForFree=None, isPartOf=None, license=None, permissions=None) -> bool:
        raise NotImplementedError

    @abstractmethod
    def evalA2(self, identifier=None, url=None) -> bool:
        raise NotImplementedError

    @abstractmethod
    def evalI1(self, supportingData=None, buildInstructions=None) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    def evalI2(self, relatedLink=None, supportingData=None, isPartOf=None, referencePublication=None) -> bool:
        raise NotImplementedError

    @abstractmethod
    def evalR1_1(self, citation=None, license=None, referencePublication=None) -> bool:
        raise NotImplementedError   

    @abstractmethod
    def evalR1_2(self, address=None, affiliation=None, author=None, citation=None, contributor=None,
                copyrightHolder=None, copyrightYear=None, dateCreated=None, dateModified=None,
                datePublished=None, editor=None, email=None, funder=None, funding=None, maintainer=None, 
                producer=None, provider=None, publisher=None, codeRepository=None) -> bool:
        raise NotImplementedError

    @abstractmethod
    def evalR2(self, softwareRequirement=None, softwareSuggestions=None) -> bool:
        raise NotImplementedError

    @abstractmethod
    def evalR3(self, review=None) -> bool:
        raise NotImplementedError


class BaseEvaluator(Evaluator):
    """
    Class for implementing evaluation functions.
    """

    def __init__(self,codemeta_file):

        self.codemeta_file = codemeta_file

    def validate_codemeta_file(self) -> Dict:

        codemeta_json = evaluator_utils.run_codemeticulous_validation(self.codemeta_file)

        return codemeta_json
    
    def evalF1_1(self, citation=None, identifier=None, sameAs=None, isPartOf=None, url=None) -> Tuple[bool, List[str]]:

        """
        Description from Chue Hong et. al, RDA FAIR4RS WG. (2022). FAIR Principles for Research Software (FAIR4RS Principles) (1.0). 
        Zenodo. https://doi.org/10.15497/RDA00068

        The use of identifiers for more than the software project (often synonymous with “software concept”
        or “software product”) improves findability by enabling components to be assigned distinct identifiers
        e.g, a software library, and a function in that library. The relationship between these components is
        embodied in the associated metadata. Granularity levels for software are shown in Figure 1 in Appendix A. 
        These principles do not prescribe which granularity levels should be assigned identifiers, as this is likely 
        to be implementation-specific.

        """

        # Get all function arguments dynamically
        all_args = {key: value for key, value in locals().items() if key != "self" and value is not None}

        # # initialize result to False
        # result = False

        # Extract URLs from all provided arguments
        extracted_urls = {
                        key: urls
                        for key, value in all_args.items()
                        if value and (urls := codemeta_parser.extract_urls_from_field(value, regex_filter=['https://']))
                        }
        if extracted_urls:
            result, log = evaluator_utils.validate_and_log_urls(extracted_urls,'is a distinct identifier.')
        else: 
            result = False
            log = [f"No URLs found in {list(all_args.keys())}"]

        return result, log

    def evalF1_2(self, softwareVersion=None, version=None) -> Tuple[bool, List[str]]:

        """
        Description from Chue Hong et. al, RDA FAIR4RS WG. (2022). FAIR Principles for Research Software (FAIR4RS Principles) (1.0). 
        Zenodo. https://doi.org/10.15497/RDA00068

        To make different versions of the same software (or component) findable, each version needs to be assigned a 
        different identifier. The relationship between versions is embodied in the associated metadata. What is considered 
        a “version” is defined by the owner of the software: in many cases this will be something that the owner wants to 
        specifically identify and use and/or “release” or “publish” so that others can use and reference/cite. There are 
        existing software engineering practices (e.g., version control, semantic versioning) around the management and versioning 
        of software that may form part of the implementation of these relationships. Capturing the relationships between different 
        versions of software will lead to greater understanding of the evolution of code, its authorship, ownership, description 
        and purpose, amongst other things.
        
        """

        # Get all function arguments dynamically
        all_args = {key: value for key, value in locals().items() if key != "self" and value is not None}

        result, log = evaluator_utils.validate_and_log_version(all_args,'represents valid semantic versioning.')

        return result, log

    def evalF2(self, description=None, fileSize=None) -> Tuple[bool, List[str]]:

        """
        Description from Chue Hong et. al, RDA FAIR4RS WG. (2022). FAIR Principles for Research Software (FAIR4RS Principles) (1.0). 
        Zenodo. https://doi.org/10.15497/RDA00068

        Software requires descriptive metadata to support indexing, search and discoverability. This metadata must itself be FAIR 
        (F4), should follow community standards, and use controlled vocabularies. The FAIR4RS principles do not define which standards 
        should be used, as this is better captured in guidance for implementing the principles coming out of each community. R1, R1.1, 
        and R1.2 describe categories of metadata that enable reuse.
        
        """

        # Set to True as it passes Codemeta validation
        result = True
        log = ['Codemeta file passed validation through codemeticulous.']

        return result, log

    def evalF3(self, codeRepository=None, hasPart=None, identifier=None, publisher=None) -> Tuple[bool, List[str]]:

        """
        Description from Chue Hong et. al, RDA FAIR4RS WG. (2022). FAIR Principles for Research Software (FAIR4RS Principles) (1.0). 
        Zenodo. https://doi.org/10.15497/RDA00068

        The association between the metadata (wherever it is stored; see F4) and the software should be made explicit by mentioning the 
        software's globally unique and persistent identifier in its associated metadata. In conjunction with A1, this means the metadata 
        describes how the software can be obtained. Metadata are not required to include references for all of the softwares dependencies 
        in order for software to be findable. I2 and R2 describe how references to dependencies increase the likelihood that software is 
        interoperable and reusable.

        """

        log = []

        # Get all function arguments dynamically
        all_args = {key: value for key, value in locals().items() if key != "self" and value is not None}

        if "identifier" in all_args:
            identifier = all_args["identifier"]
            if isinstance(identifier, list):
                identifier = {'url':['http://doi.org/' + id for id in identifier]}
            else:
                identifier = {'url':['http://doi.org/' + identifier]}

            result, log = evaluator_utils.validate_and_log_urls(identifier, 'a globally unique and persistent identifier for software.')
        else:
            result = False
            log = ['No identifier term found.']

        return result, log

    def evalF4(self, applicationCategory=None, applicationSubCategory=None, isAccessibleForFree=None, keywords=None, identifier=None) -> Tuple[bool, List[str]]:

        """
        Description from Chue Hong et. al, RDA FAIR4RS WG. (2022). FAIR Principles for Research Software (FAIR4RS Principles) (1.0). 
        Zenodo. https://doi.org/10.15497/RDA00068

        Making the metadata about the software FAIR, including making it readable and discoverable by both humans and machines, improves the 
        findability of software by supporting searching and indexing by others. It allows the metadata to be published in or harvested by a 
        registry or catalog or repository, or by a search engine. FAIR metadata also enables and encourages citation of research software.

        """

        # initialize log
        log = []
        result_list = []

        # Get all function arguments dynamically
        all_args = {key: value for key, value in locals().items() if key != "self" and value is not None}

        # check if software is deposited in accepted registry/catalog/repository
        # eg. zenodo, ieda
        if "identifier" in all_args:
            # print(all_args["identifier"])
            identifier = all_args["identifier"]
            if isinstance(identifier, list):
                for id in identifier:
                    # for repo in ACCEPTED_FAIR_REPOSITORIES:
                    result, log = evaluator_utils.check_substring_regex(id,ACCEPTED_FAIR_REPOSITORIES,'point to DOI in FAIR-aligned repository',log=log)
                    result_list.append(result)
                # return True if all True, False if otherwise
                result = all(result_list)
            else:
                # for repo in ACCEPTED_FAIR_REPOSITORIES:
                result, log = evaluator_utils.check_substring_regex(identifier,ACCEPTED_FAIR_REPOSITORIES,'point to DOI in FAIR-aligned repository')
        else:
            result = False
            log = ['No identifier term found.']     

        return result, log
    
    def evalA1_1(self, downloadUrl=None, installUrl=None, isAccessibleForFree=None, license=None, permissions=None, url=None) -> Tuple[bool, List[str]]:
        """
        Description from Chue Hong et. al, RDA FAIR4RS WG. (2022). FAIR Principles for Research Software (FAIR4RS Principles) (1.0). 
        Zenodo. https://doi.org/10.15497/RDA00068

        It is the openness of the communications protocol (including the resolver for the identifier) that is important, not the implementation 
        of the infrastructure that supports it. Here “open” means that there are no restrictions to implementing it and “free” means that there 
        are no fees or licensing costs to implement it.
        
        """

        # Get all function arguments dynamically
        all_args = {key: value for key, value in locals().items() if key != "self" and value is not None}

        # Extract URLs from all provided arguments
        extracted_urls = {
                        key: urls
                        for key, value in all_args.items()
                        if value and (urls := codemeta_parser.extract_urls_from_field(value))
                        }
        # extracted_urls = {key: codemeta_parser.extract_urls_from_field(value) for key, value in all_args.items() if value}
        if extracted_urls:
            result, log = evaluator_utils.validate_and_log_urls(extracted_urls, 'an open link to the software.')
        else:
            result = False
            log = [f"No URLs found in {list(all_args.keys())}"]

        return result, log

    def evalA1_2(self, downloadUrl=None, hasPart=None, installUrl=None, isAccessibleForFree=None, isPartOf=None, license=None, permissions=None) -> Tuple[bool, List[str]]:
        """
        Description from Chue Hong et. al, RDA FAIR4RS WG. (2022). FAIR Principles for Research Software (FAIR4RS Principles) (1.0). 
        Zenodo. https://doi.org/10.15497/RDA00068

        The FAIR Guiding Principles put specific emphasis on enhancing the ability of machines to use digital objects. In the context of software, 
        there are often conditions of access, for instance, requiring a license server to be contacted, requirement for payment before use, or 
        restrictions based on the privilege level of the user.
        
        """

        # # Get all function arguments dynamically
        # all_args = {key: value for key, value in locals().items() if key != "self" and value is not None}

        result = False
        log = []

        if isAccessibleForFree is not None:    
            if isAccessibleForFree:
                # software openly accesible
                result = True
                log.append('Software is accessible for free.')
                # print('evalA1_2 logs: software is accessible for free.')
            else:
                result = False
                log.append('Software is NOT accessible for free.')
        
        if license is not None:
                    
            # extracted_urls = codemeta_parser.extract_urls_from_field(license,regex_filter=APPROVED_LICENSES)
            # if extracted_urls:
            if result:
                _, log = evaluator_utils.check_if_field_in_keywords(license["name"],APPROVED_LICENSES,'an approved license.')
            else:
                result, log = evaluator_utils.check_if_field_in_keywords(license["name"],APPROVED_LICENSES,'an approved license.')

        # unsure what keywords to use for permissions
        if permissions is not None:
            pass

        # unsure how to use hasPart
        if hasPart is not None:
            pass

        # unsure how to use isPartOf
        if isPartOf is not None:
            pass

        if not log:
            log = ['Link in license term nor flag in isAccessibleForFree term provided']

        return result,log

    def evalA2(self, identifier=None, url=None) -> Tuple[bool, List[str]]:
        """
        Description from Chue Hong et. al, RDA FAIR4RS WG. (2022). FAIR Principles for Research Software (FAIR4RS Principles) (1.0). 
        Zenodo. https://doi.org/10.15497/RDA00068

        Availability of software may change over time, because there is a cost to maintaining access or because the software has degraded and is no 
        longer safely usable, or because dependencies are no longer available. The metadata describing the software is generally easier and cheaper 
        to store and maintain than the software itself (e.g., in the software repository, or in a software registry or catalog) and there is value 
        in understanding the details of the software even if it is no longer accessible.

        """

        # Get all function arguments dynamically
        all_args = {key: value for key, value in locals().items() if key != "self" and value is not None}

        # Extract URLs from all provided arguments
        extracted_urls = {
                        key: urls
                        for key, value in all_args.items()
                        if value and (urls := codemeta_parser.extract_urls_from_field(value,regex_filter=SOFTWARE_REGISTRIES))
                        }
        # extracted_urls = {key: codemeta_parser.extract_urls_from_field(value,regex_filter=SOFTWARE_REGISTRIES) for key, value in all_args.items() if value}
        if extracted_urls:
            result,log = evaluator_utils.validate_and_log_urls(extracted_urls,'providing access to the software metadata.')
        else:
            result = False
            log = [f"No URLs found in {list(all_args.keys())}"]

        return result,log

    def evalI1(self, supportingData=None, buildInstructions=None) -> Tuple[bool, List[str]]:

        """
        Description from Chue Hong et. al, RDA FAIR4RS WG. (2022). FAIR Principles for Research Software (FAIR4RS Principles) (1.0). 
        Zenodo. https://doi.org/10.15497/RDA00068

        Software interoperates through the exchange of data. This includes the use of data and metadata types, controlled vocabularies, and formats that 
        are formally defined throughstandards to facilitate the exchange. Whereas F4 requires that metadata describing the software are FAIR, this principle 
        ensures that the way that software interacts with other software is clearly described. A domain-relevant standard is an agreed standard that addresses 
        the needs of a given community (or communities). Examples of community standards for data are curated by the FAIRSharing Registry at 
        https://fairsharing.org/standards/. Where software interacts via APIs, these should be documented so that their capabilities can be inspected and 
        understood by humans and machines, and they should be open APIs where possible.

        """

        # Get all function arguments dynamically
        all_args = {key: value for key, value in locals().items() if key != "self" and value is not None}

        if "supportingData" in all_args:
            # Validate interoperability based on data exchange formats
            result_interoperability, log = evaluator_utils.validate_data_interoperability(
                all_args["supportingData"],
                ACCEPTED_DATA_FORMATS,
                "Test Data"
            )
        else:
            result_interoperability = False
            log = ['supportingData term not provided.']


        if "buildInstructions" in all_args:
            # Check specifically for API documentation links
            result_api_docs, log = evaluator_utils.check_for_api_documentation(
                all_args["buildInstructions"],
                API_KEYWORDS,
                log=log
            )
        else:
            result_api_docs = False
            log.append('buildInstructions term not provided.')

        # Pass only if both validations are True
        if result_interoperability and result_api_docs:
            # print(f"evaI1 logs: Passed interoperability evaluation.")
            result = True
        else:
            result = False

        return result, log

    def evalI2(self, relatedLink=None, supportingData=None, isPartOf=None, referencePublication=None) -> Tuple[bool, List[str]]:
        """
        Description from Chue Hong et. al, RDA FAIR4RS WG. (2022). FAIR Principles for Research Software (FAIR4RS Principles) (1.0). 
        Zenodo. https://doi.org/10.15497/RDA00068

        Some software includes references to external data objects required to execute the software (e.g., parameter files for certain applications). 
        Ideally, the data would be FAIR as well, and references to external data would be fully qualified. Qualified references should be to digital 
        objects (e.g., metadata, other software, data), as well as to non-digital objects that have a virtual presence in digital systems (e.g., 
        samples, reagents, instruments, etc.) with which the software interacts. These qualified references should be described using identifiers 
        and/or controlled vocabularies. “Qualified” means specifying the authoritative source for an identifier or vocabulary item, possibly including 
        a resolvable reference to further information about the source. Ideally this is in a form that includes a resolver within the reference (e.g., 
        in the form of a persistent identifier, or URL). This information can also improve the reusability of software by explicitly including 
        references to articles and data sets that document its use. Examples of qualified references might include: software X is implemented using 
        software A (a programming language); software X uses software B (a library/dependency); software X is tested within software C (a platform); 
        software X extends software D.

        """

        # result = False

        # Get all function arguments dynamically
        all_args = {key: value for key, value in locals().items() if key != "self" and value is not None}

        # Extract URLs from all provided arguments
        extracted_urls = {
                        key: urls
                        for key, value in all_args.items()
                        if value and (urls := codemeta_parser.extract_urls_from_field(value,regex_filter=['http://','https://','doi:']))
                        }
        # extracted_urls = {key: codemeta_parser.extract_urls_from_field(value,regex_filter=['http://','https://','doi:']) for key, value in all_args.items() if value}
        if extracted_urls:
            result,log = evaluator_utils.validate_and_log_urls(extracted_urls,'a qualified reference.')
        else:
            result = False
            log = [f"No URLs found in {list(all_args.keys())}"]

        return result,log


    def evalR1_1(self, citation=None, license=None, referencePublication=None) -> Tuple[bool, List[str]]:
        """
        Description from Chue Hong et. al, RDA FAIR4RS WG. (2022). FAIR Principles for Research Software (FAIR4RS Principles) (1.0). 
        Zenodo. https://doi.org/10.15497/RDA00068

        To support a wide range of reuse scenarios, the license should be as unrestrictive as possible and, to avoid license proliferation, choosing a 
        widely used and recognized license is strongly recommended. This license must also be compatible with the requirements of the licenses of the 
        software's dependencies so that the software can be legally combined.

        """

        # Get all function arguments dynamically
        all_args = {key: value for key, value in locals().items() if key != "self" and value is not None}

        # Extract URLs from all provided arguments
        ## XX -- fix license

        result, log = evaluator_utils.check_if_field_in_keywords(license["name"],APPROVED_LICENSES,'an approved license.')

        return result, log

    def evalR1_2(self, address=None, affiliation=None, author=None, citation=None, contributor=None,
                copyrightHolder=None, copyrightYear=None, dateCreated=None, dateModified=None,
                datePublished=None, editor=None, email=None, funder=None, funding=None, maintainer=None, 
                producer=None, provider=None, publisher=None,codeRepository=None) -> Tuple[bool, List[str]]:
        """
        Description from Chue Hong et. al, RDA FAIR4RS WG. (2022). FAIR Principles for Research Software (FAIR4RS Principles) (1.0). 
        Zenodo. https://doi.org/10.15497/RDA00068

        Software provenance is a type of metadata that describes why and how the software came to be, as well as who contributed what, when and where. 
        Provenance is sometimes referred to as lineage or pedigree. This extends beyond capturing a log of changes to source code as it is developed. 
        Good provenance metadata clarifies the origins and intent behind the development of the software, and establishes authenticity and trust. As a 
        type of metadata this overlaps with the metadata called for in guiding principles F2 and F4.

        """

        # maybe search for active github or gitlab link as this has provenance

        result = False
        log = ['Challenging to evaluate provenance; not evaluated.']

        # # Get all function arguments dynamically
        # all_args = {key: value for key, value in locals().items() if key != "self" and value is not None}

        # if "codeRepository" in all_args:
        #     result, log = evaluator_utils.check_substring_regex(all_args["codeRepository"],ACCEPTED_SOFTWARE_REPOSITORIES,'point to version controlled software')
        # else:
        #     result = False
        #     log = ['codeRepository term not provided.']

        return result, log

    def evalR2(self, softwareRequirement=None, softwareSuggestions=None) -> Tuple[bool, List[str]]:
        """
        Description from Chue Hong et. al, RDA FAIR4RS WG. (2022). FAIR Principles for Research Software (FAIR4RS Principles) (1.0). 
        Zenodo. https://doi.org/10.15497/RDA00068

        Software is rarely standalone and in most cases is built upon other software (e.g., dependencies), it should include appropriate references to 
        other software (e.g., requirements, imports, libraries) which are necessary to compile and run the software. “Qualified” here means specifying 
        the authoritative source for an identifier, possibly including a resolvable reference to further information about the source. To follow this 
        principle, it is desirable but not required that the other software referenced implements the FAIR4RS Principles. In many programming languages, 
        base methods or functions take a reference to a named entity, possibly in combination with a version number or qualifying domain and resolves 
        this to a source. This principle goes beyond this in calling for qualified references to external dependencies, meaning that the reference 
        itself resolves to the source via the qualifying authority. This guiding principle calls for qualified references in software to other software 
        (in aid of reuse). Principle I2 calls for qualified references to anything other than software (in aid of interoperability).

        """

        # Get all function arguments dynamically
        all_args = {key: value for key, value in locals().items() if key != "self" and value is not None}

        # Extract URLs from all provided arguments
        extracted_urls = {
                        key: urls
                        for key, value in all_args.items()
                        if value and (urls := codemeta_parser.extract_urls_from_field(value))
                        }
        # extracted_urls = {key: codemeta_parser.extract_urls_from_field(value) for key, value in all_args.items() if value}
        if extracted_urls:
            result,log = evaluator_utils.validate_and_log_urls(extracted_urls, 'a qualified reference to other relevant software.')
        else:
            result = False
            log = [f"No URLs found in {list(all_args.keys())}"]

        return result

    def evalR3(self, review=None) -> Tuple[bool, List[str]]:
        """
        Description from Chue Hong et. al, RDA FAIR4RS WG. (2022). FAIR Principles for Research Software (FAIR4RS Principles) (1.0). 
        Zenodo. https://doi.org/10.15497/RDA00068

        Software, including its documentation and license, should meet domain-relevant community standards and coding practices (e.g., choice of programming 
        language, standards for testing, usage of file formats, accessibility [in the sense of usable by as many people as possible]) that enable reuse. 
        While the FAIR4RS Principles do not specify particular community standards, the intent is to ensure that practitioners are aware of what others are 
        doing and using in the community, e.g., through initiatives like FAIRsharing (Sansone et al., 2019), whilst acknowledging that community standards 
        are (and should be) under constant development.

        Communities can encompass research domains, programming languages, and technical approaches. Examples of community standards might include: 
        BioSchemas from ELIXIR for describing resources in the life sciences and schema.org for general description of resources; Common Workflow 
        Language; and the package managers commonly used by a programming language such as Maven (Java), npm (Javascript), PyPI (Python) and CRAN 
        (R). It is important to note that the FAIR Guiding Principles address research outputs, not research processes, so standards should also be 
        limited to best practice about the software itself, not the process of designing, developing, or maintaining it, such as the R community 
        standards for creating packages5 or the PEP 8 Style Guide for Python Code6.

        """

        # # we can use the JOSS badge for code review 
        # result = False

        # Get all function arguments dynamically
        all_args = {key: value for key, value in locals().items() if key != "self" and value is not None}

        if 'review' in all_args.keys():
            # print(f'evalR3 logs: {review.reviewBody}')
            result = True
            log = [f"{review['reviewBody']}"]
        else:
            result = False
            log = ['Not code reviewed']

        return result, log