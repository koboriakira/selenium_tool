import * as cdk from 'aws-cdk-lib';
import {
  aws_ec2 as ec2,
  aws_ecs as ecs,
} from 'aws-cdk-lib';
import { Construct } from 'constructs';

export class TjpwScheduleStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // VPCを作成する
    const vpc = new ec2.Vpc(this, 'TjpwScheduleVpc', {
      maxAzs: 1,
    });

    // ECSクラスタを作成する
    const cluster = new ecs.Cluster(this, 'TjpwScheduleCluster', {
      vpc: vpc,
    });

    // Chromeコンテナを作成する
    const chromeTaskDefinition = new ecs.FargateTaskDefinition(this, 'TjpwScheduleChromeTaskDefinition', {
      memoryLimitMiB: 512,
      cpu: 256,
    });
    const chromeContainer = chromeTaskDefinition.addContainer('ChromeContainer', {
      image: ecs.ContainerImage.fromRegistry('seleniarm/standalone-chromium:114.0'),
      portMappings: [
        { containerPort: 4444, hostPort: 4444 },
        { containerPort: 5900, hostPort: 5900 },
        { containerPort: 7900, hostPort: 7900 },
      ],
      environment: {
        TZ: 'Asia/Tokyo',
        LANGUAGE: 'ja_JP.UTF-8',
        LANG: 'ja_JP.UTF-8',
        LC_ALL: 'ja_JP.UTF-8',
      },
    });

    // appコンテナを作成する
    const appTaskDefinition = new ecs.FargateTaskDefinition(this, 'TjpwScheduleAppTaskDefinition', {
      memoryLimitMiB: 512,
      cpu: 256,
    });
    const appContainer = appTaskDefinition.addContainer('AppContainer', {
      image: ecs.ContainerImage.fromAsset('../docker/tjpw_schedule'),
      environment: {
        SELENIUM_URL: `http://${chromeContainer.containerName}:4444`,
        TZ: 'Asia/Tokyo',
      },
    });

    // // chromeコンテナとappコンテナの間に依存関係を設定する
    // appContainer.addContainerDependencies({
    //   container: chromeContainer,
    //   condition: ecs.ContainerDependencyCondition.START,
    // });
  }
}
