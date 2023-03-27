#!/usr/bin/env python
"""
Get secret from AWS-secret manager and store them in a variable which then be using by group_vars to authenticate ansible playbook
"""
import boto3
import json
import argparse

def get_account_details():
    parser = argparse.ArgumentParser(Description="Collecting argument to get AWS secret")
    parser.add_argument('--region')
