#!python3.5

import os
import json
from glob import glob
from jsonschema import Draft4Validator, ValidationError, RefResolver

abs_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'schemas')
schema_path = os.path.join(abs_path, 'schema.json')

with open(schema_path) as schema_file:
    schema = json.load(schema_file)
    resolver = RefResolver('file://' + abs_path + '/', schema)
    validator = Draft4Validator(schema, resolver = resolver)

    for f in glob('./data/valid/*.json'):
        with open(f) as sample_file:
            sample = sample_file.read()

            try:
                errors = sorted(validator.iter_errors(json.loads(sample)),
                        key=str)
                for error in errors:
                    print("file: %s:" %f)
                    print("trace:", error.message)
                    print("path:", list(error.path),'\n')
            except ValidationError as err:
                print(err.message)

    for f in glob('./data/invalid/*.json'):
        with open(f) as sample_file:
            sample = sample_file.read()

            try:
                errors = sorted(validator.iter_errors(json.loads(sample)),
                        key=str)
                assert len(errors) > 0, \
                    "Expected to find a ValidationError in file %s, but found none..." %f

            except ValidationError as err:
                print(err.message)
