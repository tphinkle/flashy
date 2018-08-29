
# Imports

# Python standard library
import datetime
import io
import json
import os
import sys

# AWS
import boto3

# Program specific
import constants
import experiment


#


# Need to authenticate first! (via aws-okta)


S3_BUCKET_STAGE = 'zillow-analytics-stage'
S3_EXPERIMENT_BASE_DIRECTORY_STAGE = 'prestonh/adwords-adcopy/test/experiments/'
S3_EXPERIMENT_QUEUE_FILE_PATH_STAGE = 'prestonh/adwords-adcopy/test/experiments/queue/'
S3_EXPERIMENT_ACTIVE_FILE_PATH_STAGE = 'prestonh/adwords-adcopy/test/experiments/active/'
S3_EXPERIMENT_COMPLETE_FILE_PATH_STAGE = 'prestonh/adwords-adcopy/test/experiments/complete/'

S3_BUCKET = S3_BUCKET_STAGE
S3_EXPERIMENT_BASE_DIRECTORY = S3_EXPERIMENT_BASE_DIRECTORY_STAGE
S3_EXPERIMENT_QUEUE_FILE_PATH = S3_EXPERIMENT_QUEUE_FILE_PATH_STAGE
S3_EXPERIMENT_ACTIVE_FILE_PATH = S3_EXPERIMENT_ACTIVE_FILE_PATH_STAGE
S3_EXPERIMENT_COMPLETE_FILE_PATH = S3_EXPERIMENT_COMPLETE_FILE_PATH_STAGE





def setup_s3_test_queue():
    # Get client
    s3_client = get_s3_client()

    # Push experiments to queue
    experiment_configs = [{
            "EXPERIMENT_NAME": "responsive_0",
            "START_SETTINGS": {"START_MODE": "AUTOMATIC", "START_DATE": "2018-08-10"}
            },
            {
            "EXPERIMENT_NAME": "responsive_1",
            "START_SETTINGS": {"START_MODE": "AUTOMATIC", "START_DATE": "2018-08-10"}
            },
            {
            "EXPERIMENT_NAME": "responsive_2",
            "START_SETTINGS": {"START_MODE": "AUTOMATIC", "START_DATE": "2018-08-11"}
            },
            {
            "EXPERIMENT_NAME": "responsive_3",
            "START_SETTINGS": {"START_MODE": "AUTOMATIC", "START_DATE": "2018-08-11"}
            },
            {
            "EXPERIMENT_NAME": "responsive_4",
            "START_SETTINGS": {"START_MODE": "AUTOMATIC", "START_DATE": "2018-08-11"}
            }]
    for experiment_config in experiment_configs:
        experiment_name = experiment_config['experiment_name']

        add_experiment_to_S3(experiment_config, [])





def add_experiment_to_S3(experiment_config, experiment_file_paths):

    # Check experiment name ok
    experiment_name = experiment_config['EXPERIMENT_NAME']


    # Get client
    s3_client = get_s3_client()

    # Push config file
    Key = GET_S3_EXPERIMENT_CONFIG_FILE_PATH(experiment_name, 'queue')
    buffer = io.BytesIO(json.dumps(experiment_config).encode('utf8'))
    s3_client.upload_fileobj(buffer, S3_BUCKET, Key)

    # Create queue sub-folders
    sub_path = S3_EXPERIMENT_QUEUE_FILE_PATH + experiment_name + '/'
    s3_client.put_object(Bucket = S3_BUCKET, Body = '', Key = sub_path + 'input/')

    # Push input files to input subfolder
    for experiment_file_path in experiment_file_paths:
        experiment_file_name = experiment_file_path.split('/')[-1]
        Key = sub_path + 'input/' + experiment_file_name
        s3_client.upload_file(experiment_file_path, S3_BUCKET, Key)


def get_ready_experiment_names():
    # Get all experiments in the queue
    experiment_names = get_all_experiment_names_by_stage(stage = 'queue')
    ready_experiment_names = []

    # Launch all experiments that are ready
    for experiment_name in experiment_names:
        if check_experiment_start_ready(experiment_name):
            ready_experiment_names.append(ready_experiment_name)

    return ready_experiment_names

def check_experiment_start_ready(experiment_name):

    # Load the config file
    experiment_config = get_experiment_config_s3(experiment_name, 'queue')


    # Get start settings
    experiment_start_mode = experiment_config['START_SETTINGS']['START_MODE']

    if experiment_start_mode == 'AUTOMATIC':

        # Check if today's date is past scheduled start date
        start_date = datetime.datetime.strptime(experiment_config['START_SETTINGS']['START_DATE'], '%Y-%m-%d')
        today_date = datetime.datetime.now()
        if start_date <= today_date:
            return True
        else:
            return False


    else:
        return False




def get_experiment_config_s3(experiment_name, phase):
    # Load the config file
    s3_client = get_s3_client()
    config_Key = GET_S3_EXPERIMENT_CONFIG_FILE_PATH(experiment_name, phase)
    experiment_config = s3_client.get_object(Bucket = S3_BUCKET, Key = config_Key)
    experiment_config = json.loads(experiment_config['Body'].read())

    return experiment_config
