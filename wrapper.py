import argparse
import sys
import os
import subprocess
import pickle
import re
import glob
from time import strftime, localtime, sleep
import yaml
from threading import Thread


def main():
    assert args.cloud is not None
    assert args.tests is not None
    assert args.config_file is not None and os.path.exists(args.config_file)

    with open(args.config_file) as config_file:
        data_dict = yaml.full_load(config_file)

    test_suite = data_dict.get('test_suite')
    for cloud_provider in test_suite:
        cloud_provider['cloud'] = re.sub(r'\d+', r'', cloud_provider['cloud'])
        if 'all' in args.cloud or cloud_provider['cloud'] in args.cloud:
            execute(cloud_provider, args.output_folder)
            # t = Thread(target=execute, args=(cloud_provider, args.output_folder))
            # t.start()

def execute(cloud_provider, output):
    output_folder = f"{output}/{strftime('%Y%m%d%H%M', localtime())}/{cloud_provider.get('cloud')}"
    create_results_dir(output_folder)

    pkb_run = create_run_cmd(cloud_provider, output_folder)

    try:
        proc = subprocess.check_output(pkb_run, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(e)
        error = e.stderr.decode("UTF-8") 
        print(error.split("\n")[-3])
        
def create_results_dir(output_path):
    if not os.path.isdir(output_path):
        os.makedirs(output_path)
    else:
        return

def create_run_cmd(cloud_provider, results_location):
    pkb_run = ['python', 'pkb.py']
    pkb_run.extend(["--cloud", cloud_provider['cloud']])

    if 'globals' in cloud_provider:
        for option, value in cloud_provider['globals'].items():
            pkb_run.extend(["--" + option, str(value)])

    tests_to_run = []
    for test in cloud_provider['tests']:
        if test['test'] in args.tests or 'all' in args.tests:
            tests_to_run.append(test['test'])
            if 'options' in test:
                for option in test['options']:
                    pkb_run.extend(["--" + option, str(test['options'][option])])

    pkb_run.extend(["--benchmarks", ",".join(tests_to_run)])

    machine = cloud_provider['globals']['machine_type']
    if isinstance(machine, dict):
        machine = '_'.join([str(v) for _, v in machine.items()])

    file_name = '{}_{}_{}.{}'.format(cloud_provider['cloud'], machine, '_'.join(args.tests), 'csv')
    file_path = '{}/{}'.format(results_location, file_name)

    pkb_run.extend(["--csv_path", file_path])

    return pkb_run


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Execute tests on indicated cloud platforms')
    parser.add_argument('-c', '--cloud', required=True, nargs='+',
                        choices=['all', 'AWS', 'GCP', 'Rackspace', 'Azure', 'AliCloud'],
                        help='The cloud service providers you wish to test on')
    parser.add_argument('-t', '--tests', required=True, nargs='+',
                        choices=['all', 'iperf', 'fio', 'ping', 'coremark', 'unixbench', 'tensorflow'],
                        help='The tests that we have certified for use against the clouds')
    parser.add_argument('-f', '--config_file', default='config/basic.yaml',
                        nargs='?', help='The configuration file for the tests that we will use')
    parser.add_argument('-o', '--output_folder', default='../output', help='location to store output')

    args = parser.parse_args()

    main()
