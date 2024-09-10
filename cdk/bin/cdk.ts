#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { TjpwScheduleStack } from '../lib/tjpw-schedule-stack';

const app = new cdk.App();
new TjpwScheduleStack(app, 'TjpwScheduleStack', {});
