from abc import ABC, abstractmethod
from typing import Dict, Any
from utils import evaluator_utils
from utils import codemeta_parser
from constants import SOFTWARE_REGISTRIES, APPROVED_LICENSES
 

class Evaluator(ABC):
    """
    Abstract base class for FAIR4RS indicators.
    """

    @abstractmethod
    def evalF1(self, citation=None, identifier=None, sameAs=None, isPartOf=None, url=None) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    def evalF1_1(self, isPartOf=None, identifier=None) -> bool:
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
    def evalF4(self, applicationCategory=None, applicationSubCategory=None, isAccessibleForFree=None, keywords=None) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    def evalA1(self, codeRepository=None, downloadUrl=None) -> bool:
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
    def evalI1(self, input=None, output=None, runtimePlatform=None) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    def evalI2(self, relatedLink=None, supportingData=None, isPartOf=None, referencePublication=None) -> bool:
        raise NotImplementedError

    @abstractmethod
    def evalR1(self, description=None, applicationCategory=None, applicationSubCategory=None, keywords=None) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    def evalR1_1(self, citation=None, license=None, referencePublication=None) -> bool:
        raise NotImplementedError   

    @abstractmethod
    def evalR1_2(self, address=None, affiliation=None, author=None, citation=None, contributor=None,
                copyrightHolder=None, copyrightYear=None, dateCreated=None, dateModified=None,
                datePublished=None, editor=None, email=None, funder=None, funding=None, maintainer=None, 
                producer=None, provider=None, publisher=None) -> bool:
        raise NotImplementedError

    @abstractmethod
    def evalR2(self, softwareRequirement=None, softwareSuggestions=None) -> bool:
        raise NotImplementedError

    @abstractmethod
    def evalR3(self, referencePublication=None) -> bool:
        raise NotImplementedError


class MyEvaluator(Evaluator):
    """
    Class for implementing evaluation functions.
    """

    def __init__(self,codemeta_file):

        self.codemeta_file = codemeta_file

    def validate_codemeta_file(self) -> Dict:

        codemeta_json = evaluator_utils.run_codemeticulous_validation(self.codemeta_file)

        return codemeta_json

    def evalF1(self, citation=None, identifier=None, sameAs=None, isPartOf=None, url=None) -> bool:

        # Get all function arguments dynamically
        all_args = {key: value for key, value in locals().items() if key != "self" and value is not None}

        # initialize result to False
        result = False

        # Extract URLs from all provided arguments
        extracted_urls = {key: codemeta_parser.extract_urls_from_field(value,regex_filter='https://doi.org/') for key, value in all_args.items() if value}
        if extracted_urls:
            result = evaluator_utils.validate_and_log_urls(extracted_urls,'evalF1', 'is a globally unique and persistent identifier.')

        return result
    
    def evalF1_1(self, isPartOf=None, identifier=None) -> bool:

        # XX -- challenging to implement

        return False

    def evalF1_2(self, softwareVersion=None, version=None) -> bool:

        # Get all function arguments dynamically
        all_args = {key: value for key, value in locals().items() if key != "self" and value is not None}

        result = evaluator_utils.validate_and_log_version(all_args,'evalF1_2', 'represents valid semantic versioning.')

        return result

    def evalF2(self, description=None, fileSize=None) -> bool:

        # Set to True as it passes Codemeta validation

        return True

    def evalF3(self, codeRepository=None, hasPart=None, identifier=None, publisher=None) -> bool:

        # XX -- challenging to implement.
        # how does this differ from F1?

        print('evalF3 logs: Challenging to implement.')

        return False

    def evalF4(self, applicationCategory=None, applicationSubCategory=None, isAccessibleForFree=None, keywords=None) -> bool:

        # XX -- challenging to implement.
        # how does this differ from F2?

        print('evalF4 logs: Challenging to implement.')

        return False

    def evalA1(self, codeRepository=None, downloadUrl=None) -> bool:
        return False
    
    def evalA1_1(self, downloadUrl=None, installUrl=None, isAccessibleForFree=None, license=None, permissions=None, url=None) -> bool:

        # Get all function arguments dynamically
        all_args = {key: value for key, value in locals().items() if key != "self" and value is not None}

        # Extract URLs from all provided arguments
        extracted_urls = {key: codemeta_parser.extract_urls_from_field(value) for key, value in all_args.items() if value}
        if extracted_urls:
            result = evaluator_utils.validate_and_log_urls(extracted_urls,'evalA1_1', 'provides access to the software.')

        return result

    def evalA1_2(self, downloadUrl=None, hasPart=None, installUrl=None, isAccessibleForFree=None, isPartOf=None, license=None, permissions=None) -> bool:

        # XX -- challenging to implement.
        # 

        print('evalA1_2 logs: Challenging to implement.')

        return False

    def evalA2(self, identifier=None, url=None) -> bool:

        # Get all function arguments dynamically
        all_args = {key: value for key, value in locals().items() if key != "self" and value is not None}

        # Extract URLs from all provided arguments
        extracted_urls = {key: codemeta_parser.extract_urls_from_field(value,regex_filter=SOFTWARE_REGISTRIES) for key, value in all_args.items() if value}
        if extracted_urls:
            result = evaluator_utils.validate_and_log_urls(extracted_urls,'evalA2', 'provides access to the software metadata.')

        return result

    def evalI1(self, input=None, output=None, runtimePlatform=None) -> bool:

        # XX -- challenging to implement.
        # unsure what the domain relevant community standards are.

        print('evalI1 logs: Challenging to implement.')

        return False

    def evalI2(self, relatedLink=None, supportingData=None, isPartOf=None, referencePublication=None) -> bool:

        # XX -- challenging to implement.
        # unsure what identifiers and/or controlled vocabularies are

        print('evalI2 logs: Challenging to implement.')

        return False

    def evalR1(self, description=None, applicationCategory=None, applicationSubCategory=None, keywords=None) -> bool:
        return False

    def evalR1_1(self, citation=None, license=None, referencePublication=None) -> bool:

        # Get all function arguments dynamically
        all_args = {key: value for key, value in locals().items() if key != "self" and value is not None}

        # Extract URLs from all provided arguments
        extracted_urls = {key: codemeta_parser.extract_urls_from_field(value,regex_filter=APPROVED_LICENSES) for key, value in all_args.items() if value}
        if extracted_urls:
            result = evaluator_utils.validate_and_log_urls(extracted_urls,'evalR1_1', 'is an approved license.')

        return result  

    def evalR1_2(self, address=None, affiliation=None, author=None, citation=None, contributor=None,
                copyrightHolder=None, copyrightYear=None, dateCreated=None, dateModified=None,
                datePublished=None, editor=None, email=None, funder=None, funding=None, maintainer=None, 
                producer=None, provider=None, publisher=None) -> bool:
        
        # XX -- challenging to implement. 
        # there are an overwhelming amount of aspects to provenance

        print('evalR1_2 logs: Challenging to implement.')

        return False

    def evalR2(self, softwareRequirement=None, softwareSuggestions=None) -> bool:

        # XX -- challenging to implement.
        # unsure how to define "qualified" reference to other software.

        print('evalR2 logs: Challenging to implement.')

        return False

    def evalR3(self, referencePublication=None) -> bool:
        return False