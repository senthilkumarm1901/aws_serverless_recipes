import json 
import os
os.environ['HF_HOME'] = '/tmp/model'
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

from presidio_anonymizer import AnonymizerEngine
from presidio_analyzer import AnalyzerEngine, EntityRecognizer, RecognizerResult, Pattern, PatternRecognizer

from presidio_analyzer.nlp_engine import NlpArtifacts,NlpEngineProvider


# the models are already downloaded in the Docker Container
# tokenizer = AutoTokenizer.from_pretrained("Jean-Baptiste/camembert-ner")
# ner_model = AutoModelForTokenClassification.from_pretrained("Jean-Baptiste/camembert-ner")

new_model="ab-ai/pii_model"
tokenizer = AutoTokenizer.from_pretrained(new_model,cache_dir='/tmp/model')
ner_model = AutoModelForTokenClassification.from_pretrained(new_model,cache_dir='/tmp/model')

# nlp = pipeline('ner', model=ner_model, tokenizer=tokenizer, aggregation_strategy="simple")

# list of entities: https://microsoft.github.io/presidio/supported_entities/#list-of-supported-entities
DEFAULT_ANOYNM_ENTITIES = [
"ACCOUNTNUMBER",
"FIRSTNAME",
"ACCOUNTNAME",
"PHONENUMBER",
"CREDITCARDCVV",
"CREDITCARDISSUER",
"PREFIX",
"LASTNAME",
"AMOUNT",
"DATE",
"DOB",
"COMPANYNAME",
# "BUILDINGNUMBER",
"STREET",
"SECONDARYADDRESS",
"STATE",
"EMAIL",
"CITY",
"CREDITCARDNUMBER",
"SSN",
"URL",
"USERNAME",
"PASSWORD",
"COUNTY",
"PIN",
"MIDDLENAME",
"IBAN",
"GENDER",
"AGE",
"ZIPCODE",
"SEX"
]



class TransformerRecognizer(EntityRecognizer):
    def __init__(
        self,
        model_id_or_path,
        mapping_labels,
        aggregation_strategy="simple",
        supported_language="en",
        ignore_labels=["O", "MISC"],
    ):
        # inits transformers pipeline for given mode or path
        self.pipeline = pipeline(
            "token-classification", model=model_id_or_path, aggregation_strategy=aggregation_strategy, ignore_labels=ignore_labels
        )
        # map labels to presidio labels
        self.label2presidio = {x:x for x in DEFAULT_ANOYNM_ENTITIES}

        # passes entities from model into parent class
        super().__init__(supported_entities=list(self.label2presidio.values()), supported_language=supported_language)

    def load(self) -> None:
        """No loading is required."""
        pass

    def analyze(
        self, text: str, entities = None, nlp_artifacts: NlpArtifacts = None
    ):
        """
        Extracts entities using Transformers pipeline
        """
        results = []

        predicted_entities = self.pipeline(text)
        if len(predicted_entities) > 0:
            for e in predicted_entities:
                if(e['entity_group'] not in self.label2presidio):
                    continue
                converted_entity = self.label2presidio[e["entity_group"]]
                if converted_entity in entities or entities is None:
                    results.append(
                        RecognizerResult(
                            entity_type=converted_entity, start=e["start"], end=e["end"], score=e["score"]
                        )
                    )
        return results
     


def lambda_handler(event, context):
    # This function will be triggered when the Lambda is invoked
    text = event["text_to_be_masked"]
    # transformer_res = nlp(text)

    #mapping_labels = {"PROPN": "PERSON","XFAMIL": "PERSON"}
    mapping_labels = {"PER":"PERSON",'LOC':'LOCATION','ORG':"ORGANIZATION",'PHONE_NUMBER':'PHONE_NUMBER'}
    configuration = {"nlp_engine_name":"spacy",
                    "models":[{"lang_code": 'en', "model_name":"en_core_web_sm"}]}


    to_keep = []
    lang = 'en'

    provider = NlpEngineProvider(nlp_configuration=configuration)
    nlp_engine = provider.create_engine()

    # Pass the created NLP engine and supported_languages to the AnalyzerEngine
    analyzer = AnalyzerEngine(
        nlp_engine=nlp_engine,
        supported_languages = "en"
    )

    # transformers_recognizer = TransformerRecognizer("Jean-Baptiste/roberta-large-ner-english", mapping_labels)
    transformers_recognizer = TransformerRecognizer(new_model, mapping_labels)
    analyzer.registry.add_recognizer(transformers_recognizer)


    # Text Analyzer
    analyzer_results = analyzer.analyze(text=text, entities = DEFAULT_ANOYNM_ENTITIES, allow_list = to_keep, language=lang)

    # Text Anonymizer
    engine = AnonymizerEngine()
    result = engine.anonymize(text=text, analyzer_results=analyzer_results)

    # Restructuring anonymizer results

    annonymized_output = result.text

    # anonymization_results =  {"anonymized": result.text,"found": [entity.to_dict() for entity in analyzer_results]}

    # words = [{'word': text[obj['start']:obj['end']], 'entity_type':obj['entity_type'], 'start':obj['start'], 'end':obj['end']} for obj in anonymization_results['found']]
    
    # # anonymization_results = json.loads(json.dumps(anonymization_results))
    # print(words)

    # for list1 in anonymization_results['found']:
    #     for element in list1:
    #         for k in element:
    #             if element[k] is None:
    #                 element[k] = 'None'

    print(annonymized_output)

    return {
        'statusCode': 200,
        'body': json.dumps(
            {
                "input_event": event,
                "annonymized_output": annonymized_output
            }),   
    }