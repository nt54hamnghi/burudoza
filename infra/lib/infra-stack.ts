import * as cdk from 'aws-cdk-lib';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import { DockerImageAsset } from 'aws-cdk-lib/aws-ecr-assets';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as ecsPatterns from 'aws-cdk-lib/aws-ecs-patterns';
import { Construct } from 'constructs';
import { join } from 'path';

function genid(service: string) {
	const Service = service.charAt(0).toUpperCase() + service.slice(1);
	return `Burudoza${Service}`;
}

export class BurudozaStack extends cdk.Stack {
	constructor(scope: Construct, id: string, props?: cdk.StackProps) {
		super(scope, id, props);

		const vpc = new ec2.Vpc(this, genid('vpc'), {
			maxAzs: 2, // maximum number of availability zone, default is All
		});

		const cluster = new ecs.Cluster(this, genid('cluster'), {
			vpc: vpc,
		});

		const asset = new DockerImageAsset(this, genid('dockerAsset'), {
			directory: join(__dirname, '../..'),
		});

		const image = ecs.ContainerImage.fromDockerImageAsset(asset);

		new ecsPatterns.ApplicationLoadBalancedFargateService(
			this,
			genid('fargateService'),
			{
				assignPublicIp: true,
				cluster: cluster,
				cpu: 2048, // 2 vCPU
				taskImageOptions: {
					image: image,
					containerPort: 8501,
				},
				memoryLimitMiB: 4096, // 4 BG of RAM
				publicLoadBalancer: true,
			}
		);
	}
}

// import * as ecr from 'aws-cdk-lib/aws-ecr';
// const repo = ecr.Repository.fromRepositoryName(
// 	this,
// 	genid('repository'),
// 	'burudoza'
// );
